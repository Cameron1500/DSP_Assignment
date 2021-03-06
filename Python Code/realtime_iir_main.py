""" Modules """
from pyfirmata2 import Arduino
from scipy import signal
import numpy as np

import realtime_plot as rtp
import iir_filter as iir

""" Constants """
# Arduino Sample Rate
fs = 650                # BF 3/01/22 - changed to "true" sample rate Max 1000
# Nyquist
fn = fs / 2
fc = 5

""" IIR Filter Design """
# Noise Removal
sos = signal.bessel(1, fc / fn, "lowpass", output="sos", norm="mag") # BF 3/01/22 - changed to bessel

x_filter = iir.IIR_filter(sos)
y_filter = iir.IIR_filter(sos)
z_filter = iir.IIR_filter(sos)

""" Real Time Plotters """
sample_plot = rtp.RealtimePlots(fs, 2, ["X", "Y", "Z"], sample_limits=[-0.25,0.25], channels=3)
orientation_plot = rtp.RealtimeVectorPlot()

""" Sample Process Function """
def addX(data):
    # Zeroing from measurements
    data -= 0.335
    f = x_filter.filter(data)

    sample_plot.addSample(data, f, channel=0)
    orientation_plot.addSample(f, channel=0)

def addY(data):
    # Zeroing from measurements
    data -= 0.340
    f = y_filter.filter(data)

    sample_plot.addSample(data, f, channel=1)
    orientation_plot.addSample(f, channel=1)

def addZ(data):
    # Zeroing from measurements
    data -= 0.340
    f = z_filter.filter(data)

    sample_plot.addSample(data, f, channel=2)
    orientation_plot.addSample(f, channel=2)
    
""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000/fs)
board.analog[0].register_callback(addX)
board.analog[0].enable_reporting()
board.analog[1].register_callback(addY)
board.analog[1].enable_reporting()
board.analog[2].register_callback(addZ)
board.analog[2].enable_reporting()

""" Show Real Time Plots """
rtp.plt.show()
board.exit()
