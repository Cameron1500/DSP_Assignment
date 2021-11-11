import matplotlib.pyplot as plt
import numpy as np

def fft(data, fs, title="FFT"):
    fig, ax = plt.subplots()

    _fft = abs(np.fft.fft(data))
    _fx = np.linspace(0, fs, len(_fft))

    ax.set_title(title)
    ax.plot(_fx, _fft)

N = 2000
fs = 500

r = np.random.rand(N)
fft(r, fs, title="No Filter")

""" IIR Filter """
import iir_filter
from scipy import signal
sos = signal.butter(10, 150 / (fs/2), "highpass", output="sos")
f = iir_filter.IIR_filter(sos)

""" Do Filter """
fw = np.zeros(N)
for i in range(N):
    fw[i] = f.filter(r[i])

fft(fw, fs, title="Filtered")

plt.show()