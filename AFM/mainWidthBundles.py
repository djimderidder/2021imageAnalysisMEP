# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
"import packages"
import numpy as np
import pandas as pd
import scipy
import os

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

from skimage.filters import  gaussian,threshold_otsu
from skimage.morphology import skeletonize
from skimage import measure

"====CONFIG==="
"1: define name of excel document and excel sheets"
excelNameI = "height.xlsx"
imageSheet = "resultsHexConcentrationAFM120"
"2: define width of figure in nm"
figWidth = 5000
"3: define amount of bins in histogram"
histBins = 50


"=====CODE====="
"import crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(os.getcwd(), 'input', excelNameI)
I = pd.read_excel(absolute_path_I, sheet_name=imageSheet).to_numpy()
I = (I-min(I.ravel()))*10**9
#I[I > 60] = np.median(I) #turn on if thresholding doesnt detects filaments
"preprocess"
I2 = gaussian(I, sigma=2)
t = threshold_otsu(I)
t2 = threshold_otsu(I2)
mask = I2>t2
"find skeleton"
skel = skeletonize(mask*1)
skelCoord = np.transpose(np.array(np.where(skel)))
"find contours"
contours = measure.find_contours(I, t) #change to t2 if tail foreground distribution too high
contours2 = []
dist = np.array([])
for contour in contours:
    if contour .shape[0]>30:
        contours2.append(contour)
        dist = np.append(dist,scipy.spatial.distance.cdist(skelCoord,contour).min(axis=0))
"prepare plot"
fig = plt.figure(tight_layout=True)
fig.set_size_inches(7,4)
gs = gridspec.GridSpec(1, 1)
ax2 = fig.add_subplot(gs[0, 0])
"plot skeleton"
ax2.imshow(I, cmap=plt.cm.gray)
ax2.plot(skelCoord[:,1],skelCoord[:,0],'y.')
plt.xlim([128, 384])
plt.ylim([64,192])
ax2.axis('off')
"plot contours"
c=np.empty([3,1])
for contour in contours2:
    #ax3.imshow(I,'gray')
    ax2.plot(contour[:, 1], contour[:, 0],'m', linewidth=2)
    #ax3.axis('off')
"prepare next plot"
fig = plt.figure(tight_layout=True)
fig.set_size_inches(10,4)
gs2 = gridspec.GridSpec(1, 1)
ax3 = fig.add_subplot(gs2[0, 0])
"plot histogram"
histData=2*dist*figWidth/I.shape[1]
ax3.hist(histData,bins=histBins,weights=np.zeros_like(histData) + 1. / histData.size)
ax3.set_xlabel('measured width [nm]',fontsize=20)
ax3.set_ylabel('frequency',fontsize=20)
plt.setp(ax3.get_yticklabels(), fontsize=15);
plt.setp(ax3.get_xticklabels(), fontsize=15);
"print mean and std"
print(np.mean(histData))
print(np.std(histData))