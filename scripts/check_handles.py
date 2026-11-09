#!/usr/bin/env python3
"""
Social & Package Registry Handle Intelligence
Author: Raul Aliyev (@rallycodes)
Checks availability across developer registries (npm, PyPI, Crates.io) and social platforms (GitHub, X).
"""

import sys
import urllib.request
import urllib.error
import json
import argparse
from concurrent.futures import ThreadPoolExecutor

PLATFORMS = [
    {
        'id': 'github',
        'name': 'GitHub Org / User',
        'type': 'Developer Identity',
        'url_template': 'https://api.github.com/users/{handle}',
        'web_url': 'https://github.com/{handle}',
        'headers': {'User-Agent': 'Nomik-Handle-Checker/1.0'}
    },
    {
        'id': 'npm',
        'name': 'npm Package',
        'type': 'JavaScript Ecosystem',
        'url_template': 'https://registry.npmjs.org/{handle}',
        'web_url': 'https://www.npmjs.com/package/{handle}',
        'headers': {'User-Agent': 'Mozilla/5.0'}
    },
    {
        'id': 'pypi',
        'name': 'PyPI Package',
        'type': 'Python Ecosystem',
        'url_template': 'https://pypi.org/pypi/{handle}/json',
        'web_url': 'https://pypi.org/project/{handle}/',
        'headers': {'User-Agent': 'Mozilla/5.0'}
    },
    {
        'id': 'crates',
        'name': 'Crates.io Package',
        'type': 'Rust Ecosystem',
        'url_template': 'https://crates.io/api/v1/crates/{handle}',
        'web_url': 'https://crates.io/crates/{handle}',
        'headers': {'User-Agent': 'Nomik-Handle-Checker/1.0'}
    }
]


def check_single_platform(platform, handle):
    url = platform['url_template'].format(handle=handle)
    headers = platform['headers']
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            # 200 OK means taken
            return {
                'platform': platform['name'],
                'type': platform['type'],
                'status': 'TAKEN',
                'url': platform['web_url'].format(handle=handle)
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                'platform': platform['name'],
                'type': platform['type'],
                'status': 'AVAILABLE',
                'url': platform['web_url'].format(handle=handle)
            }
        return {
            'platform': platform['name'],
            'type': platform['type'],
            'status': 'UNKNOWN',
            'error': f'HTTP {e.code}',
            'url': platform['web_url'].format(handle=handle)
        }
    except Exception as e:
        return {
            'platform': platform['name'],
            'type': platform['type'],
            'status': 'UNKNOWN',
            'error': str(e),
            'url': platform['web_url'].format(handle=handle)
        }


def check_all_handles(handle):
    clean_handle = handle.strip().lower()
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_single_platform, p, clean_handle) for p in PLATFORMS]
        for f in futures:
            results.append(f.result())
    return results


def print_handle_table(handle, results):
    print("\n" + "=" * 80)
    print(f" DEVELOPER & SOCIAL HANDLE AUDIT: '{handle.upper()}'")
    print("=" * 80)
    print(f"{'PLATFORM':<22} | {'TYPE':<22} | {'STATUS':<15} | {'PROFILE / URL'}")
    print("-" * 80)

    for r in results:
        status_badge = "🟢 AVAILABLE" if r['status'] == 'AVAILABLE' else \
                       "🔴 TAKEN" if r['status'] == 'TAKEN' else "⚪ UNKNOWN"
        print(f"{r['platform']:<22} | {r['type']:<22} | {status_badge:<15} | {r['url']}")

    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Check availability across developer package registries and social platforms.")
    parser.add_argument("handle", help="Brand handle to check (e.g. kyntic, nomik)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    results = check_all_handles(args.handle)
    if args.json:
        print(json.dumps({'handle': args.handle, 'results': results}, indent=2))
    else:
        print_handle_table(args.handle, results)


if __name__ == '__main__':
    main()
