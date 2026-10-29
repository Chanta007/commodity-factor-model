#!/usr/bin/env python3
"""Generate the public explanation's figures as deterministic SVGs.

The figures carry aggregate results, never market observations. Every number is
also in the prose; the figure shows the shape. Run:

    python3 scripts/make_figures.py

The output is byte-identical on every run, so a diff means a number changed.
"""
from __future__ import annotations

import pathlib

W, H = 1000, 560
BG = "#fbf7f0"
INK = "#1c1c1c"
MUTED = "#6b6258"
GRID = "#e6ded2"
ORANGE = "#d95f02"
TEAL = "#1b9e77"
GRAY = "#b9afa2"
RED = "#c0392b"
AMBER = "#d99a00"
FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif")

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs" / "figures"


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, body, size=16, fill=INK, weight="400", anchor="start", family=FONT,
         transform=""):
    extra = ' transform="%s"' % transform if transform else ""
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
            'font-weight="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, family, size, fill, weight, anchor, extra, esc(body)))


def rect(x, y, w, h, fill, rx=0, stroke="none", sw=0, opacity=1.0):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s" opacity="%s"/>'
            % (x, y, w, h, rx, fill, stroke, sw, opacity))


def line(x1, y1, x2, y2, stroke=GRID, sw=1, dash=""):
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, extra))


def arrow(x1, y1, x2, y2, stroke=MUTED, sw=2):
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" '
            'marker-end="url(#arrow)"/>' % (x1, y1, x2, y2, stroke, sw))


def frame(title, subtitle, height=H):
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" role="img">' % height,
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>' % MUTED,
        rect(0, 0, 1000, height, BG),
        text(60, 76, title, size=34, weight="700"),
        text(60, 108, subtitle, size=18, fill=MUTED),
        line(60, 132, 940, 132),
    ]


def finish(parts):
    return "\n".join(parts + ["</svg>", ""])


def write(name, parts):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(finish(parts), encoding="utf-8")


def coefficients():
    p = frame("Scarcity moves the curve",
              "Annualised carry per one standard deviation of seasonal scarcity")
    rows = [("Oil  (WTI)", 0.0311, "t 3.49", 190, ORANGE),
            ("Gas  (Henry Hub)", 0.1724, "t 6.86", 320, TEAL)]
    scale = 640 / 0.20
    for label, value, tstat, y, colour in rows:
        p.append(text(60, y + 6, label, size=20, weight="600"))
        p.append(rect(60, y + 22, 640, 34, GRID, rx=8))
        p.append(rect(60, y + 22, max(8, value * scale), 34, colour, rx=8))
        p.append(text(60 + max(8, value * scale) + 14, y + 46,
                      "%.4f  (%s)" % (value, tstat), size=20, weight="700",
                      fill=colour))
    p.append(text(60, 470,
                  "Controlled regression: policy buffer, short rate, industrial production, dollar,",
                  size=16, fill=MUTED))
    p.append(text(60, 495,
                  "realised volatility and month dummies. A higher coefficient means the same",
                  size=16, fill=MUTED))
    p.append(text(60, 520,
                  "scarcity reading implies more backwardation. HAC t-statistics are in parentheses.",
                  size=16, fill=MUTED))
    write("coefficients.svg", p)


def factor():
    p = frame("One factor, but not one market",
              "First-component share of weekly changes across nine energy prices")
    groups = [("All nine", 0.561, 0.243), ("Excluding gas", 0.667, 0.260)]
    scale = 360 / 0.80
    baseline = 470
    for i, (label, share, null) in enumerate(groups):
        x = 190 + i * 370
        for j, (value, colour, cap) in enumerate(((share, TEAL, "observed"),
                                                  (null, GRAY, "null"))):
            h = value * scale
            p.append(rect(x + j * 120, baseline - h, 92, h, colour, rx=8))
            p.append(text(x + j * 120 + 46, baseline - h - 14, "%.3f" % value,
                          size=22, weight="700", fill=colour, anchor="middle"))
            p.append(text(x + j * 120 + 46, baseline + 28, cap, size=15,
                          fill=MUTED, anchor="middle"))
        p.append(text(x + 106, baseline + 52, label, size=20, weight="600",
                      anchor="middle"))
    p.append(line(60, baseline, 940, baseline, stroke=MUTED, sw=2))
    write("factor.svg", p)


def walkforward():
    p = frame("It beats a seasonal naive, not a random walk",
              "Out-of-sample mean absolute error, expanding window")
    groups = [("Oil", (0.120, 0.168), "-28%"), ("Gas", (0.173, 0.369), "-53%")]
    scale = 280 / 0.40
    baseline = 430
    for i, (label, (model, naive), gain) in enumerate(groups):
        x = 220 + i * 380
        for j, (value, colour, cap) in enumerate(((model, TEAL, "model"),
                                                  (naive, GRAY, "seasonal naive"))):
            h = value * scale
            p.append(rect(x + j * 110, baseline - h, 84, h, colour, rx=8))
            p.append(text(x + j * 110 + 42, baseline - h - 12, "%.3f" % value,
                          size=20, weight="700", fill=colour, anchor="middle"))
            p.append(text(x + j * 110 + 42, baseline + 26, cap, size=14,
                          fill=MUTED, anchor="middle"))
        p.append(text(x + 97, baseline + 50, label, size=20, weight="600",
                      anchor="middle"))
        p.append(text(x + 97, baseline + 80, gain + " lower error", size=16,
                      weight="700", fill=TEAL, anchor="middle"))
    p.append(line(60, baseline, 940, baseline, stroke=MUTED, sw=2))
    write("walkforward.svg", p)


def scorecard():
    p = frame("The scorecard", "Every rule is registered before it is run", height=460)
    cards = [("12", "confirmed", TEAL), ("2", "no edge", AMBER), ("1", "falsified", RED)]
    for i, (number, label, colour) in enumerate(cards):
        x = 70 + i * 300
        p.append(rect(x, 180, 270, 190, "#ffffff", rx=20, stroke=GRID, sw=2))
        p.append(text(x + 135, 285, number, size=76, weight="700", fill=colour,
                      anchor="middle"))
        p.append(text(x + 135, 330, label, size=20, weight="600", anchor="middle"))
    p.append(text(60, 420,
                  "The falsified rule is the gas convexity term. The two no-edge rules are the",
                  size=15, fill=MUTED))
    p.append(text(60, 440, "weekly inventory build in oil and gas.", size=15, fill=MUTED))
    write("scorecard.svg", p)


def curve():
    p = frame("Two shapes of the same curve",
              "Scarcity shows up as backwardation; ample stock shows up as contango")
    panels = [("Backwardation", "scarce stock", 260, 1, ORANGE),
              ("Contango", "ample stock", 540, -1, TEAL)]
    for title, note, x, slope, colour in panels:
        p.append(rect(x, 180, 200, 250, "#ffffff", rx=16, stroke=GRID, sw=2))
        p.append(text(x + 100, 212, title, size=20, weight="700", anchor="middle",
                      fill=colour))
        p.append(text(x + 100, 236, note, size=14, fill=MUTED, anchor="middle"))
        # Axes
        p.append(line(x + 30, 400, x + 170, 400, stroke=MUTED, sw=2))
        p.append(line(x + 30, 400, x + 30, 270, stroke=MUTED, sw=2))
        # Curve
        y1 = 300 if slope > 0 else 380
        y2 = 380 if slope > 0 else 300
        p.append('<path d="M %d %d C %d %d, %d %d, %d %d" fill="none" '
                 'stroke="%s" stroke-width="5" stroke-linecap="round"/>'
                 % (x + 40, y1, x + 80, y1, x + 120, y2, x + 160, y2, colour))
        p.append(text(x + 100, 430, "nearby → deferred", size=13, fill=MUTED,
                      anchor="middle"))
        p.append(text(x + 14, 340, "price", size=12, fill=MUTED, anchor="middle",
                      transform="rotate(-90 %d 340)" % (x + 14)))
    p.append(text(60, 500,
                  "Schematic, not data. The model measures the annualised slope as",
                  size=16, fill=MUTED))
    p.append(text(60, 525, "4 × ln(nearby / fourth contract).", size=16, fill=MUTED))
    write("curve.svg", p)


def pipeline():
    p = frame("From a physical observation to a testable idea",
              "Five handoffs, each with a different job", height=400)
    boxes = [("1", "Data", "what arrived"), ("2", "State", "scarcity, carry"),
             ("3", "Evidence", "coefficients"), ("4", "Gates", "confirmed?"),
             ("5", "Idea", "expression")]
    for i, (number, label, note) in enumerate(boxes):
        x = 50 + i * 185
        colour = TEAL if i == 3 else INK
        p.append(rect(x, 190, 160, 120, "#ffffff", rx=18, stroke=GRID, sw=2))
        p.append(text(x + 80, 232, number, size=26, weight="700", fill=colour,
                      anchor="middle"))
        p.append(text(x + 80, 264, label, size=20, weight="700", anchor="middle"))
        p.append(text(x + 80, 290, note, size=14, fill=MUTED, anchor="middle"))
        if i < 4:
            p.append(arrow(x + 162, 250, x + 182, 250))
    p.append(text(60, 360,
                  "A plausible number is not a finding, and a finding is not a trade.",
                  size=17, fill=MUTED))
    write("pipeline.svg", p)


if __name__ == "__main__":
    coefficients()
    factor()
    walkforward()
    scorecard()
    curve()
    pipeline()
    print("wrote", len(list(OUT.glob("*.svg"))), "figures to", OUT)