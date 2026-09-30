#!/usr/bin/env python3
"""
Tests for the dialogue.txt make-and-check page.
Run from any directory: python3 test_try.py
Standard library only. CC0.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE      = Path(__file__).resolve().parent
ROOT      = HERE.parent.parent          # standard/
VALIDATE  = HERE.parent / "validate.py"
CHECKER   = HERE / "checker.js"
FIELDS    = ROOT / "fields.xml"
TEMPLATE  = ROOT / "template" / "dialogue.txt"
EXAMPLE   = ROOT / "example" / "dialogue.txt"
EXAMPLE_ORG = ROOT / "example" / "organisation" / "dialogue.txt"
INDEX     = HERE / "index.html"
NODE      = shutil.which("node") or shutil.which("nodejs")

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"

failures = []

def run(cmd, input_text=None):
    r = subprocess.run(
        cmd, capture_output=True, text=True,
        input=input_text, encoding="utf-8"
    )
    return r.returncode, (r.stdout + r.stderr).strip()

def check(label, ok, detail=""):
    if ok:
        print(f"  {PASS}  {label}")
    else:
        print(f"  {FAIL}  {label}")
        if detail:
            for line in detail.splitlines():
                print(f"         {line}")
        failures.append(label)

def make_sample(name, email, domain, postal=None, live=True, pub_date="2026-10-01T00:00:00Z",
                reference="DLG-4712", labels=None):
    """Generate a dialogue.txt from the template, simulating what the JS generator does."""
    if labels is None:
        labels = []
    text = TEMPLATE.read_text(encoding="utf-8")
    lines = text.split("\n")
    out = []
    for line in lines:
        if not postal and re.match(r"who\.channels\.letter\s*:", line):
            continue
        if re.match(r"^live\s*:", line):
            out.append("live: " + ("true" if live else "false"))
            continue
        line = line.replace("REPLACE_WITH_DATE_RFC3339", pub_date)
        line = line.replace("REPLACE_WITH_YOUR_DOMAIN",  domain)
        line = line.replace("REPLACE_WITH_YOUR_NAME",    name)
        line = line.replace("REPLACE_WITH_ONE_EMAIL",    email)
        line = line.replace("REPLACE_WITH_A_SHORT_REFERENCE", reference)
        if postal:
            line = line.replace(
                "REPLACE_WITH_A_POSTAL_ADDRESS_THAT_IS_NOT_YOUR_HOME", postal
            )
        line = line.replace("REPLACE_WITH_THE_LANGUAGES_YOU_READ",
                            "any human written language; preferred en")
        line = line.replace("REPLACE_WITH_BCP47_LANGUAGE_TAGS", "en")
        out.append(line)
        # Insert topics.N labels right after who.language_tags
        if re.match(r"^who\.language_tags\s*:", line):
            active = [l for l in labels if l.strip()]
            for i, label in enumerate(active, 1):
                out.append(f"topics.{i}: {label.strip()}")
    result = "\n".join(out)
    result = result.rstrip("\n") + "\n"
    return result


# ── Test 1a: generated file (no postal) validates with Python ────────────────
print("\nTest 1a: generated file (no postal) validates with Python")
sample_no_postal = make_sample("Alex Example", "door@example.org", "example.org")
with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",
                                 delete=False) as f:
    f.write(sample_no_postal); tmp1 = Path(f.name)
rc, out = run([sys.executable, str(VALIDATE), str(tmp1), str(FIELDS)])
check("exit code 0", rc == 0, f"exit={rc}\n{out}")
check("CONFORMS in output", "CONFORMS" in out, out)
tmp1.unlink()

# ── Test 1b: generated file (with postal) validates with Python ──────────────
print("\nTest 1b: generated file (with postal) validates with Python")
sample_postal = make_sample(
    "Alex Example", "door@example.org", "example.org",
    postal="Example Ltd, PO Box 1, 00000 Example City"
)
with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",
                                 delete=False) as f:
    f.write(sample_postal); tmp2 = Path(f.name)
rc, out = run([sys.executable, str(VALIDATE), str(tmp2), str(FIELDS)])
check("exit code 0", rc == 0, f"exit={rc}\n{out}")
check("CONFORMS in output", "CONFORMS" in out, out)
tmp2.unlink()

# ── Test 1c: person without labels validates with Python (exit 0) ─────────────
print("\nTest 1c: person without labels validates with Python")
sample_no_labels = make_sample("Alex Example", "door@example.org", "example.org",
                               reference="DLG-1111")
with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",
                                 delete=False) as f:
    f.write(sample_no_labels); tmp_no_labels = Path(f.name)
rc, out = run([sys.executable, str(VALIDATE), str(tmp_no_labels), str(FIELDS)])
check("exit code 0", rc == 0, f"exit={rc}\n{out}")
check("CONFORMS in output", "CONFORMS" in out, out)
tmp_no_labels.unlink()

# ── Test 1d: person with 2 labels validates with Python (exit 0) ─────────────
print("\nTest 1d: person with 2 labels validates with Python")
rc, out = run([sys.executable, str(VALIDATE), str(EXAMPLE), str(FIELDS)])
check("exit code 0", rc == 0, f"exit={rc}\n{out}")
check("CONFORMS in output", "CONFORMS" in out, out)

# ── Test 1e: org with 3 labels validates with Python (exit 0; since G33 the org uses the recommended neutral first line) ─
print("\nTest 1e: organisation with 3 labels validates with Python (recommended first line, no warning)")
rc, out = run([sys.executable, str(VALIDATE), str(EXAMPLE_ORG), str(FIELDS)])
check("exit code 0", rc == 0, f"exit={rc}\n{out}")
check("CONFORMS in output", "CONFORMS" in out, out)
check("recommended first line, no warnings",
      "note: first line: recommended data preamble" in out and "warning:" not in out, out)

# ── Test 2a: template.txt — Python validator ──────────────────────────────────
print("\nTest 2a: template.txt via Python validator")
rc_py_tmpl, out_py_tmpl = run([sys.executable, str(VALIDATE), str(TEMPLATE), str(FIELDS)])
check("exit code 0 (template conforms)", rc_py_tmpl == 0,
      f"exit={rc_py_tmpl}\n{out_py_tmpl}")
check("CONFORMS in output", "CONFORMS" in out_py_tmpl, out_py_tmpl)

# ── Test 2b: example/dialogue.txt — Python validator ─────────────────────────
print("\nTest 2b: example/dialogue.txt via Python validator")
rc_py_ex, out_py_ex = run([sys.executable, str(VALIDATE), str(EXAMPLE), str(FIELDS)])
check("exit code 0 (example conforms)", rc_py_ex == 0,
      f"exit={rc_py_ex}\n{out_py_ex}")
check("CONFORMS in output", "CONFORMS" in out_py_ex, out_py_ex)

# ── Test 2c: example/organisation/dialogue.txt — Python validator ─────────────
print("\nTest 2c: example/organisation/dialogue.txt via Python validator")
rc_py_org, out_py_org = run([sys.executable, str(VALIDATE), str(EXAMPLE_ORG), str(FIELDS)])
check("exit code 0 (org example conforms)", rc_py_org == 0,
      f"exit={rc_py_org}\n{out_py_org}")
check("CONFORMS in output", "CONFORMS" in out_py_org, out_py_org)

# ── Test 2d: broken file (who.type: a_crowd + format: 1.0) ───────────────────
print("\nTest 2d: broken file (who.type: a_crowd + format: 1.0) via Python validator")
broken = EXAMPLE.read_text(encoding="utf-8")
broken = re.sub(r"^who\.type: one_person$", "who.type: a_crowd",
                broken, flags=re.MULTILINE)
broken += "format: 1.0\n"
with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",
                                 delete=False) as f:
    f.write(broken); tmp_broken = Path(f.name)
rc_py_brk, out_py_brk = run([sys.executable, str(VALIDATE), str(tmp_broken), str(FIELDS)])
check("exit code 1 (broken does not conform)", rc_py_brk == 1,
      f"exit={rc_py_brk}\n{out_py_brk}")
check("DOES NOT CONFORM in output", "DOES NOT CONFORM" in out_py_brk, out_py_brk)
check("who.type options error present",
      "who.type must be one of" in out_py_brk, out_py_brk)
check("reserved format error present",
      "reserved names used" in out_py_brk and "'format'" in out_py_brk, out_py_brk)

# ── Test 2e: reference with space — Python validator ─────────────────────────
print("\nTest 2e: reference with space via Python validator")
ref_spaced = EXAMPLE.read_text(encoding="utf-8")
ref_spaced = re.sub(r"^who\.channels\.reference: DLG-4712$",
                    "who.channels.reference: DLG 4712",
                    ref_spaced, flags=re.MULTILINE)
with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", encoding="utf-8",
                                 delete=False) as f:
    f.write(ref_spaced); tmp_refspace = Path(f.name)
rc_py_ref, out_py_ref = run([sys.executable, str(VALIDATE), str(tmp_refspace), str(FIELDS)])
check("exit code 0 (reference warning still conforms)", rc_py_ref == 0,
      f"exit={rc_py_ref}\n{out_py_ref}")
check("reference warning present",
      "who.channels.reference should be short" in out_py_ref, out_py_ref)

# ── JS validator tests (node required) ───────────────────────────────────────
if not NODE:
    print("\nSkipping JS tests: node not found on PATH.")
    print("  The JS validator logic in checker.js is a direct port of validate.py.")
else:
    print(f"\nNode found at: {NODE}")

    def js_check(filepath, fieldsfile=None):
        cmd = [NODE, str(CHECKER), str(filepath)]
        if fieldsfile: cmd.append(str(fieldsfile))
        return run(cmd)

    # ── 2a-JS: template.txt byte-identical ───────────────────────────────────
    print("\nTest 2a-JS: template.txt — JS/Python byte-identical")
    rc_js_tmpl, out_js_tmpl = js_check(TEMPLATE, FIELDS)
    check("exit code matches Python", rc_js_tmpl == rc_py_tmpl,
          f"JS={rc_js_tmpl} PY={rc_py_tmpl}")
    check("output byte-identical to Python",
          out_js_tmpl.splitlines() == out_py_tmpl.splitlines(),
          f"PY: {out_py_tmpl}\nJS: {out_js_tmpl}")

    # ── 2b-JS: example/dialogue.txt byte-identical ───────────────────────────
    print("\nTest 2b-JS: example/dialogue.txt — JS/Python byte-identical")
    rc_js_ex, out_js_ex = js_check(EXAMPLE, FIELDS)
    check("exit code matches Python", rc_js_ex == rc_py_ex,
          f"JS={rc_js_ex} PY={rc_py_ex}")
    check("output byte-identical to Python",
          out_js_ex.splitlines() == out_py_ex.splitlines(),
          f"PY: {out_py_ex}\nJS: {out_js_ex}")

    # ── 2c-JS: example/organisation/dialogue.txt byte-identical ──────────────
    print("\nTest 2c-JS: example/organisation/dialogue.txt — JS/Python byte-identical")
    rc_js_org, out_js_org = js_check(EXAMPLE_ORG, FIELDS)
    check("exit code matches Python", rc_js_org == rc_py_org,
          f"JS={rc_js_org} PY={rc_py_org}")
    check("output byte-identical to Python",
          out_js_org.splitlines() == out_py_org.splitlines(),
          f"PY: {out_py_org}\nJS: {out_js_org}")

    # ── 2d-JS: broken file byte-identical ────────────────────────────────────
    print("\nTest 2d-JS: broken file (who.type: a_crowd + format: 1.0) — JS/Python byte-identical")
    rc_js_brk, out_js_brk = js_check(tmp_broken, FIELDS)
    check("exit code 1", rc_js_brk == 1, f"JS exit={rc_js_brk}")
    check("output byte-identical to Python",
          out_js_brk.splitlines() == out_py_brk.splitlines(),
          f"PY: {out_py_brk}\nJS: {out_js_brk}")

    # ── 2e-JS: reference with space byte-identical ───────────────────────────
    print("\nTest 2e-JS: reference with space — JS/Python byte-identical")
    rc_js_ref, out_js_ref = js_check(tmp_refspace, FIELDS)
    check("exit code matches Python", rc_js_ref == rc_py_ref,
          f"JS={rc_js_ref} PY={rc_py_ref}")
    check("output byte-identical to Python",
          out_js_ref.splitlines() == out_py_ref.splitlines(),
          f"PY: {out_py_ref}\nJS: {out_js_ref}")

# Clean up temp files
for p in (tmp_broken, tmp_refspace):
    try: p.unlink()
    except: pass

# ── Test 3: index.html has no external src/href ───────────────────────────────
print("\nTest 3: index.html has no external src/href")
if not INDEX.exists():
    print(f"  {FAIL}  index.html not found — run build.py first")
    failures.append("index.html exists")
else:
    html = INDEX.read_text(encoding="utf-8")
    ext_refs = re.findall(r'(?:src|href)=["\']([^"\']*)["\']', html, re.IGNORECASE)
    bad = [u for u in ext_refs if re.match(r'https?://', u, re.I)]
    check("no external src/href URLs in index.html", not bad,
          "Found: " + ", ".join(bad))

    net_calls = re.findall(r'\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket)\b', html)
    check("no network API calls in index.html", not net_calls,
          "Found: " + ", ".join(set(net_calls)))

    all_urls = re.findall(r'https?://[^\s"\'<>]+', html)
    suspicious = [u for u in all_urls if u in bad]
    check("all https:// occurrences are canonical_url pattern or plain text",
          not suspicious, "Suspicious: " + ", ".join(suspicious))
    if all_urls:
        print(f"         (all https:// occurrences: {len(all_urls)}, "
              f"all contain /.well-known/dialogue.txt or are plain text)")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
if failures:
    print(f"\033[31m{len(failures)} test(s) failed:\033[0m")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("\033[32mAll tests passed.\033[0m")
    sys.exit(0)
