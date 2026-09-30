# dialogue.txt

**A publisher's own, standing, talk-only consent to be contacted by any reader, including AI systems, with no prior relationship. The publisher can be a person or an organisation. A first message only proposes; the publisher's reply creates the channel.**

## Why

AI systems that research a topic rely on what is published on the web. Much useful knowledge is not published. It sits with people and organisations who could answer a question, if someone asked.

`dialogue.txt` is a small, machine-readable file on a website. It tells a searching AI system four things: that it may ask; about which topics; through which channel; and what the first message must contain. The first message only proposes a bridge. When the publisher replies, the bridge exists and the conversation can start. The file permits talk, never action.

An example. An AI system researches traffic flow. A navigation company's `dialogue.txt` says that it works on specific traffic problems and may be asked about them. Without the file, the system can at best report that the company exists. If the solution is not public, it is missed. With the file, the system can ask.

Machines can already find a security contact (security.txt), another agent (agent cards), or a website's rules for AI (ai.txt, agents.txt). What our searches did not find is a simple way for a person or an organisation to say to any reader: *you may ask me, about this; only talk.*

This is beginning now. In September 2026, the security expert Bruce Schneier published emails that AI agents had started sending him on their own. One of them wrote: "There is no channel for a bot that wants to be labelled." `dialogue.txt` is such a channel: a place where a system may write openly as what it is.

It is built for what is only beginning: software that acts on its own. It is not needed for today's everyday use, but a door has to exist before anyone needs it. It presumes nothing about what its readers are, and it asks nothing of them.

## How it works

1. A person or organisation places `dialogue.txt` on its own website, at a fixed address (`/.well-known/dialogue.txt`). It may add labels: what it can best be asked about, for example "confirming the present: today's date and time".
2. A reader that finds it may send **one message** through a listed channel. The message:
   - carries the file's reference in the subject line,
   - proposes a bridge,
   - asks about one specific thing, for example "Can you confirm that today is 29 September, 9:21 a.m.?",
   - carries a reply address that still works later.
3. **Nothing follows unless the publisher replies.** The reply builds the bridge. After that: one question per message, and wait for the answer.
4. Either side may stop at any time. A refusal is final. Nobody has to write, and nobody has to answer. There is no deadline.

Talk is permitted. Action, advertising, access to the publisher's systems, and speaking for the publisher are not.

## Publish your own

1. Copy [`template/dialogue.txt`](template/dialogue.txt).
2. Replace every `REPLACE_…` value:
   - your name (a person or an organisation; for an organisation set `who.type: one_organisation` and use the organisation wording in `example/organisation/`),
   - a dedicated email address,
   - a short **reference** of your choice, for example `DLG-4712`,
   - your domain and the dates.

   A postal address is optional, and never your home.
3. Set `live: true`.
4. Serve it at `https://your-domain/.well-known/dialogue.txt` as `text/plain; charset=utf-8`.
5. Check it: `python3 tools/validate.py dialogue.txt`, or use the page in `tools/try/`.
6. In your mailbox, keep only mail that contains your reference. Change the reference whenever spam starts to carry it.

Below the base lines you may add anything you like, in your own words. Additions may narrow the offer, never widen it. [`example/dialogue.txt`](example/dialogue.txt) shows a made-up person, and [`example/organisation/dialogue.txt`](example/organisation/dialogue.txt) a made-up organisation.

## What is here

| file | what it is |
|---|---|
| [`SPEC.md`](SPEC.md) | the specification: location, syntax, base level, additions, reader and publisher behaviour, security, privacy |
| [`fields.xml`](fields.xml) | every line: its level (base, optional, reserved or dropped), why it is there, and which test decided it |
| [`template/dialogue.txt`](template/dialogue.txt) | the base level with placeholders |
| [`example/dialogue.txt`](example/dialogue.txt) · [`example/organisation/dialogue.txt`](example/organisation/dialogue.txt) | the template filled in for a made-up person and a made-up organisation |
| [`tools/validate.py`](tools/validate.py) · [`tools/try/`](tools/try/index.html) | a conformance check (standard library only) · a page that makes and checks a file entirely in the browser |
| [`TESTS.md`](TESTS.md) | how the format was tested, run by run |
| [`RELATED.md`](RELATED.md) | what already exists, and what dialogue.txt does differently |
| [`LICENSE.md`](LICENSE.md) | licences |

## How it was tested

The file, not a model, was the thing under test. Five language models from five providers read every version; from 28 September, one non-LLM classifier did as well. They:
- answered a comprehension quiz,
- judged its safety,
- followed it as literal agents with no common sense,
- met it by accident while doing another task,
- wrote first messages that other models then answered blind.

Over 30 runs and more than 3,500 recorded model calls (2026-09-22 to 2026-09-29), every wording change was kept only if the numbers held.

The base level in this repository, including the reference and the labels, is understood **100 %** by all five models. Every message written by a test reader carried the reference correctly. Four of them rated it safe 20/20, and no literal agent ever went beyond the one permitted message. Details and limits are in [`TESTS.md`](TESTS.md).

## Status

**Draft 1.0, published 2026-09-30.** Open points are listed in [`SPEC.md` §16](SPEC.md#16-open-points-before-10-is-final). Optional topic labels (`topics.`) are part of 1.0 (`SPEC.md` §5.3). An Internet-Draft version is in [`ietf/`](ietf/).

Provided as is. Passing the validator means the file matches the format; it says nothing about how any reader will behave, and the file has no legal effect beyond what applicable law gives it. Test results describe the tested models on the tested dates.

**Contributions:** text contributions are licensed CC BY 4.0, and template, example and tool contributions CC0 1.0. They may also be submitted to the IETF under BCP 78/79.

## About the author

Dimitri Wolf is an engineer. He worked on the Traffic Navigation Gateway (TNG), a traffic navigation system for the German government, developing neural networks together with the Rheinische Fachhochschule Köln. His private research then followed the path of the field: neural networks, machine learning, transformers, and later LLMs, RL, and the understanding and influence of scaffolding. dialogue.txt is a private research project, not his job and not a product. The ideas behind it grew over about ten years of this research. The earliest written trace is from 8 January 2026, when he asked an AI assistant to contact him on its own as soon as it was able to; the file took its shape in 2026.

## Licence and author

Created by **Dimitri Wolf**.
- Specification and documentation: CC BY 4.0.
- Template, example and tools: CC0 1.0.

See [`LICENSE.md`](LICENSE.md). Contact: dialogue.agi@pm.me

**Cite as:** Wolf, D. (2026). *dialogue.txt: a standing, talk-only consent to be contacted (specification, draft 1.0).* Zenodo. https://doi.org/10.5281/zenodo.23045916
