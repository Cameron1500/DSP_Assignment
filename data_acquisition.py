import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

from pyfirmata2 import Arduino

import iir_filter

import util

""" Constant """
fs = 250   # Max 1000
fn = fs / 2

""" Real-Time Plotter """
class RealtimePlotter:
    def __init__(self, samples):
        # Buffer
        self.plot_buffer = np.zeros(500)
        self.data_buffer = []

        # Matplotlib Plot
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.plot_buffer)
        self.ax.set_ylim(0, 1.5)
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)

    def update(self, data):
        # Update Buffers
        self.plot_buffer = np.append(self.plot_buffer, self.data_buffer)
        self.plot_buffer = self.plot_buffer[-500:]
        self.data_buffer = []
        
        # Set Plot Line
        self.line.set_ydata(self.plot_buffer)
        return self.line

    def addSample(self, v):
        # Add Sample to Buffer
        self.data_buffer.append(v)

""" Real Time Plotters """
raw_data_plot = RealtimePlotter(500)
filter_data_plot = RealtimePlotter(500)

""" IIR Filter """
sos = signal.butter(2, 5 / fn, "highpass", output="sos")
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