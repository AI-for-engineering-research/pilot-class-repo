# Property-based tests for the ideal Brayton (gas-turbine) cycle.
# Uses ONLY Julia's built-in Test stdlib — no PBT package needed.
# Hand-rolled random loops show the "generate → assert" idea directly.

using Test

# ── Brayton cycle formulas ─────────────────────────────────────────────────────

"""Thermal efficiency of an ideal Brayton cycle.
   r = pressure ratio (>1), γ = ratio of specific heats (>1)"""
brayton_efficiency(r, γ) = 1.0 - r^(-(γ - 1) / γ)

"""Isentropic temperature ratio across a compressor.
   T2/T1 = r^((γ-1)/γ)"""
isentropic_temp_ratio(r, γ) = r^((γ - 1) / γ)

# ── Random helpers ─────────────────────────────────────────────────────────────
rand_r(lo=1.1, hi=40.0) = lo + rand() * (hi - lo)   # pressure ratio
rand_γ(lo=1.1, hi=1.7) = lo + rand() * (hi - lo)     # ratio of specific heats

N = 1000   # trials per property

@testset "Brayton Cycle Properties" begin

    @testset "Efficiency is strictly between 0 and 1" begin
        for _ in 1:N
            r, γ = rand_r(), rand_γ()
            η = brayton_efficiency(r, γ)
            # Physical requirement: you can't have negative or ≥100 % thermal efficiency
            if !(0 < η < 1)
                @error "Efficiency out of (0,1)" r γ η expected="0 < η < 1"
            end
            @test 0 < η < 1
        end
    end

    @testset "Efficiency increases with pressure ratio (monotonic MR)" begin
        # Metamorphic relation: higher r → higher η at fixed γ
        for _ in 1:N
            r1 = rand_r(1.1, 20.0)
            r2 = rand_r(r1 + 0.1, 40.0)   # r2 > r1
            γ  = rand_γ()
            η1 = brayton_efficiency(r1, γ)
            η2 = brayton_efficiency(r2, γ)
            if !(η2 > η1)
                @error "Monotonicity MR violated: higher r must give higher η" r1 r2 γ η1 η2 expected="η(r2) > η(r1)"
            end
            @test η2 > η1
        end
    end

    @testset "Efficiency → 0 as pressure ratio → 1 (limit property)" begin
        # As r → 1⁺ the cycle collapses and η → 0
        for _ in 1:N
            r = 1.0 + rand() * 0.01   # r in (1.0, 1.01)
            γ = rand_γ()
            η = brayton_efficiency(r, γ)
            if !(η < 0.02)
                @error "Limit property violated: η must be < 0.02 when r ≈ 1" r γ η expected="η < 0.02"
            end
            @test η < 0.02   # must be very small
        end
    end

    @testset "Isentropic temperature ratio > 1 for r > 1 (compressor heats air)" begin
        for _ in 1:N
            r, γ = rand_r(), rand_γ()
            ratio = isentropic_temp_ratio(r, γ)
            # Compressing gas isentropically always raises its temperature
            if !(ratio > 1.0)
                @error "Isentropic ratio must be > 1 for r > 1" r γ ratio expected="ratio > 1.0"
            end
            @test ratio > 1.0
        end
    end

    @testset "Isentropic ratio is inverse of expansion ratio (round-trip MR)" begin
        # Metamorphic relation: compress by r, then expand by r → back to T1
        # More directly: ratio(r,γ) * ratio(1/r, γ) == 1.0
        for _ in 1:N
            r, γ = rand_r(), rand_γ()
            fwd = isentropic_temp_ratio(r, γ)
            bwd = isentropic_temp_ratio(1/r, γ)
            product = fwd * bwd
            if !isapprox(product, 1.0; rtol=1e-10)
                @error "Round-trip MR violated: ratio(r,γ)*ratio(1/r,γ) must equal 1" r γ fwd bwd product expected=1.0
            end
            @test isapprox(product, 1.0; rtol=1e-10)
        end
    end

end
