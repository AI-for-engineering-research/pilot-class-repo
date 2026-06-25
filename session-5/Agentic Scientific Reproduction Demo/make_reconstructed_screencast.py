#!/usr/bin/env python3
"""Build a reconstructed terminal-style screencast from a Pi JSONL session log.

The source log contains hidden reasoning/thinking chunks and large binary image
payloads. This exporter deliberately omits reasoning, redacts image/base64 data,
and keeps only user prompts, assistant-visible text, tool calls, and tool results.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
SESSION_LOG = Path(
    "/Users/prashanth/.pi/agent/sessions/--Users-prashanth-codes-AgenticAI_course-trial--/"
    "2026-06-18T18-51-22-345Z_019edc12-d569-7f45-8356-f323bde56a5c.jsonl"
)
VIDEO_OUT = ASSETS / "agentic-reproduction-demo.mp4"
POSTER_OUT = ASSETS / "video-poster.png"
EXPORT_MD = ROOT / "transcript.md"
WIDTH, HEIGHT = 1600, 900
MAX_EXPORT_CHARS = 4200
MAX_VIDEO_CHARS = 1300


@dataclass
class Event:
    role: str
    text: str
    timestamp: str = ""
    critical: str | None = None
    duration: float = 0.45


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


F_TITLE = font(34, True)
F_UI = font(20, True)
F_MONO = font(19)
F_MONO_BOLD = font(19, True)
F_CALLOUT = font(24, True)
F_BODY = font(20)

COLORS = {
    "user": (232, 176, 75),
    "assistant": (238, 243, 251),
    "toolCall": (142, 160, 232),
    "toolResult": (95, 210, 194),
    "toolError": (217, 138, 168),
    "system": (168, 178, 196),
}


def clean(s: str, limit: int) -> str:
    s = s.replace("\r", "")
    s = re.sub(r"iVBORw0KGgo[0-9A-Za-z+/=]+", "[redacted image/base64 payload]", s)
    s = re.sub(r"data:image/[^\s]+", "[redacted image data]", s)
    s = re.sub(r"\n{4,}", "\n\n\n", s)
    if len(s) > limit:
        s = s[:limit].rstrip() + f"\n… [truncated to {limit} chars for readability]"
    return s


def text_from_content(content: list[dict], limit: int) -> str:
    parts: list[str] = []
    for item in content:
        typ = item.get("type")
        if typ == "text":
            parts.append(item.get("text", ""))
        elif typ == "image":
            parts.append("[image payload redacted]")
        elif typ == "toolCall":
            name = item.get("name", "tool")
            args = json.dumps(item.get("arguments", {}), ensure_ascii=False, indent=2)
            parts.append(f"{name}({args})")
        elif typ in {"thinking", "reasoning"}:
            # Do not export hidden/private reasoning.
            continue
    return clean("\n".join(p for p in parts if p), limit)


def classify_critical(text: str) -> str | None:
    checks = [
        ("Eq. (6)", "Equation extracted: κ-Köhler theory becomes code"),
        ("kappa-Kohler equation", "Equation extracted: κ-Köhler theory becomes code"),
        ("ImportError", "RED: the public module did not exist yet"),
        ("comparison failed", "TDD caught a constants/tolerance mismatch"),
        ("f(a) and f(b) must have different signs", "Hypothesis found a tiny-κ numerical edge case"),
        ("python: command not found", "Environment bug: system python was unavailable"),
        ("No module named 'PIL'", "Environment bug: image tooling was missing outside UV"),
        ("pdftoppm", "PDF page rendered for figure extraction"),
        ("threshold", "Digitization by thresholding and log-axis calibration"),
        ("figure1_digitized_points.csv", "Digitized points become regression data"),
        ("unexpected keyword argument 'digitized_points'", "Overlay API evolved through a failing test"),
        ("11 passed", "Final validation: all tests pass"),
        ("git commit", "Progress checkpointed in git"),
    ]
    for needle, label in checks:
        if needle in text:
            return label
    return None


def parse_events() -> list[Event]:
    events: list[Event] = []
    for line in SESSION_LOG.read_text(errors="ignore").splitlines():
        obj = json.loads(line)
        msg = obj.get("message")
        if not msg:
            continue
        role = msg.get("role")
        timestamp = obj.get("timestamp", "")
        if role == "user":
            text = text_from_content(msg.get("content", []), MAX_EXPORT_CHARS)
            events.append(Event("user", text, timestamp, "Pause: user prompt defines the next objective", 7.0))
        elif role == "assistant":
            content = msg.get("content", [])
            tool_bits = [c for c in content if c.get("type") == "toolCall"]
            text_bits = [c for c in content if c.get("type") == "text"]
            for c in tool_bits:
                name = c.get("name", "tool")
                args = json.dumps(c.get("arguments", {}), ensure_ascii=False, indent=2)
                text = clean(f"CALL {name}\n{args}", MAX_EXPORT_CHARS)
                crit = classify_critical(text)
                events.append(Event("toolCall", text, timestamp, crit, 0.55 if not crit else 3.0))
            if text_bits:
                text = text_from_content(text_bits, MAX_EXPORT_CHARS)
                crit = classify_critical(text)
                events.append(Event("assistant", text, timestamp, crit, 2.4 if not crit else 4.5))
        elif role == "toolResult":
            text = text_from_content(msg.get("content", []), MAX_EXPORT_CHARS)
            if not text.strip():
                continue
            is_error = bool(msg.get("isError"))
            crit = classify_critical(text)
            duration = 0.75
            if is_error or crit:
                duration = 4.8
            events.append(Event("toolError" if is_error else "toolResult", text, timestamp, crit, duration))
    return events


def reproduction_events(events: list[Event]) -> list[Event]:
    """Keep the screen reconstruction focused on the scientific reproduction work."""

    selected: list[Event] = []
    for ev in events:
        if ev.role == "user" and "video + article" in ev.text:
            break
        if ev.role == "user" and "literal reconstructed screen cast" in ev.text:
            break
        selected.append(ev)
    return selected


def write_markdown(events: list[Event]) -> None:
    out = [
        "# Redacted Pi session log transcript",
        "",
        "This is exported from the Pi JSONL session log for the scientific-reproduction portion of the demo. Hidden reasoning/thinking chunks and image/base64 payloads are omitted; tool outputs are truncated when extremely long.",
        "",
    ]
    events = reproduction_events(events)
    for i, ev in enumerate(events, 1):
        label = ev.role.upper()
        out.append(f"## {i:03d}. {label} · {ev.timestamp}")
        if ev.critical:
            out.append(f"**Key moment:** {ev.critical}")
            out.append("")
        fence = "text" if ev.role in {"toolResult", "toolError", "toolCall"} else "markdown"
        out.append(f"```{fence}")
        out.append(clean(ev.text, MAX_EXPORT_CHARS))
        out.append("```")
        out.append("")
    EXPORT_MD.write_text("\n".join(out))


def draw_bg() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), (7, 11, 20))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((-250, -220, 780, 650), fill=(80, 95, 180, 70))
    d.ellipse((850, 120, 1850, 1100), fill=(30, 150, 132, 58))
    d.ellipse((760, -280, 1460, 420), fill=(155, 90, 150, 36))
    img = img.filter(ImageFilter.GaussianBlur(28))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0, 72))
    return img


def line_wrap(prefix: str, text: str, width: int = 78) -> list[str]:
    lines: list[str] = []
    # Width is intentionally conservative: these lines are rendered into the
    # left terminal pane of the video. If this is too wide, long user prompts
    # visually collide with the right-side "Current moment" card.
    for raw in text.splitlines():
        if raw == "":
            lines.append(prefix.rstrip())
            continue
        wrapped = wrap(raw, width=width, replace_whitespace=False, drop_whitespace=False) or [""]
        for j, w in enumerate(wrapped):
            lines.append((prefix if j == 0 else " " * len(prefix)) + w)
    return lines


def render_frame(events: list[Event], idx: int, elapsed: float, total: float) -> Image.Image:
    img = draw_bg()
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((34, 28, WIDTH - 34, HEIGHT - 28), radius=26, fill=(5, 9, 18, 218), outline=(255, 255, 255, 38), width=1)
    d.text((64, 50), "Pi reconstructed session log · Petters & Kreidenweis Fig. 1", font=F_TITLE, fill=(238, 243, 251))
    d.text((64, 92), "Literal log playback: user prompts pause, agent/tool output scrolls quickly, key failures pause with callouts", font=F_BODY, fill=(168, 178, 196))

    terminal = (58, 132, 1070, 820)
    d.rounded_rectangle(terminal, radius=18, fill=(0, 0, 0, 210), outline=(95, 210, 194, 72), width=1)
    for x, c in [(86, (217, 138, 168)), (112, (232, 176, 75)), (138, (95, 210, 194))]:
        d.ellipse((x, 154, x + 13, 167), fill=c)
    d.text((166, 150), "exported-log.txt", font=F_UI, fill=(168, 178, 196))

    visible_lines: list[tuple[str, str]] = []
    start = max(0, idx - 32)
    for ev in events[start : idx + 1]:
        label = {
            "user": "USER",
            "assistant": "ASSISTANT",
            "toolCall": "TOOL CALL",
            "toolResult": "TOOL RESULT",
            "toolError": "TOOL ERROR",
        }.get(ev.role, ev.role.upper())
        prefix = f"[{label}] "
        snippet = clean(ev.text, MAX_VIDEO_CHARS)
        for ln in line_wrap(prefix, snippet):
            visible_lines.append((ev.role, ln))
    visible_lines = visible_lines[-30:]
    y = 190
    for role, ln in visible_lines:
        color = COLORS.get(role, (238, 243, 251))
        f = F_MONO_BOLD if role == "user" else F_MONO
        if role == "user" and ln.startswith("[USER]"):
            d.rounded_rectangle((76, y - 4, 1052, y + 23), radius=6, fill=(232, 176, 75, 28))
        if role == "toolError" and ln.startswith("[TOOL ERROR]"):
            d.rounded_rectangle((76, y - 4, 1052, y + 23), radius=6, fill=(217, 138, 168, 30))
        d.text((86, y), ln, font=f, fill=color)
        y += 21

    current = events[idx]
    callout = (1100, 132, 1542, 820)
    d.rounded_rectangle(callout, radius=22, fill=(255, 255, 255, 22), outline=(255, 255, 255, 42), width=1)
    d.text((1128, 162), "Current moment", font=F_UI, fill=(232, 176, 75))
    d.text((1128, 196), current.role.upper(), font=F_TITLE, fill=COLORS.get(current.role, (238, 243, 251)))
    if current.critical:
        d.rounded_rectangle((1128, 250, 1512, 336), radius=16, fill=(232, 176, 75, 30), outline=(232, 176, 75, 80), width=1)
        yy = 266
        for ln in wrap(current.critical, width=34):
            d.text((1148, yy), ln, font=F_CALLOUT, fill=(255, 232, 185))
            yy += 28
    else:
        d.text((1128, 250), "Fast-forwarding through", font=F_BODY, fill=(168, 178, 196))
        d.text((1128, 276), "routine agent/tool output", font=F_BODY, fill=(168, 178, 196))

    summary = {
        "user": "Pause here: this is where the human constrains the work and defines what trust should look like.",
        "assistant": "Assistant message: summarizing progress or handing back a validated artifact.",
        "toolCall": "Tool call: the agent leaves the chat and manipulates files, runs tests, or inspects artifacts.",
        "toolResult": "Tool result: observable evidence. This is where bugs and passing tests become visible.",
        "toolError": "Error output: the most useful part of the loop. The next edit is driven by this failure.",
    }.get(current.role, "")
    yy = 380
    for ln in wrap(summary, width=39):
        d.text((1128, yy), ln, font=F_BODY, fill=(210, 220, 235))
        yy += 26

    d.text((1128, 560), "Playback rule", font=F_UI, fill=(95, 210, 194))
    rule = "User prompts and critical failures are slow. Routine commands are quick. The point is not to watch typing; it is to see the agentic feedback loop."
    yy = 592
    for ln in wrap(rule, width=42):
        d.text((1128, yy), ln, font=F_BODY, fill=(168, 178, 196))
        yy += 25

    progress = elapsed / max(total, 1)
    d.rounded_rectangle((64, 845, WIDTH - 64, 858), radius=7, fill=(255, 255, 255, 36))
    d.rounded_rectangle((64, 845, 64 + int((WIDTH - 128) * progress), 858), radius=7, fill=(95, 210, 194, 190))
    d.text((64, 864), f"event {idx + 1}/{len(events)}", font=F_UI, fill=(168, 178, 196))
    return img


def build_video(events: list[Event]) -> None:
    tmp = ASSETS / "reconstructed_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    total = sum(ev.duration for ev in events)
    elapsed = 0.0
    concat = []
    # Keep the video focused on the original scientific reproduction discussion,
    # not the later meta-work of generating this lesson page.
    selected = reproduction_events(events)
    total = sum(ev.duration for ev in selected)
    for i, ev in enumerate(selected):
        frame = render_frame(selected, i, elapsed, total)
        path = tmp / f"frame_{i:03d}.png"
        frame.save(path)
        concat.append((path, ev.duration))
        elapsed += ev.duration
    POSTER_OUT.write_bytes((tmp / "frame_000.png").read_bytes())

    list_path = tmp / "concat.txt"
    with list_path.open("w") as handle:
        for path, duration in concat:
            handle.write(f"file '{path}'\n")
            handle.write(f"duration {duration:.3f}\n")
        handle.write(f"file '{concat[-1][0]}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-vf",
            "fps=12,format=yuv420p",
            "-movflags",
            "+faststart",
            str(VIDEO_OUT),
        ],
        check=True,
    )
    for p in tmp.glob("*.png"):
        p.unlink()
    list_path.unlink(missing_ok=True)
    tmp.rmdir()


def main() -> None:
    events = parse_events()
    write_markdown(events)
    build_video(events)
    print(f"wrote {VIDEO_OUT}")
    print(f"wrote {EXPORT_MD}")


if __name__ == "__main__":
    main()
