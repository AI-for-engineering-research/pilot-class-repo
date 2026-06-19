# Agentic Scientific Reproduction Demo — Session 5

This session is a reconstructed log-playback of an AI-agent coding session that reproduced Figure 1 from Petters & Kreidenweis (2007), *A single parameter representation of hygroscopic growth and cloud condensation nucleus activity*.

Open:

- `Agentic Scientific Reproduction Demo.html`

The lesson includes:

- a generated MP4 rebuilt from the exported Pi JSONL session log;
- literal log playback: user prompts pause, agent/tool output scrolls quickly, and interesting failures pause with callouts;
- interactive jump buttons that seek to key moments in the video;
- a right-hand artifact panel that changes with the video time;
- an article explaining the workflow, bugs, and teaching points;
- a redacted exported Pi session log in `transcript.md`;
- the full exported HTML session log in `session_log.html` for deeper inspection;
- copied artifacts from the working repo:
  - `assets/extracted-paper-figure1.png`
  - `assets/recreated-figure1.png`
  - `assets/figure1-digitized-overlay.png`
  - `assets/figure1-pretty-overlay.png`
  - `data/figure1_digitized_points.csv`
- `make_reconstructed_screencast.py`, the exporter used to rebuild the MP4 from the redacted Pi log
- `session_log.html`, the full browsable session log artifact

## Key teaching points

1. **Prompt process, not just output.** The original request specified UV, git, TDD, and property tests, so the agent had to produce an auditable workflow.
2. **Use physics as an oracle.** Limiting cases and monotonicity properties tested the κ-Köhler implementation without requiring hand-computed answers everywhere.
3. **Let property tests find weird edges.** Hypothesis found a tiny-positive-κ case that broke the root bracketing logic; this became a useful teaching bug.
4. **Turn visual agreement into data.** Digitizing the published figure created CSV regression points and an overlay plot.
5. **Make the process visible.** The lesson shows failures, fixes, commits, and artifacts rather than presenting only the polished final plot.

## Local preview

From the course repo root:

```bash
./build.sh
python3 -m http.server -d _site 8000
```

Then open the Session 05 link from the Classes modal, or navigate directly to:

```text
http://localhost:8000/session-5/Agentic%20Scientific%20Reproduction%20Demo/Agentic%20Scientific%20Reproduction%20Demo.html
```

## Provenance

The MP4 is not an original screen recording. It was generated after the fact from the Pi JSONL session log. The exporter omits hidden reasoning/thinking chunks and redacts image/base64 payloads, then renders a terminal-style playback that pauses on user prompts and critical failures. This is explicitly noted in the lesson so students understand the difference between an authentic recording and a reconstructed teaching artifact.
