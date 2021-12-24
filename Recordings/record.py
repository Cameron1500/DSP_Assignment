import matplotlib.pyplot as plt
from pyfirmata2 import Arduino
import numpy as np
import time

""" Arrays """
# Sample Rate
fs = 1000
length = float(input("Record time: "))
N = int(fs * length)

x = np.zeros(N)
y = np.zeros(N)
z = np.zeros(N)

xn = 0
yn = 0
zn = 0

""" Convert Normalized Voltage to Acceleration """
def v2a(n_volt):
    # Normalised voltage to voltage and Re-centre (3.3V / 2 = 0g)
    volts = (n_volt * 5) - (3.3 / 2)
    # Convert to acceleration (300mV per g)
    return volts / 0.3

""" Callbacks """
def addX(data):
    global xn
    if xn < N:
        x[xn] = v2a(data)
    xn += 1

def addY(data):
    global yn
    if yn < N:
        y[yn] = v2a(data)
    yn += 1

def addZ(data):
    global zn
    if zn < N:
        z[zn] = v2a(data)
    zn += 1

""" Aurdino Data Aquisition """
board = Arduino(Arduino.AUTODETECT)
board.analog[0].register_callback(addY)
board.analog[0].enable_reporting()
board.analog[1].register_callback(addX)
board.analog[1].enable_reporting()
board.analog[2].register_callback(addZ)
board.analog[2].enable_reporting()
board.samplingOn(1000/fs)

print("Recording...")

while True:
    time.sleep(0.1)
    if xn >= N or yn >= N or zn >= N:
        break
board.exit()

""" Plot Recording """
plt.plot(x)
plt.plot(y)
plt.plot(z)
plt.show()

cut_a = input("Cut start sample: ")
cut_b = input("Cut stop sample: ")

if cut_a == '':
    cut_a = 0
else:
    cut_a = int(cut_a)

if cut_b == '':
    cut_b = N
else:
    cut_b = int(cut_b)

x = x[cut_a:cut_b]
y = y[cut_a:cut_b]
z = z[cut_a:cut_b]

plt.plot(x)
plt.plot(y)
plt.plot(z)
plt.show()

i = input("Save (Y/n):")
if i == 'Y' or i == 'y' or i == '':
    file_name = input("Enter file name: ")
    
    file = open("./Recordings/"+file_name+".csv", "w")

    for i in range(len(x)):
        file.write("{},{},{}\n".format(x[i], y[i], z[i]))
    
    file.close()