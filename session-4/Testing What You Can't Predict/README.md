# Testing What You Can't Predict — Session 4

A pan-zoom mindmap lesson on **property-based testing (PBT)** and **metamorphic
testing (MT)** for agentic engineering workflows. The presentation lives in
`Testing What You Can't Predict.html` — open it directly in a browser (works over
`file://` or when served). It is a single self-contained file; the only external
resource is Google Fonts.

## The lesson in one paragraph

A lot of research code can't be tested with `assert f(x) == known`, because you
can't compute the expected answer in advance — the *oracle problem*. Two tools
work anyway: a **property test** states something that must hold for every input
and lets a library (Hypothesis in Python; the `Test` stdlib or Supposition.jl in
Julia) generate inputs that try to break it; a **metamorphic test** states a
known relationship between two runs (scaling, symmetry, round-trip), so you never
need either exact answer. The through-line for this course: in an agentic loop the
model writes code, runs tests, reads the failure, and tries again, so the test
output is the agent's main feedback signal. An Anthropic + Hypothesis study
(arXiv:2510.09907) showed a Claude Opus 4.1 agent autonomously finding real bugs
this way, and the closing node asks students to add a property suite to one of
their own codes.

## Navigation

The view opens on the whole map (overview), panel closed. Arrow keys tour the
nodes and zoom in close; the detail sidebar opens only when you click a node.

- `←` `→` (also `↑ ↓`, `Space`, `PageUp/Down`) — tour previous / next node (zooms, no panel)
- Click any node (or `Enter` on the focused node) — open the detail panel
- `Esc` or the `×` button — close the panel
- `Home` / `End` — first / last node
- `F` — toggle fullscreen
- Drag the canvas to pan; scroll / trackpad to zoom
- Bottom-left minimap: click to recenter, drag to pan; shows the viewport rectangle

## Node outline (walkthrough order)

The tour starts with why testing matters for agents, then the two tools, then the
examples, then choosing a property, then the closing result and assignment. Node
colors group related ideas; the branches are not labelled or lettered.

1. **Root** — *Testing What You Can't Predict* (the oracle problem; tests as the agent's feedback signal)

The agentic loop (indigo)
2. The Agentic Feedback Loop (test output is the agent's feedback signal; the circular trap an agent hits when it writes both code and example test; metamorphic relations break it)
3. Write → Run → Read → Fix *(flowchart #1, incl. "tests too weak?" branch)*
4. Agents Imitate Your Tests (Simon Willison, agentic engineering patterns)

The two tools (teal)
5. The Problem & The Two Tools
6. Property-Based Testing (QuickCheck origin; Hypothesis; integrated shrinking; Supposition.jl)
7. Metamorphic Testing (Chen, Cheung & Yiu 1998; relations between runs)
8. Property vs. Example

Five examples (amber) — pseudocode in the lesson; runnable code shared in `examples/`
9. Five Examples (overview)
10. **Ideal Gas: Scaling** — double the moles → double the pressure
11. **Ideal Gas: Boyle's Law** — at fixed n, T the product P·V is constant
12. **Gas Turbine: Monotonicity** — efficiency rises with pressure ratio, stays in (0, 1)
13. **Temperature: Round-Trip** — °C → K → °C recovers the input
14. **A Property Catches a Bug** — a buggy adiabatic relation, caught by the property

How to choose a property (green)
15. How to Choose a Property *(flowchart #2: oracle? → metamorphic → pattern menu, incl. monotonicity)*
16. Scaling & Linearity
17. Symmetry & Invariance
18. Round-Trip & Idempotence

The closing result + assignment (rose)
19. Agents Doing This Now (the Anthropic + Hypothesis study folds in here: 100 packages, 56% valid, numpy.random.wald, arXiv:2510.09907)
20. **Your Assignment**

## Running the examples

From `examples/`:

```bash
# Python, uses Hypothesis  (pip install hypothesis pytest)
pytest ideal_gas_hypothesis.py

# Python, hand-rolled, stdlib only  (prints PASS for all 3 properties)
python3 ideal_gas_plain.py

# Julia, Test stdlib only
julia gas_turbine_properties.jl

# Julia, Test stdlib only
julia temperature_roundtrip.jl

# Python, stdlib only — intentionally buggy; the property CATCHES it
# (prints the counterexample and exits non-zero)
python3 buggy_caught_by_property.py
```

`ideal_gas_hypothesis.py` uses **Hypothesis**; the other four are **hand-rolled**
generate-and-check loops so you can see what a property test is underneath a
library. `buggy_caught_by_property.py` is designed to fail — the property catches
the planted bug and prints the counterexample. The lesson HTML shows these
properties as language-agnostic pseudocode; the runnable code lives here in
`examples/`.

## Assignment

Add a property-based test suite to one of your own research codes, document it,
and demo it next class. Pick one function; ask "what must always be true?"
(units, signs, conservation, scaling, symmetry, a round-trip that returns the
original); write 1–3 properties; if you can't predict the exact output, find a
metamorphic relation between two runs instead; commit the test file with a short
note on each property; come ready to show one property that failed first and what
it caught.

## Sources

- Hypothesis docs — https://hypothesis.readthedocs.io
- Agentic PBT paper (arXiv) — https://arxiv.org/abs/2510.09907
- Anthropic write-up — https://red.anthropic.com/2026/property-based-testing/
- Hillel Wayne, "Metamorphic Testing" — https://www.hillelwayne.com/post/metamorphic-testing/
- QuickCheck (Claessen & Hughes, ICFP 2000) — https://doi.org/10.1145/351240.351266
- Julia `Test` stdlib — https://docs.julialang.org/en/v1/stdlib/Test/
- Supposition.jl — https://github.com/Seelengrab/Supposition.jl
- Simon Willison, "Designing agentic loops" — https://simonwillison.net/2025/Sep/30/designing-agentic-loops/
