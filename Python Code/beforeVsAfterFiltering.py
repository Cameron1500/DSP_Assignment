
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

thisRecording2Plot = ["SwipeUp_1.csv"]
RecordingsDirRelPath = "Recordings/" # directory of recordings relative to the project root
figuresRelPath = "Figures/" # figures dir relative to the project root
saveNames = ["filterDesign_BeforeVsAfterFilt_UnderMotion.png"]
doSave = True
doShow= True
fs = 650
Ts = 1/fs                  # sample period
fn = fs / 2
fc = 5                     # hz
plt.figure(0,figsize=(10,5))
plt.title(f"Raw Accelerometer Under Motion Data pre/post Filtering, Cuttof: {fc}Hz")
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

def testFilter(IIRCoeficients,testSignal):
    testFilter = IIR_filter(IIRCoeficients)
    fSignal = np.empty(len(testSignal))
    for i in range(len(testSignal)):
        fSignal[i] = testFilter.filter(testSignal[i])
    return fSignal

for i in range(len(saveNames)):
    savePath.append(os.path.join(figuresDirAbsPath,saveNames[i]))

loadRecordingsPath= []
for i in range(len(thisRecording2Plot)):
    loadRecordingsPath.append(os.path.join(recordingsDirAbsPath , thisRecording2Plot[i]))

nTraces = len(loadRecordingsPath)
colNames = ['x', 'y', 'z']
legendList = []
sos = signal.bessel(2, fc / fn, "lowpass", output="sos", norm="mag")
colors = plt.cm.gist_rainbow(np.linspace(0, 1, 3))
linestyles = ["-","--",":","-."]
for i in range(nTraces):
    thisRecording2Plot = loadRecordingsPath[i]
    print(f"reading: {os.path.basename(thisRecording2Plot)}")
    ################## load data #############################
    thisRecording = pandas.read_csv(thisRecording2Plot, names = colNames)
    N = len(thisRecording)
    t = np.arange(0, N*Ts ,Ts)
    for ii in range(len(thisRecording.columns)):
        selectedAccel = thisRecording[colNames[ii]].to_numpy() #
        thisAccel = selectedAccel #
        thisAccel_filt = testFilter(sos, thisAccel)
        ################## do plotting #############################
        plt.plot(t,thisAccel_filt, linestyle=linestyles[1],color=colors[ii], linewidth = 1)
        plt.plot(t,thisAccel, linestyle=linestyles[0], color=colors[ii], alpha = 0.4)
        legendList.append(f"{colNames[ii]} After Filtering")
        legendList.append(f"{colNames[ii]} Before Filtering")
plt.xlabel("time (s)")
plt.legend(legendList)
plt.ylabel("Acceleration (Raw)")
plt.grid()
# plt.xlim((0,500))
# plt.ylim((0,26))
if doSave:
    plt.savefig(savePath[0])
if doShow:
    plt.show()
