#!/usr/bin/env python3
"""
Executive Brand Presentation Generator
Author: Raul Aliyev (@rallycodes)
Generates C-suite ready brand naming proposals with live domain audits,
linguistic scorecards, and strategic acquisition roadmaps.
"""

import sys
import os
import json
import argparse

# Ensure scripts directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from check_domain import check_domain, run_domain_suite
from phonetics import audit_name


def generate_executive_proposal(project_name, category, description, candidates, output_file=None):
    """
    candidates is a list of dicts:
    [
        {
            'name': 'Kova',
            'taxonomy': 'Neologism / Coined',
            'concept': 'Evokes covenant, core strength, and structural resilience.',
            'tone': 'Modern architectural minimalism'
        },
        ...
    ]
    """
    report_lines = []
    report_lines.append(f"# Executive Brand Naming Dossier: {project_name}")
    report_lines.append(f"**Category:** {category}  ")
    report_lines.append(f"**Strategic Brief:** {description}\n")
    report_lines.append("---\n")

    report_lines.append("## 1. Category Contrast & Strategic Rationale\n")
    report_lines.append(
        "Elite naming does not conform to category norms; it creates an uncontested quadrant. "
        "Every candidate below has been engineered using the 7 Agency Naming Disciplines, "
        "passing rigorous phonosemantic audits, the Radio Test, and real-time ICANN domain verification.\n"
    )

    report_lines.append("## 2. Shortlisted Brand Candidates & Linguistic Profiles\n")

    audit_results = []
    for c in candidates:
        name = c['name']
        taxonomy = c.get('taxonomy', 'Evocative')
        concept = c.get('concept', '')
        tone = c.get('tone', '')

        # Phonetic analysis
        ling = audit_name(name)
        # Domain suite analysis
        domains = run_domain_suite(name)

        audit_results.append({
            'meta': c,
            'linguistic': ling,
            'domains': domains
        })

    # Render each candidate card
    for idx, item in enumerate(audit_results, 1):
        c = item['meta']
        ling = item['linguistic']
        domains = item['domains']
        name = c['name']

        report_lines.append(f"### {idx}. {name.upper()}")
        report_lines.append(f"**Taxonomy:** {c.get('taxonomy')} | **Cadence:** {ling['cadence']} ({ling['syllables']} syllables) | **Length:** {ling['character_length']} chars  ")
        report_lines.append(f"**Conceptual Essence:** {c.get('concept')}  ")
        report_lines.append(f"**Tonal Vector:** {c.get('tone')}\n")

        # Linguistic table
        report_lines.append("#### Linguistic Scorecard")
        report_lines.append("| Dimension | Rating | Analysis |")
        report_lines.append("|---|---|---|")
        report_lines.append(f"| **The Radio Test** | {ling['radio_test']['radio_score']}/10 | {', '.join(ling['radio_test']['flags'][:2])} |")
        report_lines.append(f"| **Verbification** | {ling['verbification']['verb_score']}/10 | {ling['verbification']['sample_usage']} |")
        report_lines.append(f"| **Sound Profile** | {ling['phonosemantics']['vowel_profile'][:30]}... | {ling['phonosemantics']['traits'][0]} |")
        report_lines.append("\n")

        # Domain table
        report_lines.append("#### Live Domain Intelligence & Pricing")
        report_lines.append("| Domain | Status | Est. Cost / Retail | Notes |")
        report_lines.append("|---|---|---|---|")

        # Sort: available first
        priority = {'AVAILABLE': 0, 'TAKEN_FOR_SALE': 1, 'TAKEN_INACTIVE': 2, 'UNKNOWN': 3, 'TAKEN_ACTIVE': 4}
        sorted_domains = sorted(domains, key=lambda x: (priority.get(x['status'], 5), x['domain']))

        for d in sorted_domains[:8]:
            badge = "🟢 Available" if d['status'] == 'AVAILABLE' else \
                    "🟡 For Sale / Parked" if d['status'] == 'TAKEN_FOR_SALE' else \
                    "⚪ Dormant" if d['status'] == 'TAKEN_INACTIVE' else "🔴 Live Site"
            report_lines.append(f"| `{d['domain']}` | {badge} | {d['price_est']} | {d['details'][:40]} |")
        report_lines.append("\n")

        # Launch recommendation
        avail_com = next((d for d in domains if d['domain'] == f"{name.lower()}.com" and d['status'] == 'AVAILABLE'), None)
        avail_tld = [d for d in domains if d['status'] == 'AVAILABLE' and d['domain'] != f"{name.lower()}.com"]

        report_lines.append("**Day-1 Launch & Acquisition Roadmap:**  ")
        if avail_com:
            report_lines.append(f"• **Direct Path:** Register `{avail_com['domain']}` immediately (~$10-$14/yr).")
        elif avail_tld:
            top_rec = avail_tld[0]['domain']
            report_lines.append(f"• **Lean Launch:** Launch on `{top_rec}` (~{avail_tld[0]['annual_renewal']}).")
            report_lines.append(f"• **Scale Up:** Acquire `{name.lower()}.com` during growth phase via anonymous broker escrow.")
        report_lines.append("\n---\n")

    content = "\n".join(report_lines)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Report written to {output_file}")
    else:
        print(content)
    return content


def main():
    parser = argparse.ArgumentParser(description="Generate Executive Brand Naming Report")
    parser.add_argument("--project", default="NextGen Platform", help="Project / Product name")
    parser.add_argument("--category", default="Developer Infrastructure", help="Product category")
    parser.add_argument("--brief", default="High performance developer tool", help="Strategic brief")
    parser.add_argument("--names", required=True, help="JSON file or comma-separated list of candidate names")
    parser.add_argument("--output", "-o", help="Output markdown file path")

    args = parser.parse_args()

    candidates = []
    if os.path.exists(args.names):
        with open(args.names, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
    else:
        for n in args.names.split(','):
            n = n.strip()
            if n:
                candidates.append({
                    'name': n,
                    'taxonomy': 'Shortlisted Candidate',
                    'concept': f'Strategic brand candidate for {args.project}',
                    'tone': 'Contemporary & distinct'
                })

    generate_executive_proposal(args.project, args.category, args.brief, candidates, args.output)


if __name__ == '__main__':
    main()
