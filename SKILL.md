---
name: nomik
description: Agency-grade brand naming, domain intelligence, linguistic phonosemantics, and trademark viability auditor. Created by Raul Aliyev (@rallycodes). Use whenever the user wants to name a company, startup, app, product, platform, software, tool, service, or feature, or asks to check domain availability, find available domains, check domain pricing, audit a brand name, or find a name with great taste and zero AI clichés. Always invoke this skill when the user asks "what should I name...", "help me name...", "find a brand name for...", "check domain...", "is this domain taken...", or requests creative brand strategy.
author: Raul Aliyev (@rallycodes)
license: MIT
---

# Nomik: Brand Naming & Domain Intelligence Agency
*Created by Raul Aliyev (@rallycodes)*

An agency-grade naming and domain verification engine matching the standards of top-tier branding firms (Lexicon Branding, Wolff Olins, Pentagram, Collins, and Igor).

This skill enforces high-taste, zero-slop naming architectures, runs phonosemantic audits, and executes real-time ICANN domain checks with live pricing across TLDs and strategic modifier suites.

---

## The Anti-AI-Slop Laws (Zero Tolerance)

Before generating or evaluating any candidate name, you must strictly reject:
1. **Suffix Stuffing:** No `-ify` (Taskify), `-ly` (Quickly), `-io` (Brandio), `-sy` (Worksy), `-ix` (Flowix), `-ora` (Taskora).
2. **Generic Tech Mashups:** No `Smart-`, `Omni-`, `Data-`, `Cloud-`, `Neuro-`, `Synap-`, `Meta-`, `Nexa-`, `Hyper-`, `Intel-` mashed with abstract nouns (`CloudFlow`, `DataPulse`, `OmniSync`, `NeuroCore`).
3. **Sterile Latin Abstractions:** No `Lumina`, `Apex`, `Nexus`, `Vertex`, `Momentum`, `Catalyst`, `Prism`, `Synergy`, `Zenith`, `Verto`.
4. **Literal Feature Snoozes:** No `EasyInvoice`, `QuickCode`, `FastForm`.

*For the complete taste filter, read `references/anti_slop_rules.md`.*

---

## Bundled Deterministic Scripts

Always use the bundled scripts to ensure factual accuracy and avoid hallucinated availability:

| Script | Command | Purpose |
|---|---|---|
| **Domain Suite Audit** | `python scripts/check_domain.py --brand <name>` | Audits all core TLDs (`.com`, `.ai`, `.io`, `.app`, `.co`, `.dev`, `.so`) and modifier suites (`get-`, `use-`, `try-`, `-hq`, `-app`, `-labs`) with live socket DNS, RDAP, HTTP parking lander detection, and pricing. |
| **Developer & Social Handles** | `python scripts/check_handles.py <handle>` | Checks availability across GitHub, npm, PyPI, and Crates.io in parallel. |
| **Trademark Clearance** | `python scripts/check_trademark.py <name> --category <cat>` | Audits Abercrombie distinctiveness spectrum and generates direct USPTO, WIPO, and EUIPO clearance query links. |
| **Linguistic & Visual Rhythm** | `python scripts/phonetics.py <name>` | Computes trochaic cadence, plosive/fricative profile, Radio Test score (1-10), verb potential, and visual ascender/descender kerning balance. |
| **Executive Dossier** | `python scripts/generate_report.py --project "<P>" --category "<C>" --brief "<B>" --names "<N1,N2>"` | Assembles an agency-grade executive presentation report with tables and roadmaps. |

*Scripts directory path:* `scripts/check_domain.py`, `scripts/check_handles.py`, `scripts/check_trademark.py`, `scripts/phonetics.py`, `scripts/generate_report.py`.

---

## The `/nomik` Slash Command Workflow

When the user triggers `/nomik`:

### 1. Direct Argument Provided (e.g. `/nomik <name>` or `/nomik <idea>`):
- **If a specific candidate name or domain is given** (e.g. `/nomik stripe.com` or `/nomik audit kyntic`):
  Execute `check_domain.py`, `check_handles.py`, `phonetics.py`, and `check_trademark.py` immediately.
- **If a product idea or description is given** (e.g. `/nomik high-performance Rust key-value store`):
  Execute the 6-Step Agency Naming Pipeline directly without delay.

### 2. Standalone `/nomik` (No Arguments):
Run the **Rapid 3-Question Intake Wizard**:
1. **The Superpower:** What does the product do in one sentence, and what is its core technical or emotional unfair advantage?
2. **The Tonal Vector:** Who is it for, and what personality should it project? (e.g., Enterprise/Authoritative, Developer/Minimalist, Consumer/Warm, Provocative/Challenger).
3. **Launch & Budget Constraints:** Do you prefer an available action-modifier `.com` (`get{name}.com`), a modern TLD (`.ai`, `.io`, `.app`), or do you have budget for an aftermarket acquisition?

---

## The 6-Step Agency Naming Workflow

### Step 1: Strategic Brief & Category Contrast
Analyze the product, target audience, and competitive landscape:
- **What is the product?** Core superpower, user emotion, technical reality.
- **Who are the category incumbents?** (e.g. In CRM: *Salesforce*, *HubSpot*, *Pipedrive*).
- **What are the category clichés?** (e.g. Enterprise blue, sales-pipe jargon).
- **Where is the Uncontested Quadrant?** Determine the counter-positioning vector (e.g. Warm/Architectural like *Attio* or Human/Conversational like *Folk*).

### Step 2: Generation Across the 7 Agency Taxonomies
Generate names systematically across the 7 proven disciplines (*read `references/naming_taxonomies.md`*):
1. **Neologisms & Coined Morphemes:** (e.g. *Pentium, Sonos, Acura, Spotify, Vercel*)
2. **Real-Word Arbitrary & Transferred:** (e.g. *Apple, Stripe, Slack, Linear, Square, Figma*)
3. **Evocative & Metaphorical:** (e.g. *Amazon, Safari, Swiffer, Patagonia, Oracle*)
4. **High-Impact Compounds:** (e.g. *Superhuman, Masterclass, DoorDash, Palantir*)
5. **Etymological & Classical Roots:** (e.g. *Monzo, Chronos, Meraki, Velo, Kumo*)
6. **Monosyllabic & Compressed:** (e.g. *Stripe, Arc, Loom, Base, Scale, Ramp*)
7. **Provocative & Category-Inverting:** (e.g. *Liquid Death, Oatly, Impossible Foods*)

### Step 3: Linguistic & Phonosemantic Vetting
Run `python scripts/phonetics.py <name>` for each top candidate:
- **Plosives (/b, p, t, d, k, g/):** Deliver certainty, punch, and structural weight.
- **Fricatives (/f, v, s, z/):** Deliver speed, flow, frictionlessness, and modern elegance.
- **Vowel Psychology:** Front vowels (/i, e/) for nimble speed; back vowels (/a, o, u/) for authority and luxury.
- **The Radio Test:** Score must be ≥ 7.5/10. Can a listener spell the name accurately on their first try?
- **Verb Potential:** Can customers say "Let me [brand] this"?
*Read `references/phonosemantics.md`.*

### Step 4: Real-Time ICANN Domain Verification
Execute `python scripts/check_domain.py --brand <name>`:
- Never guess or assume a domain is available.
- Categorize availability:
  - **🟢 AVAILABLE:** Unregistered in registry. Available at standard retail price (~$10-$14/yr for .com, ~$35 for .io, ~$70 for .ai).
  - **🟡 FOR SALE / PARKED:** Resolves to broker lander (Dan, Sedo, Afternic, GoDaddy). Note detected price or negotiation bracket ($1k - $25k+).
  - **⚪ DORMANT / INACTIVE:** Registered in RDAP but has no live web host. Target for private broker outreach.
  - **🔴 TAKEN (LIVE):** Active operational company.
*Read `references/domain_playbook.md`.*

### Step 5: The 7-Pillar Agency Stress-Test Matrix
Grade every shortlisted name across the 7 pillars (1-10 scale):
1. **Category Distinctiveness:** Cuts through category noise instantly.
2. **The Radio Test:** Instant spelling transparency over audio/phone.
3. **Mouthfeel & Prosody:** Trochaic or monosyllabic rhythm, effortless tongue movement.
4. **Brand Elasticity:** Can scale into adjacent products without friction.
5. **Verbification Index:** Natural conversion into an everyday action verb.
6. **Global Cultural Safety:** Clean across Spanish, French, German, Mandarin, Japanese, Arabic (*read `references/cultural_checks.md`*).
7. **Domain & Acquisition Viability:** Viable Day-1 launch path + clear long-term .com strategy.

### Step 6: Executive Presentation & Acquisition Roadmap
Deliver a structured dossier for the founder or executive:
- **The Strategic Angle:** Why this name wins against the competition.
- **Linguistic Scorecard:** Prosody, phonosemantics, Radio Test results.
- **Live Domain Audit & Pricing Table:** Real status, renewal costs, and parking lander links.
- **The Billion-Dollar Launch Roadmap:**
  - *Option A (Lean Launch):* Launch on modern extension (`.ai`, `.io`, `.app`) or action modifier (`get{brand}.com`).
  - *Option B (Growth Upgrade):* Anonymous escrow negotiation playbook for exact `.com` post-funding.

