# Domain evidence and pricing

## Scope the lookup

Build domains from the actual candidate and the permitted extensions. If the user allows an exact `.com` or `.app`, a quote on either can qualify. If they require both, verify both. Check extra TLDs or aftermarket options only when useful within the brief. A modified domain can be explored separately if the user explicitly wants alternatives.

Use `python scripts/check_domain.py --list "name.com,name.app" --json` for screening. Inspect the underlying evidence when the result affects the shortlist. DNS, redirects, and parking pages help identify use or a possible sale. Confirm registration status with the authoritative registry's RDAP or another supported registration-data service. [ICANN Lookup](https://lookup.icann.org/en/faq)

## Keep the evidence separate

| Evidence | What to report |
|---|---|
| Authoritative lookup returns a registration record | Registered. Describe active use, parking, or a for-sale listing only if separately observed. |
| Authoritative lookup returns a valid no-record result | No registration record found. Registrar availability and price remain pending until checked. |
| Timeout, rate limit, unsupported lookup, ambiguous response, or inconclusive DNS | Unknown. Retry through a relevant authoritative source if practical. |
| Registrar offers the exact domain for registration | Quote the registrar, link, check date, currency, initial term and total, renewal when shown, and any visible required fees. Mark missing fields as unverified. |
| Registrar lists a premium, reserved, or unavailable name | Record the registrar result. Check another registrar or the registry if sources disagree. Preserve both findings if unresolved. |
| Marketplace or owner explicitly offers the exact domain | Record the asking price or “inquiry only” and the source. Keep acquisition cost separate from recurring costs. |

Use the exact result for the domain. A generic TLD price card, a script's `price_est`, a quote on another extension, or an estimated negotiation range cannot establish an exact price. Compare the initial term and renewal on equivalent terms and flag a discounted first year or a required multi-year purchase. If the user sets a recurring budget and renewal is missing, mark budget fit pending.

For larger lists, screen in batches, then obtain exact quotes for the candidates whose eligibility depends on price. Report each name's evidence tier and the counts checked. Refresh the leader's evidence before presenting a final recommendation if the quotes may be stale.

## Acquisition options

When aftermarket is within scope, compare a listed buy-now price with the user's ceiling. For an inquiry-only or dormant domain, label any acquisition as speculative. If the user wants a negotiation plan, include the cost ceiling, a way to verify ownership and transfer, and escrow or a reputable marketplace for settlement. Get authorization before contacting a seller, placing an offer, or registering a domain.

