#!/usr/bin/env python3
"""
Check a dialogue.txt against the field registry (fields.xml), format 1.0 draft.
usage: python3 validate.py path/to/dialogue.txt [path/to/fields.xml]
Exit code 0 = conforms, 1 = does not conform. Standard library only. CC0.
Provided as is. Passing the validator means the file matches the format; it says nothing about how any reader will behave, and the file has no legal effect beyond what applicable law gives it. Test results describe the tested models on the tested dates.
"""
import re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

def parse(text):
    """Lenient parse: key: value lines; '#' lines are comments; anything else is ignored (unknown lines)."""
    comments, pairs = [], {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line: continue
        if line.startswith("#"): comments.append(line); continue
        m = re.match(r"^([A-Za-z0-9_.+\-]+)\s*:\s*(.*)$", line)
        if m: pairs[m.group(1)] = m.group(2).strip()
    return comments, pairs

RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    doc = Path(sys.argv[1]).read_text(encoding="utf-8")
    reg = ET.parse(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent / "fields.xml").getroot()
    comments, kv = parse(doc)
    errors, warnings, notes = [], [], []
    base = [f for f in reg.iter("field") if f.get("level") == "base"]
    optional = {f.get("key") for f in reg.iter("field") if f.get("level") == "optional"}
    live = kv.get("live") == "true"

    pre = next(f for f in base if f.get("key") == "#1")
    alts = {a.text: (a.get("for"), a.get("tested", "")) for a in pre.findall("alternative")}
    first = comments[0] if comments and doc.lstrip().startswith("#") else ""
    if first == pre.find("value").text: notes.append("first line: recommended data preamble")
    elif first in alts:
        who_for, tested = alts[first]
        (warnings if tested.startswith("pending") else notes).append(f"first line: alternative preamble for {who_for} ({tested})")
    elif first: warnings.append("first line is a comment but not a tested preamble wording")
    else: errors.append("first line must be the data preamble comment")
    fmt = next(f for f in base if f.get("key") == "#2").find("value").text
    if fmt not in comments: errors.append("the format comment line is missing or changed")

    for f in base:
        key, rule, val = f.get("key"), f.get("rule"), f.find("value").text
        if key.startswith("#"): continue
        if key == "who.channels.<kind>":
            base_keys = {b.get("key") for b in base}
            ch = [k for k in kv if k.startswith("who.channels.") and k.count(".") == 2 and kv[k] and " " not in k]
            ch = [k for k in ch if k not in optional and k not in base_keys]
            if not ch: errors.append("at least one who.channels.<kind> line is required")
            continue
        if key not in kv: errors.append(f"missing base line: {key}"); continue
        v = kv[key]
        if rule == "fixed":
            if key == "does_not_authorize":
                have = {x.strip() for x in v.split(",")}; need = {x.strip() for x in val.split(",")}
                if need - have: errors.append(f"does_not_authorize is missing: {sorted(need - have)}")
                if have - need: notes.append(f"does_not_authorize extended (narrowing): {sorted(have - need)}")
            elif v != val: errors.append(f"{key} must be exactly '{val}' (found '{v}')")
        elif key == "short_text":
            n = len(re.findall(r"[A-Za-z']+", v))
            if n > 100: warnings.append(f"short_text has {n} words (limit 100)")
            st_alts = {a.text: a.get("for") for a in f.findall("alternative")}
            if v in st_alts: notes.append(f"short_text: tested wording for {st_alts[v]}")
            elif v != val: warnings.append("short_text differs from the tested wording: make sure it does not widen the offer")
        elif f.get("options") and v not in f.get("options").split("|") and "REPLACE_" not in v:
            errors.append(f"{key} must be one of {f.get('options').split('|')} (found '{v}')")
        if key == "who.channels.reference" and "REPLACE_" not in v and (" " in v or len(v) > 32):
            warnings.append("who.channels.reference should be short and without spaces, so it can be copied into a subject line")

    for k in ("published", "last_updated"):
        if k in kv and not kv[k].startswith("REPLACE_") and not RFC3339.match(kv[k]): errors.append(f"{k} is not an RFC 3339 date-time")
    cu = kv.get("canonical_url", "")
    if cu and not cu.startswith("REPLACE_") and not re.match(r"^https://[^/]+/\.well-known/dialogue\.txt$", cu) and "REPLACE_" not in cu:
        errors.append("canonical_url must be https://<domain>/.well-known/dialogue.txt")
    if kv.get("live") not in ("true", "false"): errors.append("live must be true or false")

    placeholders = [k for k, v in kv.items() if "REPLACE_" in v]
    if placeholders: (errors if live else warnings).append(f"unfilled placeholders: {placeholders}")
    res_prefix = [r.get("prefix") for r in reg.iter("reserved") if r.get("prefix")]
    res_key = [r.get("key") for r in reg.iter("reserved") if r.get("key")]
    reserved = [k for k in kv if k in res_key or any(k.startswith(x) for x in res_prefix)]
    if reserved: errors.append(f"reserved names used (not part of 1.0): {reserved}")

    known = {f.get("key") for f in base} | optional
    def is_known(k):
        if k in known or k.startswith("who.channels."): return True
        return any(o.endswith("*") and k.startswith(o[:-1]) for o in known) or any(k in o.split(", ") for o in optional)
    added = [k for k in kv if not is_known(k) and k not in reserved]
    opt_used = [k for k in kv if k not in {f.get("key") for f in base} and not k.startswith("who.channels.") and is_known(k)]
    if opt_used: notes.append(f"optional lines used: {len(opt_used)}")
    if added: notes.append(f"lines added by the person (narrow only): {added}")

    ok = not errors
    print(("CONFORMS" if ok else "DOES NOT CONFORM") + f" to dialogue.txt 1.0 (draft) — live: {kv.get('live')}")
    for label, items in (("error", errors), ("warning", warnings), ("note", notes)):
        for i in items: print(f"  {label}: {i}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
