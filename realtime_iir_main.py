""" Modules """
from pyfirmata2 import Arduino
from scipy import signal
import numpy as np

import realtime_plot as rtp
import gesture_detect as gd
import iir_filter as iir

""" Constants """
# Arduino Sample Rate
fs = 1000   # Max 1000
# Nyquist
fn = fs / 2

""" IIR Filter Design """
# DC Noise Removal (0.1Hz High-pass)
sos_hp = signal.butter(2, 0.5 / fn, "highpass", output="sos")
# Anti-Alising (~500Hz Low Pass)
sos_lp = signal.butter(2, 5 / fn, "lowpass", output="sos")

# Combine Filters
sos = np.concatenate([sos_lp, sos_hp])
f = iir.IIR_filter(sos)

""" Gesture Detect """
gesture_detector = gd.GestureDetect(0.005)

""" Real Time Plotters """
raw_data_plot = rtp.RealtimePlot(fs, 2, "Pre-Filter", fs_calc=True)
filter_data_plot = rtp.RealtimePlot(fs, 2, "Post-Filter")

""" Sample Process Function """
def processSample(data):
    raw_data_plot.addSample(data)

    filter_data = f.filter(data)
    filter_data_plot.addSample(filter_data)

    gesture_detector.processSample(filter_data)

""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000/fs)
board.analog[0].register_callback(processSample)
board.analog[0].enable_reporting()

""" Show Real Time Plots """
rtp.plt.show()
board.exit()