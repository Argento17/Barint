# Return: P403

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P403_legal_compliance_c3_review.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-06-25T06:15:47.134266+00:00 |
| Finished | 2026-06-25T06:22:49.017323+00:00 |
| Exit code | 0 |

---

## Output

```
**Corrected Map**

1. **Accessibility**
- Correct authorities: `חוק שוויון זכויות לאנשים עם מוגבלות, תשנ"ח-1998`, especially ss. `19יא`, `19יב`, `19מב`, `19נא`; `תקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), תשע"ג-2013`, regs. `35א`, `35ה`, `35ו`, `91`; `ת"י 5568`, generally WCAG 2.0 AA.
- Obligation: internet services must comply with Israeli Standard 5568 at `AA` level: reg. `35א(א)`.
- Important correction: for internet accessibility, reg. `35א(ד)(1)` creates a notice-and-cure structure: generally no “violation” before notice is sent and the issue is not fixed within a reasonable time, no later than `60 days`.
- Accessibility statement: reg. `35ה` requires a website accessibility statement including the accessibility adaptations made, accessibility coordinator details, and contact details for missing adaptations/accessibility requests.
- Accessibility coordinator: not universally required for every company/site. `s.19מב` and reg. `91` require a `רכז נגישות` for an employer with at least `25 employees`. If below that, naming a contact is still required in the web statement, but the statutory coordinator duty is not triggered.
- Damages correction: the correct no-proof-of-damage civil amount is `₪50,000` under `s.19נא(ב)`, not `₪300,000`. Administrative sanctions are separate and can be higher; under `s.26ז(ג)` they range by violator size/category, up to `₪218,820` for some listed violations.
- Size/exemption correction: “no size exemption applies to a company” is overstated. Reg. `35ו` contains limited web exemptions/reduced duties, including very small turnover/exempt dealer thresholds and existing site/app exemptions around `₪1,000,000` turnover, renewable every 3 years. Applicability depends on current facts.

2. **Privacy**
- Correct authorities: `חוק הגנת הפרטיות, תשמ"א-1981`, as amended by Amendment 13 in force `14 Aug 2025`; `תקנות הגנת הפרטיות (אבטחת מידע), תשע"ז-2017`; cross-border transfer regulations: `תקנות הגנת הפרטיות (העברת מידע אל מאגרי מידע שמחוץ לגבולות המדינה), תשס"א-2001`.
- Correction: the statute does not literally say “a Hebrew privacy policy is mandatory.” It requires statutory notice when requesting personal information for database processing: `s.11`. For a Hebrew Israeli consumer site, a Hebrew notice/privacy page is the defensible way to satisfy this.
- `s.11` notice must disclose: whether disclosure is legally required or voluntary and consequences of refusal; purpose; controller name/contact; recipients and purposes of transfer; rights of access and correction under ss. `13`, `14`.
- GA4: online identifiers/cookies/IP-related identifiers fall within the amended definition of `מידע אישי`, which includes indirect identification via an `מזהה מקוון` in `s.3`. GA4 also creates transfer/disclosure issues to Google and likely cross-border processing.
- Database registration: analytics-only does **not** automatically trigger registration. Under amended `s.8א`, registration is mainly required for a public body database or a database whose main purpose is collecting personal data for transfer to others as a business/for consideration, with data on more than `10,000` persons. A normal first-party analytics database for Bari should usually not be registrable on that ground.
- Notification to PPA: under `s.8א(ב)`, a sensitive-information database with data on more than `100,000` persons requires notice. GA4 traffic analytics should not normally be “special sensitivity” unless it profiles sensitive health/diet/supplement behavior in a way that crosses the statutory threshold.
- Privacy officer/DPO: not mandatory at small scale merely because GA4 runs. `s.17ב1` requires DPO for public bodies, data brokers/direct marketing databases over `10,000`, large-scale systematic monitoring as a core activity, or large-scale processing of specially sensitive information. Incidental GA4 on an editorial site is lower risk, but this becomes closer if Bari performs persistent health-interest profiling, ad targeting, or large-scale segmentation.
- New Amendment 13 penalties: registration/notification violations under `s.8א` can be `₪150,000`, doubled to `₪300,000` for databases with `1,000,000+` persons: `s.23כו(א)`. `s.11` notice failures can be calculated per person: `₪50/person`, or `₪100/person` for sensitive data, with statutory floors such as `₪30,000`: `s.23כו(ג)`. For indefinite groups, formulas include `₪2/person` or `₪4/person` for sensitive data, with `₪20,000/₪40,000` floors: `s.23כו(ד)`. Continuing violations add `1/100` per day; repeat violations can add an equal amount: `s.23ל`.

3. **Cookies / Consent**
- Israeli law differs from EU intuition: Israel has no general ePrivacy-style mandatory prior opt-in cookie banner for GA4.
- Hard-law posture is Privacy Law notice, purpose limitation, consent where required, cross-border disclosure, security, and rights handling. Consent under `s.3` may be express or implied, but it must be informed.
- Minimum defensible Israeli-only posture: prominent Hebrew privacy/cookie notice, identify GA4/Google, purposes, cookie/identifier use, cross-border transfer, retention if known, opt-out/browser controls, contact, access/correction rights, and avoid loading non-essential advertising/profiling tags without a stronger consent mechanism.
- If Bari later targets EU/UK users or uses ad personalization/remarketing, the answer changes materially.

4. **Supplements / Health Claims**
- Authorities: `הוראות בריאות הציבור (מזון) (איסור ייחוס סגולות מרפא למצרך מזון), תשל"ח-1978`; `חוק הגנת הצרכן, תשמ"א-1981` ss. `2`, `7`, `7א`; Ministry of Health food/supplement advertising and registration practice.
- Core line: nutritional fact, ingredient disclosure, comparative editorial assessment, and “high sodium / low fiber / contains caffeine / label says X mg” are generally different from therapeutic disease claims.
- High-risk/prohibited territory: claims that a food/supplement cures, prevents, treats, relieves, or is effective for a disease, medical condition, symptom, physiological disorder, or named therapeutic outcome, e.g. “prevents diabetes,” “treats anxiety,” “lowers cholesterol,” “anti-inflammatory treatment,” “immune cure.”
- Third-party rater issue: the 1978 rule is framed around attributing healing properties in advertising/publication context. I did not verify the exact section text in a primary accessible source, so the precise textual scope is **unverified** here. Risk analysis: even if the rule primarily targets advertisers/manufacturers, Bari can still create exposure through consumer-protection/misleading-publication theories, MoH pressure, and defamation/negligence if it editorially repeats therapeutic claims as true.
- Safer editorial posture: quote label claims only as “the label/manufacturer claims,” do not validate disease efficacy, avoid recommendations to use supplements for conditions, distinguish “nutritional composition” from “medical benefit,” and use “not medical advice” as support, not as a cure-all.

5. **Defamation / Product Disparagement**
- Authorities: `חוק איסור לשון הרע, תשכ"ה-1965`.
- A company/product manufacturer can sue because `s.1` includes harm to business and “אדם” includes a corporation.
- Truth/public interest: `s.14` is strong for verifiable facts if Bari can prove the scraped label data, methodology, and statements are true, and the public interest in food/supplement evaluation is clear.
- Fair opinion/good faith: `s.15`, especially `s.15(4)` and `s.15(6)`, can be strong for ratings if the score is clearly an opinion/judgment based on disclosed facts and methodology. It weakens sharply if factual predicates are wrong, methodology is hidden, language implies undisclosed facts, or the publication is excessive/malicious.
- No-proof damages: `s.7א` allows up to `₪50,000`, indexed, without proof of damage; double for intent to harm under `s.7א(ג)`.
- Notice-and-takedown: Israeli defamation law does not provide a clean statutory DMCA-style safe harbor. For Bari’s own ratings, Bari is the publisher, so takedown doctrine is secondary. If there is no UGC, comments, accounts, or forums, platform liability is not the main issue.
- Concrete risk reducers: store screenshots/source URL/date for every label scrape; separate facts from score/opinion; publish methodology; avoid “dangerous/fraud/scam/illegal” unless proven; include product dispute channel; log corrections; publish material corrections; keep historical evidence after retailer pages change.

**Launch Risk Ranking**

1. **Accessibility: high likelihood × medium/high severity**
- Common claimant/enforcement area; easy to test; Hebrew public-facing site. Biggest immediate legal hygiene item.

2. **Defamation/product disparagement: medium likelihood × high severity**
- Named commercial products, low scores, supplement brands. Severity is driven by injunction/correction demands, litigation cost, and business-harm allegations, not just damages.

3. **Privacy/GA4: medium likelihood × medium severity**
- PPA enforcement risk is lower than accessibility at small scale, but Amendment 13 raises sanctions. Fixable with proper notice, GA4 configuration, minimization, and no ad profiling by default.

4. **Supplement/health claims: medium likelihood × medium/high severity**
- Severity rises if Bari uses disease language or repeats manufacturer therapeutic claims as editorial conclusions.

5. **Cookies banner specifically: low/medium likelihood × low/medium severity**
- No Israeli EU-style opt-in rule for GA4 alone; risk is mainly inadequate privacy notice/consent and cross-border transparency.

**Missed Issues**

- Terms of use/editorial disclaimer: not a substitute for law, but important to define editorial nature, no medical advice, no purchase advice, correction process, methodology limits, and governing Hebrew text.
- IP/scraping/product images: retailer/manufacturer images and product copy can raise copyright, database, website terms, and passing-off/unfair competition issues. Product facts are safer than photos/marketing copy.
- Comparative advertising / hidden advertising: `חוק הגנת הצרכן` s. `7` treats misleading advertising and advertorial masking seriously. If Bari has sponsorships, affiliate links, paid placements, or brand relationships, disclosure becomes critical.
- Consumer-organization representation: `חוק הגנת הצרכן` s. `7ב` restricts entities funded/benefiting commercially from presenting themselves as solely consumer-protection bodies.
- Minors: if content is likely directed to minors, `s.7א` consumer-protection restrictions on marketing to minors become relevant, especially supplements.
- MoH supplement registration: avoid implying MoH approval/efficacy. Verify whether listed supplements are lawfully marketed only if the page discusses legality; otherwise do not create legal-status conclusions.
- Hebrew vs English: for Israeli consumers, Hebrew should be the governing user-facing privacy/accessibility/terms text. English can be secondary.
- Data retention/security: GA4 retention settings, access controls, processor terms, and deletion processes matter under the 2017 security regulations and Amendment 13 accountability structure.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.next.agent.switched: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba820001rp2R6jfZaYUcYw", "timestamp": "2026-06-25T06:15:51.584Z", "agent": "build"}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "user", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "time": {"created": 1782368151584}, "age
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "text", "text": "You are an independent expert reviewer (C3). The orchestrator is consulting you for a second opinion. The site owner i
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6ba9d5001FUgstaWjhjyzh7", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_efd6b
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bd56e001IHGN3djvE0RUnI", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "**Researching legal information**\
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " gather"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " research"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " task"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " best"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " route"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " utilize"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " resources"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " possibly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " government"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " websites"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " credible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " want"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " remember"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " boiler"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "plate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " focus"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " solely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " providing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " Using"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "fetch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " help"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " streamline"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " process"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " my"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " citations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " relevant"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " properly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " sourced"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " back"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " response"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " Let's"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " get"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": " started"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bd6ee001FMKEQ0OxHpBP1h", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6be36a001mwUBN8t4HVBvI5", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " authorities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " directly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " possible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " then"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " obligations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " guidance"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "/b"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "est"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "-pr"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "actice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " launch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "partID": "prt_efd6be36a001mwUBN8t4HVBvI5", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6be36a001mwUBN8t4HVBvI5", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bfaa7001ooJuB1ep0tQxOa", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_swghc5L492GAEn0VTQMiDbS7", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bfae2001URmlMkT1nRniE7", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_TICjin2hfuVPJOWVoTlfBGPF", "state": {"status": "running", "input": {"url": "https://www.gov
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bfaef001ASey4aLt2G60w2", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_xIaI8KTqoesZcNaxHeNYIxed", "state": {"status": "running", "input": {"url": "https://www.gov
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6bfafa001rlVdT5aGfAKOpq", "messageID": "msg_efd6ba9d5001FUgstaWjhjyzh7", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_P7hkuVQXNyZIE8duyM8O5UgB", "state": {"status": "running", "input": {"url": "https://www.gov
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_TICjin2hfuVPJOWVoTlfBGPF", "state": {"status": "error", "input": {"url": "https://www.gov.i
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_P7hkuVQXNyZIE8duyM8O5UgB", "state": {"status": "error", "input": {"url": "https://www.gov.i
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_xIaI8KTqoesZcNaxHeNYIxed", "state": {"status": "error", "input": {"url": "https://www.gov.i
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_swghc5L492GAEn0VTQMiDbS7", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c07a7001CwzA3TP055kHDV", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6b
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6ba9d5001FUgstaWjhjyzh7", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6ba9d5001FUgstaWjhjyzh7", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c173e001aCqPbKsG8pBDVp", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c195f0014MYD0EU66C08CL", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "**Gathering legal information**\n\
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " fetch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " laws"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " regulations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " Ne"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "vo"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " fine"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " thinking"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " accurate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "-to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "-date"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " There"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " lot"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " consider"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " when"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " comes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " details"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " making"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " sure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " get"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " essential"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " want"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " necessary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " context"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " clarity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " let"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": " find"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c195f0014MYD0EU66C08CL", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c195f0014MYD0EU66C08CL", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c25f8001pBzfpgGtwdKwK3", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "Some"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " gov"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": ".il"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " pages"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " block"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " automated"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " fetch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "es"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "-check"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "ing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " against"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " accessible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " regulator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " publications"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " available"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " relying"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " secondary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": " summaries"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "partID": "prt_efd6c25f8001pBzfpgGtwdKwK3", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c25f8001pBzfpgGtwdKwK3", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c3d90001LMpw2yP6zWwc5e", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_qVucMCZ9kwAS5lMQbXcEhuJp", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c3e12001F71tw7qZ4Su2Ld", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_xcWJi3vOzaXNFl5fJXOZYVUL", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c423a001zyrKtUThw2Ok90", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_6Zc4gtcMH0HSUmi2wiFMI7y2", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c4253001HH1pPkgAeNfKET", "messageID": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_35G54O65HacixCjhsPmZacTI", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_qVucMCZ9kwAS5lMQbXcEhuJp", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_xcWJi3vOzaXNFl5fJXOZYVUL", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_6Zc4gtcMH0HSUmi2wiFMI7y2", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_35G54O65HacixCjhsPmZacTI", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c5963001zny4X4gqz7X0Ui", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6c
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c0d13001Z9ecM8pWmBw3GK", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c5ed7001G86EhqPnhFjfbU", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c6adf0017s0zyEU0ziwqgf", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c6dac001eMIjjwdQrXmboB", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c6dac001eMIjjwdQrXmboB", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c8b32001kkyDeyPL2Gy2OB", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_3LXc7gCBX1bKrfR9PA1yh1wr", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c8b540018WSZ2VYC1J5yzy", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_fS9C3MqKSk7xADkXBFhC4T1r", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c8b6e001QjvPLzSfgGkAVG", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_p812GH6H9FEcx0b69c89Ipir", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c8b830017ahaQ0402ygs2S", "messageID": "msg_efd6c5ed7001G86EhqPnhFjfbU", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_zdKZuBGeDZPgEjIy8u0bLNAV", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_3LXc7gCBX1bKrfR9PA1yh1wr", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_p812GH6H9FEcx0b69c89Ipir", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_zdKZuBGeDZPgEjIy8u0bLNAV", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_fS9C3MqKSk7xADkXBFhC4T1r", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6c96020019zFn5bymvgl3gF", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6c
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c5ed7001G86EhqPnhFjfbU", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c5ed7001G86EhqPnhFjfbU", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6ca7fe001IBt001dyQp61Ac", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cafb4001Xc35G83536Jb4r", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cafb4001Xc35G83536Jb4r", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " error"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " pass"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " already"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " cookie"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " position"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " e"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " opt"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "-in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " hard"}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "-law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " hook"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " Law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "cons"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "ent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " purpose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " limitation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " regulator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " guidance"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " online"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": " tracking"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "partID": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cb2ef001GBHLmxpXGpEG7r", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cd26a0010vqsh84glOd1qr", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_sjIcTaZ5R2d5kCL67CWOR43R", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cd2f4001LI7MQ9UFclMARz", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_mUJ81N4f05CUGXOsjyQrWnMS", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cd33a001Ob1jmEaMpFNgPS", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_sjIcTaZ5R2d5kCL67CWOR43R", "state": {"status": "error", "input": {"url": "https://www.nevo.
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_RPXmXhwkQId4UrNA2UeNUa0A", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cd3b1001vMuhDlIQLWYZsw", "messageID": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_6RUJ5K8i7NeX0cEreJJDNAtb", "state": {"status": "running", "input": {"url": "https://www.nev
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_RPXmXhwkQId4UrNA2UeNUa0A", "state": {"status": "error", "input": {"url": "https://www.nevo.
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_6RUJ5K8i7NeX0cEreJJDNAtb", "state": {"status": "error", "input": {"url": "https://www.nevo.
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "webfetch", "callID": "call_mUJ81N4f05CUGXOsjyQrWnMS", "state": {"status": "completed", "input": {"url": "https://www.n
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cd9ba001n3TBymMibhhGay", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6c
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6c9bc7001lZ5AiX5FHwiR75", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6ceaa5001gR0RhgCWRbMCLO", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cee10001RmL4XkHadDhDKo", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6cee10001RmL4XkHadDhDKo", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6d0be1001QYn60oa7sUNR21", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " seeing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "197"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " regulation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " through"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " fetch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " tool"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " mark"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " precise"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " verified"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " substant"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "iate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " mark"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " specific"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "number"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " cannot"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " filling"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": " gaps"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "partID": "prt_efd6d0be1001QYn60oa7sUNR21", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6d0be1001QYn60oa7sUNR21", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd6d0e46001pHzIrBX0YAYECp", "messageID": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  session.created: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "version": "1.17.4", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "d
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "task", "callID": "call_kTGKKgSvpVVuz5s5cyQhqoHV", "state": {"title": "Extract legal sections", "metadata": {"parentSes
  session.next.model.switched: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33df001lO0FtCpLtwkQlI", "timestamp": "2026-06-25T06:17:32.895Z", "model": {"id": "gpt-5.5", "providerID": "openai", "variant": "d
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "user", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "time": {"created": 1782368252895}, "age
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "text", "text": "From the fetched Nevo tool-output files in C:\\Users\\HP\\.local\\share\\opencode\\tool-output if accessible, extract 
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "task", "callID": "call_kTGKKgSvpVVuz5s5cyQhqoHV", "state": {"title": "Extract legal sections", "metadata": {"parentSes
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d33f4001l8V6RFgvF5iK0e", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_efd
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d5abc001zIDBlgzFF9Q22u", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d5c2d001mElfWRLL2J3uxF", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "**Searching for accessible files**
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " search"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " files"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "\u2019re"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " accessible"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " So"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " tools"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " glob"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " read"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " grep"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " locate"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " them"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " end"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " absolute"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " paths"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " final"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " results"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " suspect"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " will"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " adds"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " another"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " layer"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " consider"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " focus"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " finding"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " output"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " files"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " related"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " task"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " Al"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "right"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " let's"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " get"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": " started"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "partID": "prt_efd6d5c2d001mElfWRLL2J3uxF", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d5c2d001mElfWRLL2J3uxF", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d6950001nPL9xNBQLmf49s", "messageID": "msg_efd6d33f4001l8V6RFgvF5iK0e", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "glob", "callID": "call_V0pzIaOxgn9xUC8C49RyPyyL", "state": {"status": "running", "input": {"pattern": "**/*", "path": 
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "glob", "callID": "call_V0pzIaOxgn9xUC8C49RyPyyL", "state": {"status": "completed", "input": {"pattern": "**/*", "path"
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d6fc9001By1ugoYdJ9oxD0", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6d
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d33f4001l8V6RFgvF5iK0e", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d33f4001l8V6RFgvF5iK0e", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d7573001Bg40pvodMNZ6Kd", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d7df1001Vaot6oV6RLvGfF", "messageID": "msg_efd6d7573001Bg40pvodMNZ6Kd", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d7f59001ojDff0pfl5ZYiB", "messageID": "msg_efd6d7573001Bg40pvodMNZ6Kd", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d7f59001ojDff0pfl5ZYiB", "messageID": "msg_efd6d7573001Bg40pvodMNZ6Kd", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d97ea001U2eZdcc1Rh6AvB", "messageID": "msg_efd6d7573001Bg40pvodMNZ6Kd", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_jisrVvRV51wGJKtuurakTfIW", "state": {"status": "running", "input": {"pattern": "19\u05e0\u05d0|
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6d97fb001Hgu5aBgfAgAiJR", "messageID": "msg_efd6d7573001Bg40pvodMNZ6Kd", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_I3TcuRFb0lgqwvEoRp77GU5c", "state": {"status": "running", "input": {"pattern": "\u05e0\u05d1\u0
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_I3TcuRFb0lgqwvEoRp77GU5c", "state": {"status": "completed", "input": {"pattern": "\u05e0\u05d1\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_jisrVvRV51wGJKtuurakTfIW", "state": {"status": "completed", "input": {"pattern": "19\u05e0\u05d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6da12a001S1UH41WmslTgis", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6d
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d7573001Bg40pvodMNZ6Kd", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6d7573001Bg40pvodMNZ6Kd", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6da6c0001MDwzpIqDLcAIhv", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6db1b4001ncofouWEBt5L1J", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6db366001i6uWQQHUVHpH1g", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6db366001i6uWQQHUVHpH1g", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ddfed0012qnEAWgtbgFxk4", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_zkrkMAjYIf7IN1AdQapjvT2I", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6de001001zdymtp75agfXAY", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_8jLusfs4nZPy6FIK4cy5NIn7", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6de032001catCXv04V1rpmV", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_uYcN7Jd8Ohu9GZHKNaNF4n8C", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6de04e001A5vFZOxitPIXlj", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_pkYmatgtezqEK9lTLPFM7eGJ", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6de06d001evb3XTXWhlWKXI", "messageID": "msg_efd6da6c0001MDwzpIqDLcAIhv", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_qiI3Un5dvonFfv66miNXPY27", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_pkYmatgtezqEK9lTLPFM7eGJ", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_qiI3Un5dvonFfv66miNXPY27", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_zkrkMAjYIf7IN1AdQapjvT2I", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_8jLusfs4nZPy6FIK4cy5NIn7", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_uYcN7Jd8Ohu9GZHKNaNF4n8C", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6df2b8001d2c8TBNb3BNsur", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6d
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6da6c0001MDwzpIqDLcAIhv", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6da6c0001MDwzpIqDLcAIhv", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6df8a4001oTlalz76fnZAj8", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e01910015vY6VUoH2HJZ1t", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e03cd001O8zt2KuWCk5aX9", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e03cd001O8zt2KuWCk5aX9", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e26c7001c46mG2eF9f4Cjd", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_j2J5chE8WUQ6ct2ZFC8N8oQn", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e26df001c9F1vyeOmyyL58", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_aiLpKr70W5cB6VYZ1gAplEkH", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e26f40019wAm3z22Gp4HGC", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_tOzeeW4akNEGod8jJAonNxIe", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e26fc001Hy4FNcJO0nQoPq", "messageID": "msg_efd6df8a4001oTlalz76fnZAj8", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_YUnQGXk2CdxgJIh98D40wjLM", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_j2J5chE8WUQ6ct2ZFC8N8oQn", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_aiLpKr70W5cB6VYZ1gAplEkH", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_tOzeeW4akNEGod8jJAonNxIe", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_YUnQGXk2CdxgJIh98D40wjLM", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e2ce2001mLnttPJus5JVXS", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6d
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6df8a4001oTlalz76fnZAj8", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6df8a4001oTlalz76fnZAj8", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e3237001pAUdIXBjGByAer", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e3c47001huB8KGpqyAJiB7", "messageID": "msg_efd6e3237001pAUdIXBjGByAer", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e41bb001Dg70wC3n83NzZO", "messageID": "msg_efd6e3237001pAUdIXBjGByAer", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e41bb001Dg70wC3n83NzZO", "messageID": "msg_efd6e3237001pAUdIXBjGByAer", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e494a001dA5NzaCSVwTvZq", "messageID": "msg_efd6e3237001pAUdIXBjGByAer", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_CwbN37zmCjZ9OJfADheKNKgs", "state": {"status": "running", "input": {"pattern": "^11\\\\.|11\\. 
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_CwbN37zmCjZ9OJfADheKNKgs", "state": {"status": "completed", "input": {"pattern": "^11\\\\.|11\\
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "add"}
  file.watcher.updated: {"file": "C:\\Bari\\.git\\index.lock", "event": "unlink"}
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e57ee001cTyDDcXDhrt3wU", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6e
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e3237001pAUdIXBjGByAer", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e3237001pAUdIXBjGByAer", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e5d75001akJb6tn0G9AIkl", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e666c001lH5U60KM3UN5ai", "messageID": "msg_efd6e5d75001akJb6tn0G9AIkl", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e6864001qKLZJoEYbyTsO5", "messageID": "msg_efd6e5d75001akJb6tn0G9AIkl", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e6864001qKLZJoEYbyTsO5", "messageID": "msg_efd6e5d75001akJb6tn0G9AIkl", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e6c73001k2fyc6h4lyna8m", "messageID": "msg_efd6e5d75001akJb6tn0G9AIkl", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_vrdSauHNXOW1hUbJdG4b8szF", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_vrdSauHNXOW1hUbJdG4b8szF", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e7826001Iudy5yfgYIi9Xu", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6e
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e5d75001akJb6tn0G9AIkl", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e5d75001akJb6tn0G9AIkl", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e7da20010cPc5BJq4dhhUs", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e86a5001aiEXIBKhc86nip", "messageID": "msg_efd6e7da20010cPc5BJq4dhhUs", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e8868001uPXwyMQCEGzZ3C", "messageID": "msg_efd6e7da20010cPc5BJq4dhhUs", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e8868001uPXwyMQCEGzZ3C", "messageID": "msg_efd6e7da20010cPc5BJq4dhhUs", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e8f0b001ZucLE6Eacs6OdC", "messageID": "msg_efd6e7da20010cPc5BJq4dhhUs", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_OuhqZoZ41ZWqArQAHDPilMFd", "state": {"status": "running", "input": {"pattern": "\u05ea\u05d5\u0
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "grep", "callID": "call_OuhqZoZ41ZWqArQAHDPilMFd", "state": {"status": "completed", "input": {"pattern": "\u05ea\u05d5\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6e9fca001nFFFCEjGNQbvhJ", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6e
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e7da20010cPc5BJq4dhhUs", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6e7da20010cPc5BJq4dhhUs", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ea52100186TLz79voaTBmO", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6eb2800010Smnn0jtMHClrt", "messageID": "msg_efd6ea52100186TLz79voaTBmO", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ec790001dDW5ai7nV3xBts", "messageID": "msg_efd6ea52100186TLz79voaTBmO", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_S4gNgfyvJu1qhbUhFU7abQ3W", "state": {"status": "running", "input": {"filePath": "C:\\Users\\HP\
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"type": "tool", "tool": "read", "callID": "call_S4gNgfyvJu1qhbUhFU7abQ3W", "state": {"status": "completed", "input": {"filePath": "C:\\Users\\H
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ed2830015ScVheuWckdAbi", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6e
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ea52100186TLz79voaTBmO", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ea52100186TLz79voaTBmO", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ed7df001KBbx8SPOt2BY5B", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ee115001ZT1zGK1sm07iqZ", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "snapshot
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ee44d0019Urg7eBL8px7Vy", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6ee44d0019Urg7eBL8px7Vy", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6f4b65001LZcBJJNNjquTHd", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Read"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " extraction"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "C"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Users"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "HP"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "local"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "share"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "encode"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-output"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "efd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "422"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "f"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "UM"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "BC"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "W"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "j"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Z"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "na"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "x"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "`\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "C"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Users"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "HP"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "local"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "share"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "encode"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-output"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "efd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "436"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "e"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "001"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "x"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Un"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Q"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "H"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Ab"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "37"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "r"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "PD"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "ZW"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "`\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "C"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Users"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "HP"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "local"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "share"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "encode"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-output"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\\"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "tool"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "_"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "efd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "45"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "162"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "w"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "az"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "BN"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "pe"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "yt"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "TO"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "`\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Equal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Rights"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Disabilities"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Law"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d4\u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e2\u05d5\u05d1\u05d3\u05d9\u0
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05dc\u05e4\u05d7\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9\u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " ..."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d;"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " duties"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05d9\u05d3\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05dc\u05e6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05d1\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "...\u201d"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05e5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d5\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d3\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "..."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " civil"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " tort"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " court"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " award"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05d9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d1\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2\u05dc\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d3\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05db"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d7\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "26"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " representation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " penalty"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "27"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "360"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "26"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " administrative"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " penalties"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "310"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e7\u05d8\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "830"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e8\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "680"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "620"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e7\u05d8\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "660"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e8\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "27"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "360"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "940"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e7\u05d8\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "220"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e8\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "41"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "030"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05dc\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "940"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e7\u05d8\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "220"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e8\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "218"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "820"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "26"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e2\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05d9\u05dc\u05d9\u05d5\u0
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d7\u05d9\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e7\u05d8\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05e2\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05d9\u05dc\u05d9\u05d5\u0
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d5\u05e2\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05d9\u05dc\u05d9\u05d5\u0
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Service"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Regulations"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " internet"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " standard"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " level"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "AA"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sent"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " fixed"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05da"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d6\u05de\u05df"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1\u05d9\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d0\u05da"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05d7\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9\u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " statement"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " adaptations"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " details"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " contact"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " missing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " adaptations"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/request"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " technological"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " exemption"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " valid"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " years"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " renewable"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " once"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " years"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " registered"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " internet"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " service"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " exemption"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "500"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de\u05e9\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e4\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d1\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d9\u05ea"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05dc\u05db\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05d5\u05ea\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " personal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " documents"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "31"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " request"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d5\u05d7\u05e8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05de"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d9\u05de\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u201d.\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " exempt"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " dealer"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " exempt"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " temporary"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " until"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "26"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " existing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/app"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " exemption"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " renewable"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " years"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " employer"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " employees"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " least"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " appoint"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e0\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " updates"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "once"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " year"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Privacy"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Protection"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Law"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Amendment"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " broker"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/direct"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " etc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " personal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-info"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " within"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "30"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " days"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " state"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " duty"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "cons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "ent"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " consequence"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " refusal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " purpose"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " controller"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " name"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/contact"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " recipients"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/p"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "ur"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "poses"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " rights"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sections"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " listed"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " bodies"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " controller"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "processor"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " broker"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/direct"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-scale"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " systematic"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " monitoring"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-scale"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " special"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-sensitive"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " processing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "(d"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " failure"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " appoint"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d0\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " subject"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " order"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " stop"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/c"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "orrect"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "notification"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violations"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "150"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "+"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " failure"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " request"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " info"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " minimum"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/dis"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "cretion"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "ary"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " floor"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "30"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " failure"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " indefinite"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " group"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " info"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " floor"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "40"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " failure"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " appoint"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05d0\u05d5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " person"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " formula"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " floor"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "40"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " continuing"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " adds"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " day"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " repeated"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " adds"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " amount"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " equal"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sanction"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d9\u05e3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " +"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Fifth"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Schedule"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " reductions"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Fifth"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Schedule"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " cumulative"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " reductions"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "70"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " appointment"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "),("}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ")**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " reduction"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " micro"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "mall"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " business"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "40"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**,"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "70"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "140"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " depending"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " violation"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " class"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " -"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " reduce"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "Un"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "verified"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " actual"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " post"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " updated"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " Privacy"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " sanction"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " amounts"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " beyond"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " update"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " mechanism"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "\u05dc\u05d1"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " were"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " these"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": " files"}
  message.part.delta: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "partID": "prt_efd6f4b65001LZcBJJNNjquTHd", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd6f4b65001LZcBJJNNjquTHd", "messageID": "msg_efd6ed7df001KBbx8SPOt2BY5B", "sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "type": "
  message.part.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "part": {"id": "prt_efd7011c6001HBZg0P1kmK1cTh", "reason": "stop", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6ed7df00
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ed7df001KBbx8SPOt2BY5B", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "msg_efd6ed7df001KBbx8SPOt2BY5B", "parentID": "msg_efd6d33dd001AflmqEnCMQIZzb", "role": "assistant", "mode": "explore", "agent": "explore
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB"}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"type": "tool", "tool": "task", "callID": "call_kTGKKgSvpVVuz5s5cyQhqoHV", "state": {"status": "completed", "input": {"description": "Extract l
  session.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"id": "ses_10292cc37ffeo16DR9ZCe7paQB", "slug": "silent-wolf", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari"
  session.diff: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "diff": []}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd701ccd001YsdPK7i1Lie5rf", "reason": "tool-calls", "snapshot": "e01287c99ceeb4b0eec24e676becacb195454b23", "messageID": "msg_efd6c
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd6cdf1d001X3bhSY4sHqJWL2", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd702231001V4X2NiGdf5HUEv", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_10292cc37ffeo16DR9ZCe7paQB", "info": {"role": "user", "time": {"created": 1782368252895}, "agent": "explore", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"d
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd702d3d001xM3h0Ot5OeCvrn", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "snapshot
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd703a76001xSxyeuhwwFNt7j", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd703a76001xSxyeuhwwFNt7j", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd7082220013b6BlZajzu4mXO", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Correct"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Map"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Correct"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " authorities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05d5\u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d6\u05db"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "199"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ss"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05d5\u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d6\u05db"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05e9\u05d9\u05dd"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e2\u05dd"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d5\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1\u05dc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05e8\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "),"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " regs"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "556"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " generally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " WC"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "AG"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " AA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Obl"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "igation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " internet"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " services"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " comply"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Standard"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "556"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "AA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " level"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Important"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " internet"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " creates"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " structure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " generally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "vi"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "olation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " fixed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " within"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " time"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " later"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "60"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " days"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requires"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " website"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " adaptations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " made"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " details"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " contact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " details"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " missing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " adaptations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/access"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requests"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " universally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " company"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/site"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "91"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " require"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e8\u05db\u05d6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2\u05d9\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " employer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " least"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "25"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " employees"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " naming"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " contact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " coordinator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " duty"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " triggered"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Dam"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ages"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correct"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-proof"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "amage"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " civil"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " amount"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "19"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Administrative"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sanctions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "26"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " range"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " viol"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ator"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " size"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/category"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "218"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "820"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " listed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " violations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Size"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/ex"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "emption"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " size"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " exemption"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " applies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " company"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " overst"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ated"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Reg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "35"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " contains"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " limited"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " exemptions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/re"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "duced"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " duties"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/ex"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "empt"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " dealer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " existing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/app"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " exemptions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " turnover"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " renewable"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " years"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Applic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " depends"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " current"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Correct"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " authorities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "198"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " amended"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Amendment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " force"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Aug"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1\u05d8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d9\u05d3\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "),"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-border"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transfer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " regulations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05ea\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e4\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1\u05e8\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d9\u05d3\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d0\u05dc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d9\u05d3\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e9\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05dc\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05de\u05d3\u05d9\u05e0\u0
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "),"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statute"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " literally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " policy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mandatory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requires"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " when"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requesting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " personal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " processing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " way"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " satisfy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclosure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " legally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " voluntary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consequences"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " refusal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purpose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " controller"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " name"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/contact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " recipients"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purposes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transfer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rights"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " access"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ss"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " online"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " identifiers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ookies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/IP"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-related"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " identifiers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " fall"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " within"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " amended"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " definition"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de\u05d9\u05d3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d0\u05d9\u05e9\u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " which"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " includes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " indirect"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " identification"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " via"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d6\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " creates"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transfer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/dis"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "closure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " issues"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Google"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-border"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " processing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " analytics"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " automatically"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " trigger"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " amended"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mainly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " whose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purpose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " collecting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " personal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transfer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " others"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " business"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consideration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-party"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " analytics"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " usually"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registr"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "able"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ground"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Notification"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " P"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "PA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requires"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " traffic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " analytics"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " normally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "special"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitivity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " profiles"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "iet"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " behavior"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " way"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " crosses"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " officer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/D"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mandatory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scale"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " merely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " runs"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "17"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " requires"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " D"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "PO"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " bodies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " brokers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/direct"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " databases"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "10"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-scale"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " systematic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " monitoring"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " core"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " activity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-scale"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " processing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " specially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Inc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "idental"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " becomes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " closer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " performs"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " persistent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-interest"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " profiling"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ad"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " targeting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-scale"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " segmentation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " New"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Amendment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " penalties"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "notification"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " violations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "150"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " doubled"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " databases"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "+"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " persons"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "11"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " failures"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " calculated"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " person"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/person"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/person"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " floors"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " such"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "30"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " indefinite"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " groups"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " formulas"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/person"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/person"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sensitive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "40"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " floors"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05d5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Continuing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " violations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " add"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " day"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " repeat"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " violations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " add"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " equal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " amount"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "23"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05dc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Cookies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Consent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " differs"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " intuition"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israel"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " e"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mandatory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " prior"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " opt"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cookie"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " banner"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hard"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " posture"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purpose"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " limitation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " required"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-border"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclosure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " security"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rights"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " handling"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Consent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " express"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " implied"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " informed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Minimum"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " posture"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " prominent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ookie"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " identify"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Google"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purposes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cookie"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "identifier"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-border"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transfer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " retention"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " known"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " opt"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-out"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/browser"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " controls"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " contact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " access"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "orrection"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rights"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " loading"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " non"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-essential"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "fil"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " tags"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mechanism"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " later"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " targets"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "UK"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " users"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " uses"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ad"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " personalization"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "remark"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "eting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " answer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " changes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " materially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Supp"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "lements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Authorities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d1\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d0\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e6\u05d9\u05d1\u05d5\u0
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d9\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05e1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05dc\u05d5\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e6\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05da"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05de\u05d6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "),"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e9\u05dc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "197"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05de"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "198"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ss"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`;"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Ministry"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " food"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " practice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Core"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " nutritional"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " fact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ingredient"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclosure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "high"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sodium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " fiber"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " contains"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " caffeine"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " X"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " generally"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " different"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " therapeutic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disease"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " High"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "hibited"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " territory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " food"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cures"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " prevents"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " treats"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rel"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ieves"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " effective"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disease"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " condition"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " symptom"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " physiological"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disorder"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " named"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " therapeutic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " outcome"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " e"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".g"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "pre"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "vents"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " diabetes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "t"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "reat"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " anxiety"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "low"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cholesterol"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "anti"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-inflammatory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " treatment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "immune"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\u201d\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Third"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-party"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " r"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ater"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "197"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " framed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " attribut"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " healing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " properties"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " context"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " did"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " section"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " primary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessible"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " source"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " precise"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " textual"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scope"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "un"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "verified"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " here"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " analysis"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " primarily"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " targets"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertisers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/man"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ufact"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "urers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " create"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " exposure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " through"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "tection"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "leading"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " theories"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Mo"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "H"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " pressure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " def"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "amation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/ne"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "glig"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ence"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " repeats"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " therapeutic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Sa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "fer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " posture"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " quote"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/man"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ufacturer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " validate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disease"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " efficacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " recommendations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " conditions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " distinguish"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "nut"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "r"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "itional"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " composition"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "medical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ",\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-all"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Def"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "amation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Dis"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "par"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "agement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Authorities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d0\u05d9\u05e1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05dc\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05ea\u05e9"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\"\u05d4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "196"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " company"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " manufacturer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sue"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " includes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " harm"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " business"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d3\u05dd"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " includes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " corporation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Truth"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " interest"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "14"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ver"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ifiable"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " prove"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scraped"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " true"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " interest"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " food"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " evaluation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " clear"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Fair"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " opinion"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/g"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " faith"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "15"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ratings"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " clearly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " opinion"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/j"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ud"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " based"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclosed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ens"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sharply"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " factual"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " predicates"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " wrong"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " hidden"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " implies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " undis"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "closed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " publication"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " excessive"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "icious"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-proof"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " damages"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " allows"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u20aa"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "000"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`,"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " indexed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " proof"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " damage"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " intent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " harm"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "("}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ")"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`.\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-t"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "aked"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "own"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " def"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "amation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " statutory"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " DM"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "CA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " safe"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " harbor"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " own"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ratings"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " publisher"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " tak"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "own"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " doctrine"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " secondary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " there"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " U"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "GC"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " comments"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accounts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " forums"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " platform"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " liability"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " issue"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Concrete"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " reducers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " store"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " screenshots"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/source"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " URL"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/date"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scrape"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/op"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "inion"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " publish"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "danger"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ous"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "raud"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/sc"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "am"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "illegal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " include"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " dispute"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " channel"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " log"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " corrections"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " publish"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " material"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " corrections"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " keep"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " historical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " after"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " retailer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " pages"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Launch"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Ranking"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likelihood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/high"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Common"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claimant"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/en"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "forcement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " area"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " easy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " test"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " public"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-facing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " site"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Biggest"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " immediate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " hygiene"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " item"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Def"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "amation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " dispar"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "agement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likelihood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Named"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " commercial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scores"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " brands"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " driven"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " injunction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/c"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "orrection"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " demands"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " litigation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cost"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " business"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-h"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "arm"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " allegations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " just"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " damages"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likelihood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " P"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "PA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " enforcement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accessibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " scale"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Amendment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " raises"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sanctions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Fix"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "able"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " proper"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " configuration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " minim"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ization"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " ad"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " profiling"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " default"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Supplement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "health"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likelihood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/high"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rises"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " uses"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disease"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " repeats"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " manufacturer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " therapeutic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " conclusions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " **"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Cookies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " banner"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " specifically"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likelihood"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u00d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "medium"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " severity"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " opt"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-in"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " alone"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " mainly"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " inadequate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " notice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "cons"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ent"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-border"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " transparency"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "Miss"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Issues"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "**\n\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Terms"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/editor"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclaimer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " substitute"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " define"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " editorial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " nature"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " medical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " purchase"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advice"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " correction"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " process"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " limits"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " governing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " IP"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "cr"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "aping"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " images"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " retailer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/man"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ufacturer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " images"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " raise"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " copyright"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " database"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " website"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " terms"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " passing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-off"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/un"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "fair"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " competition"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " issues"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Product"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " facts"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " safer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " photos"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "marketing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " copy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Comparative"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " /"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " hidden"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " treats"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " misleading"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advertising"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " advert"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "orial"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " masking"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " seriously"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Bari"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " sponsorship"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " affiliate"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " links"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " paid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " placements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " brand"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " relationships"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " disclosure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " becomes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " critical"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Consumer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "organization"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " representation"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d5\u05e7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05d2"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e0\u05ea"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " \u05d4\u05e6"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05e8"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05db\u05df"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d1"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " restrict"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " entities"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " funded"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "benef"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "iting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " commercially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " presenting"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " themselves"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " solely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "tection"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " bodies"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Min"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ors"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " directed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " minors"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "\u05d0"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "tection"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " restrictions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " minors"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " become"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " relevant"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Mo"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "H"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " registration"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " implying"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Mo"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "H"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " approval"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "eff"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ic"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "acy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Verify"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " listed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " law"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "fully"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " marketed"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " discusses"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " legality"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " otherwise"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " create"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-status"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " conclusions"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " vs"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " English"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Israeli"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Hebrew"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " governing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " user"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-facing"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " privacy"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/access"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "terms"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " English"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " secondary"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Data"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " retention"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "/security"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " GA"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " retention"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " settings"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " access"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " controls"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " processor"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " terms"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " deletion"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " processes"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " matter"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " security"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " regulations"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " Amendment"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " accountability"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": " structure"}
  message.part.delta: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "partID": "prt_efd7082220013b6BlZajzu4mXO", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd7082220013b6BlZajzu4mXO", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd71eaff001aMgCO6ci7xfDWG", "reason": "stop", "snapshot": "b0762567a3dfa49a22b1e9921442a30b47be9354", "messageID": "msg_efd70223100
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd702231001V4X2NiGdf5HUEv", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "part": {"id": "prt_efd71f09b001Gupd1UmivlT53x", "messageID": "msg_efd702231001V4X2NiGdf5HUEv", "sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "type": "
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "msg_efd702231001V4X2NiGdf5HUEv", "parentID": "msg_efd6ba8200015W5pgCX1V1Jw3e", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV"}
  session.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"id": "ses_102945d14ffeEKkQNzNybpVMUV", "slug": "misty-engine", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "diff": []}
  message.updated: {"sessionID": "ses_102945d14ffeEKkQNzNybpVMUV", "info": {"role": "user", "time": {"created": 1782368151584}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 01_framework/editorial/editorial_intelligence_v3.md
 M 02_products/supplements/real_corpus_v3/_addressable_shelf.json
 M 02_products/supplements/real_corpus_v3/cache/7290015318426.json
 M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/bsip2/proto_v0/src/signal_extractor.py
 M 03_operations/page_generator/conform_baseline.py
 M 03_operations/page_generator/gates/run_gates.py
 M 03_operations/page_generator/generate_page.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/reports/regression/router_regression_001.md
 M 03_operations/spine/live_manifest.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M 03_operations/validators/verify_citations.py
 M bari-web/next.config.ts
 M bari-web/src/app/globals.css
 M bari-web/src/app/sitemap.ts
 M bari-web/src/components/comparisons/cereals-comparison-page.tsx
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/cookies-coffee-comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/home/home-analysis-engine.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/components/shared/expansion-section.tsx
 M bari-web/src/data/bread-retail-curated.json
 M bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
 M bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/cheese_frontend_v4.json
 M bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json
 M bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json
 M bari-web/src/data/comparisons/hummus_frontend_v5.json
 M bari-web/src/data/comparisons/juices_frontend_v3.json
 M bari-web/src/data/comparisons/milk_frontend_v1.json
 M bari-web/src/lib/comparisons/cakes-hard-cookies-page-data.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/cookies-coffee-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
 M bari-web/src/lib/comparisons/juices-page-data.ts
 M bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts
 M bari-web/src/lib/comparisons/row-surface.ts
 M bari-web/src/lib/view-models/index.ts
 M bari-web/test-results/.last-run.json
 M integrations/clients/il_supplement_panels.py
 D presentations/nutrition_partnership/Bari_Nutrition_Partnership.pptx
 D presentations/nutrition_partnership/Bari_Nutrition_Partnership_spec.md
 D presentations/nutrition_partnership/assets/cereals_fortification.png
 D presentations/nutrition_partnership/assets/closing_pyramid.png
 D presentations/nutrition_partnership/assets/dairy_fermentation.png
 D presentations/nutrition_partnership/assets/engine_surface.png
 D presentations/nutrition_partnership/assets/expert_loop.png
 D presentations/nutrition_partnership/assets/hummus_boundary.png
 D presentations/nutrition_partnership/assets/logo_dark.png
 D presentations/nutrition_partnership/assets/logo_light.png
 D presentations/nutrition_partnership/assets/moat_flywheel.png
 D presentations/nutrition_partnership/assets/monetization_staircase.png
 D presentations/nutrition_partnership/assets/pipeline_band.png
 D presentations/nutrition_partnership/assets/problem_missing_layer.png
 D presentations/nutrition_partnership/assets/problem_trust.png
 D presentations/nutrition_partnership/assets/progress_grades.png
 D presentations/nutrition_partnership/assets/rigor_stack.png
 D presentations/nutrition_partnership/assets/roadmap_band.png
 D presentations/nutrition_partnership/assets/swimlane_90day.png
 D presentations/nutrition_partnership/assets/three_layers_band.png
 D presentations/nutrition_partnership/assets/why_now_cement.png
 D presentations/nutrition_partnership/assets/yogurt_grades.png
 D presentations/nutrition_partnership/build_deck.py
 D presentations/nutrition_partnership/make_visuals.py
 M tasks/DISPATCH_BOARD.md
?? .claude/skills/build-page/
?? .claude/skills/conformance/
?? .claude/skills/corpus/
?? .claude/skills/telemetry/
?? .claude/skills/tone/
?? 01_framework/bsip2_framework/docs/scoring/zoe_additive_quality_d6_design_v1.md
?? 01_framework/editorial/blog_backlog_v1.md
?? 02_products/_parsing_audit/task378_phase2_analytic.py
?? 02_products/_parsing_audit/task378_phase2_analytic_result.txt
?? 02_products/_parsing_audit/task378_phase2_analytic_results.json
?? 02_products/_parsing_audit/task378_phase2_check.py
?? 02_products/_parsing_audit/task378_phase2_rescore_result.txt
?? 02_products/_parsing_audit/task378_phase2_rescore_results.json
?? 02_products/_parsing_audit/task378_phase2_rescore_sim.py
?? 02_products/_parsing_audit/task378_phase2_result.txt
?? 02_products/_parsing_audit/task378_phase3_rescore_results.json
?? 02_products/_parsing_audit/task378_phase3_shufersal_scrape.json
?? 02_products/brand_backfill_sweep_task392.json
?? 02_products/bread/staging/
?? 02_products/breakfast_cereals/batch_run_cereals_task387_25g.py
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
?? 02_products/breakfast_cereals/reports/task387_stage1_cereals_25g_report.json
?? 02_products/breakfast_cereals/task385_granola_rescore.py
?? 02_products/breakfast_cereals/task385_rescore_out.txt
?? 02_products/breakfast_cereals/verify_gran_cross_category_isolation.py
?? 02_products/chocolate/_curate.txt
?? 02_products/chocolate/_score_review.txt
?? 02_products/chocolate/_score_run.log
?? 02_products/chocolate/_scrape_run.log
?? 02_products/chocolate/bsip0_outputs/
?? 02_products/chocolate/bsip2_outputs/
?? 02_products/chocolate/build_rich_chocolate.py
?? 02_products/chocolate/choc_fix_task366.py
?? 02_products/chocolate/choc_laibcatalog_ajax.py
?? 02_products/chocolate/choc_laibcatalog_check.py
?? 02_products/chocolate/choc_laibcatalog_debug.py
?? 02_products/chocolate/choc_tablets_fix_task366_20260622T130415.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T131938.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T135657.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T140340.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T141254.json
?? 02_products/chocolate/choc_task366b_finalize.py
?? 02_products/chocolate/choc_task366b_victory_probe.py
?? 02_products/chocolate/choc_victory_api_probe.py
?? 02_products/chocolate/choc_victory_branch_correct.py
?? 02_products/chocolate/choc_victory_branch_direct.py
?? 02_products/chocolate/choc_victory_catalog_probe.py
?? 02_products/chocolate/choc_victory_catalog_probe2.py
?? 02_products/chocolate/choc_victory_datajs.py
?? 02_products/chocolate/choc_victory_datajs_search.py
?? 02_products/chocolate/choc_victory_direct.py
?? 02_products/chocolate/choc_victory_final.py
?? 02_products/chocolate/choc_victory_final_scrape.py
?? 02_products/chocolate/choc_victory_js_api.py
?? 02_products/chocolate/choc_victory_nutr_api.py
?? 02_products/chocolate/choc_victory_product_direct.py
?? 02_products/chocolate/choc_victory_product_page.py
?? 02_products/chocolate/choc_victory_structure.py
?? 02_products/chocolate/choc_victory_targeted_playwright.py
?? 02_products/chocolate/choc_victory_v2_api.py
?? 02_products/chocolate/choc_victory_v3.py
?? 02_products/chocolate/choc_victory_verify.py
?? 02_products/chocolate/compare_task391.py
?? 02_products/chocolate/fresh_rescore_task391.py
?? 02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/selfverify_task391.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_task393_final/
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_task393_fresh/
?? 02_products/cookies_coffee/bsip2_outputs/run_task394_r3_measure/
?? 02_products/cookies_coffee/check_products.py
?? 02_products/cookies_coffee/inspect_on_scores.py
?? 02_products/cookies_coffee/inspect_on_scores_full.py
?? 02_products/cookies_coffee/verify_choc_stayE.py
?? 02_products/cookies_coffee/verify_final_state.py
?? 02_products/juices/bsip2_outputs/run_task389_rescore_001/
?? 02_products/juices/bsip2_outputs/run_task389_rescore_002/
?? 02_products/juices/debug2.py
?? 02_products/juices/debug3.py
?? 02_products/juices/debug_nova_signals.py
?? 02_products/juices/run_task389_rescore.py
?? 02_products/juices/write_corrected_rr.py
?? 02_products/milk_and_alternatives/patch_task378_almond_milk_sugar.py
?? 02_products/milk_and_alternatives/task378_almond_milk_rescore.json
?? 02_products/milk_and_alternatives/task378_artifact_sha256.py
?? 02_products/milk_and_alternatives/task378_copy_scan.py
?? 02_products/milk_and_alternatives/task378_sha256.py
?? 02_products/snack_bars/SNACKS_V5_SCORE_PROVENANCE.md
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_pb008.py
?? 02_products/snack_bars/_check_pb008_deep.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_gate_run_379.py
?? 02_products/snack_bars/_gate_run_379_efsa.py
?? 02_products/snack_bars/_gate_run_379_efsa_out.json
?? 02_products/snack_bars/_gate_run_379_out.json
?? 02_products/snack_bars/_gate_run_379_v2_out.json
?? 02_products/snack_bars/_verify_task365_fix.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/protein_bars_task365/
?? 02_products/snack_bars/bsip2_outputs/rescore_prot014_20260621_092813/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143230/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143317/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143502/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_150421/
?? 02_products/snack_bars/fix_task365_discard_truncated.py
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_121241.json
?? 02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_121241.json
?? 02_products/snack_bars/rescore_prot014_20260621_092813_run_record.json
?? 02_products/snack_bars/rescore_prot014_task362.py
?? 02_products/snack_bars/rescore_task365_inplace.py
?? 02_products/snack_bars/run_task365_protein_combined.py
?? 02_products/snack_bars/score_bars_task362_20260620_143317_manifest.json
?? 02_products/snack_bars/score_bars_task362_20260620_143502_manifest.json
?? 02_products/snack_bars/sugar_alcohols_blog_copy_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_embed_candidates_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v2.md
?? 02_products/snack_bars/sugar_alcohols_polyol_pct_check_v1.md
?? 02_products/supplements/magnesium_citation_correction_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v2.md
?? 02_products/supplements/magnesium_label_interpretation_v1.json
?? 02_products/supplements/magnesium_postmortem_v1.md
?? 02_products/supplements/magnesium_v3_postmortem_v1.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v10.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corpus_corrections_applied_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corrections_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_elemental_reconciliation_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_label_audit_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_ul_ruling_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3_regate.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v4.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/choc_task366_pass2_20260622_135915/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140019/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140047/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140126/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140336/
?? 03_operations/bsip1/choc_tmp/
?? 03_operations/bsip1/fresh_rescore_task391_20260624_113405/
?? 03_operations/bsip1/score_bars_task362_20260620_143230/
?? 03_operations/bsip1/score_bars_task362_20260620_143317/
?? 03_operations/bsip1/score_bars_task362_20260620_143502/
?? 03_operations/bsip1/score_bars_task362_20260620_150421/
?? 03_operations/bsip1/score_choc_task362_20260621_114229/
?? 03_operations/bsip1/score_choc_task362_20260621_114707/
?? 03_operations/bsip1/score_choc_task362_20260621_114832/
?? 03_operations/bsip1/task366_20260622T130415/
?? 03_operations/bsip2/protein_bar_lens_spec_task365.md
?? 03_operations/bsip2/proto_v0/diag_task371_step1/
?? 03_operations/bsip2/proto_v0/reports/dechain_d6_proposal_v1.md
?? 03_operations/bsip2/proto_v0/reports/glass_box/w2/_verify_d4_bars.py
?? 03_operations/bsip2/proto_v0/reports/scoring_overhaul_program_v1.md
?? 03_operations/bsip2/proto_v0/src/_t394_anchor_verify.py
?? 03_operations/bsip2/proto_v0/src/_t394_ing_verify.py
?? 03_operations/bsip2/proto_v0/src/bake_cookies_task393_final.py
?? 03_operations/bsip2/proto_v0/src/batch_run_protein_bars_task365.py
?? 03_operations/bsip2/proto_v0/src/drift_analysis_task393.py
?? 03_operations/bsip2/proto_v0/src/measure_r3_biscuit_narrow_v1.py
?? 03_operations/bsip2/proto_v0/src/regression_guard_task394_final.py
?? 03_operations/bsip2/proto_v0/src/rescore_cookies_task393.py
?? 03_operations/bsip2/proto_v0/src/rescore_cookies_task393_final.py
?? 03_operations/bsip2/proto_v0/src/run_task371_d4_score.py
?? 03_operations/bsip2/proto_v0/src/run_task388_calibrated_cosmetic_mup.py
?? 03_operations/bsip2/proto_v0/src/run_task388_clean_test.py
?? 03_operations/bsip2/proto_v0/src/run_task388_full_table.py
?? 03_operations/bsip2/proto_v0/src/run_task388_groundtruth.py
?? 03_operations/bsip2/proto_v0/src/run_task395_dechain_drift.py
?? 03_operations/bsip2/proto_v0/src/run_task395_parse_fix.py
?? 03_operations/bsip2/proto_v0/src/task395_hc_verify.py
?? 03_operations/bsip2/proto_v0/src/verify_task393.py
?? 03_operations/cc_history_analyzer/
?? 03_operations/page_generator/configs/chocolate_bars.json
?? 03_operations/page_generator/configs/chocolate_tablets.json
?? 03_operations/page_generator/configs/hummus_shelfrel_002_gates_report.md
?? 03_operations/page_generator/configs/protein_bars.json
?? 03_operations/page_generator/gates/baseline_verify.py
?? 03_operations/page_generator/gates/inversion_invariant.py
?? 03_operations/page_generator/gates/inversion_report_task395_v2.json
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? 03_operations/supplement_engine/proto_v0/prototype_absorbed_scoring.py
?? 03_operations/tools/task366_r2_verify.py
?? 03_operations/tools/task366_verify.py
?? 03_operations/tools/task366_verify_out.txt
?? 03_operations/tools/task366_wave6_audit.py
?? 03_operations/tools/task366_wave6_out.txt
?? "C\357\200\272Bari_bread_live_audit.json"
?? "C\357\200\272Bari_brined_live_audit.json"
?? "C\357\200\272Bari_hummus_live_audit.json"
?? "C\357\200\272Temppb_head.json"
?? __qa_naturalness_results.json
?? __qa_naturalness_run.py
?? __qa_number_audit.py
?? __qa_number_audit2.py
?? __qa_number_results.json
?? __qa_number_results.txt
?? _baselines/
?? _content_r2_verify.txt
?? _devserver.log
?? _fat_check.txt
?? _g6_bread_gates_report.md
?? _g6_brined_gates_report.md
?? _g6_cakes_gates_report.md
?? _g6_cheese_gates_report.md
?? _g6_milk_gates_report.md
?? _granola_audit.txt
?? _granola_content_verify.txt
?? _granola_rec.txt
?? _granola_render.html
?? _granola_score.txt
?? _granola_score2.txt
?? _granola_trace.txt
?? _granola_verify.txt
?? _meeting/
?? _milk_deploy_check.txt
?? _milk_final.txt
?? _milk_ranks.txt
?? _milk_verify.txt
?? _naturalness_result.json
?? _nut_xcheck.txt
?? _p282_dispatch.log
?? _prov_check.txt
?? _r3_final.txt
?? _r3_remaining.txt
?? _r3_verify.txt
?? _r_snacks.html
?? _render_result.txt
?? _snk_patch.py
?? _snk_verdicts_for_c3.txt
?? _task388_groundtruth.json
?? _tmp_canonical_rescore.json
?? _tmp_cereals_exact.py
?? _tmp_cereals_fix.py
?? _tmp_cereals_nodal.py
?? _tmp_final_rescore.py
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_investigate.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_rescore_script.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_update_ledger.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? _tmp_verify.py
?? _tmp_write_baselines.py
?? _verify_out.txt
?? affected_set_spine.json
?? bari-web/dev-server-err.log
?? bari-web/dev-server.log
?? bari-web/e2e/magnesium-geometry.spec.ts
?? bari-web/e2e/screenshots/
?? bari-web/e2e/task384-geometry.spec.ts
?? bari-web/geo_content.cjs
?? bari-web/geo_expand.cjs
?? bari-web/geo_full.cjs
?? bari-web/geo_leakage.cjs
?? bari-web/geo_rowhead.cjs
?? bari-web/geo_test.cjs
?? bari-web/geo_test.mjs
?? bari-web/geo_test2.cjs
?? bari-web/geo_test3.cjs
?? bari-web/mag_mobile_390.png
?? bari-web/magnesium-geometry.png
?? bari-web/public/bari-avatar-paper.png
?? bari-web/scripts/measure-dom-structure.mjs
?? bari-web/scripts/measure-granola-geometry.mjs
?? bari-web/scripts/measure-header-breakdown.mjs
?? bari-web/scripts/measure-magnesium-geometry.mjs
?? bari-web/scripts/measure-rows-detail.mjs
?? bari-web/server-err.txt
?? bari-web/server-out.txt
?? bari-web/server.log
?? bari-web/src/app/blog/sugar-alcohols/
?? bari-web/src/app/hashvaot/chocolate-bars/
?? bari-web/src/app/hashvaot/chocolate-tablets/
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/app/hashvaot/supplements/
?? bari-web/src/components/blog/sugar-alcohols-article.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart1.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart2.tsx
?? bari-web/src/components/blog/sugar-alcohols-efsa-card.tsx
?? bari-web/src/components/blog/sugar-alcohols-front-vs-back.tsx
?? bari-web/src/components/comparisons/chocolate-bars-comparison-page.tsx
?? bari-web/src/components/comparisons/chocolate-tablets-comparison-page.tsx
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-bars-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-tablets-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-magnesium-intelligence-card.tsx
?? bari-web/src/components/shared/magnesium-badge-grid.tsx
?? bari-web/src/components/shared/magnesium-safety-box.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v2.json
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/protein_combined_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v5_gates_report.md
?? bari-web/src/lib/blog/sugar-alcohols-article-content.ts
?? bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? bari-web/tmp_dev_log.txt
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
?? bari-web/verify-magnesium-clamp.js
?? check_cc_bsip0.py
?? check_cc_carbs.py
?? check_cc_remaining.py
?? check_milk_carbs.py
?? check_remaining_cheese_brined_cereals.py
?? check_unknown_carbs.py
?? check_unknown_carbs_v2.py
?? content_voice/tone_briefs/
?? dev_server_log.txt
?? diag_task371_step1.py
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? pb_head_tmp.json
?? qa_deep_check.py
?? qa_leakage_voice.py
?? qa_number_fidelity.py
?? qa_superlative_check.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? scan_sugar_null.py
?? scan_sugar_null_v2.py
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/TASK-364.md
?? tasks/TASK-365.md
?? tasks/TASK-366.md
?? tasks/TASK-367.md
?? tasks/TASK-368.md
?? tasks/TASK-369.md
?? tasks/TASK-370.md
?? tasks/TASK-372.md
?? tasks/TASK-373.md
?? tasks/TASK-379.md
?? tasks/TASK-380.md
?? tasks/TASK-383.md
?? tasks/TASK-384.md
?? tasks/TASK-384A.md
?? tasks/TASK-385.md
?? tasks/TASK-386.md
?? tasks/TASK-387.md
?? tasks/TASK-389.md
?? tasks/TASK-393.md
?? tasks/TASK-395.md
?? tasks/TASK-396.md
?? tasks/TASK-397.md
?? tasks/TASK-398.md
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_badges.py
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_result.json
?? tasks/_scratch_verdict_audit.py
?? tasks/_scratch_verdict_len.py
?? tasks/_task371_layer1_diagnostic.py
?? tasks/_task371_layer1_v2.py
?? tasks/_task371_score_one.py
?? tasks/autonomous_orchestrate.ps1
?? tasks/closed/TASK-388.md
?? tasks/closed/TASK-390.md
?? tasks/closed/TASK-391.md
?? tasks/closed/TASK-392.md
?? tasks/closed/TASK-394.md
?? tasks/digests/
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/prompts/P280_c3_snacks_challenge.md
?? tasks/prompts/P282_snacks_relief_challenge.md
?? tasks/prompts/P300_c3_magnesium_elemental_challenge.md
?? tasks/prompts/P301_c3_magnesium_recalibration_challenge.md
?? tasks/prompts/P303_c3_magnesium_v3_final_teardown.md
?? tasks/prompts/P304_c3_magnesium_content_gate.md
?? tasks/prompts/P305_c3_magnesium_content_regate.md
?? tasks/prompts/P387_granola_c3_challenge.md
?? tasks/prompts/P388_granola_c3_verify.md
?? tasks/prompts/P389_c3_magnesium_clinical_validity.md
?? tasks/prompts/P392_juices_decite_c3.md
?? tasks/prompts/P396_c3_nova_proxy_debate.md
?? tasks/prompts/P397_c3_scoring_system_replan.md
?? tasks/prompts/P402_brined_sweep_cursor.md
?? tasks/prompts/P403_legal_compliance_c3_review.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
?? tasks/prompts/_done/P391_cereals_decite_c3.md
?? tasks/prompts/_done/P393_chocolate_decite_c3.md
?? tasks/prompts/_done/P395_cookies_decite_c3.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P246_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? tasks/returns/P268_drift_report.md
?? tasks/returns/P280_return.md
?? tasks/returns/P282_return.md
?? tasks/returns/P297_return.md
?? tasks/returns/P300_return.md
?? tasks/returns/P301_return.md
?? tasks/returns/P302_return.md
?? tasks/returns/P303_return.md
?? tasks/returns/P304_return.md
?? tasks/returns/P305_return.md
?? tasks/returns/P387_return.md
?? tasks/returns/P388_return.md
?? tasks/returns/P389_return.md
?? tasks/returns/P390_return.md
?? tasks/returns/P391_return.md
?? tasks/returns/P392_return.md
?? tasks/returns/P393_return.md
?? tasks/returns/P395_return.md
?? tasks/returns/P396_return.md
?? tasks/returns/P397_return.md
?? tasks/returns/P402_cursor_out.txt
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? tasks/task392_brand_backfill.py
?? test_acceptance.py
```

### After dispatch

```
M 01_framework/editorial/editorial_intelligence_v3.md
 M 02_products/supplements/real_corpus_v3/_addressable_shelf.json
 M 02_products/supplements/real_corpus_v3/cache/7290015318426.json
 M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md
 M 03_operations/bsip2/proto_v0/src/constants.py
 M 03_operations/bsip2/proto_v0/src/router_v2.py
 M 03_operations/bsip2/proto_v0/src/score_engine.py
 M 03_operations/bsip2/proto_v0/src/signal_extractor.py
 M 03_operations/page_generator/conform_baseline.py
 M 03_operations/page_generator/gates/run_gates.py
 M 03_operations/page_generator/generate_page.py
 M 03_operations/reports/regression/regression_check_001.md
 M 03_operations/reports/regression/router_regression_001.md
 M 03_operations/spine/live_manifest.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M 03_operations/validators/verify_citations.py
 M bari-web/next.config.ts
 M bari-web/src/app/globals.css
 M bari-web/src/app/sitemap.ts
 M bari-web/src/components/comparisons/cereals-comparison-page.tsx
 M bari-web/src/components/comparisons/comparison-page.tsx
 M bari-web/src/components/comparisons/cookies-coffee-comparison-page.tsx
 M bari-web/src/components/comparisons/granola-comparison-page.tsx
 M bari-web/src/components/comparisons/protein-bars-comparison-page.tsx
 M bari-web/src/components/home/home-analysis-engine.tsx
 M bari-web/src/components/shared/category-prologue.tsx
 M bari-web/src/components/shared/comparison-metric-column.tsx
 M bari-web/src/components/shared/comparison-table.tsx
 M bari-web/src/components/shared/expansion-section.tsx
 M bari-web/src/data/bread-retail-curated.json
 M bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json
 M bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json
 M bari-web/src/data/comparisons/cereals_frontend_v2.json
 M bari-web/src/data/comparisons/cheese_frontend_v4.json
 M bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json
 M bari-web/src/data/comparisons/hard_cheeses_frontend_v2.json
 M bari-web/src/data/comparisons/hummus_frontend_v5.json
 M bari-web/src/data/comparisons/juices_frontend_v3.json
 M bari-web/src/data/comparisons/milk_frontend_v1.json
 M bari-web/src/lib/comparisons/cakes-hard-cookies-page-data.ts
 M bari-web/src/lib/comparisons/cereals-page-data.ts
 M bari-web/src/lib/comparisons/cookies-coffee-page-data.ts
 M bari-web/src/lib/comparisons/granola-page-data.ts
 M bari-web/src/lib/comparisons/juices-page-data.ts
 M bari-web/src/lib/comparisons/protein-bars-comparison-page-data.ts
 M bari-web/src/lib/comparisons/row-surface.ts
 M bari-web/src/lib/view-models/index.ts
 M bari-web/test-results/.last-run.json
 M integrations/clients/il_supplement_panels.py
 D presentations/nutrition_partnership/Bari_Nutrition_Partnership.pptx
 D presentations/nutrition_partnership/Bari_Nutrition_Partnership_spec.md
 D presentations/nutrition_partnership/assets/cereals_fortification.png
 D presentations/nutrition_partnership/assets/closing_pyramid.png
 D presentations/nutrition_partnership/assets/dairy_fermentation.png
 D presentations/nutrition_partnership/assets/engine_surface.png
 D presentations/nutrition_partnership/assets/expert_loop.png
 D presentations/nutrition_partnership/assets/hummus_boundary.png
 D presentations/nutrition_partnership/assets/logo_dark.png
 D presentations/nutrition_partnership/assets/logo_light.png
 D presentations/nutrition_partnership/assets/moat_flywheel.png
 D presentations/nutrition_partnership/assets/monetization_staircase.png
 D presentations/nutrition_partnership/assets/pipeline_band.png
 D presentations/nutrition_partnership/assets/problem_missing_layer.png
 D presentations/nutrition_partnership/assets/problem_trust.png
 D presentations/nutrition_partnership/assets/progress_grades.png
 D presentations/nutrition_partnership/assets/rigor_stack.png
 D presentations/nutrition_partnership/assets/roadmap_band.png
 D presentations/nutrition_partnership/assets/swimlane_90day.png
 D presentations/nutrition_partnership/assets/three_layers_band.png
 D presentations/nutrition_partnership/assets/why_now_cement.png
 D presentations/nutrition_partnership/assets/yogurt_grades.png
 D presentations/nutrition_partnership/build_deck.py
 D presentations/nutrition_partnership/make_visuals.py
 M tasks/DISPATCH_BOARD.md
?? .claude/skills/build-page/
?? .claude/skills/conformance/
?? .claude/skills/corpus/
?? .claude/skills/telemetry/
?? .claude/skills/tone/
?? 01_framework/bsip2_framework/docs/scoring/zoe_additive_quality_d6_design_v1.md
?? 01_framework/editorial/blog_backlog_v1.md
?? 02_products/_parsing_audit/task378_phase2_analytic.py
?? 02_products/_parsing_audit/task378_phase2_analytic_result.txt
?? 02_products/_parsing_audit/task378_phase2_analytic_results.json
?? 02_products/_parsing_audit/task378_phase2_check.py
?? 02_products/_parsing_audit/task378_phase2_rescore_result.txt
?? 02_products/_parsing_audit/task378_phase2_rescore_results.json
?? 02_products/_parsing_audit/task378_phase2_rescore_sim.py
?? 02_products/_parsing_audit/task378_phase2_result.txt
?? 02_products/_parsing_audit/task378_phase3_rescore_results.json
?? 02_products/_parsing_audit/task378_phase3_shufersal_scrape.json
?? 02_products/brand_backfill_sweep_task392.json
?? 02_products/bread/staging/
?? 02_products/breakfast_cereals/batch_run_cereals_task387_25g.py
?? 02_products/breakfast_cereals/batch_run_granola_task385_25g.py
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_cereals_task387_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_25g/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_off/
?? 02_products/breakfast_cereals/bsip2_outputs/run_granola_task385_on/
?? 02_products/breakfast_cereals/reports/red_team_granola_run_granola_task385_off.md
?? 02_products/breakfast_cereals/reports/task385_ev105_granola_25g_report.json
?? 02_products/breakfast_cereals/reports/task385_granola_rescore_report.json
?? 02_products/breakfast_cereals/reports/task385_run_record.json
?? 02_products/breakfast_cereals/reports/task387_stage1_cereals_25g_report.json
?? 02_products/breakfast_cereals/task385_granola_rescore.py
?? 02_products/breakfast_cereals/task385_rescore_out.txt
?? 02_products/breakfast_cereals/verify_gran_cross_category_isolation.py
?? 02_products/chocolate/_curate.txt
?? 02_products/chocolate/_score_review.txt
?? 02_products/chocolate/_score_run.log
?? 02_products/chocolate/_scrape_run.log
?? 02_products/chocolate/bsip0_outputs/
?? 02_products/chocolate/bsip2_outputs/
?? 02_products/chocolate/build_rich_chocolate.py
?? 02_products/chocolate/choc_fix_task366.py
?? 02_products/chocolate/choc_laibcatalog_ajax.py
?? 02_products/chocolate/choc_laibcatalog_check.py
?? 02_products/chocolate/choc_laibcatalog_debug.py
?? 02_products/chocolate/choc_tablets_fix_task366_20260622T130415.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T131938.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T135657.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T140340.json
?? 02_products/chocolate/choc_tablets_fix_task366b_20260622T141254.json
?? 02_products/chocolate/choc_task366b_finalize.py
?? 02_products/chocolate/choc_task366b_victory_probe.py
?? 02_products/chocolate/choc_victory_api_probe.py
?? 02_products/chocolate/choc_victory_branch_correct.py
?? 02_products/chocolate/choc_victory_branch_direct.py
?? 02_products/chocolate/choc_victory_catalog_probe.py
?? 02_products/chocolate/choc_victory_catalog_probe2.py
?? 02_products/chocolate/choc_victory_datajs.py
?? 02_products/chocolate/choc_victory_datajs_search.py
?? 02_products/chocolate/choc_victory_direct.py
?? 02_products/chocolate/choc_victory_final.py
?? 02_products/chocolate/choc_victory_final_scrape.py
?? 02_products/chocolate/choc_victory_js_api.py
?? 02_products/chocolate/choc_victory_nutr_api.py
?? 02_products/chocolate/choc_victory_product_direct.py
?? 02_products/chocolate/choc_victory_product_page.py
?? 02_products/chocolate/choc_victory_structure.py
?? 02_products/chocolate/choc_victory_targeted_playwright.py
?? 02_products/chocolate/choc_victory_v2_api.py
?? 02_products/chocolate/choc_victory_v3.py
?? 02_products/chocolate/choc_victory_verify.py
?? 02_products/chocolate/compare_task391.py
?? 02_products/chocolate/fresh_rescore_task391.py
?? 02_products/chocolate/fresh_rescore_task391_20260624_113405_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114229_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114707_manifest.json
?? 02_products/chocolate/score_choc_task362_20260621_114832_manifest.json
?? 02_products/chocolate/score_chocolate_task362.py
?? 02_products/chocolate/selfverify_task391.py
?? 02_products/chocolate/victory_branch_captured.json
?? 02_products/chocolate/victory_branch_found.json
?? 02_products/chocolate/victory_v2_raw.json
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_task393_final/
?? 02_products/cookies_coffee/bsip2_outputs/run_cookies_task393_fresh/
?? 02_products/cookies_coffee/bsip2_outputs/run_task394_r3_measure/
?? 02_products/cookies_coffee/check_products.py
?? 02_products/cookies_coffee/inspect_on_scores.py
?? 02_products/cookies_coffee/inspect_on_scores_full.py
?? 02_products/cookies_coffee/verify_choc_stayE.py
?? 02_products/cookies_coffee/verify_final_state.py
?? 02_products/juices/bsip2_outputs/run_task389_rescore_001/
?? 02_products/juices/bsip2_outputs/run_task389_rescore_002/
?? 02_products/juices/debug2.py
?? 02_products/juices/debug3.py
?? 02_products/juices/debug_nova_signals.py
?? 02_products/juices/run_task389_rescore.py
?? 02_products/juices/write_corrected_rr.py
?? 02_products/milk_and_alternatives/patch_task378_almond_milk_sugar.py
?? 02_products/milk_and_alternatives/task378_almond_milk_rescore.json
?? 02_products/milk_and_alternatives/task378_artifact_sha256.py
?? 02_products/milk_and_alternatives/task378_copy_scan.py
?? 02_products/milk_and_alternatives/task378_sha256.py
?? 02_products/snack_bars/SNACKS_V5_SCORE_PROVENANCE.md
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_pb008.py
?? 02_products/snack_bars/_check_pb008_deep.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_gate_run_379.py
?? 02_products/snack_bars/_gate_run_379_efsa.py
?? 02_products/snack_bars/_gate_run_379_efsa_out.json
?? 02_products/snack_bars/_gate_run_379_out.json
?? 02_products/snack_bars/_gate_run_379_v2_out.json
?? 02_products/snack_bars/_verify_task365_fix.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/protein_bars_task365/
?? 02_products/snack_bars/bsip2_outputs/rescore_prot014_20260621_092813/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143230/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143317/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_143502/
?? 02_products/snack_bars/bsip2_outputs/score_bars_task362_20260620_150421/
?? 02_products/snack_bars/fix_task365_discard_truncated.py
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_corpus_task365_20260621_121241.json
?? 02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_115610.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120233.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_120733.json
?? 02_products/snack_bars/protein_combined_manifest_task365_20260621_121241.json
?? 02_products/snack_bars/rescore_prot014_20260621_092813_run_record.json
?? 02_products/snack_bars/rescore_prot014_task362.py
?? 02_products/snack_bars/rescore_task365_inplace.py
?? 02_products/snack_bars/run_task365_protein_combined.py
?? 02_products/snack_bars/score_bars_task362_20260620_143317_manifest.json
?? 02_products/snack_bars/score_bars_task362_20260620_143502_manifest.json
?? 02_products/snack_bars/sugar_alcohols_blog_copy_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_embed_candidates_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v1.md
?? 02_products/snack_bars/sugar_alcohols_blog_nutrition_spec_v2.md
?? 02_products/snack_bars/sugar_alcohols_polyol_pct_check_v1.md
?? 02_products/supplements/magnesium_citation_correction_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v1.md
?? 02_products/supplements/magnesium_clinical_content_spec_v2.md
?? 02_products/supplements/magnesium_label_interpretation_v1.json
?? 02_products/supplements/magnesium_postmortem_v1.md
?? 02_products/supplements/magnesium_v3_postmortem_v1.md
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v10.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corpus_corrections_applied_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_corrections_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_elemental_reconciliation_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_label_audit_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_ul_ruling_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v3_regate.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v4.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/choc_task366_pass2_20260622_135915/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140019/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140047/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140126/
?? 03_operations/bsip1/choc_task366_pass2_20260622_140336/
?? 03_operations/bsip1/choc_tmp/
?? 03_operations/bsip1/fresh_rescore_task391_20260624_113405/
?? 03_operations/bsip1/score_bars_task362_20260620_143230/
?? 03_operations/bsip1/score_bars_task362_20260620_143317/
?? 03_operations/bsip1/score_bars_task362_20260620_143502/
?? 03_operations/bsip1/score_bars_task362_20260620_150421/
?? 03_operations/bsip1/score_choc_task362_20260621_114229/
?? 03_operations/bsip1/score_choc_task362_20260621_114707/
?? 03_operations/bsip1/score_choc_task362_20260621_114832/
?? 03_operations/bsip1/task366_20260622T130415/
?? 03_operations/bsip2/protein_bar_lens_spec_task365.md
?? 03_operations/bsip2/proto_v0/diag_task371_step1/
?? 03_operations/bsip2/proto_v0/reports/dechain_d6_proposal_v1.md
?? 03_operations/bsip2/proto_v0/reports/glass_box/w2/_verify_d4_bars.py
?? 03_operations/bsip2/proto_v0/reports/scoring_overhaul_program_v1.md
?? 03_operations/bsip2/proto_v0/src/_t394_anchor_verify.py
?? 03_operations/bsip2/proto_v0/src/_t394_ing_verify.py
?? 03_operations/bsip2/proto_v0/src/bake_cookies_task393_final.py
?? 03_operations/bsip2/proto_v0/src/batch_run_protein_bars_task365.py
?? 03_operations/bsip2/proto_v0/src/drift_analysis_task393.py
?? 03_operations/bsip2/proto_v0/src/measure_r3_biscuit_narrow_v1.py
?? 03_operations/bsip2/proto_v0/src/regression_guard_task394_final.py
?? 03_operations/bsip2/proto_v0/src/rescore_cookies_task393.py
?? 03_operations/bsip2/proto_v0/src/rescore_cookies_task393_final.py
?? 03_operations/bsip2/proto_v0/src/run_task371_d4_score.py
?? 03_operations/bsip2/proto_v0/src/run_task388_calibrated_cosmetic_mup.py
?? 03_operations/bsip2/proto_v0/src/run_task388_clean_test.py
?? 03_operations/bsip2/proto_v0/src/run_task388_full_table.py
?? 03_operations/bsip2/proto_v0/src/run_task388_groundtruth.py
?? 03_operations/bsip2/proto_v0/src/run_task395_dechain_drift.py
?? 03_operations/bsip2/proto_v0/src/run_task395_parse_fix.py
?? 03_operations/bsip2/proto_v0/src/task395_hc_verify.py
?? 03_operations/bsip2/proto_v0/src/verify_task393.py
?? 03_operations/cc_history_analyzer/
?? 03_operations/page_generator/configs/chocolate_bars.json
?? 03_operations/page_generator/configs/chocolate_tablets.json
?? 03_operations/page_generator/configs/hummus_shelfrel_002_gates_report.md
?? 03_operations/page_generator/configs/protein_bars.json
?? 03_operations/page_generator/gates/baseline_verify.py
?? 03_operations/page_generator/gates/inversion_invariant.py
?? 03_operations/page_generator/gates/inversion_report_task395_v2.json
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? 03_operations/supplement_engine/proto_v0/prototype_absorbed_scoring.py
?? 03_operations/tools/task366_r2_verify.py
?? 03_operations/tools/task366_verify.py
?? 03_operations/tools/task366_verify_out.txt
?? 03_operations/tools/task366_wave6_audit.py
?? 03_operations/tools/task366_wave6_out.txt
?? "C\357\200\272Bari_bread_live_audit.json"
?? "C\357\200\272Bari_brined_live_audit.json"
?? "C\357\200\272Bari_hummus_live_audit.json"
?? "C\357\200\272Temppb_head.json"
?? __qa_naturalness_results.json
?? __qa_naturalness_run.py
?? __qa_number_audit.py
?? __qa_number_audit2.py
?? __qa_number_results.json
?? __qa_number_results.txt
?? _baselines/
?? _content_r2_verify.txt
?? _devserver.log
?? _fat_check.txt
?? _g6_bread_gates_report.md
?? _g6_brined_gates_report.md
?? _g6_cakes_gates_report.md
?? _g6_cheese_gates_report.md
?? _g6_milk_gates_report.md
?? _granola_audit.txt
?? _granola_content_verify.txt
?? _granola_rec.txt
?? _granola_render.html
?? _granola_score.txt
?? _granola_score2.txt
?? _granola_trace.txt
?? _granola_verify.txt
?? _lock_chocolate_bars_frontend_v1_gates_report.md
?? _lock_chocolate_tablets_frontend_v1_gates_report.md
?? _meeting/
?? _milk_deploy_check.txt
?? _milk_final.txt
?? _milk_ranks.txt
?? _milk_verify.txt
?? _naturalness_result.json
?? _nut_xcheck.txt
?? _p282_dispatch.log
?? _prov_check.txt
?? _r3_final.txt
?? _r3_remaining.txt
?? _r3_verify.txt
?? _r_snacks.html
?? _render_result.txt
?? _snk_patch.py
?? _snk_verdicts_for_c3.txt
?? _task388_groundtruth.json
?? _tmp_canonical_rescore.json
?? _tmp_cereals_exact.py
?? _tmp_cereals_fix.py
?? _tmp_cereals_nodal.py
?? _tmp_final_rescore.py
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_investigate.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_rescore_script.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_update_ledger.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? _tmp_verify.py
?? _tmp_write_baselines.py
?? _verify_out.txt
?? affected_set_spine.json
?? bari-web/dev-server-err.log
?? bari-web/dev-server.log
?? bari-web/e2e/magnesium-geometry.spec.ts
?? bari-web/e2e/screenshots/
?? bari-web/e2e/task384-geometry.spec.ts
?? bari-web/geo_content.cjs
?? bari-web/geo_expand.cjs
?? bari-web/geo_full.cjs
?? bari-web/geo_leakage.cjs
?? bari-web/geo_rowhead.cjs
?? bari-web/geo_test.cjs
?? bari-web/geo_test.mjs
?? bari-web/geo_test2.cjs
?? bari-web/geo_test3.cjs
?? bari-web/mag_mobile_390.png
?? bari-web/magnesium-geometry.png
?? bari-web/public/bari-avatar-paper.png
?? bari-web/scripts/measure-dom-structure.mjs
?? bari-web/scripts/measure-granola-geometry.mjs
?? bari-web/scripts/measure-header-breakdown.mjs
?? bari-web/scripts/measure-magnesium-geometry.mjs
?? bari-web/scripts/measure-rows-detail.mjs
?? bari-web/server-err.txt
?? bari-web/server-out.txt
?? bari-web/server.log
?? bari-web/src/app/blog/sugar-alcohols/
?? bari-web/src/app/hashvaot/chocolate-bars/
?? bari-web/src/app/hashvaot/chocolate-tablets/
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/app/hashvaot/supplements/
?? bari-web/src/components/blog/sugar-alcohols-article.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart1.tsx
?? bari-web/src/components/blog/sugar-alcohols-chart2.tsx
?? bari-web/src/components/blog/sugar-alcohols-efsa-card.tsx
?? bari-web/src/components/blog/sugar-alcohols-front-vs-back.tsx
?? bari-web/src/components/comparisons/chocolate-bars-comparison-page.tsx
?? bari-web/src/components/comparisons/chocolate-tablets-comparison-page.tsx
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-bars-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-chocolate-tablets-intelligence-card.tsx
?? bari-web/src/components/hashvaot/featured-magnesium-intelligence-card.tsx
?? bari-web/src/components/shared/magnesium-badge-grid.tsx
?? bari-web/src/components/shared/magnesium-safety-box.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/chocolate_bars_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1.json
?? bari-web/src/data/comparisons/chocolate_tablets_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v2.json
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/protein_combined_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v5_gates_report.md
?? bari-web/src/lib/blog/sugar-alcohols-article-content.ts
?? bari-web/src/lib/comparisons/chocolate-bars-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-bars-shelf-filters.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-comparison-page-data.ts
?? bari-web/src/lib/comparisons/chocolate-tablets-shelf-filters.ts
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? bari-web/tmp_dev_log.txt
?? bari-web/tmp_shots/hashvaot_index_mobile.png
?? bari-web/tmp_shots/mag_mobile_0scroll.png
?? bari-web/tmp_shots/mag_visual_check.cjs
?? bari-web/tmp_shots/oxide_safety_check.cjs
?? bari-web/tmp_shots/oxide_safety_visible.png
?? bari-web/tmp_shots/supp_check.cjs
?? bari-web/tmp_shots/supplements_index.png
?? bari-web/verify-magnesium-clamp.js
?? check_cc_bsip0.py
?? check_cc_carbs.py
?? check_cc_remaining.py
?? check_milk_carbs.py
?? check_remaining_cheese_brined_cereals.py
?? check_unknown_carbs.py
?? check_unknown_carbs_v2.py
?? content_voice/tone_briefs/
?? dev_server_log.txt
?? diag_task371_step1.py
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? pb_head_tmp.json
?? qa_deep_check.py
?? qa_leakage_voice.py
?? qa_number_fidelity.py
?? qa_superlative_check.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? scan_sugar_null.py
?? scan_sugar_null_v2.py
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/TASK-364.md
?? tasks/TASK-365.md
?? tasks/TASK-366.md
?? tasks/TASK-367.md
?? tasks/TASK-368.md
?? tasks/TASK-369.md
?? tasks/TASK-370.md
?? tasks/TASK-372.md
?? tasks/TASK-373.md
?? tasks/TASK-379.md
?? tasks/TASK-380.md
?? tasks/TASK-383.md
?? tasks/TASK-384.md
?? tasks/TASK-384A.md
?? tasks/TASK-385.md
?? tasks/TASK-386.md
?? tasks/TASK-387.md
?? tasks/TASK-389.md
?? tasks/TASK-393.md
?? tasks/TASK-395.md
?? tasks/TASK-396.md
?? tasks/TASK-397.md
?? tasks/TASK-398.md
?? tasks/TASK-399.md
?? tasks/TASK-400.md
?? tasks/_scratch_mag_labels/
?? tasks/_scratch_naturalness_badges.py
?? tasks/_scratch_naturalness_check.py
?? tasks/_scratch_naturalness_result.json
?? tasks/_scratch_verdict_audit.py
?? tasks/_scratch_verdict_len.py
?? tasks/_task371_layer1_diagnostic.py
?? tasks/_task371_layer1_v2.py
?? tasks/_task371_score_one.py
?? tasks/autonomous_orchestrate.ps1
?? tasks/closed/TASK-388.md
?? tasks/closed/TASK-390.md
?? tasks/closed/TASK-391.md
?? tasks/closed/TASK-392.md
?? tasks/closed/TASK-394.md
?? tasks/digests/
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/prompts/P280_c3_snacks_challenge.md
?? tasks/prompts/P282_snacks_relief_challenge.md
?? tasks/prompts/P300_c3_magnesium_elemental_challenge.md
?? tasks/prompts/P301_c3_magnesium_recalibration_challenge.md
?? tasks/prompts/P303_c3_magnesium_v3_final_teardown.md
?? tasks/prompts/P304_c3_magnesium_content_gate.md
?? tasks/prompts/P305_c3_magnesium_content_regate.md
?? tasks/prompts/P387_granola_c3_challenge.md
?? tasks/prompts/P388_granola_c3_verify.md
?? tasks/prompts/P389_c3_magnesium_clinical_validity.md
?? tasks/prompts/P392_juices_decite_c3.md
?? tasks/prompts/P396_c3_nova_proxy_debate.md
?? tasks/prompts/P397_c3_scoring_system_replan.md
?? tasks/prompts/P402_brined_sweep_cursor.md
?? tasks/prompts/P403_legal_compliance_c3_review.md
?? tasks/prompts/_done/P283_protein_bars_r3_mechanical.md
?? tasks/prompts/_done/P297_hc_satfat_rule_challenge.md
?? tasks/prompts/_done/P302_c3_magnesium_v3_real_calibration_challenge.md
?? tasks/prompts/_done/P390_granola_decite_c3.md
?? tasks/prompts/_done/P391_cereals_decite_c3.md
?? tasks/prompts/_done/P393_chocolate_decite_c3.md
?? tasks/prompts/_done/P395_cookies_decite_c3.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P246_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? tasks/returns/P268_drift_report.md
?? tasks/returns/P280_return.md
?? tasks/returns/P282_return.md
?? tasks/returns/P297_return.md
?? tasks/returns/P300_return.md
?? tasks/returns/P301_return.md
?? tasks/returns/P302_return.md
?? tasks/returns/P303_return.md
?? tasks/returns/P304_return.md
?? tasks/returns/P305_return.md
?? tasks/returns/P387_return.md
?? tasks/returns/P388_return.md
?? tasks/returns/P389_return.md
?? tasks/returns/P390_return.md
?? tasks/returns/P391_return.md
?? tasks/returns/P392_return.md
?? tasks/returns/P393_return.md
?? tasks/returns/P395_return.md
?? tasks/returns/P396_return.md
?? tasks/returns/P397_return.md
?? tasks/returns/P402_cursor_out.txt
?? tasks/task368_d4_impact_analysis.py
?? tasks/task368_output.txt
?? tasks/task392_brand_backfill.py
?? test_acceptance.py
```

### Delta

### New / modified since dispatch
  ?? _lock_chocolate_bars_frontend_v1_gates_report.md
  ?? _lock_chocolate_tablets_frontend_v1_gates_report.md
  ?? tasks/TASK-399.md
  ?? tasks/TASK-400.md
