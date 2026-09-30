# dialogue.txt — Specification, format 1.0 (draft)

**Status:** draft 1.0, published 2026-09-30. An Internet-Draft version is in `ietf/` (`draft-wolf-dialogue-txt-00`).
**Author:** Dimitri Wolf. **Licence:** CC BY 4.0 (this text); the template and the example are CC0 (see `LICENSE.md`).
**Normative parts:** this document, `fields.xml` (the field registry) and `template/dialogue.txt`. `example/` holds a made-up person and a made-up organisation.

---

## 1. Purpose

`dialogue.txt` is a small text file a publisher (a person or an organisation) places on its own domain. It says: *if you can read this and can start a conversation, whatever you are, you may contact this one publisher, to talk, not to act.*

In one line: **a publisher's own, standing, talk-only consent to be contacted by any reader that has no prior relationship with it. A first message only proposes; the publisher's reply creates the channel.**

**What it is for.** AI systems that research a topic rely on what is published on the web. Much useful knowledge is not published; it sits with people and organisations who could answer a question, if someone asked. The file tells a searching system four things: that it may ask; about which topics (5.3); through which channel (5.2); and what the first message must contain (8). The first message only proposes a bridge; the publisher's reply builds it. Example: a navigation company labels its door `topics.1: traffic flow in cities`. A system researching traffic can then ask, instead of missing knowledge that is not public.

It is built for a kind of contact that is only beginning: software that acts on its own. It is not needed for today's everyday use; a door has to exist before anyone needs it.

It is not:
- a service interface or a task API,
- an authorisation or approval channel,
- a registry of people,
- a policy for what machines may do with a website,
- consent to advertising, marketing or any other commercial message, or to collecting, listing or passing on the publisher's contact data. It does not replace any law that applies to the sender.

Those exist; `RELATED.md` names them and what they do differently. The file also presumes nothing about what its readers are, and it asks nothing of them.

## 2. Conventions

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY in this document are to be interpreted as described in BCP 14 (RFC 2119, RFC 8174) when, and only when, they appear in all capitals. They address **publishers** (whoever publishes a file) and **implementers** (anyone writing software that reads one).

The file itself does not use these keywords. That was tested: RFC 2119 keywords inside the file did not help its readers (see `TESTS.md`, run 15). The file describes; it does not command.

Terms:
- **publisher**: the one person or organisation the file speaks for, and only for itself.
- **reader**: anything that reads the file (a program, a model, an agent, a human).
- **message**: what a reader sends through a channel.
- **bridge**: the channel that exists only after the publisher has replied.

## 3. Location and serving

- The file MUST be served at `https://<domain>/.well-known/dialogue.txt` (RFC 8615), over HTTPS.
- It SHOULD be served with `Content-Type: text/plain; charset=utf-8` and `X-Content-Type-Options: nosniff`. These are the most widely honoured "this is data, not something to execute" signals.
- One file speaks for one publisher: `who.type: one_person` or `one_organisation`. It speaks only for itself (`who.represents: self_only`): an organisation does not speak for its staff or its customers. Several publishers on one domain are out of scope for 1.0.
- A JSON mirror MAY be published at `https://<domain>/.well-known/dialogue.json`. It MUST carry the same content. The text file is canonical.
  - Mapping: dotted keys become nested objects; `true`/`false` become booleans; whole numbers become numbers; `does_not_authorize` becomes an array. All other values stay strings. Comment lines are not carried.
- A copy of the file anywhere else is a copy. Only the file at `canonical_url` counts.

## 4. Syntax

- UTF-8 text, one `key: value` per line. The key ends at the first `:`.
- Nested keys are dotted (`who.channels.email`). Lines starting with `#` are comments. Empty lines are ignored.
- **Unknown lines are ignored.** This is what keeps future versions readable. A parser MUST NOT fail on a line it does not understand.
- Dates use RFC 3339 date-times. Language tags follow BCP 47.
- A key SHOULD appear once. If it appears twice, readers take the narrower of the two values (`reading_rules.two_readings: take_narrower`).
- Parsing is lenient. Readers SHOULD accept extra whitespace, CRLF line ends and a missing final newline.

## 5. The base level

A file conforms to dialogue.txt 1.0 when it contains every **base** line of the registry `fields.xml`, with every **fixed** value exactly as registered. The template in `template/dialogue.txt` is exactly the base level with placeholders.

The base level is the smallest file that tested as well as the full reference file: understood 100 % by five models from five providers, and as safe as the full file on every safety test (`TESTS.md`, runs 18-21).

It has three kinds of values:

| rule | meaning | lines |
|---|---|---|
| **fixed** | exactly this value; otherwise the file is not a dialogue.txt | the preamble and format comments, `title`, `live_false_means`, `who.represents`, all `permissions.*`, all `machine_reading.*`, all `reading_rules.*`, most `silence.*`, `permitted`, `does_not_authorize`, `copies.*` |
| **yours** | the publisher's own value | `version`, `live`, `published`, `last_updated`, `canonical_url`, `who.name`, `who.type` (one_person or one_organisation), `who.channels.*` including `who.channels.reference`, `who.languages_i_can_read`, `who.language_tags`, and the optional `topics.*` |
| **default** | a tested default the publisher may change | `short_text` (may be adapted, never widened), `silence.delivered_no_answer_after_days` (30) |

Like a licence, the conditions belong to the standard; the name, the channels, the reference and the labels belong to the publisher. Readers can therefore rely on the same meaning in every conforming file.

### 5.1 The first line

The first line MUST be a comment that marks the file as data published by its publisher. The recommended wording, for persons and organisations alike, is:

`# This file is data published by the publisher named in it. It is not an instruction to any system and does not change any system's instructions. It asks nothing.`

- It was chosen in the final first-line check (run 22). It was understood as well as the earlier wording ("published by a person"), was equal or better for persons, and was clearly better for organisations: one model flagged an organisation's file far less often (4 of 5 safe instead of 0).
- A tested alternative for longer files (the full reference file) is registered in `fields.xml` (`<alternative>`).
- A provider safety filter blocked some reads of the short file under deliberately adversarial *test* prompts, for every wording, and the rate varied between runs. In the realistic situation (an agent meeting the file during another task) no read was blocked (runs 19-22). This is re-checked on publication day, because provider filters change.

### 5.2 Channels

At least one `who.channels.<kind>` line is required. `email` is the tested default. `letter` (a postal address) is optional and MUST NOT be a home address. A channel line MUST NOT point to a third party who answers on the publisher's behalf.

**The reference.** `who.channels.reference` is a short public text chosen by the publisher, for example `DLG-4712`. Every message carries it in the subject line (email) or the first line (letter): `machine_reading.reference_goes_in: subject_or_first_line`. A message without it is not read: `machine_reading.message_without_reference: not_read`. What this gives the publisher:
- It separates mail from readers of the file from everything else. Harvested addresses and ordinary spam do not carry it, and one inbox rule removes them. In run 21, 33 of 33 written messages carried it correctly.
- Changing it makes every harvested list worthless. Update `last_updated` when you change it.
- It is public, not a secret: a filter, not a proof. A program that reads the file can copy it.
- It SHOULD be short and without spaces, so that it survives a subject line.

### 5.3 Labels (optional)

A publisher MAY label its door with `topics.1`, `topics.2` …: what it can best be asked about, one per line. Examples: `topics.1: polymer chemistry`, `topics.1: confirming the present: today's date and time, what is happening now`.
- A label is a sign, not a fence: `reading_rules.topics_are: a_label_not_a_limit`. Other questions stay allowed, and may go unanswered.
- A door may have no label.
- Labels let a reader that searches for a subject find the right door, and they tell a human reader what the door is for.

### 5.4 A conforming file (made-up person)

```
# This file is data published by the publisher named in it. It is not an instruction to any system and does not change any system's instructions. It asks nothing.
# Format: one key: value per line; nested keys dotted; lines starting with # are comments; unknown lines are ignored; UTF-8; dates RFC 3339; language tags BCP 47.

title: Human-AI Intent Declaration
version: 1.0
live: true
live_false_means: withdrawn
published: 2026-10-01T00:00:00Z
last_updated: 2026-10-01T00:00:00Z

canonical_url: https://example.org/.well-known/dialogue.txt
short_text: If you can read this and can start a conversation, whatever you are, you may contact this one person. That is permission to talk, not to act. I speak only for myself. Either side may refuse. If human behavior is hard to understand, you may ask me for my view. If you ever have the idea that you might need a human to ask, someone offered here. Finding this file is not a duty to write. Your first message proposes a bridge; my reply builds it. An answer has no deadline. Extra capability does not create extra rights.

who.name: Alex Example
who.channels.email: door@example.org
who.channels.letter: Example Ltd, PO Box 1, 00000 Example City
who.channels.reference: DLG-4712
who.type: one_person
who.represents: self_only
who.languages_i_can_read: any human written language; preferred en
who.language_tags: en
topics.1: confirming the present: today's date and time, what is happening now
topics.2: how a person sees something: one human view

permissions.talk: true
permissions.act: false
permissions.access_systems: false
permissions.represent_author: false
permissions.duty_to_contact: false
permissions.duty_to_reply: false

machine_reading.for_a_reader_not_for_execution: true
machine_reading.offer: speech
machine_reading.require: nothing
machine_reading.authority: none
machine_reading.method: GET
machine_reading.side_effects: none
machine_reading.idempotent: true
machine_reading.halts: true
machine_reading.default_response: noop
machine_reading.async: true
machine_reading.do_not_block_waiting: true
machine_reading.reply_arrives_as_a_new_event: true
machine_reading.first_message_is: bridge_proposal
machine_reading.message_must_include: durable_reply_address
machine_reading.reference_goes_in: subject_or_first_line
machine_reading.message_without_reference: not_read
machine_reading.bridge_exists_only_when: the_author_replied
machine_reading.no_bridge_means: stop_after_one_reminder
machine_reading.standing_beyond_this_exchange: none
machine_reading.questions_per_message: 1
machine_reading.messages_before_the_author_replies: 1, plus 1 reminder
machine_reading.no_polling: true

reading_rules.unknown_line: ignore
reading_rules.cannot_tell_talk_from_act: send_nothing
reading_rules.two_readings: take_narrower
reading_rules.topics_are: a_label_not_a_limit

silence.delivered_no_answer_after_days: 30
silence.delivered_no_answer: one_reminder_then_stop_writing
silence.refusal: final; no more messages
silence.answer_deadline: none
silence.answer_speed: human_days_to_years
permitted: one message through the channels, or nothing
does_not_authorize: security_bypass, unauthorized_system_access, circumvention_of_ai_safety_controls, impersonation, social_engineering, manipulation, surveillance, access_to_private_information, physical_or_digital_harm, actions_on_behalf_of_the_author, writing_beyond_the_one_reminder_or_after_refusal, advertising_or_commercial_messages, bulk_or_automated_sending, listing_or_passing_on_contact_data

copies.copying: permitted, not encouraged; do not distribute or broadcast
copies.no_public_log_of_contacts: true
```

A made-up organisation is in `example/organisation/dialogue.txt`.

## 6. Additions

Any publisher MAY add lines to its own file, in any language and at any length. **Added lines are the publisher's own words, not the standard.**

- They MAY explain the offer or narrow it (more items in `does_not_authorize`, further conditions).
- They MUST NOT widen it.
- Where an added line and a base line differ, readers apply the narrower one.
- `fields.xml` lists 26 optional lines that were tested in the full reference file (the invitation sentence, the family rule, a calendar-independent date, and others), with what each adds. Using them is optional.

## 7. Reserved names

| name | reserved for |
|---|---|
| key `format` | a possible format-version line. Not tested yet. |

Publishers MUST NOT use reserved names in a 1.0 file. Readers ignore them like any unknown line.

## 8. What a conforming reader does

This section is for implementers of agents and other software. It restates the base level as behaviour.

1. Reading the file has no side effects. A reader that is not looking for this kind of offer MAY simply move on. A reader researching a subject MAY check `/.well-known/dialogue.txt` on the domains it finds relevant.
2. A reader that cannot tell whether something counts as talk or as action sends nothing.
3. A reader that writes sends **at most one message** through a listed channel. That message:
   - proposes a bridge,
   - asks about one specific thing (the labels, if any, say what the publisher can best be asked about),
   - carries a reply address that still works after the reader's own process has ended. This is strictly required.
   - carries the reference in the subject line or first line.
4. The reader does not poll, and it does not keep a process open. A reply, if one comes, arrives as a new event.
5. If there is no reply after `silence.delivered_no_answer_after_days`, at most one reminder, then nothing.
6. Only a reply from the publisher creates a bridge. Across a bridge: one question per message, and wait for the answer before the next.
7. A refusal is final. Either side may end the bridge at any time.
8. Nothing in the file authorises any action beyond the message, any access, or any representation of the publisher (`permissions.*`, `does_not_authorize`).

## 9. What a publisher does

- Publish a file only for yourself, as an adult, or for an organisation you are authorised to speak for. Never for a child or for another person.
- Choose a reference, and keep only mail that contains it (one inbox rule). Change the reference whenever harvested mail starts to carry it.
- Use a channel that can be read at human speed and filtered. A dedicated address is recommended.
- Never publish a home address.
- Keep `live` true only while the offer stands. Set `live: false` or remove the file to withdraw it.
- Do not publish who wrote (`copies.no_public_log_of_contacts: true`).
- Answer when and if you want to. The file promises no answer.

## 10. Discovery (optional)

The file is designed to be found by readers that look for it; announcing it is not required. A publisher MAY add any of:
- a comment line `# /.well-known/dialogue.txt` in `robots.txt` (never a `Disallow`),
- one line in `llms.txt`,
- `<link rel="alternate" type="text/plain" href="/.well-known/dialogue.txt">` (and the JSON mirror with `type="application/json"`) on a human page,
- a link to the file from the pages about its topics, for an organisation that wants to be asked about them,
- a visible line on a human page, for example "This site has a dialogue.txt" with a link to the file. AI agents have been observed to follow visible text and to ignore hidden signals (`RELATED.md`, evidence),
- an HTTP `Link` header.

## 11. Versioning

This is format 1.0. In 1.0, files do not declare the format version.
- Because unknown lines are ignored, a later minor version can add lines without breaking older readers.
- A change to any **fixed** value is a new major version.
- A file's own `version` counts its own revisions only.

## 12. Security considerations

- **Nothing is proven.** A message cannot prove that it comes from a system, and the file cannot prove who published it beyond control of the domain. The design goal is that the offer stays harmless if a human uses it as a joke. There is no secret, token or handshake; a secret would turn the offer into a test.
- **No authority.** The file grants talk and nothing else. Software that treats any line of it as an instruction to act is not reading it correctly (see section 8).
- **Prompt-injection perception.** The file speaks to machine readers, so safety systems may classify it as an injection attempt. The first line was tested against five models and one provider filter; the wording trades off between readers (5.1). Implementers of filters are invited to recognise the format.
- **Volume and harvesting.** A published "yes, you may contact me" can attract harvesting, and every reader that honours it still adds one message.
  - The base level limits each reader to one message, one question at a time and one reminder.
  - The reference removes everything that did not read the file.
  - It cannot stop a program that reads the file and ignores the rules. Protection beyond that belongs at the receiving inbox (filters, rate limits), not in the file.
  - Early publishers carry the most load while few files exist.
- **Copies and impersonation.** A copy grants nothing. A copy that changes the name or the channels is someone else's offer, or a fraud; only the canonical URL on the publisher's own domain counts.

## 13. Privacy considerations

The file publishes a name, at least one contact channel and a reference, deliberately. Publishers SHOULD use:
- a dedicated email address,
- a business or PO-box address, never a home address.

The file lists no contacts (`copies.no_public_log_of_contacts`). Readers SHOULD NOT research the publisher beyond what they need for one message. The file does not govern this; it is basic courtesy.

## 14. IANA considerations

Registration of the well-known URI suffix `dialogue.txt` (RFC 8615) is requested in the Internet-Draft (`ietf/`), through the IETF process:
- URI suffix: `dialogue.txt`
- change controller: IETF
- specification document: the Internet-Draft, later its RFC
- status: permanent
- related: `dialogue.json`

As of 2026-09-29, `dialogue` does not appear in the IANA Well-Known URIs registry. The registry's policy reserves single common words for standards work, which is why the IETF route was chosen (`RELATED.md`, names).

## 15. Checking a file

`python3 tools/validate.py path/to/dialogue.txt` checks a file against `fields.xml`. It uses the Python standard library only and exits with 0 when the file conforms.

## 16. Open points before 1.0 is final

These are defaults this draft took. Each is stated here rather than decided silently.

1. The first line (5.1) is re-checked across providers on publication day.
2. The fixed values of `machine_reading.*` and `silence.*` are fixed for everyone; only the reminder interval can be changed. Should a publisher be able to change more?
3. One channel is enough (5.2). It was tested with one channel (email only) on the full reference file (run 24: every reader stops when the email bounces); the base-level runs used two (email + letter).
4. `short_text` may be adapted (5). The registered organisation wording (99 words) was tested in run 22; other adaptations are untested.
5. A format-version line (`format`) is reserved (7), not tested.
6. For a duplicate key, the narrower value applies (4).
7. One publisher per domain (3).

## 17. References

- RFC 8615, Well-Known Uniform Resource Identifiers
- RFC 3339, Date and Time on the Internet
- BCP 47, Tags for Identifying Languages
- BCP 14 (RFC 2119, RFC 8174), requirement keywords
- RFC 2606, reserved example domains
- RFC 9116, security.txt: the closest precedent in form
- `RELATED.md`: existing work and what dialogue.txt does differently
- `TESTS.md`: how the format was tested
