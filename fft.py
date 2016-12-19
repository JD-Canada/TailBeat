# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:48:56 2016

@author: Jason
"""

import matplotlib.pyplot as plt

import numpy as np
import scipy as sy
import pylab as pyl
import pandas as pd


"""
Import contour data output from TailBeat.py
"""
data=pd.read_csv('contourarea.txt')                                                       #read in txt file with contour areas
data.columns=['Contour Area'] #names column header


"""
Data pre-processing
"""
data.ix[(data['Contour Area']>500)|(data['Contour Area']<50),('Contour Area')]=None #removes unwanted large and small contours, i.e. window when no fish is present and noise contours because of glare
data=data.interpolate() #interpolates the remaining points 
data['time']=data.index #adds "time" column based on index, which is actually the frame number from the video
yRaw=data['Contour Area'].tolist() #turn the pandas dataframe into a list



"""
Take a look at the original data signal
"""
xRaw=data['time'].tolist()
pyl.plot(xRaw, yRaw)



"""
Trim the array around the valid signal
"""
yTrimmed=yRaw[100:275] #keeps only wanted portion of data (i.e. frame range with a good signal)
xTrimmed=xRaw[100:275]
pyl.plot(xTrimmed, yTrimmed)



"""
Detrend the signal - use only if needed
"""
length=len(yTrimmed)
xPolyFit = sy.linspace(0, length*0.002, num=length)

model=np.polyfit(xPolyFit,yTrimmed,2) #fits second order polynomial 
predicted = np.polyval(model, xPolyFit) #creates points using fitted polynomial
yDetrended = yTrimmed-predicted
#plot the original, trend to remove and detrended data
fig, axes = plt.subplots(nrows=3, sharex=True)
axes[0].plot(xTrimmed, yTrimmed, 'ro')
axes[0].set(title='Original Data and 2nd Order Polynomial Trend')

axes[1].plot(xTrimmed, predicted, 'ro')
axes[1].set(title='Trend to remove')

axes[2].plot(xTrimmed, yDetrended, 'ro')
axes[2].set(title='Detrended Residual')

plt.show()



"""
Take and plot the power spectral density
"""
#choose one or the other
y=yTrimmed
y=yDetrended

pyl.subplot(211)
pyl.plot(xPolyFit, y)
pyl.subplot(212)
plt.psd(y, NFFT=64, Fs=500, noverlap=0,pad_to=300)
