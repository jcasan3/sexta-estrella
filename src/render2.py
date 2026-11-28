# -*- coding: utf-8 -*-
"""Render v2: fondos animados estilo Vice City (ilustración original), tipografía grande,
transiciones, sacudidas y subtítulos palabra a palabra. 1080x1920 a 30 fps."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
from content2 import VIDEOS2, CHANNEL, HANDLE

ROOT = os.environ.get("SE_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30
FONTS = os.path.join(ROOT, "fonts")
GF = "/usr/share/fonts/truetype/google-fonts/"
_fc = {}
def F(size, kind="anton"):
    path = {"anton": f"{FONTS}/Anton-Regular.ttf", "black": f"{FONTS}/Poppins-Black.ttf",
            "xbold": f"{FONTS}/Poppins-ExtraBold.ttf", "bold": f"{GF}Poppins-Bold.ttf"}[kind]
    k = (size, kind)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

YEL = (255, 214, 64); PINK = (255, 64, 160); CYAN = (64, 230, 255); WHITE = (255, 255, 255)
RED = (255, 52, 72); GREEN = (60, 230, 120); GREY = (190, 190, 210); BLACK = (0, 0, 0)
rng = np.random.default_rng(11)

def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0.0, min(1.0, x)); c = 2.2; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t

def grad(h, stops, w=1):
    ys = np.linspace(0, 1, h)[:, None]; out = np.zeros((h, 3), np.float32)
    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        m = ((ys[:, 0] >= p0) & (ys[:, 0] <= p1)); t = ((ys[:, 0] - p0) / max(1e-6, p1 - p0))[m][:, None]
        out[m] = np.array(c0) * (1 - t) + np.array(c1) * t
    return Image.fromarray(np.repeat(out[:, None, :], w, axis=1).astype(np.uint8), "RGB").convert("RGBA")

def glow(img, r=18, k=1.0):
    g = img.filter(ImageFilter.GaussianBlur(r))
    if k != 1: g.putalpha(g.getchannel("A").point(lambda a: min(255, int(a * k))))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(img); return out

# ---------------- fondos (ilustración original) ----------------
EXT = 1500  # ancho de las capas para el paneo
def palm(h, lean=0.0, color=(10, 4, 22, 255)):
    im = Image.new("RGBA", (int(h * 0.9), h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx = im.width // 2
    pts = []
    for i in range(40):
        t = i / 39; x = cx + lean * h * 0.25 * t ** 2; y = h - t * h * 0.82; pts.append((x, y))
    for i in range(len(pts) - 1):
        wdt = int(lerp(h * 0.05, h * 0.025, i / 39)); d.line([pts[i], pts[i + 1]], fill=color, width=wdt)
    tx, ty = pts[-1]
    for a in range(9):
        ang = -math.pi + a * math.pi / 8 + 0.15 * math.sin(a); L = h * (0.38 + 0.08 * (a % 3))
        seg = []
        for j in range(16):
            s = j / 15; seg.append((tx + math.cos(ang) * L * s, ty + math.sin(ang) * L * s * 0.55 + (s ** 2) * L * 0.35))
        for j in range(len(seg) - 1):
            d.line([seg[j], seg[j + 1]], fill=color, width=max(3, int(h * 0.03 * (1 - j / 16))))
            if j % 2 == 0:
                px, py = seg[j]; d.line([(px, py), (px + 14 * math.cos(ang + 1.3), py + 26)], fill=color, width=4)
    return im

def skyline(w, h, base, n, hmin, hmax, col, win=None, neon=None, seed=0):
    r = np.random.default_rng(seed); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 0
    while x < w:
        bw = int(r.uniform(60, 150)); bh = int(r.uniform(hmin, hmax)); top = base - bh
        d.rectangle([x, top, x + bw, base], fill=col)
        if r.random() < 0.3: d.rectangle([x + bw * 0.4, top - 40, x + bw * 0.45, top], fill=col)
        if neon is not None and r.random() < 0.45:
            d.line([(x, top), (x + bw, top)], fill=neon + (255,), width=4)
        if win:
            for wy in range(int(top + 14), int(base - 10), 22):
                for wx in range(int(x + 8), int(x + bw - 8), 16):
                    if r.random() < 0.28: d.rectangle([wx, wy, wx + 6, wy + 9], fill=win[r.integers(len(win))] + (int(r.uniform(140, 255)),))
        x += bw + int(r.uniform(2, 14))
    return im

class Scenes:
    def __init__(self):
        self.c = {}
    def get(self, name):
        if name not in self.c: self.c[name] = getattr(self, "mk_" + name)()
        return self.c[name]

    def mk_city(self):
        sky = grad(H, [(0, (8, 2, 30)), (0.38, (40, 8, 80)), (0.6, (160, 30, 120)), (0.66, (255, 120, 90)), (1, (20, 6, 40))], EXT)
        d = ImageDraw.Draw(sky)
        for _ in range(140):
            x, y = rng.uniform(0, EXT), rng.uniform(0, 800); r = rng.choice([1, 1, 2]); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(rng.uniform(80, 200))))
        sun = Image.new("RGBA", (EXT, H), (0, 0, 0, 0)); ImageDraw.Draw(sun).ellipse([EXT / 2 - 260, 1000, EXT / 2 + 260, 1520], fill=(255, 150, 80, 200))
        sky.alpha_composite(sun.filter(ImageFilter.GaussianBlur(60)))
        far = skyline(EXT, H, 1270, 0, 160, 420, (70, 20, 110, 255), seed=1, neon=PINK)
        near = skyline(EXT, H, 1270, 0, 90, 300, (22, 6, 42, 255), win=[YEL, CYAN, (255, 140, 200)], seed=2, neon=CYAN)
        water = grad(H - 1270, [(0, (40, 10, 70)), (1, (6, 2, 18))], EXT)
        refl = Image.alpha_composite(far, near).crop((0, 1270 - 420, EXT, 1270)).transpose(Image.FLIP_TOP_BOTTOM)
        refl.putalpha(refl.getchannel("A").point(lambda a: a // 3)); water.alpha_composite(refl.resize((EXT, H - 1270)).filter(ImageFilter.GaussianBlur(3)))
        palms = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        palms.alpha_composite(palm(980, 0.5), (-260, 1000)); palms.alpha_composite(palm(860, -0.6).transpose(Image.FLIP_LEFT_RIGHT), (W - 560, 1120))
        return dict(sky=sky, far=far, near=near, water=water, palms=palms)

    def mk_beach(self):
        sky = grad(H, [(0, (40, 10, 90)), (0.35, (220, 60, 130)), (0.58, (255, 170, 80)), (0.62, (255, 220, 140)), (1, (255, 220, 140))], EXT)
        sun = Image.new("RGBA", (600, 600), (0, 0, 0, 0)); sd = ImageDraw.Draw(sun)
        for i in range(600):
            t = i / 600; sd.line([(0, i), (600, i)], fill=(255, int(lerp(240, 80, t)), int(lerp(120, 140, t)), 255))
        m = Image.new("L", (600, 600), 0); md = ImageDraw.Draw(m); md.ellipse([0, 0, 599, 599], fill=255)
        for k in range(8): yy = 300 + k * 36; md.rectangle([0, yy, 600, yy + 5 + k * 3], fill=0)
        sun.putalpha(m); sky.alpha_composite(glow(sun, 40), (EXT // 2 - 300, 640))
        sea = grad(H - 1180, [(0, (60, 30, 120)), (0.5, (30, 90, 150)), (1, (20, 140, 160))], EXT)
        sand = grad(380, [(0, (255, 200, 140)), (1, (230, 150, 110))], EXT)
        palms = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        palms.alpha_composite(palm(1250, 0.7, (20, 6, 30, 255)), (-420, 760)); palms.alpha_composite(palm(1050, -0.5, (20, 6, 30, 255)).transpose(Image.FLIP_LEFT_RIGHT), (W - 620, 900))
        return dict(sky=sky, sea=sea, sand=sand, palms=palms)

    def mk_highway(self):
        sky = grad(H, [(0, (6, 2, 24)), (0.42, (50, 10, 90)), (0.52, (255, 80, 140)), (0.56, (30, 8, 50)), (1, (10, 4, 20))], EXT)
        city = skyline(EXT, H, 1000, 0, 60, 230, (30, 8, 60, 255), win=[YEL, CYAN], seed=5, neon=PINK)
        car = Image.new("RGBA", (620, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(car)
        d.rounded_rectangle([40, 90, 580, 300], radius=40, fill=(14, 6, 24, 255)); d.polygon([(120, 95), (180, 10), (440, 10), (500, 95)], fill=(14, 6, 24, 255))
        d.polygon([(150, 92), (196, 28), (424, 28), (470, 92)], fill=(60, 30, 90, 255))
        tl = Image.new("RGBA", car.size, (0, 0, 0, 0)); td = ImageDraw.Draw(tl)
        td.rounded_rectangle([60, 150, 230, 185], radius=12, fill=RED + (255,)); td.rounded_rectangle([390, 150, 560, 185], radius=12, fill=RED + (255,))
        car.alpha_composite(glow(tl, 22, 2.0)); d.rounded_rectangle([250, 210, 370, 245], radius=6, fill=(230, 230, 230, 255))
        d.rectangle([70, 290, 160, 330], fill=(5, 2, 8, 255)); d.rectangle([460, 290, 550, 330], fill=(5, 2, 8, 255))
        return dict(sky=sky, city=city, car=car)

    def mk_police(self):
        c = self.get("city"); base = Image.alpha_composite(c["sky"], c["far"]); base.alpha_composite(c["near"])
        dark = Image.new("RGBA", base.size, (0, 0, 10, 150)); base.alpha_composite(dark)
        red = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(red).ellipse([-500, 300, 600, 1700], fill=(255, 20, 40, 150))
        blue = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(blue).ellipse([480, 300, 1580, 1700], fill=(30, 80, 255, 150))
        return dict(base=base, red=red.filter(ImageFilter.GaussianBlur(120)), blue=blue.filter(ImageFilter.GaussianBlur(120)), water=c["water"])

    def mk_map(self):
        MW, MH = 1800, 2600
        im = grad(MH, [(0, (6, 20, 50)), (1, (4, 10, 30))], MW); d = ImageDraw.Draw(im)
        for x in range(0, MW, 90): d.line([(x, 0), (x, MH)], fill=(40, 120, 180, 50), width=2)
        for y in range(0, MH, 90): d.line([(0, y), (MW, y)], fill=(40, 120, 180, 50), width=2)
        land = [(150, 520), (700, 470), (900, 560), (1180, 540), (1380, 600), (1420, 760), (1460, 1000), (1520, 1260), (1560, 1500),
                (1600, 1760), (1560, 1990), (1440, 2120), (1300, 2060), (1210, 1900), (1110, 1720), (1000, 1560), (960, 1380), (900, 1180),
                (860, 960), (760, 820), (560, 760), (360, 790), (160, 740)]
        lay = Image.new("RGBA", (MW, MH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.polygon(land, fill=(30, 150, 120, 255))
        for i, (x, y) in enumerate([(1330, 2200), (1240, 2270), (1140, 2320), (1030, 2350), (920, 2360)]):
            ld.ellipse([x - 34 + i * 3, y - 18, x + 34, y + 18], fill=(30, 150, 120, 255))
        edge = Image.new("RGBA", (MW, MH), (0, 0, 0, 0)); ImageDraw.Draw(edge).line(land + [land[0]], fill=CYAN + (255,), width=8)
        im.alpha_composite(glow(edge, 16)); im.alpha_composite(lay)
        sw = Image.new("RGBA", (MW, MH), (0, 0, 0, 0)); ImageDraw.Draw(sw).ellipse([1150, 1550, 1450, 1950], fill=(20, 100, 70, 200)); im.alpha_composite(sw.filter(ImageFilter.GaussianBlur(30)))
        pins = [(1500, 1820), (1180, 2300), (1290, 1760), (380, 640), (1050, 900), (1240, 700)]
        return dict(map=im, pins=pins, size=(MW, MH))

    def mk_night(self):
        sky = grad(H, [(0, (2, 4, 18)), (0.45, (10, 20, 50)), (0.62, (30, 50, 70)), (0.68, (8, 18, 26)), (1, (2, 6, 10))], EXT)
        d = ImageDraw.Draw(sky)
        for _ in range(260):
            x, y = rng.uniform(0, EXT), rng.uniform(0, 1100); r = rng.choice([1, 1, 1, 2]); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, int(rng.uniform(60, 230))))
        moon = Image.new("RGBA", (520, 520), (0, 0, 0, 0)); ImageDraw.Draw(moon).ellipse([110, 110, 410, 410], fill=(235, 240, 255, 255))
        md = ImageDraw.Draw(moon)
        for cx, cy, r in ((200, 210, 30), (300, 300, 22), (250, 330, 14)): md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(205, 212, 235, 255))
        sky.alpha_composite(glow(moon, 50, 1.2), (EXT // 2 + 80, 200))
        trees = Image.new("RGBA", (EXT, H), (0, 0, 0, 0)); td = ImageDraw.Draw(trees); r = np.random.default_rng(21)
        x = 0
        while x < EXT:
            h = r.uniform(250, 620); w = r.uniform(18, 34); base = 1240
            td.rectangle([x, base - h, x + w, base], fill=(3, 8, 10, 255))
            for k in range(6):
                yy = base - h + k * h / 7; ww = (40 + 22 * k) * r.uniform(0.7, 1.2)
                td.ellipse([x + w / 2 - ww, yy - 26, x + w / 2 + ww, yy + 26], fill=(3, 8, 10, 255))
            x += r.uniform(70, 190)
        water = grad(H - 1240, [(0, (10, 22, 34)), (1, (2, 4, 8))], EXT)
        refl = trees.crop((0, 1240 - 620, EXT, 1240)).transpose(Image.FLIP_TOP_BOTTOM)
        refl.putalpha(refl.getchannel("A").point(lambda a: a // 4)); water.alpha_composite(refl.resize((EXT, H - 1240)).filter(ImageFilter.GaussianBlur(4)))
        fog = Image.new("RGBA", (EXT, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
        for k in range(9): fd.ellipse([k * 180 - 200, 1120 + (k % 3) * 40, k * 180 + 260, 1300 + (k % 3) * 40], fill=(150, 190, 210, 60))
        ufo = Image.new("RGBA", (560, 1400), (0, 0, 0, 0)); ud = ImageDraw.Draw(ufo)
        ud.polygon([(250, 120), (310, 120), (520, 1400), (40, 1400)], fill=(190, 255, 230, 60))
        ud.ellipse([110, 70, 450, 170], fill=(40, 50, 70, 255), outline=(150, 255, 220, 255), width=6); ud.ellipse([200, 20, 360, 110], fill=(120, 230, 210, 220))
        for i in range(6): ud.ellipse([135 + i * 55, 115, 155 + i * 55, 135], fill=YEL + (255,))
        return dict(sky=sky, trees=trees, water=water, fog=fog.filter(ImageFilter.GaussianBlur(40)), ufo=glow(ufo, 25, 1.2))

    def mk_studio(self):
        """Cuarto gamer nocturno (ilustración original): pared con LEDs, tele con atardecer synthwave, consola y mando."""
        wall = grad(H, [(0, (10, 4, 26)), (0.5, (24, 8, 52)), (0.7, (14, 6, 30)), (1, (4, 2, 10))], EXT); d = ImageDraw.Draw(wall)
        for x in range(0, EXT, 120): d.line([(x, 0), (x, 1180)], fill=(255, 255, 255, 10), width=2)
        shelf = Image.new("RGBA", (EXT, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shelf); r = np.random.default_rng(7)
        for sx in (60, EXT - 420):
            for k in range(3):
                y = 360 + k * 230; sd.rectangle([sx, y, sx + 360, y + 16], fill=(40, 20, 70, 255))
                x = sx + 20
                while x < sx + 330:
                    w = r.uniform(30, 70); h = r.uniform(60, 170); col = [PINK, CYAN, YEL, (140, 90, 255)][int(r.integers(4))]
                    sd.rounded_rectangle([x, y - h, x + w, y], radius=8, fill=(20, 10, 40, 255), outline=col + (200,), width=4); x += w + r.uniform(12, 30)
        tv = Image.new("RGBA", (860, 520), (0, 0, 0, 0)); td = ImageDraw.Draw(tv)
        scr = grad(460, [(0, (40, 10, 90)), (0.55, (255, 70, 150)), (0.62, (255, 190, 90)), (0.63, (30, 10, 60)), (1, (10, 4, 30))], 800)
        sdd = ImageDraw.Draw(scr); sdd.ellipse([280, 120, 520, 360], fill=(255, 190, 90, 255))
        for k in range(7): yy = 245 + k * 16; sdd.rectangle([270, yy, 530, yy + 3 + k], fill=(255, 70, 150, 255))
        for k in range(12):
            z = k / 12; yy = 290 + 170 * z ** 1.6; sdd.line([(0, yy), (800, yy)], fill=(255, 80, 200, 160), width=2)
        for k in range(-8, 9): sdd.line([(400 + k * 30, 290), (400 + k * 140, 460)], fill=(255, 80, 200, 140), width=2)
        td.rounded_rectangle([0, 0, 860, 520], radius=26, fill=(6, 4, 10, 255)); tv.alpha_composite(scr, (30, 30))
        desk = grad(H - 1430, [(0, (30, 14, 50)), (1, (8, 4, 14))], EXT)
        pad = Image.new("RGBA", (360, 220), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
        pd.ellipse([0, 40, 170, 220], fill=(16, 10, 26, 255)); pd.ellipse([190, 40, 360, 220], fill=(16, 10, 26, 255)); pd.rounded_rectangle([60, 30, 300, 150], radius=60, fill=(16, 10, 26, 255))
        pd.rounded_rectangle([130, 56, 230, 76], radius=8, fill=CYAN + (255,))
        for cx, cy in ((90, 100), (270, 100)): pd.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(60, 50, 80, 255))
        return dict(wall=wall, shelf=shelf, tv=tv, desk=desk, pad=pad)

SC = Scenes()

def background(scene, t, beat_t, pin_state=None):
    if scene == "city":
        c = SC.get("city"); ox = int(200 + 140 * math.sin(t * 0.25))
        fr = c["sky"].crop((ox // 3, 0, ox // 3 + W, H)).copy()
        fr.alpha_composite(c["far"].crop((ox // 2, 0, ox // 2 + W, H))); fr.alpha_composite(c["near"].crop((ox, 0, ox + W, H)))
        wt = c["water"].crop((ox, 0, ox + W, c["water"].height)); fr.alpha_composite(wt, (0, 1270))
        d = ImageDraw.Draw(fr)
        for k in range(14):
            y = 1290 + k * 45 + (t * 40 % 45); xs = (k * 173 + t * 60) % W
            d.line([(xs, y), (xs + 120, y)], fill=(255, 160, 220, 70), width=3)
        sway = int(10 * math.sin(t * 1.3)); fr.alpha_composite(c["palms"], (sway, 0))
        return fr
    if scene == "beach":
        c = SC.get("beach"); ox = int(200 + 100 * math.sin(t * 0.3))
        fr = c["sky"].crop((ox // 2, 0, ox // 2 + W, H)).copy(); fr.alpha_composite(c["sea"].crop((ox, 0, ox + W, c["sea"].height)), (0, 1180))
        d = ImageDraw.Draw(fr)
        for k in range(18):
            y = 1200 + k * 30; w = 60 + k * 14; xs = (k * 211 + t * (30 + k * 6)) % (W + 200) - 100
            d.line([(xs, y), (xs + w, y)], fill=(255, 230, 180, 120), width=3)
        fr.alpha_composite(c["sand"].crop((0, 0, W, 380)), (0, 1560 + int(6 * math.sin(t))))
        sway = int(14 * math.sin(t * 1.1)); fr.alpha_composite(c["palms"], (sway, 0))
        return fr
    if scene == "highway":
        c = SC.get("highway"); ox = int(200 + 60 * math.sin(t * 0.2))
        fr = c["sky"].crop((ox // 2, 0, ox // 2 + W, H)).copy(); fr.alpha_composite(c["city"].crop((ox, 0, ox + W, H)))
        d = ImageDraw.Draw(fr); hz = 1000
        d.polygon([(470, hz), (610, hz), (W + 500, H), (-500, H)], fill=(20, 10, 34, 255))
        for side in (-1, 1):
            d.line([(540 + side * 70, hz), (540 + side * 1050, H)], fill=PINK + (255,), width=6)
        for k in range(10):
            z = ((k / 10) + t * 1.4) % 1; y0 = hz + (H - hz) * z ** 2.2; y1 = hz + (H - hz) * min(1, (z + 0.04)) ** 2.2
            wd = 4 + 26 * z ** 2; d.polygon([(540 - wd * 0.3, y0), (540 + wd * 0.3, y0), (540 + wd, y1), (540 - wd, y1)], fill=(255, 220, 120, 230))
            for side in (-1, 1):
                x0 = 540 + side * (80 + 1100 * z ** 2.2); d.ellipse([x0 - 6 - 10 * z, y0 - 6 - 10 * z, x0 + 6 + 10 * z, y0 + 6 + 10 * z], fill=(CYAN if side < 0 else YEL) + (200,))
        bob = int(4 * math.sin(t * 9)); fr.alpha_composite(c["car"], (W // 2 - 310, 1330 + bob))
        return fr
    if scene == "police":
        c = SC.get("police"); ox = int(200 + 60 * math.sin(t * 0.3))
        fr = c["base"].crop((ox, 0, ox + W, H)).copy(); fr.alpha_composite(c["water"].crop((ox, 0, ox + W, c["water"].height)), (0, 1270))
        ph = (t * 4) % 2
        a = 1 - abs((ph % 1) - 0.5) * 2
        lay = c["red"] if ph < 1 else c["blue"]
        l2 = lay.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * (0.4 + 0.6 * a)))); fr.alpha_composite(l2)
        d = ImageDraw.Draw(fr)
        for i in range(8):
            on = (int(t * 8) + i) % 2 == 0; col = (RED if i < 4 else (40, 100, 255)) + (255 if on else 60,)
            d.rounded_rectangle([140 + i * 100, 220, 220 + i * 100, 250], radius=10, fill=col)
        return fr
    if scene == "map":
        c = SC.get("map"); MW, MH = c["size"]
        tgt_zoom, tx, ty = 1.0, MW / 2, MH / 2 + 80
        if pin_state is not None and pin_state.get("target") is not None:
            px, py = pin_state["target"]; tgt_zoom, tx, ty = 1.9, px, py + 120
        prev = pin_state.get("prev", (1.0, MW / 2, MH / 2 + 80)) if pin_state else (1.0, MW / 2, MH / 2 + 80)
        e = ease(beat_t / 0.8); z = lerp(prev[0], tgt_zoom, e); cx = lerp(prev[1], tx, e); cy = lerp(prev[2], ty, e)
        cw, ch = MW / z * (W / MW) * (MW / W), 0
        cw = W * (MW / W) / z * (W / MW) * (MW / 1800) * 1.66 / 1.66  # ventana base = mapa entero en ancho
        cw = min(MW / z * 0.92, (MH / z) * W / H); ch = cw * H / W
        x0 = max(0, min(MW - cw, cx - cw / 2)); y0 = max(0, min(MH - ch, cy - ch / 2))
        fr = c["map"].crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
        d = ImageDraw.Draw(fr); d.text((40, 1830), "Ilustración no oficial", font=F(30, "xbold"), fill=(200, 230, 255, 170))
        show = pin_state.get("show", []) if pin_state else []
        for i, (px, py) in enumerate(c["pins"]):
            if i not in show: continue
            sx = (px - x0) * W / cw; sy = (py - y0) * H / ch
            hot = pin_state.get("hot") and i in pin_state["hot"]
            r = 22 + (10 * (0.5 + 0.5 * math.sin(t * 8)) if hot else 0)
            d.ellipse([sx - r - 14, sy - r - 14, sx + r + 14, sy + r + 14], outline=(YEL if hot else WHITE) + (180,), width=5)
            d.ellipse([sx - r * 0.6, sy - r * 0.6, sx + r * 0.6, sy + r * 0.6], fill=(YEL if hot else PINK) + (255,))
        return fr
    if scene in ("night", "ufo"):
        c = SC.get("night"); ox = int(200 + 120 * math.sin(t * 0.22))
        fr = c["sky"].crop((ox // 3, 0, ox // 3 + W, H)).copy()
        if scene == "ufo":
            fr.alpha_composite(c["ufo"], (int(W / 2 - 280 + 60 * math.sin(t * 0.9)), int(80 + 20 * math.sin(t * 2.1))))
        fr.alpha_composite(c["trees"].crop((ox, 0, ox + W, H))); fr.alpha_composite(c["water"].crop((ox, 0, ox + W, c["water"].height)), (0, 1240))
        fx_ = int((t * 25) % 400); fr.alpha_composite(c["fog"].crop((fx_, 0, fx_ + W, H)))
        d = ImageDraw.Draw(fr)
        for k in range(22):  # luciérnagas
            x = (k * 137 + 40 * math.sin(t * 0.8 + k)) % W; y = 900 + (k * 71) % 700 + 30 * math.sin(t * 1.3 + k * 2)
            a = int(120 + 120 * math.sin(t * 3 + k)); r = 5 + k % 3
            d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 255, 120, max(0, a)))
        return fr
    if scene == "studio":
        c = SC.get("studio"); ox = int(200 + 90 * math.sin(t * 0.25))
        fr = c["wall"].crop((ox // 3, 0, ox // 3 + W, H)).copy(); fr.alpha_composite(c["shelf"].crop((ox // 2, 0, ox // 2 + W, H)))
        hue = (t * 0.35) % 1; led = tuple(int(255 * (0.5 + 0.5 * math.sin(2 * math.pi * (hue + k / 3)))) for k in range(3))
        strip = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(strip).rectangle([0, 1150, W, 1185], fill=led + (255,))
        fr.alpha_composite(glow(strip, 40, 1.6))
        tvx = W // 2 - 430 + int(20 * math.sin(t * 0.25)); g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([tvx - 30, 880, tvx + 890, 1440], radius=40, fill=(255, 90, 170, 90)); fr.alpha_composite(g.filter(ImageFilter.GaussianBlur(50)))
        fr.alpha_composite(c["tv"], (tvx, 900)); d = ImageDraw.Draw(fr)
        sl = int((t * 120) % 460); d.rectangle([tvx + 30, 930 + sl, tvx + 830, 936 + sl], fill=(255, 255, 255, 40))
        fr.alpha_composite(c["desk"].crop((ox, 0, ox + W, c["desk"].height)), (0, 1430))
        fr.alpha_composite(c["pad"], (W // 2 - 180, 1610 + int(5 * math.sin(t * 2))))
        return fr
    raise ValueError(scene)

VIGNETTE = None
def vignette():
    global VIGNETTE
    if VIGNETTE is None:
        y, x = np.mgrid[0:H, 0:W]; r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.7)) ** 2)
        a = np.clip((r - 0.55) * 300, 0, 200).astype(np.uint8); top = np.zeros((H, W), np.uint8)
        top[:420] = np.linspace(150, 0, 420)[:, None].astype(np.uint8)
        a = np.maximum(a, top); v = np.zeros((H, W, 4), np.uint8); v[..., 3] = a; VIGNETTE = Image.fromarray(v, "RGBA")
    return VIGNETTE

# ---------------- texto ----------------
def parse(markup):
    out, hl, buf = [], False, ""
    for ch in markup + " ":
        if ch == "*": hl = not hl; continue
        if ch == " ":
            if buf: out.append((buf, hl)); buf = ""
        else: buf += ch
    # el resaltado se aplica a la palabra en la que estaba activo
    return out

def words_hl(markup):
    res, hl, cur = [], False, ""
    for ch in markup:
        if ch == "*": hl = not hl; continue
        if ch == " ":
            if cur: res.append((cur, hl_word)); cur = ""
            continue
        if not cur: hl_word = hl
        cur += ch
        if hl: hl_word = True
    if cur: res.append((cur, hl_word))
    return res

def big_text_lines(markup, size, max_w=960, max_lines=3, kind="anton"):
    ws = words_hl(markup)
    while True:
        f = F(size, kind); sp = f.getlength(" "); lines, cur, cw = [], [], 0
        for w, h in ws:
            ww = f.getlength(w)
            if cur and cw + sp + ww > max_w: lines.append(cur); cur, cw = [], 0
            cw = cw + (sp if cur else 0) + ww; cur.append((w, h, ww))
        if cur: lines.append(cur)
        if (len(lines) <= max_lines and all(sum(x[2] for x in l) + sp * (len(l) - 1) <= max_w for l in lines)) or size < 60: break
        size -= 8
    imgs = []
    for l in lines:
        lw = sum(x[2] for x in l) + sp * (len(l) - 1); asc, desc = f.getmetrics(); st = max(6, size // 14)
        im = Image.new("RGBA", (int(lw) + st * 4 + 20, asc + desc + st * 4 + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = st * 2 + 6
        for w, h, ww in l:
            d.text((x + 8, st * 2 + 10), w, font=f, fill=(0, 0, 0, 150))
            d.text((x, st * 2), w, font=f, fill=YEL if h else WHITE, stroke_width=st, stroke_fill=BLACK); x += ww + sp
        imgs.append(im)
    return imgs

def simple(text, size, fill=WHITE, kind="anton", stroke=None, max_w=980):
    while F(size, kind).getlength(text) > max_w and size > 30: size -= 6
    f = F(size, kind); st = stroke if stroke is not None else max(4, size // 14); asc, desc = f.getmetrics()
    im = Image.new("RGBA", (int(f.getlength(text)) + st * 4 + 20, asc + desc + st * 4 + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((st * 2 + 8, st * 2 + 10), text, font=f, fill=(0, 0, 0, 140)); d.text((st * 2, st * 2), text, font=f, fill=fill, stroke_width=st, stroke_fill=BLACK)
    return im

def label(text, color=PINK):
    f = F(40, "black"); tw = int(sum(f.getlength(c) + 5 for c in text))
    im = Image.new("RGBA", (tw + 60, 78), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 77], radius=39, fill=color + (255,)); x = 30
    for c in text: d.text((x, 12), c, font=f, fill=WHITE); x += f.getlength(c) + 5
    return im

def paste(fr, img, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if alpha <= 0 or scale <= 0.01: return
    if scale != 1 or rot:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
        if rot: img = img.rotate(rot, expand=True, resample=Image.BILINEAR)
    if alpha < 1:
        img = img.copy(); img.putalpha(img.getchannel("A").point(lambda a: int(a * alpha)))
    fr.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2))) if (0 <= cx - img.width / 2 and cy - img.height / 2 >= 0 and cx + img.width / 2 <= W and cy + img.height / 2 <= H) else _paste_clip(fr, img, int(cx - img.width / 2), int(cy - img.height / 2))

def _paste_clip(fr, img, x, y):
    l, t = max(0, -x), max(0, -y); r, b = min(img.width, W - x), min(img.height, H - y)
    if r > l and b > t: fr.alpha_composite(img.crop((l, t, r, b)), (x + l, y + t))

def slam(t, t0=0.0, d=0.28):
    p = (t - t0) / d
    if p <= 0: return 0, 0
    return (1 + 0.6 * (1 - back(p))) if p < 1 else 1, min(1, p * 2.5)

def badge(kind, s=120):
    S = s * 2; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    col = {"ok": GREEN, "no": RED, "q": GREY, "star": YEL, "num": YEL}[kind]
    d.ellipse([6, 6, S - 6, S - 6], fill=col + (255,), outline=BLACK + (255,), width=10); lw = S // 10
    if kind == "ok": d.line([(S * .27, S * .52), (S * .44, S * .69), (S * .75, S * .33)], fill=BLACK, width=lw, joint="curve")
    elif kind == "no": d.line([(S * .3, S * .3), (S * .7, S * .7)], fill=BLACK, width=lw); d.line([(S * .7, S * .3), (S * .3, S * .7)], fill=BLACK, width=lw)
    elif kind == "q": f = F(int(S * .62)); d.text((S / 2 - f.getlength("?") / 2, S * .06), "?", font=f, fill=BLACK)
    elif kind == "star": d.polygon(star_pts(S / 2, S / 2 + 4, S * .32), fill=BLACK)
    return im.resize((s, s), Image.LANCZOS)

def star_pts(cx, cy, r):
    return [(cx + (r if i % 2 == 0 else r * .45) * math.cos(-math.pi / 2 + i * math.pi / 5), cy + (r if i % 2 == 0 else r * .45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]

def star_img(s, on=True):
    im = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon(star_pts(s, s, s * 0.95), fill=(YEL + (255,)) if on else (255, 255, 255, 50), outline=BLACK + (255,) if on else None)
    im = im.resize((s, s), Image.LANCZOS); return glow(im, 10, 1.5) if on else im

# ---------------- subtítulos ----------------
def chunks(say):
    ws = say.split(); out, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= 3 or w[-1] in ".,:;?!": out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def cap_img(words, active):
    size = 86
    while True:
        f = F(size); sp = f.getlength(" "); tot = sum(f.getlength(w.upper()) for w in words) + sp * (len(words) - 1)
        if tot < 940 or size < 50: break
        size -= 6
    st = 7; asc, desc = f.getmetrics(); im = Image.new("RGBA", (int(tot) + 60, asc + desc + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 30
    for i, w in enumerate(words):
        W_ = w.upper(); d.text((x, 14), W_, font=f, fill=(YEL if i == active else WHITE), stroke_width=st, stroke_fill=BLACK); x += f.getlength(W_) + sp
    return im

def fmt_num(v, dec=0):
    if dec: return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{int(round(v)):,}".replace(",", ".")

# ---------------- escena ----------------
class Beat:
    def __init__(self, b, n, idx, prev_pin):
        self.b, self.n, self.idx = b, n, idx; self.dur = n / FPS; self.cache = {}
        self.chunks = chunks(b["say"]); speech = max(0.3, self.dur - 0.25)
        flat = [(ci, wi, w) for ci, ch in enumerate(self.chunks) for wi, w in enumerate(ch)]
        tot = sum(len(w) + 2 for _, _, w in flat); t = 0.06; self.times = []
        for ci, wi, w in flat: self.times.append((t, ci, wi)); t += (len(w) + 2) / tot * (speech - 0.06)
        self.shake_t = 0.0 if b.get("sfx") in ("boom", "slam") else None
        self.prep(prev_pin)

    def prep(self, prev_pin):
        b = self.b; fx = b["fx"]; c = self.cache
        if fx == "title": c["lines"] = big_text_lines(b["text"], 170)
        elif fx == "stamp":
            fs = 430
            while F(fs).getlength(b["text"]) > 760 and fs > 200: fs -= 20
            f = F(fs); tw = int(f.getlength(b["text"])); st = Image.new("RGBA", (tw + 160, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
            d.rounded_rectangle([10, 10, st.width - 10, 550], radius=50, outline=RED + (255,), width=26, fill=(30, 0, 8, 170)); d.text((80, -20 + (430 - fs) * 0.55), b["text"], font=f, fill=RED, stroke_width=10, stroke_fill=BLACK)
            c["stamp"] = glow(st.rotate(-8, expand=True, resample=Image.BICUBIC), 20)
        elif fx == "big":
            c["label"] = label(b["label"]); c["val"] = glow(simple(b["value"], 300, YEL, max_w=1000), 25, 0.8)
            if b.get("sub"): c["sub"] = simple(b["sub"], 56, WHITE, "black", stroke=5, max_w=960)
        elif fx == "list":
            n = len(b["items"]); sz = 120 if n <= 3 else 100
            c["rows"] = []
            for m, txt in b["items"]:
                t = simple(txt, sz, WHITE, max_w=760); bd = badge(m, int(sz * 1.1)); row = Image.new("RGBA", (bd.width + 30 + t.width, max(bd.height, t.height)), (0, 0, 0, 0))
                row.alpha_composite(bd, (0, (row.height - bd.height) // 2)); row.alpha_composite(t, (bd.width + 30, (row.height - t.height) // 2)); c["rows"].append(row)
        elif fx == "timeline":
            c["pts"] = [(simple(a, 86, YEL), simple(l, 92, WHITE)) for a, l in b["points"]]
        elif fx == "stars":
            c["title"] = big_text_lines(b["text"], 170)
        elif fx == "num":
            c["badge"] = badge("num", 260); f = F(200); d = ImageDraw.Draw(c["badge"]); s = str(b["n"]); d.text((130 - f.getlength(s) / 2, 2), s, font=f, fill=BLACK)
            c["lines"] = big_text_lines(b["text"], 150)
        elif fx == "pin":
            c["name"] = simple(b["text"], 130, YEL, max_w=980); c["sub"] = label(b["sub"].upper(), PINK)
        elif fx == "vs":
            c["a"] = simple(b["a"], 210, WHITE); c["b"] = simple(b["b"], 210, YEL)
        elif fx == "counter":
            c["label"] = label(b["label"])
            if b.get("sub"): c["sub"] = simple(b["sub"], 56, WHITE, "black", stroke=5, max_w=960)
        elif fx == "bars":
            vals = [v for _, v in b["bars"]]; c["max"] = max(vals)
            c["names"] = [simple(n, 64, WHITE, "black", stroke=5, max_w=900) for n, _ in b["bars"]]
            c["vals"] = [simple(b["vlabels"][i] if b.get("vlabels") else b.get("fmt", "{}").format(fmt_num(v)), 84, YEL, max_w=400) for i, (_, v) in enumerate(b["bars"])]
            if b.get("title"): c["title"] = big_text_lines(b["title"], 110, max_lines=2)
        elif fx == "gauge":
            c["label"] = label(b["label"])
            if b.get("sub"): c["sub"] = simple(b["sub"], 56, WHITE, "black", stroke=5, max_w=960)
            c["marks"] = [(m, simple(str(m), 64, WHITE, "black", stroke=5)) for m in b.get("marks", [])]
        elif fx == "phone":
            ph = Image.new("RGBA", (640, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
            d.rounded_rectangle([0, 0, 640, 1000], radius=70, fill=(10, 8, 18, 255), outline=(255, 255, 255, 200), width=10)
            d.rounded_rectangle([24, 24, 616, 976], radius=52, fill=(26, 14, 48, 255)); d.rounded_rectangle([250, 40, 390, 72], radius=16, fill=(6, 4, 10, 255))
            ttl = b.get("app", "LEONIDA"); d.text((320 - F(54, "black").getlength(ttl) / 2, 90), ttl, font=F(54, "black"), fill=CYAN)
            c["ph"] = glow(ph, 22, 0.7); c["msgs"] = []
            for who, txt in b["items"]:
                f = F(44, "xbold"); words = txt.split(); lines, cur = [], ""
                for w_ in words:
                    if f.getlength((cur + " " + w_).strip()) > 470: lines.append(cur); cur = w_
                    else: cur = (cur + " " + w_).strip()
                lines.append(cur); hh = 40 + 56 * len(lines) + (46 if who else 0)
                m = Image.new("RGBA", (540, hh), (0, 0, 0, 0)); md = ImageDraw.Draw(m)
                md.rounded_rectangle([0, 0, 540, hh], radius=30, fill=(255, 255, 255, 240)); y = 18
                if who: md.text((26, y), who, font=F(36, "black"), fill=PINK); y += 46
                for l in lines: md.text((26, y), l, font=f, fill=(20, 10, 30)); y += 56
                c["msgs"].append(m)
        elif fx == "cta":
            c["name"] = simple(CHANNEL, 140, WHITE); c["handle"] = simple(HANDLE, 64, CYAN, "black", stroke=5)
            c["btn"] = label("SÍGUEME", RED); c["btn"] = c["btn"].resize((c["btn"].width * 2, c["btn"].height * 2), Image.LANCZOS)
            st = Image.new("RGBA", (500, 500), (0, 0, 0, 0)); d = ImageDraw.Draw(st); d.polygon(star_pts(250, 260, 240), fill=YEL, outline=BLACK, width=12)
            f = F(220); d.text((250 - f.getlength("6") / 2, 120), "6", font=f, fill=BLACK); c["star"] = glow(st.resize((330, 330), Image.LANCZOS), 20)
        # estado de mapa
        self.pin_state = None
        if b["scene"] == "map":
            pins = SC.get("map")["pins"]; p = b.get("pin"); prev = prev_pin or (1.0, 900, 1380)
            if p is None: self.pin_state = dict(target=None, show=[], prev=prev)
            elif p == "all": self.pin_state = dict(target=None, show=list(range(6)), prev=prev, hot=list(range(6)))
            else:
                ids = p if isinstance(p, list) else [p]; xs = [pins[i] for i in ids]; tgt = (sum(x for x, _ in xs) / len(xs), sum(y for _, y in xs) / len(xs))
                self.pin_state = dict(target=tgt, show=list(range(6)), prev=prev, hot=ids)
            st = self.pin_state; self.end_pin = (1.9, st["target"][0], st["target"][1] + 120) if st["target"] else (1.0, 900, 1380)
        else: self.end_pin = None

    def fg(self, fr, t):
        b, c, fx = self.b, self.cache, self.b["fx"]
        if fx == "title":
            n = len(c["lines"]); hs = sum(l.height for l in c["lines"]) - 20 * (n - 1); y = 700 - hs / 2
            for i, l in enumerate(c["lines"]):
                s, a = slam(t, 0.05 + i * 0.12); paste(fr, l, W / 2, y + l.height / 2, s, a); y += l.height - 20
        elif fx == "stamp":
            s, a = slam(t, 0.02, 0.22); paste(fr, c["stamp"], W / 2, 720, s * (1 + 0.5 * (s > 1)), a)
        elif fx == "big":
            s, a = slam(t, 0.0, 0.25); paste(fr, c["label"], W / 2, 430, 1, a)
            s, a = slam(t, 0.12); paste(fr, c["val"], W / 2, 680, s, a)
            if "sub" in c: s, a = slam(t, 0.35, 0.3); paste(fr, c["sub"], W / 2, 930, 1, a)
        elif fx == "list":
            n = len(c["rows"]); span = max(0.4, self.dur - 0.9); gap = 175 if n <= 3 else 150; y0 = 700 - (n - 1) * gap / 2
            for i, r in enumerate(c["rows"]):
                t0 = 0.1 + span * i / n; s, a = slam(t, t0, 0.22); paste(fr, r, W / 2, y0 + i * gap, s, a)
        elif fx == "timeline":
            d = ImageDraw.Draw(fr); y = 720; t2 = self.dur * 0.5; p = ease((t - t2 + 0.4) / 0.5)
            d.line([(150, y), (930, y)], fill=(255, 255, 255, 90), width=14)
            if p > 0: d.line([(150, y), (150 + 780 * p, y)], fill=YEL + (255,), width=16)
            for i, (x, t0) in enumerate(((220, 0.1), (860, t2))):
                s, a = slam(t, t0)
                if a <= 0: continue
                r = 34 * s; d.ellipse([x - r, y - r, x + r, y + r], fill=YEL + (255,), outline=BLACK + (255,), width=8)
                da, lb = c["pts"][i]; paste(fr, da, x, y - 150, s, a); paste(fr, lb, x, y + 140, s, a)
        elif fx == "stars":
            for i, l in enumerate(c["title"]):
                s, a = slam(t, 0.05); paste(fr, l, W / 2, 480 + i * (l.height - 20), s, a)
            for i in range(6):
                on = t > 0.4 + i * 0.22; img = self.cache.setdefault(("st", on), star_img(150, on))
                sc = 1.0
                if on and t - (0.4 + i * 0.22) < 0.2: sc = 1 + 0.6 * (1 - (t - (0.4 + i * 0.22)) / 0.2)
                paste(fr, img, 105 + i * 174, 820, sc, 1)
        elif fx == "num":
            s, a = slam(t, 0.0, 0.25); paste(fr, c["badge"], W / 2, 450, s, a, rot=int(8 * math.sin(t * 3)))
            n = len(c["lines"]); y = 720
            for i, l in enumerate(c["lines"]):
                s, a = slam(t, 0.15 + i * 0.1); paste(fr, l, W / 2, y + l.height / 2, s, a); y += l.height - 20
        elif fx == "pin":
            s, a = slam(t, 0.2); paste(fr, c["name"], W / 2, 420, s, a); s, a = slam(t, 0.35); paste(fr, c["sub"], W / 2, 560, 1, a)
        elif fx == "vs":
            s, a = slam(t, 0.05); paste(fr, c["a"], W / 2, 480, s, a)
            s2, a2 = slam(t, 0.45); paste(fr, c["b"], W / 2, 900, s2, a2)
            if a2 > 0:
                d = ImageDraw.Draw(fr); ang = t * 4
                for k in (0, math.pi):
                    x = W / 2 + 120 * math.cos(ang + k); y = 690 + 40 * math.sin(ang + k); d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=PINK + (255,), outline=BLACK + (255,), width=5)
                d.arc([W / 2 - 140, 630, W / 2 + 140, 750], 0, 360, fill=WHITE + (160,), width=6)
        elif fx == "counter":
            s, a = slam(t, 0.0, 0.25); paste(fr, c["label"], W / 2, 430, 1, a)
            p = ease(min(1, t / max(0.4, b.get("roll", 1.2)))); v = b["value"] * p
            txt = b.get("prefix", "") + fmt_num(v, b.get("dec", 0)) + b.get("suffix", "")
            done = p >= 1; key = ("cnt", txt)
            if key not in c: c[key] = glow(simple(txt, 280, YEL if done else WHITE, max_w=1000), 25, 0.8 if done else 0.4)
            sc = 1.0 + (0.18 * max(0, 1 - (t - b.get("roll", 1.2)) / 0.25) if done else 0)
            paste(fr, c[key], W / 2, 680, sc, 1)
            if "sub" in c: paste(fr, c["sub"], W / 2, 920, 1, slam(t, 0.3, 0.3)[1])
        elif fx == "bars":
            n = len(c["names"]); y0 = 400
            if "title" in c:
                y = 260
                for i, l in enumerate(c["title"]): s, a = slam(t, 0.0); paste(fr, l, W / 2, y + l.height / 2, s, a); y += l.height - 20
                y0 = y + 60
            d = ImageDraw.Draw(fr); gap = min(260, 900 / n)
            for i in range(n):
                t0 = 0.1 + i * min(0.5, (self.dur - 0.8) / n); p = ease((t - t0) / 0.7)
                if t < t0: continue
                y = y0 + i * gap; paste(fr, c["names"][i], 90 + c["names"][i].width / 2, y, 1, min(1, (t - t0) * 4))
                bw = max(8, 900 * (b["bars"][i][1] / c["max"]) * p); col = YEL if b["bars"][i][1] == c["max"] else CYAN
                d.rounded_rectangle([90, y + 50, 90 + bw, y + 130], radius=18, fill=col + (255,), outline=BLACK + (255,), width=6)
                if p > 0.6: v = c["vals"][i]; paste(fr, v, min(W - v.width / 2 - 10, 90 + bw - v.width / 2 - 14) if bw > v.width + 30 else 90 + bw + v.width / 2 + 10, y + 90, 1, 1)
        elif fx == "gauge":
            s, a = slam(t, 0.0, 0.25); paste(fr, c["label"], W / 2, 330, 1, a)
            d = ImageDraw.Draw(fr); cx, cy, R = W / 2, 900, 320; mx = b["max"]
            d.arc([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=(255, 255, 255, 70), width=46)
            p = ease(min(1, t / max(0.4, b.get("roll", 1.0)))); v = b["value"] * p
            d.arc([cx - R, cy - R, cx + R, cy + R], 180, 180 + 180 * v / mx, fill=(YEL if p >= 1 else CYAN) + (255,), width=46)
            for m, img in c["marks"]:
                ang = math.pi * (1 + m / mx); x1, y1 = cx + (R + 40) * math.cos(ang), cy + (R + 40) * math.sin(ang)
                d.line([(cx + (R - 30) * math.cos(ang), cy + (R - 30) * math.sin(ang)), (x1, y1)], fill=WHITE + (255,), width=8)
                paste(fr, img, cx + (R + 95) * math.cos(ang), cy + (R + 75) * math.sin(ang), 1, 1)
            wob = (0.015 * math.sin(t * 40) if p >= 1 else 0); ang = math.pi * (1 + v / mx + wob)
            d.line([(cx, cy), (cx + (R - 50) * math.cos(ang), cy + (R - 50) * math.sin(ang))], fill=RED + (255,), width=16)
            d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=BLACK + (255,), outline=RED + (255,), width=8)
            txt = fmt_num(v, b.get("dec", 0)) + b.get("suffix", ""); key = ("g", txt)
            if key not in c: c[key] = glow(simple(txt, 220, YEL if p >= 1 else WHITE, max_w=900), 22, 0.7)
            paste(fr, c[key], W / 2, 1050, 1.0 + (0.15 * max(0, 1 - (t - b.get("roll", 1.0)) / 0.25) if p >= 1 else 0), 1)
            if "sub" in c: paste(fr, c["sub"], W / 2, 1200, 1, slam(t, 0.3, 0.3)[1])
        elif fx == "phone":
            e = ease(t / 0.35); paste(fr, c["ph"], W / 2, 760 + 400 * (1 - e), 1, min(1, t * 4))
            n = len(c["msgs"]); span = max(0.4, self.dur - 0.8); y = 470
            for i, m in enumerate(c["msgs"]):
                t0 = 0.25 + span * i / n; s, a = slam(t, t0, 0.22)
                if a > 0: paste(fr, m, W / 2, y + m.height / 2, s, a)
                y += m.height + 26
        elif fx == "cta":
            s, a = slam(t, 0.0, 0.3); paste(fr, c["star"], W / 2, 430, s, a, rot=int(10 * math.sin(t * 2.5)))
            s, a = slam(t, 0.15); paste(fr, c["name"], W / 2, 700, s, a); paste(fr, c["handle"], W / 2, 820, 1, slam(t, 0.25)[1])
            pul = 1 + 0.06 * math.sin(t * 9); paste(fr, c["btn"], W / 2, 1010, pul * slam(t, 0.4)[0], slam(t, 0.4)[1])

    def caption(self, fr, t):
        if self.b["fx"] == "cta" and t > self.dur - 0.1: return
        ci, wi = 0, -1
        for t0, c_, w_ in self.times:
            if t >= t0: ci, wi = c_, w_
        if wi < 0: return
        k = ("cap", ci, wi)
        if k not in self.cache: self.cache[k] = cap_img(self.chunks[ci], wi)
        img = self.cache[k]; first = [x for x in self.times if x[1] == ci][0][0]; p = min(1, (t - first) / 0.12)
        paste(fr, img, W / 2, 1390, 0.85 + 0.15 * back(p), 1)

class Video:
    def __init__(self, v):
        self.v = v; self.durs = json.load(open(f"{ROOT}/build/{v['id']}.json")); self.total = sum(self.durs)
        self.beats = []; prev = None
        for i, (b, n) in enumerate(zip(v["beats"], self.durs)):
            bt = Beat(b, n, i, prev); self.beats.append(bt)
            if bt.end_pin: prev = bt.end_pin
        self.brand = self.mk_brand()

    def mk_brand(self):
        im = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon(star_pts(80, 120, 30), fill=YEL, outline=BLACK, width=3); d.text((124, 96), CHANNEL, font=F(40, "black"), fill=WHITE, stroke_width=3, stroke_fill=BLACK)
        return im

    def frame(self, bi, f):
        bt = self.beats[bi]; t = f / FPS; g = sum(self.durs[:bi]) + f; T = g / FPS
        fr = background(bt.b["scene"], T, t, bt.pin_state)
        fr.alpha_composite(vignette())
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bt.fg(layer, t + ((0.6 if bt.b["fx"] not in ("counter", "bars", "gauge") else 0.35) if bi == 0 else 0)); bt.caption(layer, max(t, 0.07) if bi == 0 else t)
        dx = dy = 0
        if bt.shake_t is not None and t < 0.35:
            k = (1 - t / 0.35) * 18; dx, dy = int(rng.uniform(-k, k)), int(rng.uniform(-k, k))
        fr.alpha_composite(layer, (dx, dy)) if dx >= 0 and dy >= 0 else _paste_clip(fr, layer, dx, dy)
        fr.alpha_composite(self.brand)
        d = ImageDraw.Draw(fr); d.rectangle([0, 0, W, 10], fill=(0, 0, 0, 120)); d.rectangle([0, 0, int(W * (g + 1) / self.total), 10], fill=YEL + (255,))
        if bi > 0 and f < 5:  # transición: destello + barrido
            fl = Image.new("RGBA", (W, H), (255, 255, 255, [150, 90, 50, 25, 10][f])); fr.alpha_composite(fl)
        return fr

    def render(self, out_dir=None):
        out_dir = out_dir or f"{ROOT}/build/{self.v['id']}"; os.makedirs(out_dir, exist_ok=True); files = []
        for bi, n in enumerate(self.durs):
            fin = f"{out_dir}/s{bi:02d}.mp4"; tmp = f"{out_dir}/s{bi:02d}.tmp.mp4"
            p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                  "-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
            for f in range(n): p.stdin.write(self.frame(bi, f).convert("RGB").tobytes())
            p.stdin.close()
            if p.wait() != 0: raise RuntimeError(fin)
            os.replace(tmp, fin); files.append(fin)
        lst = f"{out_dir}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in files))
        silent = f"{out_dir}/video.mp4"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
        os.makedirs(f"{ROOT}/out", exist_ok=True); final = f"{ROOT}/out/GTA6_{self.v['id']}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", f"{ROOT}/build/{self.v['id']}.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final], check=True)
        return final

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "frames":
        v = Video(next(x for x in VIDEOS2 if x["id"] == sys.argv[2])); os.makedirs(f"{ROOT}/frames", exist_ok=True)
        for spec in sys.argv[3:]:
            bi, f = map(int, spec.split(":")); f = min(f, v.durs[bi] - 1)
            v.frame(bi, f).convert("RGB").save(f"{ROOT}/frames/{v.v['id']}_{bi}_{f}.jpg", quality=85)
    else:
        for vid in sys.argv[2:]: print(Video(next(x for x in VIDEOS2 if x["id"] == vid)).render(), flush=True)
