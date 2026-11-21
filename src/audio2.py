# -*- coding: utf-8 -*-
"""Audio v2: voz Kokoro (Apache-2.0), efectos sintetizados y música synthwave con ducking."""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from content2 import VIDEOS2, spoken

ROOT = os.environ.get("SE_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KOK = os.path.join(ROOT, "voices", "kokoro")
SR = 44100; FPS = 30
VOICE = os.environ.get("SE_VOICE", "em_alex"); SPEED = float(os.environ.get("SE_SPEED", "1.15"))
LEAD, TAIL = 0.06, 0.14
rng = np.random.default_rng(3)

def resample(x, sr):
    if sr == SR: return x.astype(np.float32)
    n = int(len(x) * SR / sr)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)

def trim(x, thr=0.008):
    i = np.where(np.abs(x) > thr)[0]
    return x if len(i) == 0 else x[max(0, i[0] - 400): i[-1] + 1500]

# ---------- efectos ----------
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")
def sfx(name):
    if name == "boom":
        n = int(0.9 * SR); t = np.arange(n) / SR
        s = np.sin(2 * np.pi * (38 + 70 * np.exp(-t * 9)) * t) * np.exp(-t * 3.2) * 0.9
        s += lowpass(rng.standard_normal(n), 30) * np.exp(-t * 18) * 0.6
        return s
    if name == "slam":
        n = int(0.5 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (55 + 120 * np.exp(-t * 25)) * t) * np.exp(-t * 7) * 0.8 + rng.standard_normal(n) * np.exp(-t * 40) * 0.35
    if name == "whoosh":
        n = int(0.35 * SR); t = np.arange(n) / SR
        noise = rng.standard_normal(n); out = np.zeros(n)
        for k, w in ((3, 0.5), (9, 0.35), (25, 0.25)):
            out += lowpass(noise, k) * w
        e = np.sin(np.pi * np.clip(t / 0.35, 0, 1)) ** 2
        return out * e * 0.45
    if name == "riser":
        n = int(1.1 * SR); t = np.arange(n) / SR
        f = 200 + 900 * (t / 1.1) ** 2
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 + lowpass(rng.standard_normal(n), 4) * 0.25) * (t / 1.1) ** 1.5
    if name == "siren":
        n = int(1.0 * SR); t = np.arange(n) / SR
        f = np.where((t * 4).astype(int) % 2 == 0, 960, 640)
        return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.12 * np.minimum(1, (1 - t) * 4)
    if name == "pop":
        n = int(0.15 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * (900 - 500 * t / 0.15) * t) * np.exp(-t * 30) * 0.5
    if name == "tick":
        n = int(0.06 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 80) * 0.3
    return np.zeros(1)

# ---------- música ----------
def music(dur, seed=0):
    bpm = 112; beat = 60 / bpm; n = int(dur * SR) + SR; t = np.arange(n) / SR
    out = np.zeros(n, np.float32); f = lambda m: 440 * 2 ** ((m - 69) / 12)
    progs = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]]]
    chords = progs[seed % 2]; bar = beat * 4
    for i in range(int(dur / bar) + 2):
        ch = chords[i % 4]; s = int(i * bar * SR); e = min(n, int((i + 1) * bar * SR))
        if s >= n: break
        tt = t[s:e] - t[s]; en = np.minimum(1, tt / 0.05) * np.minimum(1, (bar - tt) / 0.2)
        saw = sum(((tt * f(m) * d) % 1 * 2 - 1) for m in ch for d in (1.0, 1.004))
        out[s:e] += 0.035 * lowpass(saw, 6)[: e - s] * en
        for k in range(8):
            bs = s + int(k * beat / 2 * SR); be = min(n, bs + int(beat / 2 * SR))
            if bs >= n: break
            bt = np.arange(be - bs) / SR
            out[bs:be] += 0.2 * np.tanh(3 * np.sin(2 * np.pi * f(ch[0] - 24) * bt)) * np.exp(-bt * 5)
        for k in range(16):
            a = s + int(k * beat / 4 * SR); b = min(n, a + int(beat / 4 * SR))
            if a >= n: break
            at = np.arange(b - a) / SR; note = ch[k % 3] + (12 if k % 4 == 2 else 0) + 12
            out[a:b] += 0.04 * np.sign(np.sin(2 * np.pi * f(note) * at)) * np.exp(-at * 12)
    for k in range(int(dur / beat) + 2):
        ks = int(k * beat * SR)
        if ks >= n: break
        kt = np.arange(min(int(0.3 * SR), n - ks)) / SR
        out[ks:ks + len(kt)] += 0.45 * np.sin(2 * np.pi * (48 + 110 * np.exp(-kt * 32)) * kt) * np.exp(-kt * 11)
        if k % 2 == 1:
            st = np.arange(min(int(0.2 * SR), n - ks)) / SR
            out[ks:ks + len(st)] += 0.18 * rng.standard_normal(len(st)).astype(np.float32) * np.exp(-st * 22)
        hs = ks + int(beat / 2 * SR)
        if hs < n:
            ht = np.arange(min(int(0.04 * SR), n - hs)) / SR
            out[hs:hs + len(ht)] += 0.07 * rng.standard_normal(len(ht)).astype(np.float32) * np.exp(-ht * 120)
    out = out[: int(dur * SR) + 2]
    fd = int(1.0 * SR); out[-fd:] *= np.linspace(1, 0, fd)
    return out

def tts():
    from kokoro_onnx import Kokoro
    return Kokoro(f"{KOK}/kokoro-v1.0.onnx", f"{KOK}/voices-v1.0.bin")

def main(ids=None):
    k = tts(); os.makedirs(f"{ROOT}/build", exist_ok=True)
    for vi, v in enumerate(VIDEOS2):
        if ids and v["id"] not in ids: continue
        parts, frames, fxlist = [], [], []
        for b in v["beats"]:
            a, sr = k.create(spoken(b["say"]), voice=VOICE, speed=SPEED, lang="es")
            x = trim(resample(np.asarray(a, np.float32), sr))
            x = np.concatenate([np.zeros(int(LEAD * SR), np.float32), x, np.zeros(int(TAIL * SR), np.float32)])
            fr = int(np.ceil(len(x) / SR * FPS)); x = np.pad(x, (0, fr * SR // FPS - len(x)))
            parts.append(x); frames.append(fr)
        voice = np.concatenate(parts); voice = voice / max(1e-6, np.abs(voice).max()) * 0.92
        L = len(voice); fx = np.zeros(L + SR, np.float32); pos = 0
        for i, (b, fr) in enumerate(zip(v["beats"], frames)):
            if i > 0:
                w = sfx("whoosh"); s0 = max(0, pos - int(0.12 * SR)); fx[s0:s0 + len(w)] += w
            if b.get("sfx"):
                s = sfx(b["sfx"]); fx[pos:pos + len(s)] += s[: len(fx) - pos]
            pos += fr * SR // FPS
        # ducking de la música bajo la voz
        mus = np.pad(music(L / SR, vi), (0, SR))[:L]
        e = np.abs(voice); e = np.convolve(e, np.ones(2048) / 2048, mode="same"); duck = 1 - 0.6 * np.clip(e / 0.08, 0, 1)
        mix = voice + 0.5 * mus * duck + 0.55 * fx[:L]
        mix = np.tanh(mix * 1.2) / np.tanh(1.2) * 0.96
        with wave.open(f"{ROOT}/build/{v['id']}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
        json.dump(frames, open(f"{ROOT}/build/{v['id']}.json", "w"))
        print(v["id"], f"{L/SR:.1f}s", frames, flush=True)

if __name__ == "__main__":
    main(sys.argv[1:] or None)
