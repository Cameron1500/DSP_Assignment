import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

import iir_filter

""" Constants """
fs = 1000
fn = fs / 2

fc = 1

test_freq = 10

filter_order = 1

time = 10
N = time * 1000

""" Filter """ 
b,a = signal.butter(filter_order, fc / fn, "lowpass")
sos = signal.butter(filter_order, fc / fn, "lowpass", output="sos")

f = iir_filter.IIR_filter(sos)

""" Frequency Response """
w,h = signal.freqz(b,a)

""" Time Response """
t = np.linspace(0, time, N)

if test_freq == 0:
    r = np.ones(N)
else:
    r = np.cos(2 * np.pi * t * test_freq)

for i in range(N):
    r[i] = f.filter(r[i])

""" Plot """
plt.figure(1)
plt.plot(w, 20 * np.log10(np.abs(h)))
plt.title("Frequency Response")

plt.figure(2)
plt.plot(t, r)
plt.title("Time Response ({:.1f}Hz)".format(test_freq))

plt.show()