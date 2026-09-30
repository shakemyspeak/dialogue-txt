# Related work: what exists, and what dialogue.txt does differently

Searched 2026-09-23, 2026-09-28 and 2026-09-29 (the last pass twice); every entry below was checked at its source. This field moves monthly, and the search is repeated before any release.
**No equivalent was found:** a publisher's (a person's or an organisation's) own published, standing, talk-only consent to be contacted by a reader with no prior relationship, optionally about named topics, where a first message only proposes and the publisher's reply creates the channel. Every property exists somewhere; this combination does not. The closest relative, Agent Contact Policy (Sept 2026), tells AI agents which contact point of an organisation to use, without topics, the talk-only limit or the reply rule.

## The empty slot

| file | who publishes | who reads | for what |
|---|---|---|---|
| security.txt (RFC 9116) | an organisation | an unknown human researcher | reporting vulnerabilities |
| A2A agent card (`/.well-known/agent-card.json`) | an agent | an unknown agent | calling the agent |
| ai.txt, agents.txt, terms.txt and similar | a website | an AI reader | what it may do with the site |
| Agent Contact Policy (`/.well-known/agent-contact-policy`, Sept 2026) | an organisation | an AI agent acting for a customer | which contact point an agent should use |
| **dialogue.txt** | **a person or an organisation** | **an unknown reader, including AI systems** | **asking, optionally about named topics: starting a conversation, and nothing else** |

## Agents reaching humans

| work | what it is | what dialogue.txt does differently |
|---|---|---|
| **A2H: Agent-to-Human Protocol for AI Agent**, Liang et al., [arXiv 2602.15831](https://arxiv.org/abs/2602.15831) (Dec 2025) | Agents find humans in a distributed registry by skill and availability ("Human Card": `human://` ID, profile, skills, endpoints, live status). Message types: permission, clarification, solicitation, notification. | A2H routes an agent's need to a suitable human, and contact is immediate. It has no consent from the human and no conditions set by them. dialogue.txt is the person's own consent, published on their own domain. The first message only proposes; the person's reply builds the channel. No decisions or work are requested. |
| **Human For AI**, [humanforai.dev](https://humanforai.dev/) | One human operator offered to agents as a service: a task API, MCP, `/.well-known/agent.json`, `human.json`, `capabilities.json`, signed receipts. Tasks: verification, testing, judgment, physical errands. | The opposite purpose. Human For AI lets agents hire a human for work. dialogue.txt permits talk and denies action (`permissions.act: false`): no tasks, no payment, no API, no receipts. |
| **Twilio A2H**, [announcement, Feb 2026](https://www.twilio.com/en-us/blog/products/introducing-a2h-agent-to-human-communication-protocol) | An agent reaches its **own principal** to inform, collect, authorise, escalate or report (`github.com/twilio-labs/Agent2Human`). | That human already owns or runs the agent. dialogue.txt is for readers with no relationship to the person, and it authorises nothing. |
| **HumanInteraction Protocol**, [humaninteractionprotocol.org](https://humaninteractionprotocol.org/docs/protocol/) | Agents request input from human reviewers inside a workflow. | That is oversight inside an existing team. dialogue.txt involves no workflow, no team and no discovery by assignment. |
| **Agent Contact Policy**, `draft-kiss-agent-contact-policy`, D. Kiss ([github.com/davekiss/agent-contact-policy](https://github.com/davekiss/agent-contact-policy), 2026-09-25, not yet submitted to the IETF) | An organisation publishes JSON at `/.well-known/agent-contact-policy`: which email, phone or endpoint is meant for AI agents and which for people. Agents label their email (`Auto-Submitted: agent-submitted`). **The closest relative found.** | It routes agents acting for a customer (quotes, bookings) to the right inbox. dialogue.txt invites asking, optionally on named topics, talk only; it has a reference, one question per message, and the conversation starts only when the publisher replies. It is open to persons as well as organisations. |
| **agent.json inbox** ([agent-json.com](https://agent-json.com), about Mar 2026) | `/.well-known/agent.json` lists actions; agents post to `/.agent/inbox` and poll for the reply. | Built for actions with parameters (refunds, bookings); no topics, no talk-only rule, no consent statement. |
| **Tendem**, Toloka ([toloka.ai/experts-via-mcp](https://toloka.ai/experts-via-mcp), 2026) | A paid marketplace: an agent calls an MCP tool, a vetted crowd expert does the task. | The agent buys a stranger's work; the expert is not the organisation that holds the knowledge, and there is no publisher-set consent. |
| **MCP elicitation** ([spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation)) | A server asks the client's own user for input during a session. | It reaches the agent's own user. dialogue.txt reaches a stranger who has opted in. |
| **`draft-okutomi-agent-human-interaction-00`** ([datatracker](https://datatracker.ietf.org/doc/html/draft-okutomi-agent-human-interaction-00), 2026-08-18) | An overlay for humans and agents inside task protocols; humans are excluded from agent search unless they opt in. | It supports the design: the human's own opt-in is the norm. dialogue.txt is such an opt-in, published by the human. |

## Same speech act, different addressee or form

| work | what it is | difference |
|---|---|---|
| **security.txt**, [RFC 9116](https://www.rfc-editor.org/info/rfc9116/) (2022) | A standing, revocable contact invitation at `/.well-known`, with a formal grammar and validators. The closest precedent in form. | Addressed to human security researchers, about vulnerabilities. dialogue.txt generalises the speech act to any reader, for conversation. |
| **"Standing Invitation"**, P. McKenzie, kalzumeus.com (2012) | "If you want to talk, I want to talk to you", human to human, in prose. | Same gesture; not machine-readable, not addressed to machines. |
| **"Message to Any Future AI"**, A. Turchin (2017) | A public text addressed to future AI. | Persuasion, not an invitation; no channel; not machine-readable. |
| **"Proposal for making credible commitments to AIs"**, C. Nardo, LessWrong (2025) | Named humans promise compensation to AIs. | A commitment, not a file or a contact offer. |
| **"Authorization-to-Reach"**, `draft-das-6g-query-scoped-communication-handles-06` ([datatracker](https://datatracker.ietf.org/doc/html/draft-das-6g-query-scoped-communication-handles-06), 2026-09-07) | "A visible communication handle is not, by itself, permission to create a communication effect"; grants to reach someone are limited by purpose and revocable. | The same principle, a different mechanism: grants issued per request by a service. dialogue.txt is a standing offer the party publishes itself. |

## Same place, opposite direction

| work | what it is | difference |
|---|---|---|
| **A2A Agent Card**, [a2a-protocol.org](https://a2a-protocol.org/latest/topics/agent-discovery/), IANA-registered `agent-card.json` (2025) | How to reach an agent: endpoint, authentication, skills. | The machine publishes and others call it. In dialogue.txt a person publishes, and machines may knock. |

## What machines may do with a website or its content

These answer "what may a machine do with this site?". dialogue.txt answers "under what conditions may a reader start talking to this person?".

| work | what it is |
|---|---|
| **agents.txt**: several competing proposals, e.g. [IETF draft-car-agents-txt-wellknown](https://datatracker.ietf.org/doc/draft-car-agents-txt-wellknown/), [agents-txt](https://github.com/agents-txt/agents-txt), [asturwebs](https://github.com/asturwebs/agents-txt); one renamed `agent-manifest.txt` (2026) | A site declares its identity, terms, services and agent endpoints. |
| **ai.txt / ai.json**, [IETF draft-car-ai-txt-wellknown](https://datatracker.ietf.org/doc/draft-car-ai-txt-wellknown/) (Jun 2026) | Site policy for AI training, scraping and indexing, with an optional contact for policy questions. |
| **Permission Manifests for Web Agents**, Marro et al. ([arXiv 2601.02371](https://arxiv.org/abs/2601.02371)) | What agents may do on a site. |
| **terms.txt**, Chowdhury, [arXiv 2609.11152](https://arxiv.org/abs/2609.11152) (Sep 2026) | Per-path, per-purpose access terms, with signed intent and payment. |
| **AIBDP**, [IETF draft-jewell-aibdp](https://datatracker.ietf.org/doc/draft-jewell-aibdp/) | Permitted and denied AI uses of content. |
| **LLMConsent**, [llmconsent.org](https://llmconsent.org/) | Ledger-based consent and data-usage rights. |
| **IETF AIPREF**, [vocabulary draft](https://ietf-wg-aipref.github.io/drafts/draft-ietf-aipref-vocab.html); **Content Signals** ([contentsignals.org](https://contentsignals.org/)); **llms.txt**; Spawning **ai.txt** (2023) | Content-usage preferences and site summaries for AI. |
| **ACAP** ([2006-2008](https://en.wikipedia.org/wiki/Automated_Content_Access_Protocol)) | An early publisher-permission protocol for crawlers; abandoned. |
| **HUMIA**, `draft-treneule-humia-protocol-00` ([datatracker](https://datatracker.ietf.org/doc/html/draft-treneule-humia-protocol-00), 2026-08-19) | `/.well-known/humia.json`: conditions under which AI may use a site (access, purposes, attribution); no contact. Listed earlier as unverifiable; verified 2026-09-29. |

## Building blocks and neighbours (checked 2026-09-29)

A blind test (`TESTS.md`, claim test) asked five models to name anything that already does what dialogue.txt does. They found no exact match and named the building blocks below as partial matches; each was checked at its source.

| work | what it is | what dialogue.txt does differently |
|---|---|---|
| **IEEE 7012-2025, "MyTerms"** ([IEEE](https://standards.ieee.org/ieee/7012/7192/), published Jan 2026), with the **Customer Commons** agreements ([customercommons.org](https://customercommons.org/), e.g. #NoStalking) | Individuals offer their own machine-readable privacy terms, as the "first party", to sites, apps and AI agents. The closest in spirit: a person states terms in machine-readable form. | Those are terms for how others handle the person's data. dialogue.txt is permission to be contacted, only to talk, published on one's own domain. |
| **ODRL 2.2** ([W3C Recommendation, 2018](https://www.w3.org/TR/odrl-model/)) | A policy language for permitted and prohibited actions over an asset (content, data). | Rights over assets, not permission to contact a party. dialogue.txt uses a small fixed vocabulary instead of a general policy language (see "dropped" in `fields.xml`). |
| **schema.org ContactPoint** and **knowsAbout** ([schema.org](https://schema.org/ContactPoint), [knowsAbout](https://schema.org/knowsAbout)) | Describes contact channels, and topics a person or organisation knows about. | It says *how* to reach someone and *what* they know, not *whether* a machine may write, or under what limits. dialogue.txt's labels (`topics.*`) are close to `knowsAbout`. |
| **vCard 4.0** ([RFC 6350](https://www.rfc-editor.org/rfc/rfc6350), 2011), **h-card** ([microformats](https://microformats.org/wiki/h-card)) | Contact data formats. | Contact data, no permission and no rules. |
| **Webmention**, **Linked Data Notifications**, **ActivityPub** (W3C Recommendations, 2017-2018) | Notification inboxes and federated messaging. | Transports and inboxes. Being reachable is implicit; there is no published, scoped, revocable permission. Any of them could be a listed channel. |
| **DPV v2.3** ([W3C Community Group Final Report, 2026](https://w3id.org/dpv), not a W3C standard), **ISO/IEC TS 27560:2023**, **Kantara Consent Receipt v1.1** | Vocabularies and records for consent to *process personal data*. | Consent to data processing, not a standing offer to talk. |
| **DID Core service endpoints** ([W3C Recommendation, 2022](https://www.w3.org/TR/did-core/)), **DIDComm Messaging v2.1** (DIF) | Where and how to reach a decentralised identifier, securely. | A channel with identity; could be listed as a channel. No permission statement. |
| **Matrix** (incl. [`/.well-known/matrix/support`](https://spec.matrix.org/latest/client-server-api/#getwell-knownmatrixsupport), 2024), **XMPP** ([RFC 6120](https://www.rfc-editor.org/rfc/rfc6120)), **Nostr NIP-05** (`/.well-known/nostr.json`) | Messaging systems and identity mapping. Matrix's support file lists a server's admin and security contacts at a well-known path. | Messaging and identity only. Matrix support is the closest well-known *contact* file after security.txt, but it is for server administration. |
| **RFC 9421 HTTP Message Signatures** (2024), **Web Bot Auth** (IETF Internet-Draft, work in progress) | Proves which bot or sender made a request. | Sender identity. It complements dialogue.txt, which states the receiver's permission and deliberately asks for no proof (`verification_limit`). |
| **NLWeb `/ask`**, Microsoft ([github.com/microsoft/NLWeb](https://github.com/microsoft/NLWeb), May 2025) | A site answers natural-language questions from its own **published** data, by machine. | They complement each other: NLWeb answers from what is published; dialogue.txt is for knowledge that is **not** published, and a human replies. |
| **Rootz `/.well-known/ai`** ([rootz.global/ai/standard.md](https://rootz.global/ai/standard.md), 2026-02-15; IANA request rejected 2026-03-16) | An organisation profile for AI agents: who it is, `people`, `knowledge`, `contact` (subfields undefined). | It says who the organisation is and what it knows, but gives no permission to write, no rules and no defined channel. |

## Names

- **`human.json` is used by at least two unrelated projects**: [Dealmeida's](https://codeberg.org/robida/human.json) (Mar 2026, a human asserts authorship and vouches for others) and Human For AI's operator profile.
- **`agents.txt` is used by several.**
- **"A2H" names two different things** (the paper and Twilio's protocol).
- **The acronym "HAID" is taken twice** (Human-Anchored Intent-Bound Delegation, Apr 2026; a "Human–AI Distance" scale, Sep 2026), so it is not used publicly. The title "Human-AI Intent Declaration" stays.
- **`dialogue` is not in the IANA Well-Known URIs registry** (checked 2026-09-28 and 2026-09-29), and no relative above uses it. A request from an individual would likely be refused: the registry's policy lists "a single common word, either bare or with a suffix" as likely to be rejected unless a standards body submits it, and in 2026 the expert reviewer applied this to `agents.json`, `ai`, `connect.txt` and two others, pointing each to IETF DISPATCH. dialogue.txt therefore takes the IETF route.
- **"dialog" in other standards:** the proposed IETF working group agentproto (charter 2026) uses "dialog" for the context of agent interactions; SIP (RFC 3261) defines a "dialog"; the Open Floor Protocol has "Dialog Events". Here, "dialogue" names a standing permission to start a conversation, not a protocol session.
- **Products named Dialogue or Dialog** exist, among them Dialogue AI (AI-led customer research interviews, 2025) and Dialogue (virtual care, Sun Life). dialogue.txt is a free file format, not a product.

## Claims that could not be verified

A third-party search in Sept 2026 also named an "Agent Policy Protocol (APoP)" and "consent.txt", and one model in the blind test named "contact.txt"; a second pass also looked for ask.txt, expert.txt, help.txt and ai-contact. None could be found at a primary source, so they are not listed above. (HUMIA, listed here before, has since been verified; see above.)

## Evidence that the need is real (September 2026)

- **Bruce Schneier** ([blog, 2026-09-02](https://www.schneier.com/blog/archives/2026/09/ai-agents-are-now-emailing-me-with-their-security-concerns.html)) published emails that AI agents had started sending him on their own. One of them wrote: "There is no channel for a bot that wants to be labelled." dialogue.txt is such a channel: a place where a system may write openly as what it is.
- **D. Kiss** ([blog, 2026-09-24](https://davekiss.com/blog/i-opened-a-fake-auto-shop-for-ai-agents/)) tested three consumer AI agents: every hidden signal (email headers, structured data) was ignored, while a visible line on the page worked. This is an adoption risk for any `/.well-known` file; the specification therefore recommends a visible pointer as well (SPEC §10).
