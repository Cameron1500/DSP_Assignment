import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

""" Constants """
fs = 100
fn = fs / 2
fc = 0.5

""" Filter Design """
b, a = signal.butter(1, fc / fn, "highpass")
w, h = signal.freqz(b,a)

""" Filter Response """
plt.plot(w,20*np.log10(h))
plt.show()