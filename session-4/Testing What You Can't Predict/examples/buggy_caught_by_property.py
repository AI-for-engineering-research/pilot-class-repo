"""
INTENTIONALLY BUGGY implementation — the property test below is SUPPOSED to find it.
This is the "watch a property test catch a real bug" classroom demo.

Domain: adiabatic process  →  T * V^(γ-1) = constant (for an ideal gas)

Given state 1 (T1, V1) and a new volume V2, the adiabatic outlet temperature is:
    T2 = T1 * (V1 / V2)^(γ-1)

THE BUG: the programmer wrote (V2 / V1) instead of (V1 / V2) — a classic
sign/inversion error that still produces a positive float, so unit tests on
a single hand-picked example might easily pass.
"""

import random
import sys

GAMMA = 1.4   # ratio of specific heats for air


# ── BUGGY function (inverted ratio) ──────────────────────────────────────────
def adiabatic_temp_buggy(T1, V1, V2):
    """WRONG: uses V2/V1 instead of V1/V2."""
    return T1 * (V2 / V1) ** (GAMMA - 1)   # <── BUG HERE


# ── Correct reference ─────────────────────────────────────────────────────────
def adiabatic_temp_correct(T1, V1, V2):
    return T1 * (V1 / V2) ** (GAMMA - 1)


# ── Property: compressing gas (V2 < V1) must RAISE its temperature ────────────
def property_compression_heats(T1, V1, V2_shrink_factor):
    """Metamorphic relation: if V2 < V1 (compression), T2 must be > T1."""
    V2 = V1 * V2_shrink_factor   # V2_shrink_factor < 1 → compression
    T2 = adiabatic_temp_buggy(T1, V1, V2)
    return T2 > T1, T1, V1, V2, T2


# ── Naive manual shrink ────────────────────────────────────────────────────────
def try_shrink(T1, V1, factor):
    """Try to produce a 'simpler' (smaller) failing case."""
    best = (T1, V1, factor)
    for t in [T1 / 2, T1 / 10, 1.0]:
        for v in [V1 / 2, V1 / 10, 1.0]:
            ok, *_ = property_compression_heats(t, v, factor)
            if not ok:
                best = (t, v, factor)
    return best


def main():
    random.seed(7)
    N = 500
    print(f"Running {N} random trials of the 'compression heats gas' property...\n")

    for i in range(N):
        T1 = random.uniform(200.0, 1500.0)   # Kelvin
        V1 = random.uniform(0.01, 10.0)      # m³
        # Compression: new volume is between 20 % and 90 % of original
        factor = random.uniform(0.2, 0.9)

        ok, T1_, V1_, V2_, T2_ = property_compression_heats(T1, V1, factor)
        if not ok:
            # Found a counterexample — try to shrink it to a simpler failing case
            sT1, sV1, sf = try_shrink(T1, V1, factor)
            _, sT1_, sV1_, sV2_, sT2_ = property_compression_heats(sT1, sV1, sf)
            correct_shrunk = round(adiabatic_temp_correct(sT1_, sV1_, sV2_), 4)
            print("=" * 60)
            print("PROPERTY VIOLATED  (this failure is intentional!)")
            print()
            print("  Property: compressing a gas adiabatically (V2 < V1) must raise its")
            print("            temperature  →  T2 > T1  for any V2 < V1, T1 > 0")
            print()
            print(f"  Original counterexample  (trial #{i+1}):")
            print(f"    Inputs:   T1={T1_:.2f} K,  V1={V1_:.4f} m³,  V2={V2_:.4f} m³  (V2 < V1: compression)")
            print(f"    Expected: T2 > T1 = {T1_:.2f} K")
            print(f"    Actual:   buggy T2 = {T2_:.4f} K  ← WRONG (temperature fell during compression)")
            print()
            print("  Shrunk minimal counterexample:")
            print(f"    Inputs:   T1={sT1_:.2f} K,  V1={sV1_:.4f} m³,  V2={sV2_:.4f} m³")
            print(f"    Expected: T2 > {sT1_:.2f} K")
            print(f"    Actual:   buggy T2 = {sT2_:.4f} K  |  correct T2 = {correct_shrunk} K")
            print()
            print("  Root cause: adiabatic_temp_buggy uses (V2/V1) instead of (V1/V2).")
            print("              When V2 < V1 the ratio is < 1, so T drops instead of rising.")
            print("=" * 60)
            sys.exit(1)   # exit non-zero to signal test failure

    # Should never reach here with the buggy implementation
    print("No counterexample found — bug was NOT caught (unexpected).")
    sys.exit(2)


if __name__ == "__main__":
    main()
