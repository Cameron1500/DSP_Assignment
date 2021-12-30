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

<<<<<<< HEAD
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
=======
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
>>>>>>> d5e011131ac90bdda21457f3226ea6a9602aac9c

plt.show()