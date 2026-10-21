"""Image renderers for Dealer Ops Daily: the daily huddle card and the email masthead.

The card is the shareable unit — a sales manager screenshots it into the team's
group text, and every copy carries the signup address. It doubles as the page's
Open Graph image, so a pasted link previews as the card too.

Brand: slate ground, amber for the one number, Outfit (the site's typeface).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "assets" / "fonts" / "Outfit-Variable.ttf"

SLATE = (15, 23, 42)        # #0F172A
SLATE_2 = (30, 41, 59)      # #1E293B rule lines
AMBER = (245, 158, 11)      # #F59E0B
INK = (248, 250, 252)       # #F8FAFC
MUTED = (148, 163, 184)     # #94A3B8
SOFT = (203, 213, 225)      # #CBD5E1

W, H = 1200, 630
PAD = 72


def _font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONT), size)
    f.set_variation_by_name(weight)
    return f


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int, max_lines: int) -> list[str]:
    words, lines, line = " ".join(text.split()).split(" "), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
            continue
        if line:
            lines.append(line)
        line = w
        if len(lines) == max_lines:
            break
    if line and len(lines) < max_lines:
        lines.append(line)
    if len(lines) == max_lines and " ".join(lines) != " ".join(words):
        last = lines[-1]
        while last and draw.textlength(last + "…", font=font) > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last.rstrip(",;:—-") + "…"
    return lines


def _wrap_hanging(draw, text: str, font, first_width: int, rest_width: int, max_lines: int) -> list[str]:
    """Wrap where line 1 is narrower (it follows an inline label) and later lines are full width."""
    words = " ".join(text.split()).split(" ")
    lines, line, width = [], "", first_width
    for i, w in enumerate(words):
        trial = f"{line} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
            continue
        lines.append(line)
        line, width = w, rest_width
        if len(lines) == max_lines:
            line = ""
            break
    if line:
        lines.append(line)
    if " ".join(lines) != " ".join(words):  # truncated: end with an ellipsis that fits
        last = lines[-1]
        w_last = rest_width if len(lines) > 1 else first_width
        while last and draw.textlength(last + "…", font=font) > w_last:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last.rstrip(",;:—-") + "…"
    return lines


def _fit(draw, text: str, weight: str, start: int, width: int, floor: int) -> ImageFont.FreeTypeFont:
    size = start
    while size > floor and draw.textlength(text, font=_font(size, weight)) > width:
        size -= 4
    return _font(size, weight)


def _header(draw, label_right: str) -> None:
    draw.text((PAD, 58), "DEALER OPS DAILY", font=_font(26, "Bold"), fill=AMBER)
    rf = _font(24, "Medium")
    draw.text((W - PAD - draw.textlength(label_right, font=rf), 60), label_right, font=rf, fill=MUTED)


def _footer(draw) -> None:
    y = H - 92
    draw.line([(PAD, y - 26), (W - PAD, y - 26)], fill=SLATE_2, width=2)
    lead = _font(28, "Medium")
    url = _font(28, "Bold")
    x = PAD
    draw.text((x, y), "Free every weekday", font=lead, fill=SOFT)
    x += draw.textlength("Free every weekday", font=lead) + 16
    draw.text((x, y), "→", font=url, fill=AMBER)
    x += draw.textlength("→", font=url) + 16
    draw.text((x, y), "carsalestrackerpro.com/brief", font=url, fill=INK)


def render_card(out: Path, *, date_label: str, number: str | None = None,
                talking_point: str | None = None, question: str | None = None,
                title: str = "", subtitle: str = "") -> bytes:
    """Huddle card when a huddle starter exists; otherwise a title card."""
    img = Image.new("RGB", (W, H), SLATE)
    d = ImageDraw.Draw(img)
    inner = W - 2 * PAD

    if number and talking_point:
        _header(d, f"HUDDLE STARTER · {date_label.upper()}")
        nf = _fit(d, number, "Bold", 150, inner, 72)
        d.text((PAD - 4, 104), number, font=nf, fill=AMBER)
        y = 104 + nf.size + 22
        tf = _font(38, "SemiBold")
        for line in _wrap(d, talking_point, tf, inner, 2):
            d.text((PAD, y), line, font=tf, fill=INK)
            y += 50
        if question:
            y += 12
            qf = _font(30, "Regular")
            lbl = _font(30, "Bold")
            d.text((PAD, y), "Ask the team:", font=lbl, fill=AMBER)
            indent = d.textlength("Ask the team: ", font=lbl)
            q_lines = _wrap_hanging(d, question, qf, inner - int(indent), inner, 2)
            for i, line in enumerate(q_lines):
                d.text((PAD + (indent if i == 0 else 0), y + 42 * i), line, font=qf, fill=SOFT)
    else:
        _header(d, date_label.upper())
        tf = _font(64, "Bold")
        y = 128
        for line in _wrap(d, title, tf, inner, 3):
            d.text((PAD, y), line, font=tf, fill=INK)
            y += 76
        if subtitle:
            sf = _font(30, "Regular")
            for line in _wrap(d, subtitle, sf, inner, 2):
                d.text((PAD, y + 14), line, font=sf, fill=SOFT)
                y += 42

    _footer(d)
    return _save(img, out)


def render_masthead(out: Path) -> bytes:
    """1200x300 header for the top of each email."""
    img = Image.new("RGB", (W, 300), SLATE)
    d = ImageDraw.Draw(img)
    d.text((PAD, 40), "EVERY WEEKDAY · BEFORE THE DOORS OPEN", font=_font(22, "SemiBold"), fill=AMBER)
    d.text((PAD, 72), "Dealer Ops Daily", font=_font(84, "Bold"), fill=INK)
    d.rectangle([PAD, 186, PAD + 96, 192], fill=AMBER)
    d.text((PAD, 212), "The 5-minute brief for people who sell cars", font=_font(34, "Medium"), fill=SOFT)
    return _save(img, out)


def _save(img: Image.Image, out: Path) -> bytes:
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists() or out.read_bytes() != data:
        out.write_bytes(data)
    return data
