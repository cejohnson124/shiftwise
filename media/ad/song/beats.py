import wave, numpy as np, json
w = wave.open('song/mono.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
x = x[:sr*40]
hop=128; win=1024
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]*np.hanning(win)
mag = np.abs(np.fft.rfft(fr,axis=1)); fps=sr/hop
S=np.log1p(100*mag); o=np.maximum(0,np.diff(S,axis=0)).sum(1)
o=np.maximum(0,o-np.convolve(o,np.ones(64)/64,'same')); o/=o.std()
# global tempo from autocorrelation of the onset envelope with a log-gaussian prior around 110 bpm
ac=np.correlate(o,o,'full')[len(o)-1:]
lags=np.arange(1,int(fps*1.2)); bpm=60*fps/lags
w_=np.exp(-0.5*(np.log2(bpm/110)/0.9)**2)
tau=lags[np.argmax(ac[lags]*w_)]
print('global tempo %.2f bpm (period %.4fs)'%(60*fps/tau, tau/fps))
# Ellis DP
alpha=100; C=o.copy(); P=-np.ones(len(o),int)
for t in range(len(o)):
    lo,hi=t-2*tau,t-tau//2
    if hi<=0: continue
    pr=np.arange(max(0,lo),hi)
    sc=C[pr]-alpha*(np.log((t-pr)/tau))**2
    j=np.argmax(sc); C[t]=o[t]+sc[j]; P[t]=pr[j]
end=len(o)-1-np.argmax(C[::-1][:tau])
b=[end]
while P[b[-1]]>=0: b.append(P[b[-1]])
b=np.array(b[::-1])/fps
iv=np.diff(b)
print('beats', len(b)); 
for a in range(0,36,4):
    m=(b[:-1]>=a)&(b[:-1]<a+4); print('%2d-%2ds mean interval %.4f (%.1f bpm)'%(a,a+4,iv[m].mean(),60/iv[m].mean()))
print(np.round(b[b<32],3).tolist())
json.dump(np.round(b,4).tolist(), open('song/beats.json','w'))
