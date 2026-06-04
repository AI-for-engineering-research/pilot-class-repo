# Session 1 - Outline and teaching plan

**Course:** Agentic AI for Engineering Research (summer pilot)
**Session:** Session 1 | about 55 minutes | Orientation and first assignment
**Instructor:** Prashanth, MIT
**GitHub org:** https://github.com/AI-for-engineering-research
**Goal of today:** Set the working norms, give a solid no-math mental model of how these tools work, and hand out the portfolio assignment that runs through the whole pilot.

---

## Arc of the session

This is a hand-picked group who chose to be here, so keep it light. The pilot is for learning and for fun. Do not bring up grading.

| # | Block | Time | One-line message |
|---|-------|------|------------------|
| 1 | Welcome and framing | 5 min | What this course is, and what it is not. |
| 2 | The three norms | 12 min | How we work: shared frontier, tool not crutch, radical transparency. |
| 3 | Quick diagnostic quiz | 5 min | Ungraded baseline so I know where to push and where to slow down. |
| 4 | How the tools actually work | 18 min | From a raw model to a full agent, in plain intuition. |
| 5 | The assignment and the ritual | 12 min | Build your public portfolio. Show it every week. |
| 6 | Recap and buffer | 3 min | The three norms, restated. Questions. |

The quiz slide is movable. Run it here or right after the fundamentals block, whichever feels right on the day.

---

## Block 1 - Welcome and framing (about 5 min)

**Title slide.** "Agentic AI for Engineering Research." Subtitle: leveraging frontier AI tools to produce real research and wield them with engineering discipline. Footer reads Prashanth, MIT, Day 1. Open with one warm sentence about what the pilot is: we use frontier AI as a power tool for real engineering-research outputs, on your own proposed projects.

**What this course is, and isn't.** Two columns.

It is:
- Using AI as a power tool for real research outputs.
- Built around your own proposed projects.
- Durable software-engineering practice, sharpened by these tools.

It isn't:
- A class on training or building frontier LLMs.
- A bag of disposable prompt tricks.
- A replacement for thinking like an engineer.

The point to land: what you keep is engineering practice. We do not care how the model was built. We care how to use it well.

---

## Block 2 - The three norms (about 12 min)

This is the cultural core of the pilot. Each norm is its own slide. The statement lands big, then shrinks to the left while the right side fills in what it means for the students.

**Norm 1. It's moving too fast for experts (and I'm certainly not one).**

- The field changes by the week. Nobody really holds the frontier, me included, and I want to be honest about that.
- What it means for you: be proactive. You will often find something before I do. Bring it to class and share it.
- The reframe: this is a shared frontier, not a fixed body of knowledge being handed down. Your job is to push it and report back. A shared frontier only moves if you push it.

**Norm 2. A tool, not a crutch.**

- AI amplifies your engineering judgment. It does not replace your fundamentals.
- The right side cycles through three things:
  1. What it means: plausible is not the same as correct. The moment you stop verifying, the tool quietly becomes a liability.
  2. A live demo. The agent writes a median function that just returns the middle element by index. A quick smoke test on [1, 2, 3] passes, because that list is already sorted. A property test then fails: reorder the same numbers and the answer changes, because the code never sorts. Plausible code, wrong code, and only your discipline catches it.
  3. The durable spine: a preview of the practices the summer actually teaches.

**The durable spine (named here, taught in later sessions).**

These are the skills AI does not make obsolete. They are how you stay the architect of work an agent generates:
- Test-driven development
- Property-based testing
- Evaluation suites
- Dependency management
- Architecture and modularity
- Cost management

Today is just the map. We pick these up starting next session, and there are more than fit on the slide.

**Norm 3. Be radically transparent.**

- Be open about how you used AI: what you prompted, what you accepted, what you rejected and why, and where it led you astray.
- Document continuously, as you go, not as a write-up at the end. Keep your portfolio site current.
- This is not an admission of weakness. Documented process is good research, and it pays off well beyond this course. The habit is hard to start and obvious in value once you have it.
- Living the example: the slide carries a short sped-up clip of this very session building these slides. Point at it. You are documenting your own process while asking them to document theirs.
- This norm flows straight into the assignment. The portfolio is where the transparency lives.

---

## Block 3 - Quick diagnostic quiz (about 5 min)

**Quick diagnostic.** A short, ungraded baseline. It tells me where to push and where to ease off. The poll is live at PollEv.com/aistuff, shown on the slide as a QR code (assets/aistuff.png). This slide is movable, so run it here or after the fundamentals block, and keep it to about two minutes.

---

## Block 4 - How the tools actually work (about 18 min, conceptual, no math)

A section divider, then a run of content slides. Intuition only.

**Section divider.** "How these tools actually work." The path for this block is raw model, then context, then agent, then harness.

**What is an LLM.** It predicts the next token, a chunk of text, given everything so far.

- Two moves on the interactive toy. First, sample a few times on the same step and watch it land on different words. That is the probabilistic core, and notice that off-topic words barely register. Second, repeatedly take the top word and append it, and a coherent sentence builds one token at a time. That is how text gets generated.
- Refine the wording against Matt Pocock's AI dictionary if it helps: https://raw.githubusercontent.com/mattpocock/dictionary-of-ai-coding/refs/heads/main/README.md

**The context window.** The model's working memory: everything it can see right now.

- It only reasons over what fits in the window. Nothing else exists for it.
- Knowledge cutoff: it does not inherently know recent events or your private data.
- Ungrounded, it will confidently invent (hallucinate). The fix is to give it tools and retrieval so it works from real, current, checkable facts.

**From a model to an agent.**

- A raw model takes text in and gives text out. One shot, no hands.
- An agent wraps the model in a loop. It acts by calling tools, observes the results, and iterates toward a goal.
- The difference between a chatbot and an agent is the loop and the tools, not the model itself.

**The agent loop (animated).** Goal sets the target. Plan decides the next step. Act calls a tool. Observe reads the result. Then back to plan until the goal is met. This is what "agentic" means. The animation is also a deliberate example of going past a static diagram.

**The harness.** All the scaffolding around the model:

- Instructions: the system prompt and rules of engagement.
- Tools: what it is allowed to call, and how.
- Control flow: the loop itself, when to act, retry, or stop.
- Memory and context: what it remembers and what you feed it.
- Environment: files, terminal, web, your codebase.
- Guardrails: the limits that keep it safe and on task.

Key line: a good harness with an okay model often beats a great model with no harness. Your engineering quality lives in the harness, which is exactly why the fundamentals matter.

**Your role: architect and verifier.** The agent supplies volume and speed. You supply judgment, framing, and verification. You cannot trust what you cannot check. That one sentence is why the course invests so heavily in tests, evaluation suites, and reproducibility.

---

## Block 5 - The assignment and the ritual (about 12 min)

This is the payoff. Give it room and energy. Before the logistics slide, have them open the GitHub org in a tab and brainstorm their project idea with the agent for a few minutes, then write down what the idea is. Frame the write-up as why, then how, then what, but start with why.

**Section divider.** "Your first assignment." It becomes the spine of the whole pilot.

**The deliverable.** Build your public portfolio site.

- A repo of your own, inside the course GitHub organization (github.com/AI-for-engineering-research).
- Who you are: a real about-you, not a stub.
- Your proposed summer project in detail: the problem, why it matters, and what success looks like.
- Due: Monday, June 8. Once you create your repo, open a pull request to the class repo that adds the link to your landing page.
- I link to every student site from the hub repo. Your site is your home base for the whole pilot.

**Not HTML. Velocity.** Head off any web-dev panic.

- You will not be graded on JavaScript. The point is to reach an impressive, live site fast and get fluent in the workflow.
- You have already installed the coding agent and wired up MIT's model provider. Let it build the site while you direct and review. Impressive and live beats hand-coded and slow.
- Working style: start in the CLI agent, not the IDE plugin, and read the code it writes by hand. That builds terminal comfort and reinforces tool, not crutch.

**The weekly ritual.** Every class, about five minutes each: open your site and walk us through what you did, what you learned, and how the project moved. The site is continuous documentation. It grows every week and is never a final report.

**The bar: go beyond static figures.**

- Not this: a screenshot of "this line went up," a wall of text nobody opens, a figure dump with no story.
- This: interactive elements and live demos, linked artifacts and code and results, a narrative someone can follow.
- This deck is the example. A slide can hold a running test and an animated loop, so your project log can too.

**Logistics.**

- GitHub org: you will get an invite, then create your own repo inside the org.
- The hub: my hub repo links out to every student site, one front door to the whole cohort.
- Getting unstuck: bring it to class. Discoveries and dead-ends are both currency here.

---

## Block 6 - Recap and buffer (about 3 min)

**Recap.** Three norms, one next step.

- Shared frontier: nobody is the expert, so be proactive and bring what you find.
- Tool, not crutch: AI amplifies your fundamentals, it never replaces them.
- Transparency: document how you used it, because the process is the research.
- Next step: your portfolio site by Monday, June 8. Take questions, and end warm.

**Before next session.** Optional but recommended: watch 3Blue1Brown on how LLMs and neural networks work, and on transformer architecture. It makes today's intuition click. https://www.youtube.com/watch?v=wjZofJX0v4M

---

## Notes to self (presenter)

- The three interactive moments (the next-token toy, the agent loop, and the smoke-test-versus-property-test demo) are where to slow down and let them play. They are the standard you are quietly setting.
- If you run short, the compressible part is the LLM-fundamentals detail. The context-window slide can be trimmed. Protect the norms and the assignment.
- Have the GitHub org open in a tab so you can demo live right after logistics.
- The diagnostic quiz is flexible. Run it where it fits, keep it to a couple of minutes, and keep it ungraded.
- The making-of clip on the transparency slide is muted and loops on its own, so it needs no clicking.
