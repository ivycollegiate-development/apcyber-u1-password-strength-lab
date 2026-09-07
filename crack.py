#!/usr/bin/env python3
"""Password cracker for the Password Strength Lab.

Reads hashed_passwords.txt and attacks each hash in stages:
  1. dictionary words (common passwords)
  2. patterns: word+year, capitals, leetspeak, symbols, digits
  3. compound words joined by a symbol (e.g. Dragon$Fly)
  4. passphrase word combos (e.g. correct-horse-battery-staple)
  5. brute force (capped at 5 characters so the lab finishes fast)

Run:             python3 crack.py
Integrity check: python3 crack.py --selftest
"""
import hashlib
import itertools
import os
import string
import sys
import time

HASH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hashed_passwords.txt")
ALGO_BY_LENGTH = {32: "md5", 40: "sha1", 64: "sha256"}
EXPECTED_COUNT = 8

DICTIONARY = [
    "123456", "password", "123456789", "12345678", "qwerty", "abc123",
    "monkey", "letmein", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "sunshine", "master", "welcome", "shadow", "ashley",
    "football", "jesus", "michael", "ninja", "mustang", "password1",
    "summer", "winter", "spring", "fall", "hello", "freedom", "fly",
    "correct", "horse", "battery", "staple",
]

YEARS = [str(y) for y in range(1990, 2027)]
SYMBOLS = "!@$&"
LEET = str.maketrans("aeio", "4310")  # vowels only: a->4 e->3 i->1 o->0


def load_hashes():
    """Return {hash_string: (row_number, algo)}."""
    targets = {}
    with open(HASH_FILE) as f:
        for i, line in enumerate(f, 1):
            hv = line.split("#")[0].strip()
            if not hv:
                continue
            algo = ALGO_BY_LENGTH.get(len(hv))
            if algo is None:
                print(f"Hash on line {i}: unknown format ({len(hv)} chars), skipping")
                continue
            targets[hv] = (i, algo)
    return targets


def h(algo, text):
    return hashlib.new(algo, text.encode()).hexdigest()


def check(candidate, targets):
    for algo in ALGO_BY_LENGTH.values():
        d = h(algo, candidate)
        if d in targets:
            return targets[d]
    return None


def selftest():
    lines = []
    with open(HASH_FILE) as f:
        for line in f:
            hv = line.split("#")[0].strip()
            if hv:
                lines.append(hv)
    ok = True
    if len(lines) != EXPECTED_COUNT:
        print(f"SELFTEST FAIL: expected {EXPECTED_COUNT} hashes, found {len(lines)}")
        ok = False
    for hv in lines:
        if len(hv) not in ALGO_BY_LENGTH or any(c not in string.hexdigits for c in hv):
            print(f"SELFTEST FAIL: bad hash {hv!r}")
            ok = False
    # sanity: known weak hash must be present and match md5('123456')
    if h("md5", "123456") not in lines:
        print("SELFTEST FAIL: md5('123456') missing — hash file was modified")
        ok = False
    print("SELFTEST PASS: hash file valid" if ok else "SELFTEST FAILED")
    sys.exit(0 if ok else 1)


def main():
    targets = load_hashes()
    print(f"Loaded {len(targets)} hashes. Cracking...\n")
    cracked = {}
    t0 = time.time()

    def found(idx, algo, pw):
        cracked[idx] = (pw, time.time() - t0, algo)
        print(f"  Hash #{idx} [{algo.upper()}] CRACKED -> {pw!r}  ({time.time()-t0:.3f}s)")

    # Stage 1: plain dictionary
    print("Stage 1: dictionary attack")
    for word in DICTIONARY:
        m = check(word, targets)
        if m and m[0] not in cracked:
            found(*m, word)

    # Stage 2: patterns — word+year, capitals, symbols, digits, leetspeak
    print("Stage 2: pattern attack (years, capitals, symbols, digits, leetspeak)")
    patterns = []
    for word in DICTIONARY:
        cap = word.capitalize()
        leet = word.translate(LEET)
        cap_leet = cap.translate(LEET)
        patterns.append(cap)
        for yr in YEARS:
            patterns.extend([word + yr, cap + yr])
        for sym in SYMBOLS:
            patterns.extend([word + sym, cap + sym, leet + sym, cap_leet + sym])
            for d in string.digits:
                patterns.extend([word + sym + d, cap + sym + d,
                                 cap_leet + sym + d, cap_leet + d + sym])
    # leetspeak alone (summer -> 5umm3r style)
    patterns.extend([word.translate(LEET) for word in DICTIONARY])

    for cand in patterns:
        if len(cracked) == len(targets):
            break
        m = check(cand, targets)
        if m and m[0] not in cracked:
            found(*m, cand)

    # Stage 3: compound words joined by a symbol (Dragon$Fly)
    print("Stage 3: compound words (Word$Word)")
    for w1 in DICTIONARY:
        for w2 in DICTIONARY:
            if w1 == w2:
                continue
            for sym in SYMBOLS:
                for combo in (w1.capitalize() + sym + w2.capitalize(),
                              w1.capitalize() + sym + w2):
                    m = check(combo, targets)
                    if m and m[0] not in cracked:
                        found(*m, combo)

    # Stage 4: passphrase word combos (correct-horse-battery-staple)
    print("Stage 4: passphrase word combos")
    words = ["correct", "horse", "battery", "staple"]
    for sep in ("-", " "):
        for r in range(2, 5):
            for combo in itertools.combinations(words, r):
                cand = sep.join(combo)
                m = check(cand, targets)
                if m and m[0] not in cracked:
                    found(*m, cand)

    # Stage 5: brute force, capped at 5 chars (the slow one)
    if len(cracked) < len(targets):
        print("Stage 5: brute force (max length 5) — this is the slow one")
        alphabet = string.ascii_lowercase + string.digits
        for length in range(1, 6):
            for tup in itertools.product(alphabet, repeat=length):
                cand = "".join(tup)
                m = check(cand, targets)
                if m and m[0] not in cracked:
                    found(*m, cand)
            if len(cracked) == len(targets):
                break

    # Summary
    print("\n" + "=" * 62)
    print(f"{'#':<4}{'ALGO':<8}{'RESULT':<22}{'TIME (s)'}")
    print("-" * 62)
    for hv, (idx, algo) in sorted(targets.items(), key=lambda kv: kv[1][0]):
        if idx in cracked:
            pw, secs, _ = cracked[idx]
            print(f"{idx:<4}{algo.upper():<8}{'CRACKED: ' + pw:<22}{secs:.3f}")
        else:
            print(f"{idx:<4}{algo.upper():<8}{'NOT CRACKED (strong!)':<22}—")
    print("=" * 62)
    print(f"\nCracked {len(cracked)}/{len(targets)}. The uncracked ones are the STRONG passwords.")
    print("Record your results in README.md!")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
