# -*- coding: utf-8 -*-
"""
theory from
https://www.sciencedirect.com/science/article/pii/0098300493900538?via%3Dihub
@author: ridderdde
"""


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

##########################################
# Loading libraries and data
##########################################
#
import numpy as np
from numpy.fft import fft2, ifft2
from scipy import signal
import os
import re
import pandas as pd


#pip install orientationpy

# Load the greyscale image (and convert it to float)
fileFolder = r"F:\AFM_sorted\5PIP2_20DOPS\hexamers\denseNetwork"
nameconfig = "fitHeightDistributionshdn.xlsx"

absolute_path_config = os.path.join(fileFolder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15

#load image
nameI = config['name'][iConfig]
scale =10000/768 #nm/px
ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]
absolute_path_I = os.path.join(fileFolder,nameI)
im =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]

#preprocessing
heightLimitUp = config['x4'][iConfig]+3*config['x5'][iConfig]
im[im>heightLimitUp]=heightLimitUp
heightLimitLow = config['x1'][iConfig]-3*config['x2'][iConfig]
im[im<heightLimitLow]=heightLimitLow
im = (im-heightLimitLow)/(heightLimitUp-heightLimitLow)*255

##########################################
# fft-based autocorrelation Correlogram
##########################################
N = im.shape[0]
N4 = int(N/4)

xystep=20
rstep=10
avgMeancorr=np.zeros(rstep)

if im.shape[0]==im.shape[1]:
    for rr in range(rstep):
        print('|==========|\n|', end = '')
        r = int(np.floor(N4*(rr+1)/rstep))
        
        paddedIm = np.zeros([N+r,N+r])
        paddedIm[r:N+r,r:r+N] = im
        dataFT = fft2(paddedIm)
        window = np.zeros(paddedIm.shape)       
        
        Meancorr = np.zeros([xystep,xystep])
        for xi in range(xystep):
            xx = int((N/2)/xystep*(xi+1))
            if xi%(xystep/10)==0:print('=', end = '');
            for yi in range(xystep):
                yy = int((N/2)/xystep*(yi+1))
                window[0:2*r,0:2*r]=im[xx+N4-r:xx+N4+r,yy+N4-r:yy+N4+r]
                dataFTw = fft2(window)
                corr = ifft2(dataFT * np.conjugate(dataFTw)).real
                #corr = signal.correlate2d(im, im[xx+N4-r:xx+N4+r,yy+N4-r:yy+N4+r], boundary='symm', mode='same')
                Meancorr[xi,yi] = np.mean(corr[0:N,0:N])/(2*r)**2
        print('|\n')
        avgMeancorr[rr]=np.mean(Meancorr)
        
R = np.linspace(0,N4,rstep+1,dtype=int)[1:]*scale
'''
fig, ax = plt.subplots()
ax.imshow(corr[0:N,0:N]);ax.plot(xx+N4,yy+N4,'x',color='white')
rect = patches.Rectangle((xx+N4-r, yy+N4-r), 2*r, 2*r, linewidth=1, edgecolor='b', facecolor='none')
ax.add_patch(rect)

rect = patches.Rectangle((N4, N4), N/2, N/2, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
'''
