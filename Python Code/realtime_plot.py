from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import time
import calcAngles
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
    def __init__(self, fs, window_time, title, labels, sample_limits=[-0.5, 0.5], channels=1):
        # Buffer
        self.buffer_size = fs * window_time
        self.buffers = []

        # Figure Plot
        self.fig, self.ax = plt.subplots()
        
        # Sample Plot
        self.ax.plot([0, self.buffer_size-1],[0,0],"r--",label="Zero")
        self.ax.set_ylim(sample_limits[0], sample_limits[1])
        self.ax.set_title(title)
        self.lines = []

        # Plot Buffers
        for i in range(channels):
            self.buffers.append(RollingBuffer(self.buffer_size))
            line, = self.ax.plot(self.buffers[i].update(), label=labels[i])
            self.lines.append(line)
        self.ax.legend()

        self.anim = FuncAnimation(self.fig, self.update, interval=100)
        self.update_count = 0

        # Sample Rate
        self.sample_count = 0
        self.label = self.ax.text(0, sample_limits[0], "Sample Rate: -", ha="left", va="bottom", fontsize=15)
        self.last = 0

    def update(self, x):
        # Buffer
        for i in range(len(self.lines)):
            self.lines[i].set_ydata(self.buffers[i].update())
        
        # Sample Rate Calc
        if self.update_count % 5 == 0: # Reduce updates for performance
            current_time = time.time()
            sample_rate = self.sample_count / (current_time - self.last)
            self.last = current_time
            self.sample_count = 0

            self.label.set_text(f"Fs: {sample_rate:.1f}Hz")
        self.update_count += 1

    def addSample(self, v, channel=0):
        if channel == 0:
            self.sample_count += 1
        self.buffers[channel].add(v)

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

        self.tLastUpdate = 0
        self.updatePeriod_s = 1
        self.label = self.ax.text(0, 0, 0, "test", transform=self.ax.transAxes)
        self.angle = np.array([0,0,0])

    def update(self, x):
        m = np.max(np.abs(self.vec))
        if m != 0:
            self.q.remove()
            self.q = self.ax.quiver(0, 0, 0, self.vec[0] / m, self.vec[1] / m, self.vec[2] / m, color="black")
            #angle calcs
            now = time.time()
            if (now - self.tLastUpdate)>self.updatePeriod_s:
                #angle between the vector and the x plane
                self.angle = calcAngles.calcAngles(self.vec)
                self.label.set_text(f"angle (deg) x:{self.angle[0]}, y:{self.angle[1]}, z:{self.angle[2]}")
                self.tLastUpdate = now

    def addSample(self, v, channel=0):
        self.vec[channel] = v
