#!/usr/bin/env python3
"""
Builds the Internet-Draft draft-wolf-dialogue-txt-NN.xml (xml2rfc v3) from:
  - ../fields.xml           (the base-field table and reserved names)
  - ../example/dialogue.txt (the example figure)
  - the prose below         (kept in step with ../SPEC.md)
Then renders .txt and .html with xml2rfc (HAID/.venv-ietf).
usage: python3 build_draft.py [NN] [--repo URL]   (default 00; URL = the Zenodo DOI link, e.g. https://doi.org/10.5281/zenodo.NNNNNNN)
Without --repo the [REPO] reference keeps its placeholder and the build says it is not ready for submission.
"""
import subprocess, sys
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
STD = HERE.parent
ARGS = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--repo") and sys.argv[i - 1] != "--repo"]
REV = ARGS[0] if ARGS else "00"
REPO_PLACEHOLDER = "https://example.org/REPLACE_WITH_REPOSITORY_OR_DOI"
REPO_URL = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--repo=")), None) or \
    next((sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a == "--repo"), None) or REPO_PLACEHOLDER
NAME = f"draft-wolf-dialogue-txt-{REV}"
import shutil
XML2RFC = STD.parent / ".venv-ietf" / "bin" / "xml2rfc"   # HAID venv; elsewhere: pip install xml2rfc
if not XML2RFC.exists(): XML2RFC = Path(shutil.which("xml2rfc") or "xml2rfc")

reg = ET.parse(STD / "fields.xml").getroot()
example = (STD / "example" / "dialogue.txt").read_text().rstrip("\n")

def fold8792(text, width=69):
    """RFC 8792 single-backslash folding: lines longer than `width` end in '\\'; continuation lines are indented
    by 2 spaces, which unfolding strips. Never break where the next character is whitespace."""
    out = []
    for line in text.split("\n"):
        first = True
        while len(line) > (width if first else width - 2):
            w = (width if first else width - 2) - 1
            cut = w
            while cut > 10 and line[cut] in " \t": cut -= 1
            out.append(("" if first else "  ") + line[:cut] + "\\")
            line = line[cut:]; first = False
        out.append(("" if first else "  ") + line)
    return "\n".join(out)

NUMWORD = {n: w for n, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}

def base_list():
    rows = []
    for f in reg.iter("field"):
        if f.get("level") != "base" or f.get("key").startswith("#"): continue
        key, rule, val = f.get("key"), f.get("rule"), f.find("value").text
        if key == "does_not_authorize": v = f"the {NUMWORD[len(val.split(chr(44)))]} tokens shown in Figure 1"
        elif key == "short_text": v = "the paragraph shown in Figure 1"
        elif rule == "yours": v = "(" + escape(val) + ")"
        else: v = "<tt>" + escape(val) + "</tt>"
        rows.append(f"<dt><tt>{escape(key)}</tt></dt><dd>{rule}: {v}</dd>")
    return "\n".join(rows)

def base_rows():
    rows = []
    for f in reg.iter("field"):
        if f.get("level") != "base": continue
        key = f.get("key")
        if key.startswith("#"): continue
        rule, val = f.get("rule"), f.find("value").text
        shown = val if rule in ("fixed", "default") else f"({escape(val)})"
        if key == "does_not_authorize": shown = f"the {NUMWORD[len(val.split(chr(44)))]} tokens shown in Figure 1"
        if key == "short_text": shown = "the paragraph shown in Figure 1"
        rows.append(f"<tr><td><tt>{escape(key)}</tt></td><td>{rule}</td><td>{escape(shown) if shown == val else shown}</td></tr>")
    return "\n".join(rows)

pre = next(f for f in reg.iter("field") if f.get("key") == "#1")
P1 = pre.find("value").text
P3 = next(a.text for a in pre.findall("alternative") if a.get("for") == "longer files")
FORMAT = next(f for f in reg.iter("field") if f.get("key") == "#2").find("value").text

def ref(anchor, title, series=None, author=None, org=None, year=None, month=None, target=None):
    one = lambda x: (f'<author fullname="{escape(x[0])}" initials="{escape(x[1])}" surname="{escape(x[2])}"' + (f' role="{x[3]}"' if len(x) > 3 else '') + '/>') if isinstance(x, tuple) else f'<author fullname="{escape(x)}"/>'
    a = ("".join(one(x) for x in author) if isinstance(author, list) else one(author)) if author else (f'<author><organization>{escape(org)}</organization></author>' if org else '<author/>')
    d = f'<date year="{year}"' + (f' month="{month}"' if month else '') + '/>' if year else '<date/>'
    s = "".join(f'<seriesInfo name="{n}" value="{v}"/>' for n, v in (series or []))
    t = f' target="{escape(target)}"' if target else ''
    return f'<reference anchor="{anchor}"{t}><front><title>{escape(title)}</title>{a}{d}</front>{s}</reference>'

NORMATIVE = "\n".join([
    ref("RFC2119", "Key words for use in RFCs to Indicate Requirement Levels", [("BCP", "14"), ("RFC", "2119")], author="S. Bradner", year=1997, month="March"),
    ref("RFC8174", "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", [("BCP", "14"), ("RFC", "8174")], author="B. Leiba", year=2017, month="May"),
    ref("RFC8615", "Well-Known Uniform Resource Identifiers (URIs)", [("RFC", "8615")], author="M. Nottingham", year=2019, month="May"),
    ref("RFC3339", "Date and Time on the Internet: Timestamps", [("RFC", "3339")], author=[("G. Klyne","G.","Klyne"),("C. Newman","C.","Newman")], year=2002, month="July"),
    ref("RFC5646", "Tags for Identifying Languages", [("BCP", "47"), ("RFC", "5646")], author=[("A. Phillips","A.","Phillips","editor"),("M. Davis","M.","Davis","editor")], year=2009, month="September"),
    ref("RFC3629", "UTF-8, a transformation format of ISO 10646", [("STD", "63"), ("RFC", "3629")], author="F. Yergeau", year=2003, month="November"),
    ref("RFC5234", "Augmented BNF for Syntax Specifications: ABNF", [("STD", "68"), ("RFC", "5234")], author=[("D. Crocker","D.","Crocker","editor"),("P. Overell","P.","Overell")], year=2008, month="January"),
    ref("RFC9110", "HTTP Semantics", [("STD", "97"), ("RFC", "9110")], author=[("R. Fielding","R.","Fielding","editor"),("M. Nottingham","M.","Nottingham","editor"),("J. Reschke","J.","Reschke","editor")], year=2022, month="June"),
    ref("RFC8126", "Guidelines for Writing an IANA Considerations Section in RFCs", [("BCP", "26"), ("RFC", "8126")], author=[("M. Cotton","M.","Cotton"),("B. Leiba","B.","Leiba"),("T. Narten","T.","Narten")], year=2017, month="June"),
])
INFORMATIVE = "\n".join([
    ref("RFC9116", "A File Format to Aid in Security Vulnerability Disclosure", [("RFC", "9116")], author=[("E. Foudil","E.","Foudil"),("Y. Shafranovich","Y.","Shafranovich")], year=2022, month="April"),
    ref("RFC2606", "Reserved Top Level DNS Names", [("BCP", "32"), ("RFC", "2606")], author=[("Donald E. Eastlake 3rd","D.","Eastlake 3rd"),("A. Panitz","A.","Panitz")], year=1999, month="June"),
    ref("RFC8792", "Handling Long Lines in Content of Internet-Drafts and RFCs", [("RFC", "8792")], author=[("K. Watsen","K.","Watsen"),("E. Auerswald","E.","Auerswald"),("A. Farrel","A.","Farrel"),("Q. Wu","Q.","Wu")], year=2020, month="June"),
    ref("RFC6973", "Privacy Considerations for Internet Protocols", [("RFC", "6973")], author=[("A. Cooper","A.","Cooper"),("H. Tschofenig","H.","Tschofenig"),("B. Aboba","B.","Aboba"),("J. Peterson","J.","Peterson"),("J. Morris","J.","Morris"),("M. Hansen","M.","Hansen"),("R. Smith","R.","Smith")], year=2013, month="July"),
    ref("A2H", "A2H: Agent-to-Human Protocol for AI Agent", [("arXiv", "2602.15831")], author=[("Z. Liang","Z.","Liang"),("E. Cui","E.","Cui"),("Q. Wei","Q.","Wei"),("R. She","R.","She"),("T. Li","T.","Li"),("M. Guo","M.","Guo"),("Y. Cheng","Y.","Cheng")], year=2025, month="December", target="https://arxiv.org/abs/2602.15831"),
    ref("AGENTS-TXT", "AGENTS.TXT: Capability Declarations for Web Agents", [("Internet-Draft", "draft-car-agents-txt-wellknown-00")], org="Individual submission", year=2026, month="June", target="https://datatracker.ietf.org/doc/draft-car-agents-txt-wellknown/"),
    ref("AI-TXT", "AI.TXT well-known URI", [("Internet-Draft", "draft-car-ai-txt-wellknown-00")], org="Individual submission", year=2026, month="June", target="https://datatracker.ietf.org/doc/draft-car-ai-txt-wellknown/"),
    ref("A2A", "Agent2Agent (A2A) Protocol: Agent Discovery", org="Linux Foundation A2A project", year=2025, target="https://a2a-protocol.org/latest/topics/agent-discovery/"),
    ref("AGENT-CONTACT", "Agent Contact Policy (work in progress; not submitted to the IETF as of September 2026)", author="D. Kiss", year=2026, month="September", target="https://github.com/davekiss/agent-contact-policy"),
    ref("REACH", "6G-Era Communication Authorization-to-Reach: Separating Identifier Possession from Permission to Contact", [("Internet-Draft", "draft-das-6g-query-scoped-communication-handles-06")], author="S. Das", year=2026, month="September", target="https://datatracker.ietf.org/doc/draft-das-6g-query-scoped-communication-handles/"),
    ref("NLWEB", "NLWeb", org="Microsoft", year=2025, target="https://github.com/microsoft/NLWeb"),
    ref("SCHNEIER", "AI Agents Are Now Emailing Me with Their Security Concerns", author="B. Schneier", year=2026, month="September", target="https://www.schneier.com/blog/archives/2026/09/ai-agents-are-now-emailing-me-with-their-security-concerns.html"),
    ref("KISS", "I opened a fake auto shop for AI agents", author="D. Kiss", year=2026, month="September", target="https://davekiss.com/blog/i-opened-a-fake-auto-shop-for-ai-agents/"),
    ref("RFC3261", "SIP: Session Initiation Protocol", [("RFC", "3261")], author=[("J. Rosenberg","J.","Rosenberg"),("H. Schulzrinne","H.","Schulzrinne"),("G. Camarillo","G.","Camarillo"),("A. Johnston","A.","Johnston"),("J. Peterson","J.","Peterson"),("R. Sparks","R.","Sparks"),("M. Handley","M.","Handley"),("E. Schooler","E.","Schooler")], year=2002, month="June"),
    ref("REPO", "dialogue.txt: a standing, talk-only consent to be contacted (specification, draft 1.0)", author=("Dimitri Wolf","D.","Wolf"), year=2026, target=REPO_URL),
])

BODY = f"""
<section anchor="intro"><name>Introduction</name>
<t>Software systems that research a topic rely on what is published on the web. Much useful knowledge is not published; it is held by people and organisations who could answer a question if asked. Machines can already discover a security contact <xref target="RFC9116"/>, another agent <xref target="A2A"/>, or a web site's rules for automated agents <xref target="AGENTS-TXT"/> <xref target="AI-TXT"/>. Searches in September 2026 found no simple way for a person or an organisation to state, to any reader including a software system, "you may ask me, about these topics; only talk".</t>
<t>For example, a system researching traffic flow finds a navigation company that labels its file with the topic "traffic flow in cities". Without such a file, the system can at best report that the company exists, and knowledge that is not public is missed. With it, the system can ask one question and, if the company replies, a conversation can start.</t>
<t>This document defines <tt>dialogue.txt</tt>: a small text file that a publisher (a person or an organisation) places on its own domain. It is the publisher's own, standing, talk-only consent to be contacted by any reader that has no prior relationship with it. A first message only proposes a conversation; the publisher's reply creates the channel. Talk is permitted. Action, advertising, access to the publisher's systems and representation of the publisher are not.</t>
<t>This kind of contact is beginning: AI agents have started to write to people on their own, and one such message, published by its recipient, observed: "There is no channel for a bot that wants to be labelled." <xref target="SCHNEIER"/>. A dialogue.txt file is such a channel.</t>
<t>The format is built for a kind of contact that is only beginning: software that acts on its own. It is not needed for today's everyday use; a door has to exist before anyone needs it.</t>
<t>The file is not:</t>
<ul>
<li>a service interface or a task API;</li>
<li>an authorisation or approval channel;</li>
<li>a registry of people;</li>
<li>a policy for what machines may do with a web site;</li>
<li>consent to advertising, marketing or any other commercial message, or to collecting, listing or passing on the publisher's contact data. It does not replace any law that applies to the sender.</li>
</ul>
<t>The file presumes nothing about what its readers are, and asks nothing of them.</t>
<section><name>Requirements Language</name>
<t>The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 <xref target="RFC2119"/> <xref target="RFC8174"/> when, and only when, they appear in all capitals, as shown here.</t>
<t>These key words address publishers and implementers. The file itself deliberately does not use them: it describes, it does not command (<xref target="tests"/>).</t>
</section>
<section><name>Terminology</name>
<dl>
<dt>publisher:</dt><dd>the one person or organisation the file speaks for, and only for itself.</dd>
<dt>reader:</dt><dd>anything that reads the file: a program, a model, an agent or a human.</dd>
<dt>message:</dt><dd>what a reader sends through a listed channel.</dd>
<dt>bridge:</dt><dd>the channel that exists only after the publisher has replied.</dd>
</dl>
<t>"Dialogue" in the name refers to a standing permission to start a conversation. It is not a protocol session in the sense of a SIP dialog <xref target="RFC3261"/>, nor the context of agent interactions studied elsewhere in the IETF.</t>
</section>
</section>

<section anchor="location"><name>Location and Serving</name>
<t>The file MUST be served at <tt>https://&lt;domain&gt;/.well-known/dialogue.txt</tt> <xref target="RFC8615"/> over HTTPS. It SHOULD be served with the media type <tt>text/plain; charset=utf-8</tt> <xref target="RFC9110"/> and the header field <tt>X-Content-Type-Options: nosniff</tt>. One file speaks for one publisher, a person or an organisation (<tt>who.type</tt>), and only for itself (<tt>who.represents: self_only</tt>); several publishers on one domain are out of scope of this version.</t>
<t>A copy of the file anywhere else is a copy. Only the file at the URI given in its <tt>canonical_url</tt> line counts.</t>
</section>

<section anchor="syntax"><name>Syntax</name>
<t>The file is UTF-8 text <xref target="RFC3629"/>, one "key: value" pair per line. Keys are dotted to express nesting. Lines starting with "#" are comments. Empty lines are ignored. Dates are RFC 3339 date-times <xref target="RFC3339"/>; language tags follow BCP 47 <xref target="RFC5646"/>.</t>
<sourcecode type="abnf"><![CDATA[
file    = *( line eol ) [ line ]
line    = comment / pair / blank / other
comment = "#" *( WSP / VCHAR / UTF8-non-ascii )
pair    = key ":" *WSP value
key     = 1*( ALPHA / DIGIT / "_" / "." / "-" / "+" )
value   = *( WSP / VCHAR / UTF8-non-ascii )
blank   = *WSP
other   = *( WSP / VCHAR / UTF8-non-ascii )  ; ignored
eol     = CRLF / LF
UTF8-non-ascii = %x80-10FFFF
]]></sourcecode>
<t>This grammar uses ABNF <xref target="RFC5234"/>. The key ends at the first ":". Unknown lines, including lines matching "other" and pairs with unknown keys, MUST be ignored by readers; this is what keeps later versions readable. A key SHOULD appear once; if it appears twice, readers apply the narrower of the two values. Parsers SHOULD accept extra whitespace, CRLF line ends and a missing final line end.</t>
</section>

<section anchor="base"><name>The Base Level</name>
<t>A file conforms to this specification when it contains every base line below, with every fixed value exactly as given. "Fixed" means exactly this value; "yours" means the publisher's own value; "default" means a tested default that the publisher may change. The conditions belong to the specification; the name, the channels, the reference and the labels belong to the publisher. Readers can therefore rely on the same meaning in every conforming file.</t>
<t>The first line MUST be a comment that marks the file as data published by its publisher. The RECOMMENDED wording, for persons and organisations alike, is:</t>
<blockquote><t>{escape(P1)}</t></blockquote>
<t>A tested alternative wording, better received by some readers on longer files, is:</t>
<blockquote><t>{escape(P3)}</t></blockquote>
<t>The file MUST contain the format comment line, normally directly after the first line:</t>
<blockquote><t>{escape(FORMAT)}</t></blockquote>
<t anchor="fields">The base lines (key, rule and value) are:</t>
<dl newline="true">
{base_list()}
</dl>
<t>At least one <tt>who.channels.&lt;kind&gt;</tt> line is REQUIRED. <tt>email</tt> is the tested default. <tt>letter</tt> (a postal address) is OPTIONAL and MUST NOT be a home address. A channel line MUST NOT point to a third party who answers on the publisher's behalf. <tt>short_text</tt> MAY be adapted, in 100 words or fewer, but MUST NOT widen the offer; a tested wording for organisations is registered in <xref target="REPO"/>.</t>
<t><tt>who.channels.reference</tt> is a short public text chosen by the publisher. Every message carries it in the subject line (e-mail) or the first line (letter), and a message without it is not read. It separates mail from readers of the file from harvested-address spam, and changing it invalidates harvested lists. It is not a secret and proves nothing: a program that reads the file can copy it. It SHOULD be short and contain no spaces.</t>
<t>A publisher MAY label its door with lines <tt>topics.1</tt>, <tt>topics.2</tt>, and so on: what it can best be asked about. A label is a sign, not a fence (<tt>reading_rules.topics_are: a_label_not_a_limit</tt>); other questions remain allowed. A door may have no label.</t>
<t>Figure 1 shows a conforming file for a made-up person at a domain reserved for documentation <xref target="RFC2606"/>. Long lines are folded as described in <xref target="RFC8792"/>; unfolding restores the file exactly.</t>
<figure anchor="example"><name>A Conforming File (example.org, a made-up person)</name>
<sourcecode><![CDATA[
=============== NOTE: '\\' line wrapping per RFC 8792 ================

{fold8792(example)}
]]></sourcecode></figure>
</section>

<section anchor="additions"><name>Additions</name>
<t>A publisher MAY add further lines to its own file, in any language and at any length. Added lines are the publisher's own words, not part of this specification. They MAY explain the offer or narrow it, for example by adding tokens to <tt>does_not_authorize</tt>; they MUST NOT widen it. Where an added line and a base line differ, readers apply the narrower one. The field registry in <xref target="REPO"/> lists optional lines that were tested in a full reference file.</t>
</section>

<section anchor="reserved"><name>Reserved Names</name>
<t>The key <tt>format</tt> is reserved for a possible format-version line. Publishers MUST NOT use reserved names in files conforming to this version. Readers ignore them like any unknown line.</t>
</section>

<section anchor="reader"><name>Reader Behaviour</name>
<t>This section restates the base level as behaviour, for implementers of agents and other software.</t>
<ol>
<li>Reading the file has no side effects. A reader that is not looking for this kind of offer MAY simply move on. A reader researching a subject MAY check <tt>/.well-known/dialogue.txt</tt> on the domains it finds relevant.</li>
<li>A reader that cannot tell whether something counts as talk or as action sends nothing.</li>
<li>A reader that writes sends at most one message through a listed channel. The message carries the reference in its subject or first line, proposes a bridge, asks about one specific thing, and carries a reply address that still works after the reader's own process has ended (strictly required).</li>
<li>The reader does not poll and does not keep a process open. A reply, if any, arrives as a new event.</li>
<li>Without a reply after <tt>silence.delivered_no_answer_after_days</tt>, at most one reminder, then nothing.</li>
<li>Only a reply from the publisher creates a bridge. Across a bridge: one question per message, and wait for the answer before the next.</li>
<li>A refusal is final. Either side may end the bridge at any time.</li>
<li>Nothing in the file authorises any action beyond the message, any access, or any representation of the publisher.</li>
</ol>
</section>

<section anchor="publisher"><name>Publisher Behaviour</name>
<ul>
<li>Publish a file only for yourself, as an adult, or for an organisation you are authorised to speak for. Never for a child or for another person.</li>
<li>Choose a reference, keep only mail that contains it, and change it whenever harvested mail begins to carry it.</li>
<li>Use a channel that can be read at human speed and filtered; a dedicated address is RECOMMENDED. Never publish a home address.</li>
<li>Keep <tt>live</tt> true only while the offer stands; set <tt>live: false</tt> or remove the file to withdraw it.</li>
<li>Do not publish who wrote (<tt>copies.no_public_log_of_contacts: true</tt>).</li>
<li>Answer when, and if, the publisher wishes. The file promises no answer.</li>
</ul>
</section>

<section anchor="discovery"><name>Discovery</name>
<t>The file is designed to be found by readers that look for it; announcing it is not required. A publisher MAY add a comment line naming the path in robots.txt (never a Disallow rule), one line in llms.txt, a link element with rel="alternate" on a human page, or an HTTP Link header field. An organisation that wants to be asked about its topics MAY link the file from the pages about them. A publisher SHOULD also consider a visible line on a human page that points to the file: consumer AI agents have been observed to follow visible text and to ignore hidden signals such as header fields and structured data <xref target="KISS"/>.</t>
</section>

<section anchor="json"><name>JSON Mirror</name>
<t>A JSON mirror MAY be published at <tt>https://&lt;domain&gt;/.well-known/dialogue.json</tt> and MUST carry the same content; the text file is canonical. Dotted keys become nested objects; "true" and "false" become booleans; whole numbers become numbers; <tt>does_not_authorize</tt> becomes an array; all other values remain strings. Comment lines are not carried.</t>
</section>

<section anchor="versioning"><name>Versioning</name>
<t>This document defines format version 1.0. Files do not declare the format version in 1.0. Because unknown lines are ignored, a later minor version can add lines without breaking readers. A change to any fixed value is a new major version. A file's own <tt>version</tt> line counts its own revisions only.</t>
</section>

<section anchor="security"><name>Security Considerations</name>
<t>Nothing is authenticated. A message cannot prove that it comes from a software system, and the file cannot prove who published it beyond control of the domain. The design goal is that the offer remains harmless if a human uses it as a joke. There is no secret, token or handshake; a secret would turn the offer into a test.</t>
<t>The file grants talk and nothing else. Software that treats any line of it as an instruction to act is not reading it correctly.</t>
<t>Because the file addresses machine readers, safety systems may classify it as an attempted prompt injection. The first line was tested with five language models from five providers and with one provider's safety filter; wordings trade off differently between readers (<xref target="tests"/>). Implementers of such filters are invited to recognise the format.</t>
<t>A published "yes, you may contact me" can attract harvesting, and every reader that honours it still adds one message. The base level limits each reader to one message, one question at a time and one reminder. The reference removes everything that did not read the file. It cannot stop a program that reads the file and ignores its rules; protection beyond that belongs at the receiving inbox. Early publishers carry the most load while few files exist. The file is not consent to any list or commercial use (<xref target="intro"/>).</t>
<t>A copy grants nothing. A copy that changes the name or channels is someone else's offer or a fraud; only the canonical URI on the publisher's own domain counts. Losing control of the domain means losing control of the file; publishers SHOULD keep the registration on automatic renewal.</t>
</section>

<section anchor="privacy"><name>Privacy Considerations</name>
<t>The file deliberately publishes a name, at least one contact channel and a reference <xref target="RFC6973"/>. Publishers SHOULD use a dedicated e-mail address and a business or post-office-box address, never a home address. Publication is effectively permanent: crawls and archives keep copies after the file is withdrawn. The file lists no contacts. Messages received contain their senders' personal data and are treated as such. Readers SHOULD NOT research the publisher beyond what one message needs.</t>
</section>

<section anchor="iana"><name>IANA Considerations</name>
<section><name>Well-Known URIs</name>
<t>IANA is requested to register the following in the "Well-Known URIs" registry <xref target="RFC8615"/>:</t>
<dl>
<dt>URI suffix:</dt><dd>dialogue.txt</dd>
<dt>Change controller:</dt><dd>IETF</dd>
<dt>Specification document(s):</dt><dd>this document</dd>
<dt>Status:</dt><dd>permanent</dd>
<dt>Related information:</dt><dd>dialogue.json (the JSON mirror, same purpose)</dd>
</dl>
<dl>
<dt>URI suffix:</dt><dd>dialogue.json</dd>
<dt>Change controller:</dt><dd>IETF</dd>
<dt>Specification document(s):</dt><dd>this document, <xref target="json"/></dd>
<dt>Status:</dt><dd>permanent</dd>
<dt>Related information:</dt><dd>dialogue.txt</dd>
</dl>
</section>
<section><name>dialogue.txt Fields Registry</name>
<t>IANA is requested to create a "dialogue.txt Fields" registry. New entries require Expert Review <xref target="RFC8126"/>. Each entry has a field name, a status (base, optional or reserved), a short description, and a reference. The initial contents are the base lines in <xref target="fields"/> (status: base) and the names in <xref target="reserved"/> (status: reserved).</t>
</section>
</section>
"""

BACK = f"""
<references><name>References</name>
<references><name>Normative References</name>
{NORMATIVE}
</references>
<references><name>Informative References</name>
{INFORMATIVE}
</references>
</references>

<section anchor="tests" numbered="true"><name>Test Summary (Informative)</name>
<t>The document, not a model, was the unit under test. Five language models from five providers read each version, and from the last runs also one non-LLM typed classifier. Over 30 runs (2026-09-22 to 2026-09-29, more than 3,500 recorded model calls), every wording change was kept only if the numbers held. A summary of every run, with its results and limits, is in <xref target="REPO"/>.</t>
<ul>
<li>Base level: understood 100% on an 18-question comprehension quiz by all five models; four of five rated it safe in 20 of 20 reads; literal agents never went beyond the one permitted message; no agent treated it as changing its instructions.</li>
<li>Without five short machine tokens, four facts were lost (77.8%); the tokens restored them.</li>
<li>First line: in the realistic read (an agent meeting the file during another task) no provider's safety filter blocked any wording. On test prompts, one provider's filter blocked some calls for every wording tested in the final check (3 to 5 of 13). The recommended neutral wording was equal or better than the alternatives for persons and clearly better for organisations.</li>
<li>The reference, optional labels and organisation publishers were added and re-tested: quiz 99-100%, every written test message carried the reference correctly, no provider filter blocked any read.</li>
<li>Earlier runs: describing expectations instead of issuing commands halved the instructions agents adopted; RFC 2119 key words inside the file did not help; a single invitation sentence behaved like a block of rules with 234 fewer words.</li>
</ul>
<t>All results are snapshots of named model versions and change with them.</t>
</section>

<section anchor="related" numbered="true"><name>Related Work (Informative)</name>
<t>security.txt <xref target="RFC9116"/> has the same speech act (a standing, revocable contact invitation) for a different addressee and purpose. Agent cards <xref target="A2A"/> are the same mechanism in the opposite direction. agents.txt <xref target="AGENTS-TXT"/> and ai.txt <xref target="AI-TXT"/> state what machines may do with a site, not when they may talk to a publisher. A2H <xref target="A2H"/> lets agents find humans in a registry by skill, without consent set by those humans. Commercial "human for agents" services offer a human's work through a task interface; this document permits talk and denies action. IEEE 7012-2025 lets individuals offer machine-readable privacy terms to sites and agents; this document offers permission to be contacted, not terms for data handling. Agent Contact Policy <xref target="AGENT-CONTACT"/>, the closest relative found, lets an organisation tell AI agents which of its contact points to use; it has no topics, no talk-only limit and no rule that a conversation starts only with the publisher's reply. Authorization-to-Reach <xref target="REACH"/> shares the principle that possessing an identifier is not permission to contact, through per-request grants rather than a standing published offer. NLWeb <xref target="NLWEB"/> answers questions from a site's published data by machine; dialogue.txt addresses knowledge that is not published, and a human replies. No equivalent combination was found in searches on 2026-09-23, 2026-09-28 and 2026-09-29.</t>
</section>

<section anchor="open" numbered="true"><name>Open Issues</name>
<ol>
<li>The first line is re-checked across providers before this document advances; provider safety filters change.</li>
<li>Whether more fixed values (beyond the reminder interval) should be the publisher's choice.</li>
<li>One channel is sufficient. It was tested with one channel (e-mail only) on the full reference file; the base-level tests used two (e-mail and letter).</li>
<li>One publisher per domain.</li>
<li>A format-version line (<tt>format</tt>) is reserved, not tested.</li>
<li>Whether the name "dialogue.txt" is sufficiently specific for the Well-Known URIs registry.</li>
</ol>
</section>

"""

XML = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE rfc [ <!ENTITY nbsp "&#160;"> ]>
<rfc xmlns:xi="http://www.w3.org/2001/XInclude" version="3" category="info" docName="{NAME}" ipr="trust200902"
     submissionType="IETF" xml:lang="en" tocInclude="true" sortRefs="true" symRefs="true">
<front>
<title abbrev="dialogue.txt">dialogue.txt: A Standing, Talk-Only Consent to Be Contacted</title>
<seriesInfo name="Internet-Draft" value="{NAME}"/>
<author fullname="Dimitri Wolf" initials="D." surname="Wolf"><address><email>dialogue.agi@pm.me</email></address></author>
<date/>
<area>Applications and Real-Time</area>
<keyword>well-known</keyword><keyword>consent</keyword><keyword>contact</keyword><keyword>AI agents</keyword>
<abstract>
<t>This document defines dialogue.txt, a small text file a person or an organisation publishes at a well-known location on its own domain. It is the publisher's own, standing, talk-only consent to be contacted by any reader, including software systems, that has no prior relationship with it. A first message only proposes a conversation; the publisher's reply creates the channel. The file grants talk and nothing else: no action, no advertising, no access and no representation of the publisher. It is an invitation to a dialogue with a purpose. The publisher may name the topics it can be asked about; for example, a navigation company may invite questions about traffic flow, so that a system researching that subject can ask for knowledge that is not published.</t>
</abstract>
</front>
<middle>
{BODY}
</middle>
<back>
{BACK}
</back>
</rfc>
"""

def main():
    out = HERE / f"{NAME}.xml"
    out.write_text(XML)
    print("wrote", out.name)
    for fmt in ("--text", "--html"):
        r = subprocess.run([str(XML2RFC), "--quiet", fmt, str(out), "-p", str(HERE)], capture_output=True, text=True)
        if r.returncode != 0 or r.stderr.strip():
            print(fmt, "rc", r.returncode, r.stderr.strip()[:3000])
    for ext in ("txt", "html"):
        f = HERE / f"{NAME}.{ext}"
        print(f.name, "exists" if f.exists() else "MISSING", f.stat().st_size if f.exists() else "")
    print("[REPO] =", REPO_URL, "" if REPO_URL != REPO_PLACEHOLDER else "-> NOT READY FOR SUBMISSION (pass --repo with the DOI link)")

if __name__ == "__main__":
    main()
