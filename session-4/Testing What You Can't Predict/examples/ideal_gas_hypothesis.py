"""
Property-based tests for the ideal gas law: P = nRT / V
Uses the Hypothesis library to generate thousands of random inputs automatically.

Metamorphic relations (MRs) express RELATIONSHIPS between outputs,
so we never need to know the "correct" output for any specific input.
"""

import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

R = 8.314  # J / (mol·K)


def pressure(n, T, V):
    """Ideal gas law: P = nRT / V"""
    return (n * R * T) / V


# --- Strategies: physically sensible ranges ---
pos_float = dict(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False)


@given(
    n=st.floats(**pos_float),
    T=st.floats(**pos_float),
    V=st.floats(**pos_float),
)
@settings(max_examples=500)
def test_pressure_is_positive(n, T, V):
    """Property: P > 0 for all positive n, T, V.
    No metamorphic relation needed — absolute invariant."""
    P = pressure(n, T, V)
    assert P > 0, (
        f"Positivity property violated: P must be > 0 for positive inputs. "
        f"n={n}, T={T}, V={V} → P={P}"
    )


@given(
    n=st.floats(**pos_float),
    T=st.floats(**pos_float),
    V=st.floats(**pos_float),
)
@settings(max_examples=500)
def test_doubling_n_doubles_pressure(n, T, V):
    """Metamorphic relation (scaling): double the moles → double the pressure.
    MR: pressure(2n, T, V) / pressure(n, T, V) ≈ 2.0"""
    p1 = pressure(n, T, V)
    p2 = pressure(2 * n, T, V)
    ratio = p2 / p1
    assert abs(ratio - 2.0) < 1e-9, (
        f"Scaling MR violated: doubling n must double P. "
        f"n={n:.4f}, T={T:.4f}, V={V:.4f} → P1={p1:.6g}, P2={p2:.6g}, ratio={ratio:.10f} (expected 2.0)"
    )


@given(
    n=st.floats(**pos_float),
    T=st.floats(**pos_float),
    V1=st.floats(**pos_float),
    V2=st.floats(**pos_float),
)
@settings(max_examples=500)
def test_boyles_law(n, T, V1, V2):
    """Metamorphic relation (Boyle's law): at fixed n, T the product P*V is constant.
    MR: P1*V1 ≈ P2*V2  (both equal nRT)"""
    p1 = pressure(n, T, V1)
    p2 = pressure(n, T, V2)
    product1, product2 = p1 * V1, p2 * V2
    rel_err = abs(product1 - product2) / product1
    assert rel_err < 1e-9, (
        f"Boyle's law MR violated: P1*V1 must equal P2*V2 at fixed n, T. "
        f"n={n:.4f}, T={T:.4f}, V1={V1:.4f}, V2={V2:.4f} "
        f"→ P1*V1={product1:.6g}, P2*V2={product2:.6g}, rel_err={rel_err:.2e}"
    )
