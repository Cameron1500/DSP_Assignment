""" Modules """
from pyfirmata2 import Arduino
from scipy import signal
import numpy as np

import realtime_plot as rtp
import iir_filter as iir

""" Constants """
# Arduino Sample Rate
fs = 1000   # Max 1000
# Nyquist
fn = fs / 2

""" IIR Filter Design """
# Noise Removal
sos = signal.butter(2, 1 / fn, "lowpass", output="sos")

x_filter = iir.IIR_filter(sos)
y_filter = iir.IIR_filter(sos)
z_filter = iir.IIR_filter(sos)

""" Real Time Plotters """
raw = rtp.RealtimePlots(fs, 2, "Raw Data", sample_limits=[-5,5], channels=3)
filtered = rtp.RealtimePlots(fs, 2, "Filtered Data", sample_limits=[-5,5], channels=3)

orientation = rtp.RealtimeVectorPlot()

""" Convert Normalized Voltage to Acceleration """
def v2a(n_volt):
    # Normalised voltage to voltage and Re-centre (3.3V / 2 = 0g)
    volts = (n_volt * 5) - (3.3 / 2)
    # Convert to acceleration (300mV per g)
    return volts / 0.3

""" Sample Process Function """
def addX(data):
    acc = v2a(data)
    raw.addSample(acc, channel=0)

    f_acc = x_filter.filter(acc)
    orientation.addSample(acc, channel=0)
    filtered.addSample(f_acc, channel=0)

def addY(data):
    acc = v2a(data)
    raw.addSample(acc, channel=1)

    f_acc = y_filter.filter(acc)
    orientation.addSample(f_acc, channel=1)
    filtered.addSample(f_acc, channel=1)

def addZ(data):
    acc = v2a(data)
    raw.addSample(acc, channel=2)

    f_acc = z_filter.filter(acc)
    orientation.addSample(f_acc, channel=2)
    filtered.addSample(f_acc, channel=2)

""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000/fs)
board.analog[0].register_callback(addY)
board.analog[0].enable_reporting()
board.analog[1].register_callback(addX)
board.analog[1].enable_reporting()
board.analog[2].register_callback(addZ)
board.analog[2].enable_reporting()

""" Show Real Time Plots """
rtp.plt.show()
board.exit()