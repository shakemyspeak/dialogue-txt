#!/usr/bin/env node
/**
 * dialogue.txt JS checker — same logic as the browser validator in page.template.html.
 * Usage: node checker.js path/to/dialogue.txt [path/to/fields.xml]
 * Exit 0 = conforms, 1 = does not conform. CC0.
 */
'use strict';
const fs   = require('node:fs');
const path = require('node:path');

/* ── XML parser (no DOM dependency) ──────────────────────────────────────── */
function unescapeXml(s) {
  return s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&')
          .replace(/&quot;/g,'"').replace(/&apos;/g,"'");
}

/**
 * Parse fields.xml.
 * Returns { fields, reservedKeys }.
 * Each field: { key, level, rule, value, options, alts }
 * where alts = [{ text, for, tested }] (all <alternative> elements).
 * reservedKeys = string[] from <reserved key="..."> elements.
 */
function parseFieldsXML(xmlStr) {
  const fields = [];
  const reservedKeys = [];

  /* fields */
  const re = /<field\s([^>]*)>([\s\S]*?)<\/field>/g;
  let m;
  while ((m = re.exec(xmlStr)) !== null) {
    const attrs = m[1], body = m[2];
    const ga = (n) => { const r = new RegExp(n+'="([^"]*)"').exec(attrs); return r ? r[1] : null; };
    const key     = unescapeXml(ga('key') || '');
    const level   = ga('level');
    const rule    = ga('rule');
    const options = ga('options');
    const vm      = /<value>([\s\S]*?)<\/value>/.exec(body);
    const value   = vm ? unescapeXml(vm[1]) : '';

    /* all alternatives */
    const alts = [];
    const altRe = /<alternative([^>]*)>([\s\S]*?)<\/alternative>/g;
    let am;
    while ((am = altRe.exec(body)) !== null) {
      const aAttrs = am[1];
      const text   = unescapeXml(am[2]);
      const forVal = ((/\bfor="([^"]*)"/.exec(aAttrs)) || [])[1] || '';
      const tested = ((/\btested="([^"]*)"/.exec(aAttrs)) || [])[1] || '';
      alts.push({ text, for: forVal, tested });
    }

    fields.push({ key, level, rule, value, options, alts });
  }

  /* reserved keys */
  const resRe = /<reserved\s([^>]*)>/g;
  let rm;
  while ((rm = resRe.exec(xmlStr)) !== null) {
    const km = /\bkey="([^"]*)"/.exec(rm[1]);
    if (km) reservedKeys.push(km[1]);
  }

  return { fields, reservedKeys };
}

function pyList(arr) {
  if (!arr.length) return '[]';
  return "['" + arr.map(s => String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'")).join("', '") + "']";
}

const RFC3339 = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/;

function parseDialogue(text) {
  const comments = [], kv = {};
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line) continue;
    if (line.startsWith('#')) { comments.push(line); continue; }
    const m = line.match(/^([A-Za-z0-9_.+\-]+)\s*:\s*(.*)$/);
    if (m) kv[m[1]] = m[2].trim();
  }
  return { comments, kv };
}

/**
 * Validate a dialogue.txt against parsed fields + reserved keys.
 * fields and reservedKeys come from parseFieldsXML().fields / .reservedKeys.
 */
function validateDialogue(text, fields, reservedKeys) {
  reservedKeys = reservedKeys || [];
  const { comments, kv } = parseDialogue(text);
  const errors = [], warnings = [], notes = [];
  const base      = fields.filter(f => f.level === 'base');
  const optKeys   = fields.filter(f => f.level === 'optional').map(f => f.key).filter(Boolean);
  const optionalSet = new Set(optKeys);
  const baseKeySet  = new Set(base.map(f => f.key));
  const live = kv['live'] === 'true';

  /* ── #1 first line ─────────────────────────────────────────────────────── */
  const pre = base.find(f => f.key === '#1');
  const altMap = {};  /* text → { for, tested } */
  for (const a of pre.alts) altMap[a.text] = { for: a.for, tested: a.tested };
  const first = (comments.length > 0 && text.trimStart().startsWith('#')) ? comments[0] : '';
  if (first === pre.value) {
    notes.push('first line: recommended data preamble');
  } else if (first in altMap) {
    const { for: who_for, tested } = altMap[first];
    (tested.startsWith('pending') ? warnings : notes).push(
      'first line: alternative preamble for ' + who_for + ' (' + tested + ')'
    );
  } else if (first) {
    warnings.push('first line is a comment but not a tested preamble wording');
  } else {
    errors.push('first line must be the data preamble comment');
  }

  /* ── #2 format comment ─────────────────────────────────────────────────── */
  const fmt = base.find(f => f.key === '#2').value;
  if (!comments.includes(fmt)) errors.push('the format comment line is missing or changed');

  /* ── base fields ───────────────────────────────────────────────────────── */
  for (const f of base) {
    const { key, rule, value, options } = f;
    if (key.startsWith('#')) continue;

    if (key === 'who.channels.<kind>') {
      const ch = Object.keys(kv).filter(k =>
        k.startsWith('who.channels.') &&
        (k.match(/\./g)||[]).length === 2 &&
        kv[k] &&
        !k.includes(' ') &&
        !optionalSet.has(k) &&
        !baseKeySet.has(k)
      );
      if (!ch.length) errors.push('at least one who.channels.<kind> line is required');
      continue;
    }

    if (!(key in kv)) { errors.push('missing base line: ' + key); continue; }
    const v = kv[key];

    if (rule === 'fixed') {
      if (key === 'does_not_authorize') {
        const have = new Set(v.split(',').map(x=>x.trim()));
        const need = new Set(value.split(',').map(x=>x.trim()));
        const miss = [...need].filter(x=>!have.has(x)).sort();
        const extra= [...have].filter(x=>!need.has(x)).sort();
        if (miss.length)  errors.push('does_not_authorize is missing: ' + pyList(miss));
        if (extra.length) notes.push('does_not_authorize extended (narrowing): ' + pyList(extra));
      } else if (v !== value) {
        errors.push(key + " must be exactly '" + value + "' (found '" + v + "')");
      }
    } else if (key === 'short_text') {
      const n = (v.match(/[A-Za-z']+/g)||[]).length;
      if (n > 100) warnings.push('short_text has ' + n + ' words (limit 100)');
      const stAlts = {};
      for (const a of f.alts) stAlts[a.text] = a.for;
      if (v in stAlts) {
        notes.push('short_text: tested wording for ' + stAlts[v]);
      } else if (v !== value) {
        warnings.push('short_text differs from the tested wording: make sure it does not widen the offer');
      }
    } else if (options && !options.split('|').includes(v) && !v.includes('REPLACE_')) {
      errors.push(key + ' must be one of ' + pyList(options.split('|')) + " (found '" + v + "')");
    }

    /* reference length/space warning */
    if (key === 'who.channels.reference' && !v.includes('REPLACE_') && (v.includes(' ') || v.length > 32)) {
      warnings.push('who.channels.reference should be short and without spaces, so it can be copied into a subject line');
    }
  }

  /* ── date checks ───────────────────────────────────────────────────────── */
  for (const k of ['published','last_updated']) {
    if (k in kv && !kv[k].startsWith('REPLACE_') && !RFC3339.test(kv[k]))
      errors.push(k + ' is not an RFC 3339 date-time');
  }

  /* ── canonical_url ─────────────────────────────────────────────────────── */
  const cu = kv['canonical_url'] || '';
  if (cu && !cu.startsWith('REPLACE_') && !cu.includes('REPLACE_') &&
      !/^https:\/\/[^/]+\/\.well-known\/dialogue\.txt$/.test(cu))
    errors.push('canonical_url must be https://<domain>/.well-known/dialogue.txt');

  /* ── live ──────────────────────────────────────────────────────────────── */
  if (kv['live'] !== 'true' && kv['live'] !== 'false')
    errors.push('live must be true or false');

  /* ── placeholders ──────────────────────────────────────────────────────── */
  const ph = Object.keys(kv).filter(k => kv[k].includes('REPLACE_'));
  if (ph.length) (live ? errors : warnings).push('unfilled placeholders: ' + pyList(ph));

  /* ── reserved (from fields.xml) ────────────────────────────────────────── */
  const reserved = Object.keys(kv).filter(k => reservedKeys.includes(k));
  if (reserved.length) errors.push('reserved names used (not part of 1.0): ' + pyList(reserved));

  /* ── known / added / optional-used ────────────────────────────────────── */
  const knownSet = new Set([...baseKeySet, ...optionalSet]);
  function isKnown(k) {
    if (knownSet.has(k) || k.startsWith('who.channels.')) return true;
    for (const o of knownSet) {
      if (o && o.endsWith('*') && k.startsWith(o.slice(0,-1))) return true;
      if (o && o.includes(', ') && o.split(', ').includes(k))  return true;
    }
    return false;
  }
  const added   = Object.keys(kv).filter(k => !isKnown(k) && !reserved.includes(k));
  const optUsed = Object.keys(kv).filter(k =>
    !baseKeySet.has(k) && !k.startsWith('who.channels.') && isKnown(k)
  );
  if (optUsed.length) notes.push('optional lines used: ' + optUsed.length);
  if (added.length)   notes.push('lines added by the person (narrow only): ' + pyList(added));

  const ok = errors.length === 0;
  const lv = kv['live'] !== undefined ? kv['live'] : 'undefined';
  const verdictLine = (ok ? 'CONFORMS' : 'DOES NOT CONFORM') + ' to dialogue.txt 1.0 (draft) — live: ' + lv;
  return { ok, verdictLine, errors, warnings, notes };
}

/* ── JSON conversion ─────────────────────────────────────────────────────── */
function toDialogueJSON(text) {
  const { kv } = parseDialogue(text);
  const result = {};
  for (const [key, raw] of Object.entries(kv)) {
    let value;
    if (key === 'does_not_authorize') {
      value = raw.split(',').map(x => x.trim());
    } else if (raw === 'true')  { value = true;
    } else if (raw === 'false') { value = false;
    } else if (/^\d+$/.test(raw)) { value = parseInt(raw, 10);
    } else { value = raw; }
    const parts = key.split('.');
    let obj = result;
    for (let i = 0; i < parts.length - 1; i++) {
      if (typeof obj[parts[i]] !== 'object' || obj[parts[i]] === null) obj[parts[i]] = {};
      obj = obj[parts[i]];
    }
    obj[parts[parts.length - 1]] = value;
  }
  return result;
}

/* ── CLI ─────────────────────────────────────────────────────────────────── */
if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args.length) {
    console.error('Usage: node checker.js path/to/dialogue.txt [path/to/fields.xml]');
    process.exit(2);
  }
  const HERE = __dirname;
  const dialoguePath = args[0];
  const fieldsPath   = args[1] || path.resolve(HERE, '../../fields.xml');

  const text   = fs.readFileSync(dialoguePath, 'utf-8');
  const xmlStr = fs.readFileSync(fieldsPath,   'utf-8');
  const { fields, reservedKeys } = parseFieldsXML(xmlStr);
  const result = validateDialogue(text, fields, reservedKeys);

  console.log(result.verdictLine);
  for (const e of result.errors)   console.log('  error: '   + e);
  for (const w of result.warnings) console.log('  warning: ' + w);
  for (const n of result.notes)    console.log('  note: '    + n);
  process.exit(result.ok ? 0 : 1);
}

module.exports = { parseFieldsXML, parseDialogue, validateDialogue, toDialogueJSON };
