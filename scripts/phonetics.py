#!/usr/bin/env python3
"""
Linguistic & Phonosemantic Scoring Engine
Author: Raul Aliyev (@rallycodes)
Agency-grade phonetics, sound symbolism, prosody, and Radio Test auditor.
Encodes the sound symbolism methodology pioneered by Lexicon Branding and cognitive linguistics.
"""

import sys
import re
import argparse
import json

PLOSIVES = {'b', 'p', 't', 'd', 'k', 'g', 'c', 'q'}
FRICATIVES = {'f', 'v', 's', 'z', 'h'}
FRICATIVE_DIGRAPHS = ['th', 'sh', 'ch', 'ph']
LIQUIDS_NASALS = {'l', 'r', 'm', 'n', 'w', 'y'}

FRONT_VOWELS = {'i', 'e'}
BACK_VOWELS = {'a', 'o', 'u'}
VOWELS = {'a', 'e', 'i', 'o', 'u', 'y'}

CONFUSING_CLUSTERS = [
    'ght', 'phth', 'sch', 'mn', 'ps', 'pn', 'gn', 'kn', 'wr',
    'xth', 'ckr', 'blr', 'ttr', 'zzl'
]

AMBIGUOUS_SPELLINGS = [
    ('c', 'Can be confused with K or S when heard'),
    ('ph', 'Often misspelled as F'),
    ('x', 'Can be heard as Z or KS'),
    ('q', 'Requires U; often misspelled'),
]


def estimate_syllables(word):
    """Accurately calculates English syllable count using phonological heuristics."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1

    # Remove silent e at the end
    cleaned = re.sub(r'e$', '', word)
    # Count vowel groups
    matches = re.findall(r'[aeiouy]+', cleaned)
    count = len(matches)

    # Adjust for words ending in -le preceded by a consonant
    if re.search(r'[^aeiouy]le$', word):
        count += 1

    # Adjust for double vowels that are usually single diphthongs
    return max(1, count)


def analyze_phonosemantics(word):
    """Analyzes sound symbolism and psychological associations of phonemes."""
    w = word.lower()
    total_chars = max(1, len(w))

    # Detect digraphs first
    fricative_count = sum(1 for ch in w if ch in FRICATIVES)
    for dg in FRICATIVE_DIGRAPHS:
        fricative_count += w.count(dg)

    plosive_count = sum(1 for ch in w if ch in PLOSIVES)
    liquid_nasal_count = sum(1 for ch in w if ch in LIQUIDS_NASALS)

    front_vowel_count = sum(1 for ch in w if ch in FRONT_VOWELS)
    back_vowel_count = sum(1 for ch in w if ch in BACK_VOWELS)
    total_vowels = front_vowel_count + back_vowel_count

    # Dominant sound personality
    traits = []
    if plosive_count >= 2:
        traits.append("Punchy, dependable, precise, impactful (Plosive-heavy: like Pentium, BlackBerry, Docker)")
    if fricative_count >= 2:
        traits.append("Frictionless, aerodynamic, fast, modern (Fricative-heavy: like Swiffer, Sonos, Swift)")
    if liquid_nasal_count >= 2:
        traits.append("Warm, organic, melodic, human (Liquid-heavy: like Loom, Monzo, Linear, Mirror)")

    vowel_profile = "Balanced"
    if total_vowels > 0:
        if front_vowel_count / total_vowels > 0.6:
            vowel_profile = "High-pitch / Front Vowels (Connotes agility, tech precision, lightweight speed)"
        elif back_vowel_count / total_vowels > 0.6:
            vowel_profile = "Deep-pitch / Back Vowels (Connotes authority, volume, institutional grounding, luxury)"

    return {
        'plosive_count': plosive_count,
        'fricative_count': fricative_count,
        'liquid_nasal_count': liquid_nasal_count,
        'vowel_profile': vowel_profile,
        'traits': traits if traits else ["Clean, neutral phonetics"]
    }


def evaluate_radio_test(word):
    """
    Evaluates 'The Radio Test' on a 1-10 scale.
    Can a person hearing this name once on a radio / podcast / call spell it accurately?
    """
    w = word.lower()
    score = 10
    flags = []

    # Check for confusing letter clusters
    for cluster in CONFUSING_CLUSTERS:
        if cluster in w:
            score -= 2
            flags.append(f"Contains tricky cluster '{cluster}'")

    # Check for dropped vowels (e.g. Flickr, Tumblr style)
    if re.search(r'[^aeiouy]{3,}$', w):
        score -= 2
        flags.append("Ends with 3 consecutive consonants (risk of dropped vowel confusion)")

    # Check for homophone ambiguities
    if w.startswith('c') and len(w) > 1 and w[1] in ['a', 'o', 'u']:
        flags.append("Starts with hard C (listeners might search with 'K')")
        score -= 0.5
    elif w.startswith('k'):
        flags.append("Starts with K (listeners might search with 'C')")
        score -= 0.5

    if 'ph' in w:
        score -= 1.5
        flags.append("Contains 'ph' (listeners will likely spell with 'f')")

    if 'x' in w and not w.startswith('x'):
        flags.append("Contains 'x' (moderately phonetic, distinct)")

    # Length penalty
    if len(w) > 10:
        score -= 1.5
        flags.append(f"Length ({len(w)} chars) increases typo likelihood")
    elif len(w) <= 6:
        score += 0.5

    final_score = max(1.0, min(10.0, score))
    return {
        'radio_score': round(final_score, 1),
        'passed_radio_test': final_score >= 7.5,
        'flags': flags if flags else ["Highly transparent spelling (passes Radio Test effortlessly)"]
    }


def evaluate_verbification(word, syllables):
    """Measures how naturally the name functions as a verb in everyday speech."""
    w = word.lower()
    score = 5.0

    if syllables == 1:
        score = 9.5  # "Slack me", "Stripe it", "Zoom in", "Box it"
    elif syllables == 2:
        score = 8.0  # "Google it", "Uber home", "Figma that"
    elif syllables == 3:
        score = 4.5  # Harder to verbify
    else:
        score = 2.0  # Almost impossible to verbify

    # Harsh Latin/Greek suffixes hurt verbification
    if w.endswith(('ation', 'ology', 'itude', 'ence', 'ance')):
        score -= 3.0

    score = max(1.0, min(10.0, score))
    sample_sentence = f"\"Let me {w} this for you\" or \"We can {w} the whole flow.\""

    return {
        'verb_score': round(score, 1),
        'sample_usage': sample_sentence
    }


def audit_name(word):
    """Runs complete linguistic and prosodic audit for a single candidate name."""
    clean_word = word.strip()
    syllables = estimate_syllables(clean_word)
    phonosemantics = analyze_phonosemantics(clean_word)
    radio = evaluate_radio_test(clean_word)
    verb = evaluate_verbification(clean_word, syllables)

    cadence = "Monosyllabic (Punchy & Direct)" if syllables == 1 else \
              "Trochaic (Strong-Weak: Optimal Brand Cadence)" if syllables == 2 else \
              "Dactylic / Multi-syllabic (Architectural / Elevated)"

    return {
        'name': clean_word,
        'syllables': syllables,
        'cadence': cadence,
        'character_length': len(clean_word),
        'radio_test': radio,
        'phonosemantics': phonosemantics,
        'verbification': verb
    }


def print_audit_report(data):
    """Renders a structured, beautiful terminal audit report."""
    name = data['name']
    radio = data['radio_test']
    ps = data['phonosemantics']
    verb = data['verbification']

    print("\n" + "=" * 80)
    print(f" LINGUISTIC & PHONOSEMANTIC AUDIT: '{name.upper()}'")
    print("=" * 80)
    print(f"Syllable Count   : {data['syllables']} ({data['cadence']})")
    print(f"Character Length : {data['character_length']} letters")
    print(f"Radio Test Score : {radio['radio_score']}/10 {'[PASSED]' if radio['passed_radio_test'] else '[CAUTION]'}")
    print(f"Verb Potential   : {verb['verb_score']}/10 -> {verb['sample_usage']}")
    print("-" * 80)
    print("PHONOSEMANTIC PROFILE (Sound Symbolism):")
    print(f"  • Plosives (/b, p, t, d, k, g/): {ps['plosive_count']}")
    print(f"  • Fricatives (/f, v, s, z, th/): {ps['fricative_count']}")
    print(f"  • Liquids/Nasals (/l, r, m, n/): {ps['liquid_nasal_count']}")
    print(f"  • Vowel Tuning: {ps['vowel_profile']}")
    print(f"  • Psychological Associations:")
    for t in ps['traits']:
        print(f"    - {t}")
    print("-" * 80)
    print("SPELLING & AUDIO FRICTION (Radio Test Details):")
    for flag in radio['flags']:
        print(f"  • {flag}")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Agency-Grade Linguistic & Phonosemantic Naming Auditor")
    parser.add_argument("name", help="Candidate brand name to audit (e.g. Stripe, Linear, Sonos)")
    parser.add_argument("--json", "-j", action="store_true", help="Output audit as JSON")
    args = parser.parse_args()

    audit = audit_name(args.name)
    if args.json:
        print(json.dumps(audit, indent=2))
    else:
        print_audit_report(audit)


if __name__ == '__main__':
    main()

