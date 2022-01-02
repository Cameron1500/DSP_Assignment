from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import matplotlib.pyplot as plt

import numpy as np
import time

from calcAngles import calcAngles

""" Rolling Buffer """
class RollingBuffer:
    def __init__(self, size):
        self.size = size
        self.plot_buffer = np.zeros(self.size)
        self.data_buffer = []
    
    def update(self):
        self.plot_buffer = np.append(self.plot_buffer, self.data_buffer)
        self.plot_buffer = self.plot_buffer[-self.size:]
        self.data_buffer = []
        return self.plot_buffer
    
    def add(self, v):
        self.data_buffer.append(v)

""" Real-Time Plotter Variable Channel """
class RealtimePlots:
    def __init__(self, fs, window_time, labels, sample_limits=[-0.5, 0.5], channels=1):
        # Buffer
        self.buffer_size = fs * window_time
        self.r_buffers = []
        self.f_buffers = []

        # Figure Plot
        self.fig, self.ax = plt.subplots(nrows=2)
        
        # Sample Plot
        self.ax[0].plot([0, self.buffer_size-1],[0,0],"r--",label="Zero")
        self.ax[0].set_ylim(sample_limits[0], sample_limits[1])
        self.ax[0].set_title("Un-Filtered")
        self.r_lines = []

        # Filter Plot
        self.ax[1].plot([0, self.buffer_size-1],[0,0],"r--",label="Zero")
        self.ax[1].set_ylim(sample_limits[0], sample_limits[1])
        self.ax[1].set_title("Filtered")
        self.f_lines = []

        # Plot Buffers
        for i in range(channels):
            self.r_buffers.append(RollingBuffer(self.buffer_size))
            line, = self.ax[0].plot(self.r_buffers[i].update(), label=labels[i])
            self.r_lines.append(line)
            
            self.f_buffers.append(RollingBuffer(self.buffer_size))
            line, = self.ax[1].plot(self.f_buffers[i].update(), label=labels[i])
            self.f_lines.append(line)
        self.ax[1].legend(loc=4)

        self.anim = FuncAnimation(self.fig, self.update, interval=100)
        self.update_count = 0

        # Sample Rate
        self.sample_count = 0
        self.label = self.ax[0].text(0, sample_limits[0], "Sample Rate: -", ha="left", va="bottom", fontsize=15)
        self.last = 0

    def update(self, x):
        # Buffer
        for i in range(len(self.r_lines)):
            self.r_lines[i].set_ydata(self.r_buffers[i].update())
            self.f_lines[i].set_ydata(self.f_buffers[i].update())
        
        # Sample Rate Calc
        if self.update_count % 5 == 0: # Reduce updates for performance
            current_time = time.time()
            sample_rate = self.sample_count / (current_time - self.last)
            self.last = current_time
            self.sample_count = 0

            self.label.set_text(f"Fs: {sample_rate:.1f}Hz")
        self.update_count += 1

    def addSample(self, v, f, channel=0):
        if channel == 0:
            self.sample_count += 1
        self.r_buffers[channel].add(v)
        self.f_buffers[channel].add(f)

""" Real-Time Vector Plotter """
class RealtimeVectorPlot:
    def __init__(self):
        self.vec = np.zeros(3)

        self.fig, self.ax = plt.subplots(subplot_kw=dict(projection="3d"))
        self.ax.set_xlim(-1.0, 1.0)
        self.ax.set_ylim(-1.0, 1.0)
        self.ax.set_zlim(-1.0, 1.0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        self.anim = FuncAnimation(self.fig, self.update, interval=100)
        self.q = self.ax.quiver(0, 0, 0, 0, 0, 1)
        self.x = self.ax.quiver(0, 0, 0, 1, 0 ,0, color="red")
        self.y = self.ax.quiver(0, 0, 0, 0, 1 ,0, color="green")
        self.z = self.ax.quiver(0, 0, 0, 0, 0 ,1, color="blue")

        self.label = self.ax.text(0, 0, 0, "test", transform=self.ax.transAxes)
        self.update_delay = 0

        # For calibration
        self.offset_angles = np.zeros(3)
        axes = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.button = Button(axes, "Calibrate")
        self.button.on_clicked(self.setOffset)

    def update(self, x):
        cur_vec = self.vec
        m = np.sqrt(cur_vec[0] * cur_vec[0] + cur_vec[1] * cur_vec[1] + cur_vec[2] * cur_vec[2])
        if m != 0:
            self.q.remove()
            self.q = self.ax.quiver(0, 0, 0, cur_vec[0] / m, cur_vec[1] / m, cur_vec[2] / m, color="black")

            # Angle Calcs
            if self.update_delay % 5 == 0:
                # Angle between the vector and the x plane
                angle = calcAngles(cur_vec)
                ma = f"Real Angle (deg),   x: {angle[0]:.1f}, y: {angle[1]:.1f}, z: {angle[2]:.1f}\n"
                angle = np.abs(angle - self.offset_angles)
                fa = f"Final Angle (deg),  x: {angle[0]:.1f}, y: {angle[1]:.1f}, z: {angle[2]:.1f}"
                self.label.set_text(ma + fa)
            self.update_delay += 1

    def setOffset(self, x):
        self.offset_angles = calcAngles(self.vec)

    def addSample(self, v, channel=0):
        self.vec[channel] = v
