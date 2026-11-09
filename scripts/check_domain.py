#!/usr/bin/env python3
"""
Domain Intelligence & Availability Checker
Author: Raul Aliyev (@rallycodes)
High-performance, multi-threaded domain verification engine for brand naming.
Checks exact registration status, active DNS, parking landers, and real pricing.
"""

import sys
import socket
import urllib.request
import urllib.error
import json
import re
import argparse
from concurrent.futures import ThreadPoolExecutor

REGISTRY_PRICING = {
    'com': {'retail_min': 10, 'retail_max': 14, 'currency': 'USD', 'category': 'Tier-1 Legacy gTLD (Global Standard)'},
    'ai': {'retail_min': 65, 'retail_max': 85, 'currency': 'USD', 'category': 'Frontier Tech ccTLD (Anguilla)'},
    'io': {'retail_min': 35, 'retail_max': 48, 'currency': 'USD', 'category': 'Developer / SaaS ccTLD (IO)'},
    'co': {'retail_min': 25, 'retail_max': 35, 'currency': 'USD', 'category': 'Modern Startup ccTLD (Colombia)'},
    'app': {'retail_min': 14, 'retail_max': 18, 'currency': 'USD', 'category': 'Google HSTS Secure gTLD'},
    'dev': {'retail_min': 14, 'retail_max': 18, 'currency': 'USD', 'category': 'Google Developer Secure gTLD'},
    'so': {'retail_min': 28, 'retail_max': 38, 'currency': 'USD', 'category': 'Clean Modern ccTLD (Somalia)'},
    'xyz': {'retail_min': 10, 'retail_max': 15, 'currency': 'USD', 'category': 'Modern / Web3 gTLD'},
    'org': {'retail_min': 11, 'retail_max': 16, 'currency': 'USD', 'category': 'Institutional / Open Source gTLD'},
    'net': {'retail_min': 12, 'retail_max': 17, 'currency': 'USD', 'category': 'Infrastructure gTLD'},
    'tech': {'retail_min': 20, 'retail_max': 32, 'currency': 'USD', 'category': 'Tech gTLD'},
    'design': {'retail_min': 35, 'retail_max': 50, 'currency': 'USD', 'category': 'Creative gTLD'},
    'studio': {'retail_min': 25, 'retail_max': 38, 'currency': 'USD', 'category': 'Creative Studio gTLD'},
    'me': {'retail_min': 15, 'retail_max': 22, 'currency': 'USD', 'category': 'Personal / Brand ccTLD'},
    'pro': {'retail_min': 16, 'retail_max': 25, 'currency': 'USD', 'category': 'Professional gTLD'},
}

DEFAULT_TLDS = ['com', 'ai', 'io', 'co', 'app', 'dev', 'so']
DEFAULT_ACTION_MODIFIERS = ['get', 'use', 'try']
DEFAULT_ENTITY_MODIFIERS = ['hq', 'app', 'labs']

FOR_SALE_SIGNALS = [
    'buy this domain', 'domain is for sale', 'this domain is available for sale',
    'dan.com', 'sedo.com', 'afternic.com', 'squadhelp.com', 'atom.com',
    'hugedomains.com', 'brandbucket.com', 'godaddy domain broker',
    'inquire about this domain', 'make an offer on this domain', 'domain broker service'
]


def inspect_web_lander(domain, timeout=3.5):
    """Probes the domain via HTTP/HTTPS to detect live sites vs parking/for-sale landers."""
    url = f"http://{domain}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_html = resp.read(15000).decode('utf-8', errors='ignore')
            title = ""
            m = re.search(r'<title[^>]*>(.*?)</title>', raw_html, re.IGNORECASE | re.DOTALL)
            if m:
                title = re.sub(r'\s+', ' ', m.group(1)).strip()
            
            lower_html = raw_html.lower()
            is_for_sale = any(signal in lower_html for signal in FOR_SALE_SIGNALS)
            
            # Detect listed price if present (e.g. $2,499 or $15,000)
            price_match = re.search(r'\$\s?([0-9]{1,3}(?:,[0-9]{3})+|\b[0-9]{3,6}\b)', raw_html)
            detected_price = price_match.group(0) if (price_match and is_for_sale) else None

            return {
                'live_http': True,
                'title': title[:90] if title else 'Live Web Host',
                'is_for_sale': is_for_sale,
                'detected_price': detected_price
            }
    except Exception:
        return {'live_http': False, 'title': '', 'is_for_sale': False, 'detected_price': None}


def query_whois_socket(domain, tld):
    """Direct Port-43 authoritative WHOIS fallback for specific registries."""
    servers = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'io': 'whois.nic.io',
        'ai': 'whois.nic.ai',
        'co': 'whois.nic.co'
    }
    server = servers.get(tld)
    if not server:
        return None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.5)
        s.connect((server, 43))
        s.send((domain + '\r\n').encode('utf-8'))
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
        text = response.decode('utf-8', errors='ignore')
        lower_text = text.lower()
        if 'no match for' in lower_text or 'not found' in lower_text or 'domain not found' in lower_text:
            return {'registered': False}
        if 'domain name:' in lower_text or 'registry domain id:' in lower_text or 'creation date:' in lower_text:
            return {'registered': True, 'raw': text[:200]}
    except Exception:
        pass
    return None


def query_rdap(domain):
    """Official ICANN Registration Data Access Protocol query."""
    url = f"https://rdap.org/domain/{domain}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RDAP-Domain-Checker/1.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            registrar = data.get('port43', 'Registered Entity')
            status_list = data.get('status', [])
            return {'status_code': 200, 'registered': True, 'registrar': registrar, 'status': status_list}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'status_code': 404, 'registered': False}
        return {'status_code': e.code, 'error': f'HTTP_{e.code}'}
    except Exception as e:
        return {'status_code': 0, 'error': str(e)}


def check_domain(domain):
    """
    Complete 3-tier domain verification:
    1. Socket DNS resolution (Instant A/AAAA lookup)
    2. RDAP & Authoritative Registry WHOIS
    3. HTTP/Lander Inspection for live sites vs aftermarket parking
    """
    domain = domain.strip().lower()
    parts = domain.split('.')
    tld = parts[-1] if len(parts) > 1 else 'com'
    pricing = REGISTRY_PRICING.get(tld, {'retail_min': 15, 'retail_max': 30, 'currency': 'USD', 'category': 'Generic TLD'})

    # Tier 1: Socket DNS
    has_active_dns = False
    ips = []
    try:
        addrs = socket.getaddrinfo(domain, 80)
        ips = list(set([a[4][0] for a in addrs]))
        has_active_dns = True
    except socket.gaierror:
        has_active_dns = False

    # If DNS resolves, check if it's an active business or a for-sale parking lander
    if has_active_dns:
        lander = inspect_web_lander(domain)
        if lander['is_for_sale']:
            price_str = f"Listed at {lander['detected_price']}" if lander['detected_price'] else "Aftermarket negotiation ($1k - $25k+)"
            return {
                'domain': domain,
                'status': 'TAKEN_FOR_SALE',
                'summary': 'Parked / Listed for sale',
                'price_est': price_str,
                'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr renewal",
                'details': f"Lander: {lander['title']}",
                'tld_info': pricing
            }
        else:
            return {
                'domain': domain,
                'status': 'TAKEN_ACTIVE',
                'summary': 'Active operational site',
                'price_est': 'Not for sale (Active business)',
                'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr renewal",
                'details': f"{lander['title']} (Resolves to {ips[0] if ips else 'IP'})",
                'tld_info': pricing
            }

    # Tier 2: Check authoritative registry (RDAP & Port-43 WHOIS)
    rdap = query_rdap(domain)
    if rdap.get('status_code') == 404:
        return {
            'domain': domain,
            'status': 'AVAILABLE',
            'summary': 'Available for immediate registration',
            'price_est': f"Standard Retail: ${pricing['retail_min']} - ${pricing['retail_max']}/yr",
            'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr",
            'details': 'Unregistered across ICANN registry',
            'tld_info': pricing
        }
    elif rdap.get('status_code') == 200:
        return {
            'domain': domain,
            'status': 'TAKEN_INACTIVE',
            'summary': 'Registered (Dormant / No Web Host)',
            'price_est': 'Private inquiry / Broker acquisition candidate',
            'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr renewal",
            'details': f"Registrar: {rdap.get('registrar', 'Active Registry Record')}",
            'tld_info': pricing
        }

    # Fallback to direct WHOIS socket for edge cases
    whois = query_whois_socket(domain, tld)
    if whois:
        if not whois['registered']:
            return {
                'domain': domain,
                'status': 'AVAILABLE',
                'summary': 'Available for immediate registration',
                'price_est': f"Standard Retail: ${pricing['retail_min']} - ${pricing['retail_max']}/yr",
                'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr",
                'details': 'Registry reports available',
                'tld_info': pricing
            }
        else:
            return {
                'domain': domain,
                'status': 'TAKEN_INACTIVE',
                'summary': 'Registered (Dormant)',
                'price_est': 'Private acquisition candidate',
                'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr renewal",
                'details': 'Authoritative registry record exists',
                'tld_info': pricing
            }

    # If inconclusive
    return {
        'domain': domain,
        'status': 'UNKNOWN',
        'summary': 'Registry lookup inconclusive',
        'price_est': f"Standard retail ~${pricing['retail_min']}-${pricing['retail_max']}/yr if open",
        'annual_renewal': f"~${pricing['retail_min']}-${pricing['retail_max']}/yr",
        'details': 'Verify directly on Cloudflare, Porkbun, or Namecheap',
        'tld_info': pricing
    }


def generate_candidate_domains(brand_name):
    """Generates the strategic domain suite according to the startup playbook."""
    slug = re.sub(r'[^a-zA-Z0-9-]', '', brand_name.lower())
    suite = []

    # 1. Exact match TLDs
    for tld in DEFAULT_TLDS:
        suite.append({'domain': f"{slug}.{tld}", 'tier': 'Exact Match', 'type': f".{tld}"})

    # 2. Action verbs (.com)
    for verb in DEFAULT_ACTION_MODIFIERS:
        suite.append({'domain': f"{verb}{slug}.com", 'tier': 'Action Modifier', 'type': f"{verb}{slug}.com"})

    # 3. Entity / Product anchors (.com)
    for entity in DEFAULT_ENTITY_MODIFIERS:
        suite.append({'domain': f"{slug}{entity}.com", 'tier': 'Entity Modifier', 'type': f"{slug}{entity}.com"})

    return suite


def run_domain_suite(brand_name, max_workers=8):
    """Checks all standard brand variations in parallel."""
    candidates = generate_candidate_domains(brand_name)
    domains_to_check = [c['domain'] for c in candidates]
    domain_tier_map = {c['domain']: c['tier'] for c in candidates}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(check_domain, domains_to_check))

    for r in results:
        r['tier'] = domain_tier_map.get(r['domain'], 'Candidate')

    return results


def print_suite_table(brand_name, results):
    """Renders a polished, terminal table of results."""
    print("\n" + "=" * 90)
    print(f" DOMAIN INTELLIGENCE AUDIT: '{brand_name.upper()}'")
    print("=" * 90)
    print(f"{'DOMAIN':<22} | {'STATUS':<15} | {'ESTIMATED COST / PRICING':<32} | {'DETAILS'}")
    print("-" * 90)

    # Sort: AVAILABLE first, then TAKEN_FOR_SALE, then TAKEN_INACTIVE, then TAKEN_ACTIVE
    priority = {'AVAILABLE': 0, 'TAKEN_FOR_SALE': 1, 'TAKEN_INACTIVE': 2, 'UNKNOWN': 3, 'TAKEN_ACTIVE': 4}
    sorted_results = sorted(results, key=lambda x: (priority.get(x['status'], 5), x['domain']))

    for r in sorted_results:
        status_display = r['status']
        if r['status'] == 'AVAILABLE':
            status_display = "🟢 AVAILABLE"
        elif r['status'] == 'TAKEN_FOR_SALE':
            status_display = "🟡 FOR SALE"
        elif r['status'] == 'TAKEN_INACTIVE':
            status_display = "⚪ DORMANT"
        elif r['status'] == 'TAKEN_ACTIVE':
            status_display = "🔴 TAKEN (LIVE)"

        print(f"{r['domain']:<22} | {status_display:<15} | {r['price_est']:<32} | {r['details'][:45]}")

    print("=" * 90)
    
    # Strategic recommendation
    exact_com = next((r for r in results if r['domain'] == f"{brand_name.lower()}.com"), None)
    ai_tld = next((r for r in results if r['domain'] == f"{brand_name.lower()}.ai"), None)
    io_tld = next((r for r in results if r['domain'] == f"{brand_name.lower()}.io"), None)
    app_tld = next((r for r in results if r['domain'] == f"{brand_name.lower()}.app"), None)
    avail_modifiers = [r['domain'] for r in results if r['status'] == 'AVAILABLE' and r['tier'] in ('Action Modifier', 'Entity Modifier')]

    print("\nSTRATEGIC DOMAIN RECOMMENDATION:")
    if exact_com and exact_com['status'] == 'AVAILABLE':
        print(f"★ UNICORN SCENARIO: Exact-match '{exact_com['domain']}' is UNREGISTERED!")
        print(f"  Register immediately on Cloudflare or Porkbun for standard retail (~$10-$14/yr).")
    elif exact_com and exact_com['status'] == 'TAKEN_FOR_SALE':
        print(f"◆ ACQUISITION TARGET: '{exact_com['domain']}' is parked for sale.")
        print(f"  Action plan: Launch on a modern extension or modifier, then acquire exact .com via anonymous escrow broker.")
        if avail_modifiers:
            print(f"  Recommended launch domains: {', '.join(avail_modifiers[:3])}")
    else:
        print(f"▲ STANDARD HIGH-GROWTH PLAYBOOK: Exact .com is actively taken.")
        recommendations = []
        if ai_tld and ai_tld['status'] == 'AVAILABLE':
            recommendations.append(f"{ai_tld['domain']} (AI/Tech frontier)")
        if io_tld and io_tld['status'] == 'AVAILABLE':
            recommendations.append(f"{io_tld['domain']} (Developer/SaaS)")
        if app_tld and app_tld['status'] == 'AVAILABLE':
            recommendations.append(f"{app_tld['domain']} (App/Web platform)")
        if avail_modifiers:
            recommendations.append(f"{avail_modifiers[0]} (Direct action .com)")
        
        if recommendations:
            print(f"  Recommended Day-1 Launch paths: {', '.join(recommendations)}")
        print(f"  Historical precedents: Dropbox launched on 'getdropbox.com', Linear on 'linear.app', Notion on 'notion.so'.")
    print("=" * 90 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Agency-Grade Domain Intelligence & Availability Checker")
    parser.add_argument("domain", nargs="?", help="Specific domain name to check (e.g. stripe.com)")
    parser.add_argument("--brand", "-b", help="Check the entire strategic domain suite for a brand name (e.g. zenith)")
    parser.add_argument("--list", "-l", help="Comma-separated list of domains to check")
    parser.add_argument("--json", "-j", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.brand:
        results = run_domain_suite(args.brand)
        if args.json:
            print(json.dumps({'brand': args.brand, 'results': results}, indent=2))
        else:
            print_suite_table(args.brand, results)
    elif args.list:
        domains = [d.strip() for d in args.list.split(',') if d.strip()]
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(check_domain, domains))
        if args.json:
            print(json.dumps({'results': results}, indent=2))
        else:
            print_suite_table("Domain Batch", results)
    elif args.domain:
        result = check_domain(args.domain)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_suite_table(args.domain, [result])
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

