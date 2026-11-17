import wave, numpy as np
w = wave.open('song/mono.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), dtype='<i2').astype(float)/32768
hop=128; win=1024
fr = np.lib.stride_tricks.sliding_window_view(x[:sr*34], win)[::hop]*np.hanning(win)
S = np.log1p(100*np.abs(np.fft.rfft(fr,axis=1)))
flux = np.maximum(0,np.diff(S,axis=0)).sum(1); fps=sr/hop
flux = np.maximum(0, flux-np.convolve(flux,np.ones(32)/32,'same'))
for bpm in (105.2,105.35,105.5):
  B=60/bpm
  for a in range(0,32,4):
    offs=np.linspace(-0.08,0.08,33); sc=[]
    for o in offs:
      ts=np.arange(0,40)*B+0.047+o; ts=ts[(ts>=a)&(ts<a+4)]
      sc.append(flux[(ts*fps).astype(int)].mean())
    print(bpm, a, 'best offset %+.3f'%offs[int(np.argmax(sc))])
