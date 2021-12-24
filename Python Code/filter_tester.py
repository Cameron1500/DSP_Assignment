import matplotlib.pyplot as plt
import numpy as np

def plot(data, labels, fs, title="", split = True):
    fig, ax = plt.subplots(ncols=2)
    N = len(data[0])

    """ Data """
    time = np.linspace(0, N/fs, N)
    
    ax[0].set_title(title)
    ax[0].set_ylim(-5, 5)
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
from pathlib import Path

source_dir = Path(__file__).resolve().parent.parent
file_name = input("File Name: ")
source_dir = source_dir / "Recordings" / file_name

if not source_dir.is_file():
    print("No recoginsied file:")
    print(source_dir)
    exit()

csv = np.loadtxt(str(source_dir), delimiter=",")
fs = 1000

""" IIR Filter """
import iir_filter
from scipy import signal
sos_hp = signal.butter(2, 0.5 / (fs/2), "highpass", output="sos")   # High Pass (DC Removal)
sos_lp = signal.butter(2, 10 / (fs/2), "lowpass", output="sos")     # Low Pass (Noise Removal)
sos = np.concatenate([sos_hp, sos_lp])

xf = iir_filter.IIR_filter(sos)
yf = iir_filter.IIR_filter(sos)
zf = iir_filter.IIR_filter(sos)

""" Do Filter """
filtered = np.zeros(shape=np.shape(csv))
for i in range(np.shape(csv)[0]):
    filtered[i,0] = xf.filter(csv[i,0])
    filtered[i,1] = yf.filter(csv[i,1])
    filtered[i,2] = zf.filter(csv[i,2])

plot([csv[:,0], csv[:,1], csv[:,2]], ["X", "Y", "Z"], fs, title="Raw Data")
plot([filtered[:,0], filtered[:,1], filtered[:,2]], ["X", "Y", "Z"], fs, title="Filtered")

plt.show()