#!/usr/bin/env ipython
import numpy as np
from numpy.core.fromnumeric import transpose
from iir_filter import IIR_filter
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import interp1d
import csv
import os
import glob as glob
import re
# this function will also test the settling time of different filter orders

####### User params ############
fs = 650   # Max 1000
fn = fs / 2
filterOrd = 1
figuresRelPath = "Figures/" # figures dir relative to the project root
saveNames = ["filterDesign_Bessel_ImpulseResp_MultipleFilterOrders.png",
             "filterDesign_Bessel_SettleTimeVsFc_MultipleFilterOrders.png"]
doSave = True
doShow= True
####### enable Tex rendering in plots ########################
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
filterOrder2Test = [2,4,6,8]
ii =0
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

# plt.figure(0,figsize=(10,10))
fig0, (ax0,ax1) = plt.subplots(2,1,figsize=(10,10))
fig1, ax0_1 = plt.subplots(1,1,figsize=(10,5))
colors = plt.cm.gist_rainbow(np.linspace(0, 1, ntraces))
linestyles = ["-","--",":","-."]
#loop through all filter designs

settlingTime = []
legendList = []
for i in range(len(filterOrder2Test)):
    thisfilterOrder = filterOrder2Test[i]
    #loop through all of the cuttoff frequecies and calculate the settling time
    settlingTime.append(np.empty(ntraces)) # a list of arrays
    ii= 0
    for fc in fc2test:
        #filter design
        sos = signal.bessel(thisfilterOrder, fc / fn, "lowpass", output="sos", norm="mag")

        # here we effectively cascade all of the biquads
        testSignal = step
        testSignal = testFilter(sos, testSignal)

        # filter frequency response
        wnorm,freqRespMag = signal.sosfreqz(sos,worN=2**18)
        freqRespSiFreqs = (wnorm/np.pi)*fn
        if testSignal[-1]<settledThresh: # if the last val < thresh interp wont work
            thisSettlingTime = np.inf
        else:
            settlingTimeFcn = interp1d(testSignal,t,kind = "linear")
            thisSettlingTime = settlingTimeFcn(settledThresh)
        settlingTime[i][ii] = thisSettlingTime
        # plot the timedomain impulse response
        ax0.plot(t, testSignal, color=colors[ii], linestyle=linestyles[i])

        # plot the frequency response
        ax1.semilogx(freqRespSiFreqs, (abs(freqRespMag)), color = colors[ii],linestyle=linestyles[i])
        ax1.axvline(fc, linestyle="--", linewidth = 0.5, color=colors[ii])

        # add legend entry
        if i ==0:
            legendList.append(f"$F_c$={fc:.2f}(Hz)" )
        ii += 1 # increment the index
ax0.set_title("Filter Impulse Response vs Cutt-off Frequency")
ax0.plot([0,tTest_s],[1.1,1.1], "k--")
ax0.plot([0,tTest_s], [settledThresh,settledThresh], "k--")
ax0.set_xlim([0,2])
ax0.axhspan(settledThresh,1.1,facecolor='k', alpha=0.2)
custom_lines = []
legendList3 = []
for i in range(len(filterOrder2Test)):
    custom_lines.append(Line2D([0], [0], color=colors[0], lw=2, linestyle=linestyles[i]))
    legendList3.append(f"Bessel Filt Ord:{filterOrder2Test[i]}")
ax0.legend(custom_lines, legendList3,loc='center right')

custom_lines = []
for i in range((ntraces)):
    custom_lines.append(Line2D([0], [0], color=colors[i], lw=2 ))
ax1.legend(custom_lines, legendList, loc='center right')
ax0.set_xlabel("time (s)")
ax0.set_ylabel("Amplitude")
ax1.set_ylabel("Amplitude $(|x|)$")
ax1.set_xlabel("Frequency (Hz)")
# ax1.set_ylim([-10,0])
if doSave:
    fig0.savefig(savePath[0])

ax0_1.set_title("Settling Time vs Cutt-off Frequency")
legendList2 = []
for i in range(len(filterOrder2Test)):
    ax0_1.plot(fc2test,settlingTime[i][:],linestyle=linestyles[i])
    legendList2.append(f"Bessel Filt Ord: {filterOrder2Test[i]}")
ax0_1.set_ylabel(f"Settling time(s) ($\pm${settledThreshPc}\\%)")
ax0_1.set_xlabel("Cuttof Freq (Hz)")
ax0_1.legend(legendList2)
ax0_1.set_ylim([0,10])
ax0_1.set_xlim([0,10])
if doSave:
    fig1.savefig(savePath[1])
if doShow:
    plt.show()
