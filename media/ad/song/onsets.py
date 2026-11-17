import wave, numpy as np
w = wave.open('song/mono.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
x = x[:sr*36]
hop=128; win=1024
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]*np.hanning(win)
mag = np.abs(np.fft.rfft(fr,axis=1)); freqs=np.fft.rfftfreq(win,1/sr)
fps=sr/hop
def env(lo,hi):
    S=np.log1p(100*mag[:,(freqs>=lo)&(freqs<hi)])
    f=np.maximum(0,np.diff(S,axis=0)).sum(1)
    return np.maximum(0,f-np.convolve(f,np.ones(64)/64,'same'))
for name,(lo,hi) in {'low':(30,200),'all':(30,11000)}.items():
    f=env(lo,hi); thr=np.percentile(f,97)
    pk=[i for i in range(2,len(f)-2) if f[i]>thr and f[i]==f[i-2:i+3].max()]
    t=np.array(pk)/fps
    print(name, len(t), np.round(t[:60],3).tolist())
    # fit grid: for each onset, nearest beat index under bpm guess, then least squares
    B=60/105.35
    k=np.round((t-0.047)/B); A=np.vstack([k,np.ones_like(k)]).T
    for it in range(3):
        (b,o),*_=np.linalg.lstsq(A,t,rcond=None); res=t-(k*b+o)
        keep=np.abs(res)<0.06; A2=A[keep]; t2=t[keep]
        (b,o),*_=np.linalg.lstsq(A2,t2,rcond=None); k=np.round((t-o)/b); A=np.vstack([k,np.ones_like(k)]).T
    res=t-(k*b+o)
    print(' fit bpm %.3f offset %.4f  |res|<40ms: %d/%d  median|res| %.3f'%(60/b,o,(np.abs(res)<0.04).sum(),len(t),np.median(np.abs(res))))
