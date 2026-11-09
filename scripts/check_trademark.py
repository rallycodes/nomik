#!/usr/bin/env python3
"""
Trademark Knockout & Legal Clearance Screener
Author: Raul Aliyev (@rallycodes)
Audits candidate brand names across the Abercrombie Distinctiveness Spectrum,
identifies Nice Classifications (Class 9, Class 42, Class 36), and generates pre-filled
direct clearance query links for USPTO, WIPO, and EUIPO databases.
"""

import sys
import urllib.parse
import json
import argparse
import re

NICE_CLASSES = {
    'software': {'class': 'Class 9', 'desc': 'Computer software, mobile applications, AI algorithms, hardware devices'},
    'saas': {'class': 'Class 42', 'desc': 'Software as a Service (SaaS), cloud infrastructure, API hosting, computer programming'},
    'fintech': {'class': 'Class 36', 'desc': 'Financial services, payment processing, algorithmic trading, banking'},
    'ecommerce': {'class': 'Class 35', 'desc': 'Online marketplaces, retail business management, advertising services'}
}

COMMON_DICTIONARY_WORDS = {
    'fast', 'smart', 'cloud', 'data', 'sync', 'flow', 'task', 'code', 'mail', 'pay',
    'lead', 'work', 'desk', 'app', 'link', 'net', 'base', 'core', 'scale', 'view'
}


def evaluate_distinctiveness(name):
    """
    Grades name on the legal Abercrombie Spectrum of Trademark Distinctiveness:
    Fanciful -> Arbitrary -> Suggestive -> Descriptive -> Generic
    """
    w = name.strip().lower()
    length = len(w)

    # Check if purely descriptive
    if any(cw in w for cw in COMMON_DICTIONARY_WORDS) and ('app' in w or 'soft' in w or 'tool' in w):
        return {
            'level': 'Descriptive (Weak Protection)',
            'grade': 'D',
            'legal_risk': 'HIGH RISK - Descriptive names cannot be registered on the USPTO Principal Register without secondary meaning.',
            'advice': 'Pivot to an arbitrary metaphor or coined neologism.'
        }

    # Check if coined / neologism (not a standard dictionary word)
    if not re.search(r'^(apple|box|stripe|slack|zoom|amazon|square)$', w) and length <= 8:
        return {
            'level': 'Fanciful / Coined Neologism (Supreme Legal Protection)',
            'grade': 'A',
            'legal_risk': 'LOW RISK - Invented words receive the broadest scope of legal trademark protection under Lanham Act § 2.',
            'advice': 'Optimal for global trademark registration across USPTO, EUIPO, and WIPO.'
        }

    # Suggestive / Arbitrary
    return {
        'level': 'Arbitrary / Suggestive (Strong Legal Protection)',
        'grade': 'B',
        'legal_risk': 'MODERATE RISK - Strong inherent distinctiveness, but requires knockout clearance to ensure no incumbent claims prior use.',
        'advice': 'Proceed with knockout search in Nice Classes 9 and 42.'
    }


def generate_trademark_links(name):
    encoded = urllib.parse.quote(name.strip())
    return {
        'uspto_search': f"https://tmsearch.uspto.gov/search/search-results?searchQuery={encoded}",
        'wipo_global_brand': f"https://branddb.wipo.int/en/similarname/search?name={encoded}",
        'euipo_esearch': f"https://euipo.europa.eu/eSearch/#details/trademarks/{encoded}",
        'trademarkia_lookup': f"https://www.trademarkia.com/trademarks-search.aspx?tn={encoded}"
    }


def audit_trademark(name, category="saas"):
    clean_name = name.strip()
    dist = evaluate_distinctiveness(clean_name)
    links = generate_trademark_links(clean_name)

    relevant_classes = [NICE_CLASSES['software'], NICE_CLASSES['saas']]
    if 'fin' in category.lower() or 'pay' in category.lower():
        relevant_classes.append(NICE_CLASSES['fintech'])

    return {
        'brand': clean_name,
        'category': category,
        'distinctiveness': dist,
        'relevant_nice_classes': relevant_classes,
        'clearance_links': links
    }


def print_trademark_report(data):
    name = data['brand']
    dist = data['distinctiveness']
    links = data['clearance_links']

    print("\n" + "=" * 80)
    print(f" TRADEMARK KNOCKOUT & LEGAL SCREENING: '{name.upper()}'")
    print("=" * 80)
    print(f"Distinctiveness Grade : [{dist['grade']}] {dist['level']}")
    print(f"Legal Protection Note : {dist['legal_risk']}")
    print(f"Action Recommendation : {dist['advice']}")
    print("-" * 80)
    print("RELEVANT NICE CLASSIFICATIONS TO CLEAR:")
    for nc in data['relevant_nice_classes']:
        print(f"  • {nc['class']}: {nc['desc']}")
    print("-" * 80)
    print("DIRECT OFFICIAL TRADEMARK CLEARANCE LINKS:")
    print(f"  • USPTO (United States) : {links['uspto_search']}")
    print(f"  • WIPO (Global Brand)   : {links['wipo_global_brand']}")
    print(f"  • EUIPO (Europe)        : {links['euipo_esearch']}")
    print(f"  • Trademarkia (Instant) : {links['trademarkia_lookup']}")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Trademark Knockout & Legal Clearance Screener")
    parser.add_argument("name", help="Candidate brand name to screen (e.g. Kyntic, Nomik)")
    parser.add_argument("--category", default="saas", help="Product category (saas, software, fintech, ecommerce)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    result = audit_trademark(args.name, args.category)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_trademark_report(result)


if __name__ == '__main__':
    main()

