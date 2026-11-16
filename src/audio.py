# -*- coding: utf-8 -*-
"""Voz (Piper es_MX, Apache-2.0) + música original sintetizada."""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from content import VIDEOS, spoken

ROOT = os.environ.get("SE_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VOICE = f"{ROOT}/voices/vits-piper-es_MX-claude-high"
SR = 44100
PAD = 0.28  # silencio tras cada frase

def tts_engine():
    from piper import PiperVoice
    return PiperVoice.load(f"{VOICE}/es_MX-claude-high.onnx", config_path=f"{VOICE}/es_MX-claude-high.onnx.json")

def say(tts, text):
    from piper import SynthesisConfig
    cfg = SynthesisConfig(length_scale=0.92, noise_scale=0.5, noise_w_scale=0.7)
    chunks = list(tts.synthesize(text, syn_config=cfg))
    return np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32), chunks[0].sample_rate

def resample(x, sr):
    n = int(len(x) * SR / sr)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)

def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0: return x
    a = max(0, idx[0] - int(0.02 * SR)); b = min(len(x), idx[-1] + int(0.05 * SR))
    return x[a:b]

def music(dur, seed=0):
    """Bucle synth original: Am-F-C-G, 104 bpm."""
    bpm = 104; beat = 60 / bpm; n = int(dur * SR) + SR
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    bar = beat * 4
    for i in range(int(dur / bar) + 2):
        ch = chords[(i + seed) % 4]; s = int(i * bar * SR); e = min(n, int((i + 1) * bar * SR))
        if s >= n: break
        tt = t[s:e] - t[s]
        env = np.minimum(1, tt / 0.3) * np.minimum(1, (bar - tt) / 0.3)
        pad = sum(np.sin(2 * np.pi * f(m) * tt) + 0.4 * np.sin(2 * np.pi * f(m) * 2.003 * tt) for m in ch)
        out[s:e] += 0.05 * pad * env
        for k in range(8):  # bajo en corcheas
            bs = s + int(k * beat / 2 * SR); be = min(n, bs + int(beat / 2 * SR))
            if bs >= n: break
            bt = np.arange(be - bs) / SR
            out[bs:be] += 0.16 * np.tanh(2 * np.sin(2 * np.pi * f(ch[0] - 24) * bt)) * np.exp(-bt * 7)
        for k in range(16):  # arpegio
            a_s = s + int(k * beat / 4 * SR); a_e = min(n, a_s + int(beat / 4 * SR))
            if a_s >= n: break
            at = np.arange(a_e - a_s) / SR
            note = ch[k % 3] + (12 if k % 4 == 3 else 0)
            out[a_s:a_e] += 0.045 * np.sign(np.sin(2 * np.pi * f(note + 12) * at)) * np.exp(-at * 14)
    rng = np.random.default_rng(1)
    for k in range(int(dur / beat) + 2):  # bombo + hat
        ks = int(k * beat * SR)
        if ks >= n: break
        kt = np.arange(min(int(0.25 * SR), n - ks)) / SR
        out[ks:ks + len(kt)] += 0.32 * np.sin(2 * np.pi * (45 + 90 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 14)
        hs = ks + int(beat / 2 * SR)
        if hs < n:
            ht = np.arange(min(int(0.05 * SR), n - hs)) / SR
            out[hs:hs + len(ht)] += 0.05 * rng.standard_normal(len(ht)).astype(np.float32) * np.exp(-ht * 90)
    out = np.pad(out, (0, SR))[:int(round(dur * SR)) + 2]
    fade = int(1.2 * SR); out[-fade:] *= np.linspace(1, 0, fade); out[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    return out

def main(only=None):
    tts = tts_engine()
    os.makedirs(f"{ROOT}/build", exist_ok=True)
    for vi, v in enumerate(VIDEOS):
        if only and v["id"] not in only: continue
        parts, durs = [], []
        for b in v["beats"]:
            xs, sr = say(tts, spoken(b["say"]))
            x = trim(resample(xs, sr))
            x = np.concatenate([x, np.zeros(int(PAD * SR), np.float32)])
            # redondea a fotogramas exactos (30 fps)
            fr = int(np.ceil(len(x) / SR * 30)); x = np.concatenate([x, np.zeros(fr * SR // 30 - len(x), np.float32)])
            parts.append(x); durs.append(fr)
        voice = np.concatenate(parts)
        voice = voice / max(1e-6, np.abs(voice).max()) * 0.9
        mus = np.pad(music(len(voice) / SR, seed=vi), (0, SR))
        mix = voice + 0.42 * mus[:len(voice)]
        mix = np.tanh(mix * 1.1) / np.tanh(1.1) * 0.95
        with wave.open(f"{ROOT}/build/{v['id']}.wav", "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((mix * 32767).astype(np.int16).tobytes())
        json.dump(durs, open(f"{ROOT}/build/{v['id']}.json", "w"))
        print(v["id"], f"{len(voice)/SR:.1f}s", durs, flush=True)

if __name__ == "__main__":
    main(sys.argv[1:] or None)
