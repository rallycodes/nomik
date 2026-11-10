---
name: nomik
description: Generate, shortlist, or audit brand names for companies, products, apps, platforms, and features. Use for naming and renaming, single-word or coined names, exact-domain availability and pricing, and preliminary checks for pronunciation, search confusion, and trademark conflicts.
license: MIT
metadata:
  author: Raul Aliyev (@rallycodes)
---

# Nomik · Brand Naming and Domain Intelligence

## 1. Lock the brief

For a product that already exists, start with the current product brief, primary user journeys, and real UI copy or screenshots when available. Identify who uses it, what they accomplish, and why they return. Separate today's workflow from the expansion the user intends. For an umbrella brand, test the name with future audiences and repeat-use cases alongside the current use case. For example, a job-search name might describe a candidate well while feeling awkward on a profile someone keeps while employed.

Carry forward explicit constraints and corrections between rounds. Record the intended name structure, immediate category cue, future scope, priority markets and languages, count, permitted exact TLDs, and price ceiling. If the user says “cheap” without a ceiling, state a working assumption and show actual costs. Ask only when a missing answer would materially change the work.

For a bare `/nomik` with no existing brief, ask what the product does, who it serves and how it should feel, and which exact TLDs and budget the user wants. With a product or idea, start from the brief. With a specific name or domain, go straight to the relevant checks. A domain-only request needs domain evidence. A brand audit also needs product fit and collision checks.

## 2. Generate within the brief

- Treat “one word” as a structural constraint. Use an existing standalone word or a meaningful coinage derived from one identifiable root. A coined name should have a defensible derivation and a plausible pronunciation. Joined words, shortened blends of independent words, and spaced phrases fail a strict one-word brief even if the domain has no spaces. Use compounds only when the brief allows them.
- Generate across several relevant naming territories and filter before external lookups. When immediate recognition matters, test the category cue before revealing the backstory. An attractive metaphor that needs a paragraph to explain its relevance is a weak fit for that brief.
- Use [naming taxonomies](references/naming_taxonomies.md) to widen the search within the brief. Use [taste filters](references/anti_slop_rules.md) to reject generic tech mashups, trendy suffix stuffing, empty abstractions, awkward synthetic spellings, and bland feature labels.
- Honor the requested count. Generate a larger internal pool to replace candidates that fail the constraints. For “add N and rank them all,” carry forward the requested earlier candidates, deduplicate, add N genuinely new names, and assess everyone on the same criteria. If the evidence supports fewer candidates than requested, give the actual coverage and label any provisional entries separately.

## 3. Verify exact domains and prices

Use [domain evidence and pricing](references/domain_playbook.md). Scope the checks to the exact TLDs and budget the user allowed. For a strict `.com` or `.app` brief, a different extension or a modifier like `get` or `hq` fails the requirement. An explicit budget is a gate when the price is known. Mark missing evidence as pending.

Keep registry status, registrar availability, and exact price separate. A registry response with no record does not establish that the name is purchasable or inexpensive. A confirmed quote identifies the exact domain, registrar, currency, initial term and price, and renewal price when shown. Give the check date and source. Keep promotional, premium, and aftermarket prices distinct.

## 4. Test product fit, language, and findability

Use [product and collision audit](references/product-and-collision-audit.md) for serious shortlists, rankings, or brand audits.

- Test the name in real UI copy and short spoken phrases for both current and future use. Check unprompted category recognition separately from the brand's ability to grow. Where the product can be rendered, inspect the most space-constrained surfaces. Label copy-only checks and proposed UI separately from a rendered check.
- Use phonetic scores for triage. Search likely pronunciations, heard spellings, and common typos. Actual search collisions and listener results outweigh the automated score. Distinguish a desk-based spelling simulation from a test with listeners.
- Screen relevant languages and markets. Report which were checked and where native-speaker input would affect the decision. Use [cultural checks](references/cultural_checks.md) and [phonosemantics](references/phonosemantics.md) as starting points.
- Assess branded search findability separately from generic category SEO. Search exact and likely heard forms and inspect the businesses that appear. Generic demand belongs in useful product and category pages.

## 5. Screen for conflicts

Check the exact name and plausible look-alikes and sound-alikes in the market and in relevant official trademark registers. Read any material record for status, jurisdiction, owner, and goods or services. Compare actual business activity, audiences, and channels. An open exact domain and an empty exact-match search can coexist with a serious near-name conflict.

Record observed facts and their implications separately. Use “hold” when material overlap or incomplete evidence makes a recommendation premature. Use “eliminate” for a clear brief failure or a collision serious enough to remove the candidate, and give the reason. Describe trademark findings as preliminary screening and state the market or register coverage. Reserve formal clearance for the appropriate review.

## 6. Deliver a decision

For a deep audit, give each requested candidate a concrete strength, a drawback, evidence, and a disposition. Apply hard constraints before ranking eligible candidates. Then compare category recognition, future scope, spelling and pronunciation, UI fit, branded findability, and domain cost according to the brief. A high average cannot offset a hard constraint or a material unresolved conflict.

Pick a leader if the evidence supports one. Explain the decisive trade-off against the nearest alternatives and when each alternative would be better. Label a conditional pick and state what would resolve the condition. For a long list, give concise reasons for every disposition and go deeper on contenders and material conflicts. If checks were partial, say how many were screened, registry-checked, and quoted at an exact price.

## Bundled tools

Run paths relative to this skill directory. Treat script outputs as inputs to the audit.

| Tool | Use |
|---|---|
| `python scripts/check_domain.py --list "name.com,name.app" --json` | Screen the exact domains the brief allows. `--brand <name>` explores a broader suite. The script's price fields are estimates or indicative ranges, and its `AVAILABLE` label needs registrar confirmation. |
| `python scripts/filter_candidates.py --names "<name1,name2>" --json` | Optional bulk screen across its default TLDs. Use exact lookups for a custom TLD set. Review underlying results rather than adopting its aggregate verdict. |
| `python scripts/phonetics.py <name> --json` | Estimate cadence, spelling friction, and visual rhythm. A passing score is a heuristic. |
| `python scripts/check_trademark.py <name> --category <category>` | Get distinctiveness notes and starting links for official searches. Inspect the records yourself. |
| `python scripts/check_handles.py <handle>` | Check developer handles when they matter to the brief. |
| `python scripts/generate_report.py --project "<project>" --category "<category>" --brief "<brief>" --names "<name1,name2>"` | Draft a report if requested. Reconcile its labels, estimates, and recommendations against your evidence before delivery. |
