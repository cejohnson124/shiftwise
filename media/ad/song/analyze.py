import wave, numpy as np, sys
w = wave.open(sys.argv[1]); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
hop = 256; win = 1024
frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
S = np.abs(np.fft.rfft(frames, axis=1))
S = np.log1p(100*S)
flux = np.maximum(0, np.diff(S, axis=0)).sum(1)
flux = flux - np.convolve(flux, np.ones(16)/16, 'same'); flux = np.maximum(flux, 0)
fps = sr/hop
# tempo by autocorrelation, 70-180 bpm
ac = np.correlate(flux, flux, 'full')[len(flux)-1:]
lags = np.arange(len(ac)); bpm = 60*fps/np.maximum(lags,1)
m = (bpm>70)&(bpm<180)
cands = sorted([(ac[l], 60*fps/l) for l in lags[m]], reverse=True)[:8]
print('tempo cands', [(round(b,2)) for _,b in cands])
# refine: search bpm grid + phase maximizing onset sum
best=None
for b in np.arange(70,180,0.05):
    period = 60/b*fps
    idx = np.arange(0, len(flux)-1, period)
    for ph in np.linspace(0, period, 24, endpoint=False):
        ii = (idx+ph).astype(int); ii=ii[ii<len(flux)]
        s = flux[ii].mean()
        if best is None or s>best[0]: best=(s,b,ph/fps)
print('best bpm %.2f phase %.3fs score %.3f'%(best[1],best[2],best[0]))
b, ph = best[1], best[2]
bar = 4*60/b
rms = [np.sqrt(np.mean(x[int((ph+i*bar)*sr):int((ph+(i+1)*bar)*sr)]**2)) for i in range(int((len(x)/sr-ph)/bar))]
for i,r in enumerate(rms): print('bar %3d t=%6.2f rms %.3f %s'%(i, ph+i*bar, r, '#'*int(r*200)))
