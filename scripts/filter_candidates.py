#!/usr/bin/env python3
"""
Candidate Name Pre-Verification Engine
Author: Raul Aliyev (@rallycodes)
Audits multiple brand name candidates in parallel against exact-match domains (.com, .ai, .io, .app).
Filters out dead/taken names so only viable, high-taste finalists are presented to founders.
"""

import sys
import os
import argparse
import json
from concurrent.futures import ThreadPoolExecutor

# Import check_domain from local directory
sys.path.insert(0, os.path.dirname(__file__))
from check_domain import check_domain

def evaluate_candidate(name):
    name = name.strip().lower()
    if not name:
        return None

    # Check the 4 most critical startup extensions
    core_domains = [f"{name}.com", f"{name}.ai", f"{name}.io", f"{name}.app"]
    
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(check_domain, core_domains))

    domain_map = {r['domain']: r for r in results}

    com_res = domain_map.get(f"{name}.com", {})
    ai_res = domain_map.get(f"{name}.ai", {})
    io_res = domain_map.get(f"{name}.io", {})
    app_res = domain_map.get(f"{name}.app", {})

    com_status = com_res.get('status', 'UNKNOWN')
    ai_status = ai_res.get('status', 'UNKNOWN')
    io_status = io_res.get('status', 'UNKNOWN')
    app_status = app_res.get('status', 'UNKNOWN')

    # Determine viability tier
    is_com_available = com_status == 'AVAILABLE'
    is_com_for_sale = com_status == 'TAKEN_FOR_SALE'
    is_ai_available = ai_status == 'AVAILABLE'
    is_io_available = io_status == 'AVAILABLE'
    is_app_available = app_status == 'AVAILABLE'

    available_clean_tlds = []
    if is_com_available: available_clean_tlds.append('.com')
    if is_ai_available: available_clean_tlds.append('.ai')
    if is_io_available: available_clean_tlds.append('.io')
    if is_app_available: available_clean_tlds.append('.app')

    if is_com_available:
        tier = 'TIER_1_UNICORN'
        verdict = f"★ UNICORN: Exact '{name}.com' is 100% AVAILABLE!"
        passed = True
    elif is_com_for_sale:
        tier = 'TIER_2_BUYABLE_COM'
        verdict = f"◆ BUYABLE .COM: '{name}.com' is parked for sale ({com_res.get('price_est', 'negotiable')}). Clean open: {', '.join(available_clean_tlds) or 'none'}"
        passed = True
    elif available_clean_tlds:
        tier = 'TIER_3_CLEAN_MODERN'
        verdict = f"▲ CLEAN MODERN TLD: Open on {', '.join(available_clean_tlds)}. (.com is {com_res.get('summary', 'taken')})"
        passed = True
    else:
        tier = 'DISQUALIFIED'
        verdict = f"❌ DEAD: All primary extensions (.com, .ai, .io, .app) are registered/taken."
        passed = False

    return {
        'name': name,
        'passed': passed,
        'tier': tier,
        'verdict': verdict,
        'available_tlds': available_clean_tlds,
        'com': com_res,
        'ai': ai_res,
        'io': io_res,
        'app': app_res
    }


def filter_candidate_names(names, max_workers=6):
    clean_names = [n.strip() for n in names if n.strip()]
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(evaluate_candidate, clean_names))
    
    # Sort: Tier 1 first, then Tier 2, then Tier 3, then Disqualified
    tier_weight = {'TIER_1_UNICORN': 0, 'TIER_2_BUYABLE_COM': 1, 'TIER_3_CLEAN_MODERN': 2, 'DISQUALIFIED': 3}
    return sorted([r for r in results if r], key=lambda x: tier_weight.get(x['tier'], 99))


def print_candidate_report(results):
    passed = [r for r in results if r['passed']]
    failed = [r for r in results if not r['passed']]

    print("\n" + "=" * 80)
    print(" NOMIK CANDIDATE PRE-VERIFICATION AUDIT")
    print("=" * 80)
    
    if passed:
        print(f"\n[✓] VIABLE FINALISTS ({len(passed)} approved):")
        print("-" * 80)
        for r in passed:
            print(f"  • {r['name'].upper():<14} | {r['tier']:<20} | {r['verdict']}")
            clean_str = ", ".join([f"{r['name']}{tld}" for tld in r['available_tlds']]) or "None"
            print(f"    Available Clean Domains: {clean_str}")
    else:
        print("\n[!] ZERO CANDIDATES PASSED. All names had taken .com, .ai, and .io domains.")

    if failed:
        print(f"\n[✗] DISQUALIFIED CANDIDATES ({len(failed)} discarded):")
        print("-" * 80)
        for r in failed:
            print(f"  • {r['name'].upper():<14} | {r['verdict']}")

    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Audit and filter candidate brand names by domain viability")
    parser.add_argument("--names", "-n", required=True, help="Comma-separated candidate names to vet (e.g. 'linear,attio,nomik,kyntic')")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    names = [n.strip() for n in args.names.split(',') if n.strip()]

    results = filter_candidate_names(names)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_candidate_report(results)


if __name__ == '__main__':
    main()
