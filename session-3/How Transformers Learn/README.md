# How Transformers Learn — Session 3

A projector lesson built around a **live micro-transformer** (embeddings, positions, one attention
head, unembedding; 1,152 parameters) that **trains for real in the browser**: real forward pass,
real backpropagation, real gradient descent, with the backward pass gradient-checked against finite
differences. Adapted from interactive demo *Tool 4 — How Transformers Learn* into a staged,
one-screen-at-a-time format for presenting.

## How to use it

Double-click **`How Transformers Learn.html`**. It needs no server, no build step, and no internet
connection (KaTeX is vendored in `lib/`; keep the folder intact).

- **← / →** move between the 7 main screens (or keys **1–7** to jump). Each screen fills the projector.
- **Space trains the model from any screen**; every panel queries the same live model, so you can
  start training on the cockpit screen and flip to any other screen to show its panels sharpening.
- Each screen has a **"what to notice" rail** on the right: short written notes the students can
  read while the model trains and you talk.
- Three **extra screens** sit outside the arrow-key flow, reachable with keys **8, 9, 0**
  (← returns to the main deck). Use them if there is time or a question invites them.

## The arc

1. **Title** — nobody writes the weights; the 16-word micro-world.
2. **The shape of the machine** — a word's vector multiplied through abstract matrices into
   next-word probabilities, with a softmax explainer in the rail; the big picture before any names.
3. **The matrices, named** — the seven real matrices (dictionary, position, query/key/value/output,
   unembedding) with plain-English jobs and LaTeX names, live heatmaps.
4. **The task** — the 16-word vocabulary, the grammar, the 48-sentence corpus, and cross-entropy.
5. **Ask it something** — type any sentence from the vocabulary; the untrained model predicts the
   next word (badly).
6. **Training, live** — loss falls to the entropy floor, embeddings cluster, attention discovers
   "says → animal". Break it with the learning rate; compare SGD vs Adam.
7. **Ask it again** — the same prediction screen after training; the bars have collapsed onto the
   right answers.

Extras: **8** one update under the microscope (backprop as blame assignment) ·
**9** the held-out test (four deleted sentences complete correctly, so the model learned the rule
rather than memorising strings) · **0** scale (the same loop at 10¹¹ parameters, plus the fine
print on what we simplified).

## Sources

Rumelhart, Hinton & Williams (1986), backpropagation · Bengio et al. (2003), neural LM ·
Kingma & Ba (2015), Adam · Vaswani et al. (2017), attention · Radford et al. (2019), GPT-2 ·
Elhage et al. (2021), transformer circuits. Math rendering: KaTeX, vendored.
