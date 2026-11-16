# -*- coding: utf-8 -*-
"""Render de Shorts 1080x1920 a 30 fps: una escena codificada por frase, luego concat + audio."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from content import VIDEOS, CHANNEL, HANDLE

ROOT = os.environ.get("SE_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/truetype/google-fonts/"
_fc = {}
def F(size, w="Bold"):
    k = (size, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(f"{FD}Poppins-{w}.ttf", size)
    return _fc[k]

PALS = [
 dict(top=(11, 6, 32), mid=(64, 16, 96), bot=(255, 94, 122), acc=(255, 210, 63), acc2=(255, 120, 190), dark=(20, 8, 40)),
 dict(top=(4, 14, 30), mid=(12, 58, 92), bot=(25, 195, 177), acc=(124, 255, 203), acc2=(110, 200, 255), dark=(4, 20, 36)),
 dict(top=(24, 6, 18), mid=(110, 20, 58), bot=(255, 154, 60), acc=(255, 228, 94), acc2=(255, 170, 120), dark=(34, 8, 20)),
]
WHITE = (255, 255, 255)
RED = (255, 72, 88); GREEN = (72, 226, 140); GREY = (190, 190, 205)

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- fondo ----------
def make_bg(pal):
    y = np.linspace(0, 1, H)[:, None]
    top, mid, bot = (np.array(pal[k], np.float32) for k in ("top", "mid", "bot"))
    a = np.clip(y / 0.62, 0, 1); b = np.clip((y - 0.62) / 0.2, 0, 1)
    col = top + (mid - top) * a ** 1.3; col = col + (bot - col) * b ** 1.6
    img = np.repeat(col[:, None, :] if col.ndim == 2 else col, W, axis=1).astype(np.uint8)
    im = Image.fromarray(img, "RGB").convert("RGBA")
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(7)
    for _ in range(90):  # estrellas
        x, yy = int(rng.uniform(0, W)), int(rng.uniform(0, 900)); r = rng.choice([1, 1, 2]); a_ = int(rng.uniform(60, 170))
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 255, 255, a_))
    # sol a rayas
    sun = Image.new("RGBA", (520, 520), (0, 0, 0, 0)); sd = ImageDraw.Draw(sun)
    for i in range(520):
        t = i / 520; c = tuple(int(pal["acc"][k] * (1 - t) + pal["bot"][k] * t) for k in range(3))
        sd.line([(0, i), (520, i)], fill=c + (255,))
    mask = Image.new("L", (520, 520), 0); ImageDraw.Draw(mask).ellipse([0, 0, 519, 519], fill=255)
    md = ImageDraw.Draw(mask)
    for k in range(7):
        yy = 250 + k * 40; md.rectangle([0, yy, 520, yy + 6 + k * 3], fill=0)
    sun.putalpha(mask)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([540 - 330, 1330 - 70, 540 + 330, 1330 + 590], fill=pal["bot"] + (90,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
    im.alpha_composite(sun, (280, 1310))
    # suelo
    d = ImageDraw.Draw(im); d.rectangle([0, 1600, W, H], fill=pal["dark"] + (255,))
    # velo para legibilidad de la zona de contenido
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(veil)
    for i in range(1250):
        vd.line([(0, i), (W, i)], fill=(0, 0, 0, int(70 * (1 - i / 1250))))
    im.alpha_composite(veil)
    return im

def make_grid(pal, n=30):
    frames = []
    hz = 1600; hh = H - hz
    for f in range(n):
        im = Image.new("RGBA", (W, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        col = pal["acc2"]
        for i in range(-14, 15):
            d.line([(540 + i * 22, 0), (540 + i * 300, hh)], fill=col + (130,), width=2)
        ph = f / n
        for k in range(12):
            z = (k + ph) / 12; yy = int(hh * z ** 2.2)
            d.line([(0, yy), (W, yy)], fill=col + (int(60 + 120 * z),), width=2)
        d.line([(0, 0), (W, 0)], fill=col + (255,), width=4)
        frames.append(im)
    return frames

# ---------- texto ----------
def parse(markup):
    words, cur, hl = [], [], False
    buf = ""
    def flush_piece():
        nonlocal buf
        if buf: cur.append((buf, hl)); buf = ""
    for ch in markup:
        if ch == "*": flush_piece(); hl = not hl
        elif ch == " ":
            flush_piece()
            if cur: words.append(list(cur)); cur.clear()
        else: buf += ch
    flush_piece()
    if cur: words.append(list(cur))
    return words

def layout(words, font, max_w):
    sp = font.getlength(" "); lines, line, lw = [], [], 0
    for w in words:
        ww = sum(font.getlength(p) for p, _ in w)
        if line and lw + sp + ww > max_w: lines.append((line, lw)); line, lw = [], 0
        lw = lw + (sp if line else 0) + ww; line.append((w, ww))
    if line: lines.append((line, lw))
    return lines

def text_img(markup, size, max_w=920, fill=WHITE, hl=None, weight="Bold", max_lines=4, lh=1.12, min_size=40):
    words = parse(markup)
    while True:
        font = F(size, weight); lines = layout(words, font, max_w)
        if (len(lines) <= max_lines and all(l[1] <= max_w for l in lines)) or size <= min_size: break
        size -= 4
    asc, desc = font.getmetrics(); line_h = int(size * lh)
    wimg = int(max(l[1] for l in lines)) + 16; himg = line_h * len(lines) + desc + 8
    im = Image.new("RGBA", (wimg, himg), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sp = font.getlength(" ")
    for i, (line, lw) in enumerate(lines):
        x = (wimg - lw) / 2; y = i * line_h
        for w, ww in line:
            for p, h in w:
                d.text((x + 3, y + 4), p, font=font, fill=(0, 0, 0, 110))
                d.text((x, y), p, font=font, fill=(hl if (h and hl) else fill))
                x += font.getlength(p)
            x += sp
    return im

def fit_img(text, max_size, max_w, fill, weight="Bold"):
    size = max_size
    while F(size, weight).getlength(text) > max_w and size > 40: size -= 6
    font = F(size, weight); wimg = int(font.getlength(text)) + 20; asc, desc = font.getmetrics()
    im = Image.new("RGBA", (wimg, asc + desc + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((13, 6), text, font=font, fill=(0, 0, 0, 120)); d.text((8, 0), text, font=font, fill=fill)
    return im

def spaced(text, size, fill, weight="Medium", track=6):
    font = F(size, weight); wimg = int(sum(font.getlength(c) + track for c in text)) + 8
    im = Image.new("RGBA", (wimg, int(size * 1.5)), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 4
    for c in text:
        d.text((x, 0), c, font=font, fill=fill); x += font.getlength(c) + track
    return im

def put(frame, img, cx, y, p=1.0, dy=50, anchor="c"):
    """Pega img con fundido + desplazamiento según progreso p (0..1)."""
    if p <= 0: return
    x = int(cx - img.width / 2) if anchor == "c" else int(cx)
    yy = int(y + (1 - p) * dy)
    if p < 1:
        img = img.copy(); img.putalpha(img.getchannel("A").point(lambda a: int(a * p)))
    frame.alpha_composite(img, (max(0, x), max(0, yy)))

# ---------- iconos (originales, dibujados) ----------
def star_pts(cx, cy, r):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

def icon(name, pal, s=240, t=0.0):
    S = s * 2; im = Image.new("RGBA", (S * 3 if name == "stars" else S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    acc = pal["acc"] + (255,); wh = WHITE + (255,); lw = S // 16
    if name == "clock":
        d.ellipse([lw, lw, S - lw, S - lw], outline=wh, width=lw)
        c = S / 2
        d.line([(c, c), (c, c - S * 0.30)], fill=acc, width=lw); d.line([(c, c), (c + S * 0.02, c - S * 0.22)], fill=acc, width=lw)
        a = -math.pi / 2 + t * 1.2; d.line([(c, c), (c + S * 0.33 * math.cos(a), c + S * 0.33 * math.sin(a))], fill=wh, width=lw // 2)
        d.ellipse([c - lw, c - lw, c + lw, c + lw], fill=acc)
    elif name == "globe":
        d.ellipse([lw, lw, S - lw, S - lw], outline=wh, width=lw)
        d.ellipse([S * 0.28, lw, S * 0.72, S - lw], outline=wh, width=lw // 2)
        d.line([(lw, S / 2), (S - lw, S / 2)], fill=wh, width=lw // 2)
        d.arc([S * 0.1, S * 0.14, S * 0.9, S * 0.5], 20, 160, fill=wh, width=lw // 2)
        d.arc([S * 0.1, S * 0.5, S * 0.9, S * 0.86], 200, 340, fill=wh, width=lw // 2)
        d.ellipse([S * 0.70, S * 0.60, S * 0.84, S * 0.74], fill=acc)
    elif name == "monitor":
        d.rounded_rectangle([lw, S * 0.12, S - lw, S * 0.72], radius=S // 14, outline=wh, width=lw)
        d.rectangle([S * 0.44, S * 0.72, S * 0.56, S * 0.86], fill=wh)
        d.rounded_rectangle([S * 0.28, S * 0.84, S * 0.72, S * 0.91], radius=S // 40, fill=wh)
    elif name == "people":
        for cx, col in ((S * 0.32, wh), (S * 0.68, acc)):
            d.ellipse([cx - S * 0.11, S * 0.14, cx + S * 0.11, S * 0.36], fill=col)
            d.rounded_rectangle([cx - S * 0.17, S * 0.42, cx + S * 0.17, S * 0.92], radius=int(S * 0.15), fill=col)
    elif name == "gauge":
        d.arc([lw, lw, S - lw, S - lw], 180, 360, fill=wh, width=lw)
        d.arc([lw, lw, S - lw, S - lw], 300, 360, fill=acc, width=lw)
        a = math.pi + (0.72 + 0.04 * math.sin(t * 5)) * math.pi; c = S / 2
        d.line([(c, c), (c + S * 0.34 * math.cos(a), c + S * 0.34 * math.sin(a))], fill=acc, width=lw)
        d.ellipse([c - lw * 1.3, c - lw * 1.3, c + lw * 1.3, c + lw * 1.3], fill=wh)
    elif name == "stars":
        for i in range(6):
            on = t * 5 > i
            d.polygon(star_pts(S * 0.25 + i * S * 0.5, S * 0.5, S * 0.22), fill=acc if on else (255, 255, 255, 60))
    return im.resize((im.width // 2, im.height // 2), Image.LANCZOS)

def badge(kind, pal, n=0, s=84):
    S = s * 2; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = {"ok": GREEN, "no": RED, "q": GREY, "num": pal["acc"]}[kind]
    d.ellipse([0, 0, S - 1, S - 1], fill=col + (255,)); dk = pal["dark"] + (255,); lw = S // 9
    if kind == "ok": d.line([(S * .26, S * .52), (S * .44, S * .70), (S * .76, S * .32)], fill=dk, width=lw, joint="curve")
    elif kind == "no": d.line([(S * .3, S * .3), (S * .7, S * .7)], fill=dk, width=lw); d.line([(S * .7, S * .3), (S * .3, S * .7)], fill=dk, width=lw)
    else:
        txt = "?" if kind == "q" else str(n); f = F(int(S * 0.6)); tw = f.getlength(txt)
        d.text(((S - tw) / 2, S * 0.08), txt, font=f, fill=dk)
    return im.resize((s, s), Image.LANCZOS)

def card(w, h, pal, border=None, alpha=44):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=34, fill=(255, 255, 255, alpha), outline=(border + (255,)) if border else (255, 255, 255, 70), width=5 if border else 2)
    return im

# ---------- subtítulos ----------
def chunks(say):
    ws = say.split(); out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= 4 or len(" ".join(cur)) >= 20 or w[-1] in ".,:;?!": out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def caption_img(words, active, pal):
    font = F(62); sp = font.getlength(" "); pad = 26
    lw = sum(font.getlength(w) for w in words) + sp * (len(words) - 1)
    if lw > 800:
        font = F(52); sp = font.getlength(" "); lw = sum(font.getlength(w) for w in words) + sp * (len(words) - 1)
    im = Image.new("RGBA", (int(lw) + pad * 2, 112), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 111], radius=26, fill=(8, 6, 20, 215))
    x = pad
    for i, w in enumerate(words):
        d.text((x, 12 if font.size == 62 else 20), w, font=font, fill=pal["acc"] if i == active else WHITE)
        x += font.getlength(w) + sp
    return im

# ---------- escenas ----------
class Scene:
    def __init__(self, v, b, nfr, pal):
        self.v, self.b, self.n, self.pal = v, b, nfr, pal
        self.dur = nfr / FPS; self.c = {}
        say = b["say"]; self.chunks = chunks(say)
        speech = max(0.3, self.dur - 0.30)
        flat = [(ci, wi, w) for ci, ch in enumerate(self.chunks) for wi, w in enumerate(ch)]
        tot = sum(len(w) + 1.5 for _, _, w in flat); t = 0; self.times = []
        for ci, wi, w in flat:
            self.times.append((t, ci, wi)); t += (len(w) + 1.5) / tot * speech
        self.prep()

    def g(self, key, fn):
        if key not in self.c: self.c[key] = fn()
        return self.c[key]

    def prep(self):
        b, pal = self.b, self.pal; k = b["kind"]
        hlc = pal["acc"]
        if k == "hook":
            self.c["kick"] = self.pill(b["kicker"])
            self.c["head"] = text_img(b["head"], 124, 940, hl=hlc, max_lines=4, lh=1.08)
        elif k in ("text", "num"):
            self.c["head"] = text_img(b["head"], 100, 930, hl=hlc, max_lines=3, lh=1.1)
            if b.get("sub"): self.c["sub"] = text_img(b["sub"], 54, 880, fill=(235, 235, 245), weight="Medium", max_lines=2)
        elif k == "big":
            self.c["label"] = spaced(b["label"], 40, pal["acc2"])
            self.c["val"] = fit_img(b["value"], 290, 960, pal["acc"])
            if b.get("sub"): self.c["sub"] = text_img(b["sub"], 52, 900, fill=(235, 235, 245), weight="Medium", max_lines=2)
        elif k == "bar":
            self.c["label"] = spaced(b["label"], 38, pal["acc2"])
            self.c["sub"] = text_img(b["sub"], 52, 900, fill=(235, 235, 245), weight="Medium")
        elif k == "list":
            self.c["title"] = text_img(b["title"], 68, 920, hl=hlc, max_lines=2)
            self.rows = []
            n = len(b["items"]); rh = 132 if n <= 5 else 116
            for i, (m, txt, sub) in enumerate(b["items"]):
                row = card(940, rh - 16, pal)
                bd = badge(m, pal, i + 1, s=rh - 48); row.alpha_composite(bd, (18, 16))
                ti = fit_img(txt, 58 if n <= 5 else 52, 520 if sub else 760, WHITE)
                row.alpha_composite(ti, (rh - 8, (rh - 16 - ti.height) // 2 + 4))
                if sub:
                    si = fit_img(sub, 38, 330, pal["acc"], "Medium"); row.alpha_composite(si, (940 - si.width - 24, (rh - 16 - si.height) // 2 + 2))
                self.rows.append(row)
            self.rh = rh
        elif k == "vs":
            self.cards = []
            for idx, (t1, t2, t3) in enumerate((b["a"], b["b"])):
                c = card(450, 520, pal, border=pal["acc"] if idx == 1 else None, alpha=50)
                a = spaced(t1, 44, pal["acc2"] if idx == 0 else pal["acc"], "Bold", 4); c.alpha_composite(a, ((450 - a.width) // 2, 60))
                vimg = fit_img(t2, 120, 360, WHITE); c.alpha_composite(vimg, ((450 - vimg.width) // 2, 190))
                if t3:
                    s3 = fit_img(t3, 50, 380, (230, 230, 240), "Medium"); c.alpha_composite(s3, ((450 - s3.width) // 2, 370))
                self.cards.append(c)
        elif k == "stamp":
            self.c["q"] = text_img(b["q"], 88, 920, max_lines=3, lh=1.1)
            f = F(330); tw = int(f.getlength(b["stamp"])); st = Image.new("RGBA", (tw + 150, 440), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
            d.rounded_rectangle([8, 8, st.width - 9, 431], radius=40, outline=RED + (255,), width=22, fill=(20, 0, 6, 150))
            d.text((75, -8), b["stamp"], font=f, fill=RED + (255,))
            self.c["stamp"] = st.rotate(8, expand=True, resample=Image.BICUBIC)
        elif k == "timeline":
            self.c["title"] = text_img(b["title"], 68, 920, hl=hlc, max_lines=2)
            self.pts = [(fit_img(a, 84, 440, pal["acc"]), fit_img(c, 56, 440, WHITE, "Medium")) for a, c in b["points"]]
        elif k == "cta":
            self.c["name"] = fit_img(CHANNEL, 104, 940, WHITE)
            self.c["handle"] = fit_img(HANDLE, 56, 900, pal["acc2"], "Medium")
            self.c["tag"] = text_img("Todo GTA 6, *solo datos confirmados*", 58, 860, hl=pal["acc"], weight="Medium", max_lines=2)
            self.c["btn"] = self.pill("SÍGUENOS", size=64, padx=70, pady=30)

    def pill(self, text, size=40, padx=34, pady=14):
        a = spaced(text, size, self.pal["dark"], "Bold", 5)
        im = Image.new("RGBA", (a.width + padx * 2, int(size * 1.5) + pady * 2), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=im.height // 2, fill=self.pal["acc"] + (255,))
        im.alpha_composite(a, (padx, pady + 2)); return im

    def draw(self, fr, f):
        b, pal = self.b, self.pal; k = b["kind"]; t = f / FPS; dur = self.dur
        E = lambda t0, d=0.38: ease((t - t0) / d)
        cx = 540
        if k == "hook":
            y = 360
            if b.get("icon"):
                ic = icon(b["icon"], pal, 230, t); put(fr, ic, cx, y, back((t - 0.0) / 0.4), dy=0); y += 280
            else: y += 90
            put(fr, self.c["kick"], cx, y, E(0.05)); y += 150
            put(fr, self.c["head"], cx, y, E(0.12), dy=70)
        elif k in ("text", "num"):
            y = 420
            if k == "num":
                nb = self.g("nb", lambda: badge("num", pal, b["n"], s=210)); p = back((t - 0.0) / 0.4)
                sz = max(2, int(210 * p)); put(fr, nb.resize((sz, sz), Image.BILINEAR), cx, 380 + (210 - sz) // 2, 1); y = 660
                if b.get("icon"):
                    ic = icon(b["icon"], pal, 130, max(0, t - 0.3) * 0.9); put(fr, ic, cx, 1135, E(0.3))
            elif b.get("icon"):
                ic = icon(b["icon"], pal, 220, t); put(fr, ic, cx, 360, back(t / 0.4), dy=0); y = 660
            else:
                y = 640 - self.c["head"].height // 2
            put(fr, self.c["head"], cx, y, E(0.08), dy=70); y += self.c["head"].height + 34
            # subrayado animado
            wbar = int(260 * E(0.25, 0.5))
            if wbar > 4: ImageDraw.Draw(fr).rounded_rectangle([cx - wbar // 2, y, cx + wbar // 2, y + 10], radius=5, fill=pal["acc2"] + (255,))
            if "sub" in self.c: put(fr, self.c["sub"], cx, y + 46, E(0.32))
        elif k == "big":
            put(fr, self.c["label"], cx, 430, E(0.0))
            v = self.c["val"]; p = back((t - 0.1) / 0.45)
            if p > 0:
                if p != 1:
                    sc = 0.6 + 0.4 * p; v2 = v.resize((max(2, int(v.width * sc)), max(2, int(v.height * sc))), Image.BILINEAR)
                else: v2 = v
                put(fr, v2, cx, 540 + (v.height - v2.height) // 2 + (290 - v.height) // 2, min(1, (t - 0.1) / 0.2), dy=0)
            y = 540 + 290 + 40
            wbar = int(420 * E(0.3, 0.5))
            if wbar > 4: ImageDraw.Draw(fr).rounded_rectangle([cx - wbar // 2, y, cx + wbar // 2, y + 12], radius=6, fill=pal["acc2"] + (255,))
            if "sub" in self.c: put(fr, self.c["sub"], cx, y + 54, E(0.4))
        elif k == "bar":
            put(fr, self.c["label"], cx, 430, E(0.0)); put(fr, self.c["sub"], cx, 520, E(0.1))
            p = ease((t - 0.2) / min(1.6, dur * 0.6)); val = int(round(b["target"] * p))
            vi = fit_img(f"{val} {b['unit']}", 250, 960, pal["acc"]); put(fr, vi, cx, 600, min(1, t / 0.2), dy=0)
            d = ImageDraw.Draw(fr); x0, x1, yb = 90, 990, 960
            d.rounded_rectangle([x0, yb, x1, yb + 76], radius=38, fill=(255, 255, 255, 50), outline=(255, 255, 255, 120), width=3)
            if p > 0.03: d.rounded_rectangle([x0 + 8, yb + 8, x0 + 8 + int((x1 - x0 - 16) * p), yb + 68], radius=30, fill=pal["acc"] + (255,))
        elif k == "list":
            put(fr, self.c["title"], cx, 360, E(0.0)); n = len(self.rows)
            y0 = 360 + self.c["title"].height + 40; span = max(0.3, dur - 1.0)
            # los elementos entran repartidos a lo largo de la frase
            start = 0.25 if n <= 3 else 0.35
            for i, row in enumerate(self.rows):
                t0 = start + (span - start) * (i / max(1, n)) if n > 1 else 0.3
                put(fr, row, cx + (1 - E(t0)) * 80, y0 + i * self.rh, E(t0), dy=0)
        elif k == "vs":
            put(fr, self.cards[0], 70 - (1 - E(0.05)) * 120, 480, E(0.05), dy=0, anchor="l")
            t1 = min(dur * 0.45, 1.6)
            put(fr, self.cards[1], 560 + (1 - E(t1)) * 120, 480, E(t1), dy=0, anchor="l")
            vs = self.g("vsb", lambda: self.pill(b.get("mid", "VS"), size=44, padx=22, pady=10)); put(fr, vs, cx, 440, back((t - t1) / 0.4), dy=0)
        elif k == "stamp":
            y = 360
            put(fr, self.c["q"], cx, y, E(0.05), dy=70)
            t0 = max(0.6, dur - 1.0); st = self.c["stamp"]; x = (t - t0) / 0.28
            if x > 0:
                sc = 1 + 1.4 * (1 - ease(x)); s2 = st if sc == 1 else st.resize((int(st.width * sc), int(st.height * sc)), Image.BILINEAR)
                yy = y + self.c["q"].height + 60 + st.height // 2
                put(fr, s2, cx, yy - s2.height // 2, min(1, x * 2), dy=0)
        elif k == "timeline":
            put(fr, self.c["title"], cx, 380, E(0.0))
            d = ImageDraw.Draw(fr); xa, xb, yl = 250, 830, 840
            t2 = dur * 0.52; pl = ease((t - t2 + 0.5) / 0.7)
            d.line([(xa, yl), (xb, yl)], fill=(255, 255, 255, 70), width=8)
            if pl > 0: d.line([(xa, yl), (xa + (xb - xa) * pl, yl)], fill=pal["acc"] + (255,), width=10)
            for i, (xx, t0) in enumerate(((xa, 0.3), (xb, t2))):
                p = back((t - t0) / 0.4)
                if p <= 0: continue
                r = int(30 * p); d.ellipse([xx - r, yl - r, xx + r, yl + r], fill=pal["acc"] + (255,), outline=WHITE + (255,), width=5)
                da, lb = self.pts[i]
                put(fr, da, xx, yl - 190, E(t0)); put(fr, lb, xx, yl + 70, E(t0 + 0.1))
        elif k == "cta":
            st = self.g("star", lambda: self.big_star()); p = back(t / 0.45); sz = max(2, int(300 * p))
            st2 = st.resize((sz, sz), Image.BILINEAR).rotate(8 * math.sin(t * 2.2), resample=Image.BICUBIC)
            put(fr, st2, cx, 330 + (300 - sz) // 2, 1)
            put(fr, self.c["name"], cx, 670, E(0.15)); put(fr, self.c["handle"], cx, 810, E(0.25))
            put(fr, self.c["tag"], cx, 910, E(0.35))
            btn = self.c["btn"]; sc = 1 + 0.05 * math.sin(t * 7); pb = E(0.5)
            if pb > 0:
                b2 = btn.resize((int(btn.width * sc), int(btn.height * sc)), Image.BILINEAR); put(fr, b2, cx, 1090 - (b2.height - btn.height) // 2, pb)

    def big_star(self):
        S = 600; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon(star_pts(300, 310, 290), fill=self.pal["acc"] + (255,))
        f = F(210); d.text((300 - f.getlength("6") / 2, 175), "6", font=f, fill=self.pal["dark"] + (255,))
        return im.resize((300, 300), Image.LANCZOS)

    def caption(self, fr, f):
        t = f / FPS; ci, wi = 0, -1
        for (t0, c, w) in self.times:
            if t >= t0: ci, wi = c, w
        if t > self.dur - 0.12: return
        img = self.g(("cap", ci, wi), lambda: caption_img(self.chunks[ci], wi, self.pal))
        fr.alpha_composite(img, (540 - img.width // 2, 1300))

class Video:
    def __init__(self, v):
        self.v = v; self.pal = PALS[v["pal"]]
        self.durs = json.load(open(f"{ROOT}/build/{v['id']}.json")); self.total = sum(self.durs)
        self.bg = make_bg(self.pal); self.grid = make_grid(self.pal)
        self.scenes = [Scene(v, b, n, self.pal) for b, n in zip(v["beats"], self.durs)]
        self.header = self.make_header()

    def make_header(self):
        im = Image.new("RGBA", (W, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon(star_pts(92, 196, 30), fill=self.pal["acc"] + (255,))
        d.text((136, 172), CHANNEL, font=F(36), fill=WHITE + (235,))
        return im

    def frame(self, si, f):
        g = sum(self.durs[:si]) + f
        fr = self.bg.copy(); fr.alpha_composite(self.grid[g % len(self.grid)], (0, 1600))
        fr.alpha_composite(self.header)
        d = ImageDraw.Draw(fr); d.rectangle([0, 0, W, 12], fill=(255, 255, 255, 50)); d.rectangle([0, 0, int(W * (g + 1) / self.total), 12], fill=self.pal["acc"] + (255,))
        sc = self.scenes[si]; sc.draw(fr, f); sc.caption(fr, f)
        # destello breve al cambiar de escena
        if si > 0 and f < 3:
            fl = Image.new("RGBA", (W, H), (255, 255, 255, [70, 40, 18][f])); fr.alpha_composite(fl)
        return fr

    def render(self):
        out_dir = f"{ROOT}/build/{self.v['id']}"; os.makedirs(out_dir, exist_ok=True); files = []
        for si, n in enumerate(self.durs):
            fin = f"{out_dir}/s{si:02d}.mp4"; tmp = f"{out_dir}/s{si:02d}.tmp.mp4"
            p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                  "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
            for f in range(n): p.stdin.write(self.frame(si, f).convert("RGB").tobytes())
            p.stdin.close()
            if p.wait() != 0: raise RuntimeError(f"ffmpeg falló en {fin}")
            os.replace(tmp, fin); files.append(fin)
        lst = f"{out_dir}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in files))
        silent = f"{out_dir}/video.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
        os.makedirs(f"{ROOT}/out", exist_ok=True); final = f"{ROOT}/out/GTA6_{self.v['id']}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", f"{ROOT}/build/{self.v['id']}.wav", "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final], check=True)
        return final

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "frames":   # python render.py frames 01_hora 0:20 3:200 ...
        v = Video(next(x for x in VIDEOS if x["id"] == sys.argv[2])); os.makedirs(f"{ROOT}/frames", exist_ok=True)
        for spec in sys.argv[3:]:
            si, f = map(int, spec.split(":")); f = min(f, v.durs[si] - 1)
            v.frame(si, f).convert("RGB").save(f"{ROOT}/frames/{v.v['id']}_{si}_{f}.jpg", quality=88)
    else:
        for vid in sys.argv[2:]:
            print(Video(next(x for x in VIDEOS if x["id"] == vid)).render(), flush=True)
