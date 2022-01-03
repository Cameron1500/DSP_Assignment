#!/usr/bin/env ipython
import numpy as np
from iir_filter import IIR_filter
from scipy import signal
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import csv
import os
import glob as glob
import re


####### User params ############
fs = 1000   # Max 1000
fn = fs / 2
figuresRelPath = "Figures/" # figures dir relative to the project root
saveNames = ["filterDesign_ImpulseResp.png","filterDesign_SettleTimeVsFc.png"]
doSave = True
doShow=True
####### enable Tex rendering ########################
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
####### figure out where the project root is ############
currentFilePath = os.getcwd()
rootDir = os.path.dirname(currentFilePath)  # this goes up 2 directory levels
figuresDirAbsPath = os.path.join(rootDir, figuresRelPath)
savePath=[]
for i in range(len(saveNames)):
    savePath.append(os.path.join(figuresDirAbsPath,saveNames[i]))
def powspace(start, stop, power, num):
    start = np.power(start, 1/float(power))
    stop = np.power(stop, 1/float(power))
    return np.power( np.linspace(start, stop, num=num), power)

def testFilter(IIRCoeficients,testSignal):
    testFilter = IIR_filter(IIRCoeficients)
    fSignal = np.empty(len(testSignal))
    for i in range(len(testSignal)):
        fSignal[i] = testFilter.filter(testSignal[i])
    return fSignal

ntraces = 10
# creates an exponentialy spaced array of cuttof frequencies to test
fc2test = powspace(0.02,20,5, ntraces)
idx =0
sos = []

#define step
tTest_s = 30 # time to plot filter response for
nsamples = fs*tTest_s
step = np.ones(nsamples)
t = np.arange(0,tTest_s,1/fs)

#
#n3DbPoint = 10**(-3/20)
settledThreshPc = 10
settledThresh = 1-settledThreshPc/100

#loop through all of the cuttof frequecies and calculate the settling time
settlingTime = np.empty(ntraces)
legendList = []
plt.figure(0,figsize=(10,5))
colors = plt.cm.gist_rainbow(np.linspace(0, 1, ntraces))
idx= 0
for fc in fc2test:
    sos.insert(idx,signal.bessel(filterOrd, fc / fn, "lowpass", output="sos", norm="mag"))
    testSignal = testFilter(sos[idx], step)
    if testSignal[-1]<settledThresh: # if the last val < thresh interp wont work
        settlingTime[idx] = np.inf
    else:
        settlingTimeFcn = interp1d(testSignal,t,kind = "linear")
        settlingTime[idx] = settlingTimeFcn(settledThresh)

    plt.plot(t,testSignal,color=colors[idx])
    legendList.append(f"$F_c$={fc:.2f}(Hz), $T_s$={settlingTime[idx]:.2f}(s)" )
    idx += 1 # increment the index
plt.plot([0,tTest_s],[1.1,1.1], "k--")
plt.plot([0,tTest_s], [settledThresh,settledThresh], "k--")
plt.xlim([0,2])
plt.axhspan(settledThresh,1.1,facecolor='k', alpha=0.2)
plt.legend(legendList, loc='center right')
plt.title("Filter Impulse Response vs Cutt-off Frequency")
plt.xlabel("time (s)")
plt.ylabel("Amp")
if doSave:
    plt.savefig(savePath[0])

plt.figure(1,figsize=(10,5))
plt.title("Settling Time vs Cutt-off Frequency")
plt.plot(fc2test,settlingTime,marker = 'o')

plt.ylabel(f"Settling time(s) ($\pm${settledThreshPc}\\%)")
plt.xlabel("Cuttof Freq (Hz)")


if doSave:
    plt.savefig(savePath[1])
if doShow:
    plt.show()
