import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time

""" Real-Time Plotter """
class RealtimePlot:
    def __init__(self, fs, buffer_size, title, running_limits=[-0.25, 0.25], fft_limits=[0,50]):
        # Buffer
        self.plot_buffer = np.zeros(buffer_size)
        self.buffer_size = buffer_size
        self.data_buffer = []

        # Figure Plot
        self.fig, self.ax = plt.subplots(nrows=2)
        
        # Running Plot
        self.ax[0].plot([0, buffer_size-1],[0,0],color="r")
        self.line_r, = self.ax[0].plot(self.plot_buffer)
        self.ax[0].set_ylim(running_limits[0], running_limits[1])
        self.ax[0].set_title(title)
        self.ani_r = animation.FuncAnimation(self.fig, self.update_running, interval=100)

        # FFT Plot
        fx = np.linspace(0, fs, buffer_size)
        self.line_f, = self.ax[1].plot(fx, self.plot_buffer)
        self.ax[1].set_ylim(fft_limits[0], fft_limits[1])
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

""" Sample Rate """
class SampleRate:
    def __init__(self):
        self.lasttime = 0
        self.samplerate_buffer = []

        self.fig, self.ax = plt.subplots()
        self.ax.set(xlim=[0,1],ylim=[0,1])
        self.fig.set_size_inches(5,0.5)
        self.ax.axis("off")

        self.label = self.ax.text(0, 0.5, "Sample Rate: -", ha="left", va="center", fontsize=20)
        self.anim = animation.FuncAnimation(self.fig, self.update, interval=250)
    
    def update(self, i):
        # Update Sample Rate
        if len(self.samplerate_buffer) == 0:
            sr = 0
        else:
            sr = np.average(self.samplerate_buffer)
        self.label.set_text(f"Sample Rate: {sr:.1f}Hz")
        self.samplerate_buffer = []
    
    def tick(self):
        # Calc Sample Rate
        current = time.time_ns()
        delta = current - self.lasttime
        if delta != 0:
            self.samplerate_buffer.append(1000000000 / delta)
        self.lasttime = current