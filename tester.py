import matplotlib.pyplot as plt
import numpy as np

def fft(data, sample_rate):
    fig, ax = plt.subplots()

    _fft = abs(np.fft.fft(data))
    _ft = np.linspace(0, sample_rate, len(_fft))

    ax.plot(_ft, _fft)