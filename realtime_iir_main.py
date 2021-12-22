""" Modules """
from pyfirmata2 import Arduino
from scipy import signal
import numpy as np

import realtime_plot as rtp
import iir_filter as iir

""" Constants """
# Arduino Sample Rate
fs = 100   # Max 1000
# Nyquist
fn = fs / 2

""" IIR Filter Design """
# DC Noise Removal (0.1Hz High-pass)
sos = signal.butter(2, 0.1 / fn, "highpass", output="sos")
x_filter = iir.IIR_filter(sos)
y_filter = iir.IIR_filter(sos)

""" Real Time Plotters """
raw = rtp.RealtimePlots(fs, 2, "Raw Data", channels=2)
filtered = rtp.RealtimePlots(fs, 2, "Filtered Data", channels=2)

""" Sample Process Function """
def addX(data):
    raw.addSample(data, channel=0)
    filtered.addSample(x_filter.filter(data), channel=0)

def addY(data):
    raw.addSample(data, channel=1)
    filtered.addSample(y_filter.filter(data), channel=1)

""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000/fs)
board.analog[0].register_callback(addY)
board.analog[0].enable_reporting()
board.analog[1].register_callback(addX)
board.analog[1].enable_reporting()

""" Show Real Time Plots """
rtp.plt.show()
board.exit()