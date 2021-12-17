import matplotlib.pyplot as plt
import numpy as np

def plot(raw, filtered, fs, title="", split = True):
    fig, ax = plt.subplots(ncols=2)
    N = len(raw)

    """ Data """
    time = np.linspace(0, N/fs, N)
    
    ax[0].set_title(title)
    ax[0].set_ylim(-0.25, 0.25)
    ax[0].plot(time, raw)
    ax[0].plot(time, filtered)

    """ FFT """
    if split:
        raw = raw[int(N/2):]
        filtered = filtered[int(N/2):]
    
    _fft_raw = 20 * np.log10(abs(np.fft.fft(raw)))
    _fft_filtered = 20 * np.log10(abs(np.fft.fft(filtered)))

    _fft_raw = _fft_raw[:int(len(_fft_raw)/2)]
    _fft_filtered = _fft_filtered[:int(len(_fft_filtered)/2)]

    _fx = np.linspace(0, fs/2, len(_fft_raw))

    ax[1].set_title(title + " FFT")
    ax[1].plot(_fx, _fft_raw)
    ax[1].plot(_fx, _fft_filtered)

""" Load Data """
A = np.loadtxt("Recordings/A.csv", delimiter=",")
B = np.loadtxt("Recordings/B.csv", delimiter=",")
C = np.loadtxt("Recordings/C.csv", delimiter=",")
fs = 1000

""" IIR Filter """
import iir_filter
from scipy import signal
sos_hp = signal.butter(2, 0.5 / (fs/2), "highpass", output="sos")   # High Pass (DC Removal)
sos_lp = signal.butter(2, 10 / (fs/2), "lowpass", output="sos")     # Low Pass (Noise Removal)
sos = np.concatenat([sos_hp, sos_lp])
f = iir_filter.IIR_filter(sos)

""" Do Filter """
A_filtered = np.zeros(len(A))
B_filtered = np.zeros(len(B))
C_filtered = np.zeros(len(C))
for i in range(len(A)):
    A_filtered[i] = f.filter(A[i])
    B_filtered[i] = f.filter(B[i])
    C_filtered[i] = f.filter(C[i])

plot(A, A_filtered, fs, title="'Recording A'")
plot(B, B_filtered, fs, title="'Recording B'")
plot(C, C_filtered, fs, title="'Recording C'")

plt.show()