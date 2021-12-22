import matplotlib.pyplot as plt
import numpy as np

def plot(data, labels, fs, title="", split = True):
    fig, ax = plt.subplots(ncols=2)
    N = len(data[0])

    print(np.shape(data))

    """ Data """
    time = np.linspace(0, N/fs, N)
    
    ax[0].set_title(title)
    ax[0].set_ylim(-0.25, 0.25)
    for i in range(len(data)):
        ax[0].plot(time, data[i], label=labels[i])
    ax[0].legend()

    """ FFT """
    if split:
        for i in range(len(data)):
            data[i] = data[i][int(N/2):]
    
    shape = np.shape(data)
    _fft = np.empty(shape=(shape[0], int(shape[1]/2)))
    for i in range(len(data)):
        data[i] = 20 * np.log10(abs(np.fft.fft(data[i])))
        _fft[i] = data[i][:int(len(data[i])/2)]
    
    _fx = np.linspace(0, fs/2, len(_fft[0]))

    ax[1].set_title(title + " FFT")
    for i in _fft:
        ax[1].plot(_fx, i)

""" Load Data """
A = np.loadtxt("Recordings/A.csv", delimiter=",")
#B = np.loadtxt("Recordings/B.csv", delimiter=",")
#C = np.loadtxt("Recordings/C.csv", delimiter=",")
fs = 1000

""" IIR Filter """
import iir_filter
from scipy import signal
sos_hp = signal.butter(2, 0.5 / (fs/2), "highpass", output="sos")   # High Pass (DC Removal)
sos_lp = signal.butter(2, 10 / (fs/2), "lowpass", output="sos")     # Low Pass (Noise Removal)
sos = np.concatenate([sos_hp, sos_lp])
f = iir_filter.IIR_filter(sos)

""" Do Filter """
A_filtered = np.zeros(len(A))
A_matched = np.zeros(len(A))
#B_filtered = np.zeros(len(B))
#C_filtered = np.zeros(len(C))
for i in range(len(A)):
    A_filtered[i] = f.filter(A[i])
    A_matched[i] = A_filtered[i] * np.abs(A_filtered[i])
    #B_filtered[i] = f.filter(B[i])
    #C_filtered[i] = f.filter(C[i])

plot([A, A_filtered, A_matched], ["Raw", "Filtered", "Matched"], fs, title="'Recording A'")
#plot([B, B_filtered], ["Raw", "Filtered"], fs, title="'Recording B'")
#plot([C, C_filtered], ["Raw", "Filtered"], fs, title="'Recording C'")

plt.show()