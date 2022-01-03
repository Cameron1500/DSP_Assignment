#!/usr/bin/env ipython

from posixpath import basename
import numpy as np
from iir_filter import IIR_filter
from scipy import signal
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import csv
import pandas
import os

thisRecording2Plot = ["Rest.csv"]
RecordingsDirRelPath = "Recordings/" # directory of recordings relative to the project root
figuresRelPath = "Figures/" # figures dir relative to the project root
saveNames = ["filterDesign_HarmonicNoise_Rest.png"]
doSave = True
doShow= True
fs = 1000
Ts = 1/fs                  # sample period
####### enable Tex rendering ########################
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
####### figure out where the project root is ############
currentFilePath = os.getcwd()
rootDir = os.path.dirname(currentFilePath)  # this goes up 2 directory levels
figuresDirAbsPath = os.path.join(rootDir, figuresRelPath)
recordingsDirAbsPath =os.path.join(rootDir,RecordingsDirRelPath)

savePath=[]

for i in range(len(saveNames)):
    savePath.append(os.path.join(figuresDirAbsPath,saveNames[i]))

loadRecordingsPath= []
for i in range(len(thisRecording2Plot)):
    loadRecordingsPath.append(os.path.join(recordingsDirAbsPath , thisRecording2Plot[i]))

plt.figure(0,figsize=(10,5))
nTraces = len(loadRecordingsPath)
colNames = ['x', 'y', 'z']
for i in range(nTraces):
    thisRecording2Plot = loadRecordingsPath[i]
    print(f"reading: {os.path.basename(thisRecording2Plot)}")
    ################## load data #############################
    thisRecording = pandas.read_csv(thisRecording2Plot, names = colNames)
    xAccel = thisRecording[["x"]].to_numpy() #
    xAccel = xAccel[:,0] # np.transpose(xAccel)
    ################## do fft #############################

    N =(len(xAccel))
    idxMax = int(N/2+1)
    df = fs/N
    fn = fs/2
    idx2Plot = np.arange(0,N/2)
    data_fft = np.fft.fft(xAccel)     #
    data_fft[0] = 0
    freqs = np.arange(0,fs,df)

    ################## do plotting #############################
    plt.plot(freqs[0:idxMax], abs(data_fft[0:idxMax]))

plt.xlabel("Freq (Hz)")
plt.ylabel("|x|")
plt.title("Harmonic Content of the Accelerometer Data")
plt.grid()
plt.xlim((0,500))
# plt.ylim((0,26))
if doSave:
    plt.savefig(savePath[0])
if doShow:
    plt.show()
