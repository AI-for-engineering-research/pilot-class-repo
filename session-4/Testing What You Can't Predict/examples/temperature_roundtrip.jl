# Round-trip and monotonicity properties for Celsius ↔ Kelvin conversion.
# Uses ONLY Julia's built-in Test stdlib.
#
# Two metamorphic relations:
#   1. Round-trip: C → K → C recovers the original value (inverse MR)
#   2. Order-preserving: if C1 < C2 then K1 < K2 (monotonic MR)

using Test

# ── Conversion functions ───────────────────────────────────────────────────────
celsius_to_kelvin(C) = C + 273.15
kelvin_to_celsius(K) = K - 273.15

# ── Random helpers ─────────────────────────────────────────────────────────────
# Physically meaningful range: −200 °C (colder than liquid nitrogen) to 2000 °C
rand_celsius(lo=-200.0, hi=2000.0) = lo + rand() * (hi - lo)

N = 2000  # trials

@testset "Celsius ↔ Kelvin Conversion Properties" begin

    @testset "Round-trip: C → K → C recovers original (inverse MR)" begin
        for _ in 1:N
            C = rand_celsius()
            K = celsius_to_kelvin(C)
            C2 = kelvin_to_celsius(K)
            # If the inverse is correct, we get back exactly what we started with
            if !isapprox(C2, C; atol=1e-10)
                @error "Round-trip C→K→C failed" C K C2 expected=C atol=1e-10
            end
            @test isapprox(C2, C; atol=1e-10)
        end
    end

    @testset "Round-trip: K → C → K recovers original (inverse MR, other direction)" begin
        # Start from Kelvin: only physically valid K ≥ 0
        for _ in 1:N
            K = rand() * 2273.15   # 0 to 2273.15 K  (matches Celsius range above)
            C = kelvin_to_celsius(K)
            K2 = celsius_to_kelvin(C)
            if !isapprox(K2, K; atol=1e-10)
                @error "Round-trip K→C→K failed" K C K2 expected=K atol=1e-10
            end
            @test isapprox(K2, K; atol=1e-10)
        end
    end

    @testset "Order-preserving: warmer Celsius → warmer Kelvin (monotonic MR)" begin
        for _ in 1:N
            C1 = rand_celsius()
            C2 = rand_celsius()
            if C1 == C2; continue; end   # skip exact ties (degenerate case)
            K1 = celsius_to_kelvin(C1)
            K2 = celsius_to_kelvin(C2)
            # The ordering of temperatures must be preserved across unit systems
            if !((C1 < C2) == (K1 < K2))
                @error "Monotonicity MR violated: ordering must be preserved" C1 C2 K1 K2 expected="(C1<C2)==(K1<K2)"
            end
            @test (C1 < C2) == (K1 < K2)
        end
    end

    @testset "Kelvin is always 273.15 more than Celsius (absolute offset property)" begin
        for _ in 1:N
            C = rand_celsius()
            offset = celsius_to_kelvin(C) - C
            if !isapprox(offset, 273.15; atol=1e-10)
                @error "Offset property violated: K - C must equal 273.15" C offset expected=273.15 atol=1e-10
            end
            @test isapprox(offset, 273.15; atol=1e-10)
        end
    end

end
