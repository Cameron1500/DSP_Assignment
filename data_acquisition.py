import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

from pyfirmata2 import Arduino

import iir_filter

""" Constant """
fs = 250   # Max 1000
fn = fs / 2

# Cutoff Frequency (Hz)
fc = 5

""" Real-Time Plotter """
class RealtimePlot:
    def __init__(self, fs, buffer_size, title):
        # Buffer
        self.plot_buffer = np.zeros(buffer_size)
        self.buffer_size = buffer_size
        self.data_buffer = []

        # Figure Plot
        self.fig, self.ax = plt.subplots(ncols=2)
        
        # Running Plot
        self.line_r, = self.ax[0].plot(self.plot_buffer)
        self.ax[0].set_ylim(0, 1.5)
        self.ax[0].set_title(title)
        self.ani_r = animation.FuncAnimation(self.fig, self.update_running, interval=100)

        # FFT Plot
        fx = np.linspace(0, fs, buffer_size)
        self.line_f, = self.ax[1].plot(fx, self.plot_buffer)
        self.ax[1].set_ylim(0, 100)
        self.ax[1].set_title(title + " FFT")
        self.ani_f = animation.FuncAnimation(self.fig, self.update_fft, interval=500)

    def update_running(self, data):
        # Update Buffers
        self.plot_buffer = np.append(self.plot_buffer, self.data_buffer)
        self.plot_buffer = self.plot_buffer[-self.buffer_size:]
        self.data_buffer = []
        
        # Set Plot Line
        self.line_r.set_ydata(self.plot_buffer)
        return self.line_r
    
    def update_fft(self, data):
        # FFT Buffer
        fft = abs(np.fft.fft(self.plot_buffer))
        
        # Set Plot Line
        self.line_f.set_ydata(fft)
        return self.line_f

    def addSample(self, v):
        # Add Sample to Buffer
        self.data_buffer.append(v)

""" Real Time Plotters """
raw_data_plot = RealtimePlot(fs, 500, "Pre-Filter")
filter_data_plot = RealtimePlot(fs, 500, "Post-Filter")

""" IIR Filter """
sos = signal.butter(2, fc / fn, "lowpass", output="sos")
f = iir_filter.IIR_filter(sos)

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
plt.show()
board.exit()