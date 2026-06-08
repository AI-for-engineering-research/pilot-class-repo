# The Attention Mechanism — Session 2

A stand-alone interactive on the **mix** step of attention: how a token's output is assembled as a weighted blend of value vectors, `out_i = Σ_j a_ij v_j`. Extracted from Tool 2's "Mix" act so it can run on its own in Session 2.

## How to use it

Double-click **`Attention Mechanism.html`**. No server, no build, no internet — keep the folder intact (`lib/` and `data/` sit next to the HTML). The panel has a **⤢ Expand** button that fills the screen for projecting; press it again or hit **Esc** to close. **Presenter mode** (top-right) enlarges type.

What you can do:

- **Pick a sentence** and **click any token** to make it the query.
- Watch the output assemble: the **flow diagram** beams each token's value into the query position weighted by attention, and the **heatmap** shows the full attention matrix `a_ij = softmax_j(q_i·k_j/√d)`.
- Toggle the **causal mask** (GloVe mode) — a token can only read what came before it.
- **GPT-2 (real)** mode: slide through all 12 layers and 12 heads of GPT-2 small's genuine attention, or jump to famous heads (previous-token, attention sink, self). The residual-stream panel shows how the query token's vector is reshaped as context folds in.
- **GloVe (identity)** mode: `W_Q=W_K=W_V=I` on real GloVe vectors — a transparent stand-in. Hit **randomize W_Q,W_K** to see that *what counts as relevant is learned*.

A coda assembles `softmax(QKᵀ/√dₖ)V` and previews multi-head attention.

## Sources

Vaswani et al. (2017), *Attention Is All You Need* · Bahdanau, Cho & Bengio (2015), attention's origin · Elhage et al. (2021), *A Mathematical Framework for Transformer Circuits* (previous-token / induction heads). Real attention exported from `gpt2-small`; vectors GloVe 100-d. Math: KaTeX.
