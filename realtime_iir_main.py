""" Modules """
from pyfirmata2 import Arduino
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import time

import iir_filter as iir

""" Constants """
# Arduino Sample Rate
fs = 1000   # Max 1000
# Nyquist
fn = fs / 2

""" IIR Filter Design """
# Second-Order HP at 0.1 Hz
sos_hp = signal.butter(2, 0.1 / fn, "highpass", output="sos")
sos_lp = signal.butter(2, 10 / fn, "lowpass", output="sos")

# Combine Filters
sos = np.concatenate([sos_lp, sos_hp])
f = iir.IIR_filter(sos)

""" Real-Time Plotter """
class RealtimePlot:
    def __init__(self, fs, window_time, title, sample_limits=[-0.25, 0.25], fft_limits=[0,50], fs_calc=False):
        # Buffer
        self.buffer_size = fs * window_time
        self.plot_buffer = np.zeros(self.buffer_size)
        self.data_buffer = []

        # Figure Plot
        self.fig, self.ax = plt.subplots(nrows=2)
        
        # Sample Plot
        self.ax[0].plot([0, self.buffer_size-1],[0,0],color="r")
        self.line_r, = self.ax[0].plot(self.plot_buffer)
        self.ax[0].set_ylim(sample_limits[0], sample_limits[1])
        self.ax[0].set_title(title)

        # FFT Plot
        fx = np.linspace(0, fs, self.buffer_size)
        self.line_f, = self.ax[1].plot(fx, self.plot_buffer)
        self.ax[1].set_ylim(fft_limits[0], fft_limits[1])
        self.ax[1].set_title(title + " FFT")

        self.anim = animation.FuncAnimation(self.fig, self.update, interval=100)
        self.update_count = 0

        # Sample Rate
        self.sample_count = 0
        self.fs_calc = fs_calc
        if self.fs_calc:
            self.label = self.ax[0].text(0, sample_limits[0], "Sample Rate: -", ha="left", va="bottom", fontsize=15)
            self.last = 0

    def update(self, x):
        # Buffer
        self.plot_buffer = np.append(self.plot_buffer, self.data_buffer)
        self.plot_buffer = self.plot_buffer[-self.buffer_size:]
        self.data_buffer = []
        self.line_r.set_ydata(self.plot_buffer)

        if self.update_count % 5 == 0: # Reduce updates for performance
            # FFT
            fft = abs(np.fft.fft(self.plot_buffer))
            self.line_f.set_ydata(fft)

            # Sample Rate
            if self.fs_calc:
                current_time = time.time()
                sample_rate = self.sample_count / (current_time - self.last)
                self.last = current_time
                self.sample_count = 0

                self.label.set_text(f"Fs: {sample_rate:.1f}Hz")
        self.update_count += 1

    def addSample(self, v):
        # Add Sample to Buffer
        self.data_buffer.append(v)
        self.sample_count += 1

""" Real Time Plotters """
raw_data_plot = RealtimePlot(fs, 2, "Pre-Filter", fs_calc=True)
filter_data_plot = RealtimePlot(fs, 2, "Post-Filter")

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