"""
Hand-rolled property-based testing — NO external library.
Shows the core idea: generate random inputs, assert a relationship, report failure.
Uses stdlib `random` only.

Domain: ideal gas law  P = nRT / V
"""

import random
import sys

R = 8.314  # J / (mol·K)
SEED = 42
NUM_TRIALS = 2000


def pressure(n, T, V):
    return (n * R * T) / V


def rand_pos(lo=0.01, hi=1000.0):
    return random.uniform(lo, hi)


def run_property(name, trials, check_fn):
    """Generate `trials` random cases, call check_fn(rng) → (ok, info). Return pass/fail."""
    failures = []
    for _ in range(trials):
        ok, info = check_fn()
        if not ok:
            failures.append(info)
            break  # stop at first failure; then try to shrink
    return failures


# ── Manual shrink: when we find a bad triple, try halving each value ──────────
def shrink(n, T, V, predicate, steps=20):
    """Naive one-at-a-time shrink toward smaller values that still fail."""
    for _ in range(steps):
        improved = False
        for cand in [(n / 2, T, V), (n, T / 2, V), (n, T, V / 2)]:
            cn, cT, cV = cand
            if cn > 1e-9 and cT > 1e-9 and cV > 1e-9 and not predicate(cn, cT, cV):
                n, T, V = cn, cT, cV
                improved = True
                break
        if not improved:
            break
    return n, T, V


# ── Property 1: positivity ────────────────────────────────────────────────────
def check_positivity():
    n, T, V = rand_pos(), rand_pos(), rand_pos()
    P = pressure(n, T, V)
    ok = P > 0
    return ok, {"property": "P > 0", "inputs": (n, T, V), "got": P}


# ── Property 2: doubling n doubles P  (scaling MR) ───────────────────────────
def check_scaling():
    n, T, V = rand_pos(), rand_pos(), rand_pos()
    p1 = pressure(n, T, V)
    p2 = pressure(2 * n, T, V)
    ratio = p2 / p1
    ok = abs(ratio - 2.0) < 1e-9
    return ok, {"property": "2n → 2P", "inputs": (n, T, V),
                "P1": p1, "P2": p2, "ratio": ratio, "expected_ratio": 2.0}


# ── Property 3: Boyle's law  P1*V1 ≈ P2*V2  (metamorphic relation) ───────────
def check_boyle():
    n, T = rand_pos(), rand_pos()
    V1, V2 = rand_pos(), rand_pos()
    p1, p2 = pressure(n, T, V1), pressure(n, T, V2)
    product1, product2 = p1 * V1, p2 * V2
    rel_err = abs(product1 - product2) / product1
    ok = rel_err < 1e-9
    return ok, {"property": "P1*V1 == P2*V2", "inputs": (n, T, V1, V2),
                "P1*V1": product1, "P2*V2": product2, "rel_err": rel_err}


def main():
    random.seed(SEED)
    all_passed = True

    tests = [
        ("Positivity  (P > 0)", check_positivity),
        ("Scaling MR  (2n → 2P)", check_scaling),
        ("Boyle's law (P1V1 = P2V2)", check_boyle),
    ]

    for name, check_fn in tests:
        failures = []
        for _ in range(NUM_TRIALS):
            ok, info = check_fn()
            if not ok:
                failures.append(info)
                break

        if failures:
            d = failures[0]
            prop = d.get("property", name)
            inputs = d.get("inputs", "?")
            extra = {k: v for k, v in d.items() if k not in ("property", "inputs")}
            print(f"FAIL  {name}")
            print(f"      Property: {prop}")
            print(f"      Inputs:   {inputs}")
            for k, v in extra.items():
                print(f"      {k}: {v}")
            all_passed = False
        else:
            print(f"PASS  {name}  ({NUM_TRIALS} trials)")

    if all_passed:
        print(f"\nAll properties passed over {NUM_TRIALS} random trials each.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
