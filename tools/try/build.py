#!/usr/bin/env python3
"""
Build index.html from page.template.html by injecting dialogue.txt template and fields.xml.
Source of truth: ../../template/dialogue.txt and ../../fields.xml (relative to this script).
Usage: python3 build.py
Standard library only. CC0.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent   # tools/try -> tools -> standard

template_html = (HERE / "page.template.html").read_text(encoding="utf-8")
dialogue_txt  = (ROOT / "template" / "dialogue.txt").read_text(encoding="utf-8")
fields_xml    = (ROOT / "fields.xml").read_text(encoding="utf-8")

# Inject as JSON string literals so the values are safely escaped
out = template_html.replace(
    "/*__TEMPLATE_TXT__*/",
    json.dumps(dialogue_txt)
).replace(
    "/*__FIELDS_XML__*/",
    json.dumps(fields_xml)
)

dest = HERE / "index.html"
dest.write_text(out, encoding="utf-8")
print(f"Written: {dest}")
print(f"  template: {len(dialogue_txt)} bytes")
print(f"  fields:   {len(fields_xml)} bytes")
print(f"  output:   {len(out)} bytes")
