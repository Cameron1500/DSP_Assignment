import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

""" Constants """
fs = 1000
fn = fs / 2

fc = 0.5

""" Filter """ 
b,a = signal.butter(2, fc / fn, "lowpass")
w1,h1 = signal.freqz(b,a)
b,a = signal.butter(4, fc / fn, "lowpass")
w2,h2 = signal.freqz(b,a)
b,a = signal.butter(6, fc / fn, "lowpass")
w3,h3 = signal.freqz(b,a)

""" Plot """
plt.plot(w1, 20 * np.log10(np.abs(h1)))
plt.plot(w2, 20 * np.log10(np.abs(h2)))
plt.plot(w3, 20 * np.log10(np.abs(h3)))
plt.show()