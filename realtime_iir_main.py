from pyfirmata2 import Arduino
from scipy import signal
import iir_filter as iir
import realtime_plot as rtp

""" Constant """
fs = 1000   # Max 1000
fn = fs / 2

# Cutoff Frequency (Hz)
fc = 5

""" Real Time Plotters """
raw_data_plot = rtp.RealtimePlot(fs, 500, "Pre-Filter")
filter_data_plot = rtp.RealtimePlot(fs, 500, "Post-Filter")

""" IIR Filter """
sos = signal.butter(2, fc / fn, "lowpass", output="sos")
f = iir.IIR_filter(sos)

""" Sample Process Function """
def processSample(data):
    raw_data_plot.addSample(data)

    filter_data = f.filter(data)
    filter_data_plot.addSample(filter_data)

""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.samplingOn(1000/fs)
board.analog[0].register_callback(processSample)
board.analog[0].enable_reporting()

""" Show Real Time Plots """
rtp.plt.show()
board.exit()