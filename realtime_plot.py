import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

""" Real-Time Plotter """
class RealtimePlot:
    def __init__(self, fs, buffer_size, title, running_limits=[-0.5, 0.5], fft_limits=[0,50], show_fft=False):
        # Buffer
        self.plot_buffer = np.zeros(buffer_size)
        self.buffer_size = buffer_size
        self.data_buffer = []

        if show_fft:
            # Figure Plot
            self.fig, self.ax = plt.subplots(ncols=2)
            
            # Running Plot
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
        else:
            # Figure Plot
            self.fig, self.ax = plt.subplots(ncols=1)
            
            # Running Plot
            self.line_r, = self.ax.plot(self.plot_buffer)
            self.ax.set_ylim(running_limits[0], running_limits[1])
            self.ax.set_title(title)
            self.ani_r = animation.FuncAnimation(self.fig, self.update_running, interval=100)

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
