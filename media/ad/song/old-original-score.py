"""Original 30s score + sound effects for the Shiftwise ad.

120 BPM (one beat = 0.5 s), so every scene change (0, 5, 9, 15, 19, 25, 27 s)
lands on a beat. Everything is synthesized here, so the track is royalty-free.

  0-9   detective pizzicato in D minor + fluorescent buzz
  9     record scratch, music cuts
  9.5   "Here Comes the Bride" (Wagner, public domain) on a cheap organ
  13/14 text hits, riser into the app
  15-29 upbeat groove in F major, dings / thud / blips on the app actions
  29    final hit, ring out to 30
"""
import wave
import numpy as np

SR = 44100
DUR = 30.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(7)
BEAT = 0.5


def hz(note):
    names = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
             "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
    n, o = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o + 1) - 69) / 12)


def add(t0, sig, gain=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= N:
        return
    sig = sig[: N - i]
    l = gain * np.cos((pan + 1) * np.pi / 4)
    r = gain * np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * l
    R[i:i + len(sig)] += sig * r


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(d, a=0.005, r=0.02):
    t = tt(d)
    e = np.ones_like(t)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def pluck(f, d=0.45, bright=1.0):
    t = tt(d)
    s = sum((1 / k) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (9 + 6 * k / bright)) for k in range(1, 6))
    return s * env(d, 0.002, 0.03)


def organ(f, d):
    t = tt(d)
    trem = 1 + 0.06 * np.sin(2 * np.pi * 5.5 * t)
    s = (np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * 2 * f * t)
         + 0.35 * np.sin(2 * np.pi * 3 * f * t) + 0.2 * np.sin(2 * np.pi * 4 * f * t))
    return s * trem * env(d, 0.03, 0.06)


def keys(f, d=0.22):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t + 0.8 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 12))
    return s * np.exp(-t * 7) * env(d, 0.002, 0.03)


def bass(f, d=0.42):
    t = tt(d)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.6 * s) * np.exp(-t * 2.5) * env(d, 0.004, 0.04)


def kick(d=0.32):
    t = tt(d)
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def noise(d):
    return rng.uniform(-1, 1, int(d * SR))


def hp(x, a=0.85):
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = a * (y[i - 1] + x[i] - x[i - 1])
    return y


def hat(d=0.05):
    t = tt(d)
    return hp(noise(d), 0.7) * np.exp(-t * 70)


def clap(d=0.18):
    t = tt(d)
    e = np.exp(-t * 22)
    for o in (0.0, 0.011, 0.022):
        e += np.where((t >= o) & (t < o + 0.008), 0.8, 0)
    return hp(noise(d), 0.5) * e * 0.6


def bell(f, d=1.0):
    t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 4) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 11))
    return s * env(d, 0.001, 0.05)


def blip(f, d=0.09):
    t = tt(d)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 30) * env(d, 0.001, 0.01)


def tick(d=0.025):
    t = tt(d)
    return hp(noise(d), 0.3) * np.exp(-t * 200)


def chord(fn, notes, t0, d, gain, spread=0.5):
    for i, n in enumerate(notes):
        p = -spread + 2 * spread * i / max(1, len(notes) - 1)
        add(t0, fn(hz(n), d), gain / len(notes), p)


# ---------------------------------------------------------------- 0-9: detective
walk = ["D2", "F2", "G#2", "A2", "D2", "F2", "A2", "G#2"]
for b in range(18):
    t0 = b * BEAT
    add(t0, pluck(hz(walk[b % 8]), 0.45, 0.8), 0.55)
    if b % 2 == 1:
        add(t0 + 0.25, pluck(hz(walk[b % 8]) * 2, 0.2, 1.4), 0.12, 0.3)
    add(t0 + 0.25, hat(), 0.07, 0.4)
    if b % 4 == 0 and b < 16:
        chord(lambda f, d: pluck(f, d, 1.5), ["D4", "F4", "A4", "C5"], t0, 0.6, 0.35)
# stab when the door opens (5.0) and a low sting on the realization (8.0)
chord(lambda f, d: pluck(f, d, 2.0), ["D3", "Ab3", "D4"], 5.0, 0.6, 0.5)
t = tt(1.0)
trem = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t)))
sting = sum(np.sin(2 * np.pi * hz(n) * t) for n in ["D3", "D#3", "A3"]) * trem * np.linspace(0.2, 1, len(t))
add(8.0, sting * env(1.0, 0.02, 0.02), 0.12)
add(8.0, kick(0.5), 0.6)

# fluorescent buzz with flicker gaps that match the light in the HTML
t = tt(9.0)
buzz = (np.sign(np.sin(2 * np.pi * 120 * t)) * 0.5 + np.sin(2 * np.pi * 240 * t)) * 0.5
flicker = np.ones_like(t)
for a, b in [(0.75, 0.82), (2.1, 2.16), (2.22, 2.28), (6.4, 6.47)]:
    flicker[int(a * SR):int(b * SR)] = 0.0
add(0.0, buzz * flicker * env(9.0, 0.05, 0.01), 0.025)

# ---------------------------------------------------------------- 9: record scratch
d = 0.38
t = tt(d)
f = 900 * np.exp(-t * 6) + 160 * np.sin(2 * np.pi * 9 * t) ** 2
ph = 2 * np.pi * np.cumsum(f) / SR
scr = (np.sin(ph) * 0.6 + hp(noise(d), 0.6) * 0.6) * np.exp(-t * 5)
add(9.0, scr, 0.55)

# ---------------------------------------------------------------- 9.5-13: wedding organ
melody = [("C4", 9.5, 0.5), ("F4", 10.0, 0.375), ("F4", 10.375, 0.125), ("F4", 10.5, 1.0),
          ("C4", 11.5, 0.5), ("G4", 12.0, 0.375), ("E4", 12.375, 0.125), ("F4", 12.5, 0.5)]
for n, t0, d in melody:
    add(t0, organ(hz(n) * 2, d * 0.95), 0.16)
chord(organ, ["F3", "A3", "C4"], 9.5, 2.0, 0.22, 0.3)
chord(organ, ["C3", "E3", "Bb3"], 11.5, 1.0, 0.22, 0.3)
chord(organ, ["F3", "A3", "C4"], 12.5, 0.5, 0.22, 0.3)
add(9.5, organ(hz("F2"), 2.0), 0.1)
add(11.5, organ(hz("C2"), 1.0), 0.1)

# 13 / 14: text hits; 14-15 riser into the app
for t0 in (13.0, 14.0):
    add(t0, kick(0.45), 0.7)
    add(t0, bass(hz("D2"), 0.5), 0.35)
t = tt(1.0)
f = 200 * 2 ** (t * 2.5)
ph = 2 * np.pi * np.cumsum(f) / SR
add(14.0, np.sin(ph) * (t ** 2) * env(1.0, 0.01, 0.01), 0.12)
add(14.0, hp(noise(1.0), 0.9) * (t ** 3), 0.08)

# ---------------------------------------------------------------- 15-29: groove
prog = [("F", ["F3", "A3", "C4", "E4"], ["F2", "F2", "A2", "C3"]),
        ("Bb", ["Bb2", "D3", "F3", "A3"], ["Bb1", "Bb1", "D2", "F2"]),
        ("Dm", ["D3", "F3", "A3", "C4"], ["D2", "D2", "F2", "A2"]),
        ("C", ["C3", "E3", "G3", "Bb3"], ["C2", "C2", "E2", "G2"]),
        ("F", ["F3", "A3", "C4", "E4"], ["F2", "F2", "A2", "C3"]),
        ("Bb", ["Bb2", "D3", "F3", "A3"], ["Bb1", "Bb1", "D2", "F2"]),
        ("C", ["C3", "E3", "G3", "Bb3"], ["C2", "E2", "G2", "C3"])]
for bar, (_, ch, bl) in enumerate(prog):
    t_bar = 15.0 + bar * 2.0
    for b in range(4):
        t0 = t_bar + b * BEAT
        add(t0, kick(), 0.75)
        if b in (1, 3):
            add(t0, clap(), 0.35)
        add(t0, hat(), 0.09, 0.35)
        add(t0 + 0.25, hat(), 0.13, 0.35)
        add(t0, bass(hz(bl[b]), 0.4), 0.4)
        chord(keys, ch, t0 + 0.25, 0.22, 0.45, 0.6)
# accent on the cut back to the manager
add(19.0, hp(noise(1.2), 0.6) * np.exp(-tt(1.2) * 4), 0.15)

# phone taps + typing (scene 15-19)
for t0 in (15.5, 16.0, 16.5):
    add(t0, tick(), 0.25, 0.2)
for i in range(16):
    add(16.5 + i * (1.0 / 16), tick(0.015), 0.12, 0.25)
# "Submitted" and "Published" dings
for t0 in (18.0, 23.0):
    add(t0, bell(hz("C6"), 1.2), 0.3, 0.1)
    add(t0 + 0.06, bell(hz("G6"), 1.0), 0.18, -0.1)
# Generate click + one blip per schedule cell filling in (14 cells, 1/16 notes)
add(20.0, tick(), 0.3)
penta = ["F5", "G5", "A5", "C6", "D6", "F6", "G6"]
for k in range(14):
    add(20.0 + k * 0.125, blip(hz(penta[k % 7])), 0.12, -0.5 + k / 13)
# flag pills land (22.0) and Publish click (23.0)
add(22.0, blip(hz("D5"), 0.15), 0.18)
add(22.125, blip(hz("A4"), 0.15), 0.18)
add(23.0, tick(), 0.3)
# board falls and hits the floor on the beat at 24.5
t = tt(0.6)
f = 70 * np.exp(-t * 6) + 35
ph = 2 * np.pi * np.cumsum(f) / SR
add(24.5, np.sin(ph) * np.exp(-t * 8) + 0.3 * hp(noise(0.6), 0.4) * np.exp(-t * 25), 0.9)

# ---------------------------------------------------------------- 29: final hit
chord(keys, ["F3", "A3", "C4", "F4", "A4"], 29.0, 1.0, 0.9, 0.6)
chord(lambda f, d: pluck(f, d, 2.0), ["F2", "F3"], 29.0, 1.0, 0.6)
add(29.0, kick(0.5), 0.9)
add(29.0, hp(noise(1.0), 0.6) * np.exp(-tt(1.0) * 3.5), 0.2)

# ---------------------------------------------------------------- mix + write
mix = np.stack([L, R], axis=1)
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.4) / np.tanh(1.4) * 0.89
fade = int(0.08 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
pcm = (mix * 32767).astype("<i2")
with wave.open("music.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote music.wav", DUR, "s")
