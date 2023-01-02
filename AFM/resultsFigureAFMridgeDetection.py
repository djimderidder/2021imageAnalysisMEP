# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 23:46:21 2022

@author: djimd
"""
import numpy as np
import pandas as pd
import os
import re
from ast import literal_eval

import cv2

from skimage.filters import meijering, sato, frangi, hessian, gaussian, threshold_otsu, prewitt_h, prewitt_v
from skimage.morphology import skeletonize, thin, binary_erosion
from skimage.feature import hessian_matrix

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

"====CONFIG==="
"1: define name of excel document and excel sheets"
nameconfig = "fitHeightDistributionshdn.xlsx"
drive = "D:\AFM_sorted"
folder = "5PIP2_20DOPS\hexamers\denseNetwork"

absolute_path_config = os.path.join(drive,folder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15

nameI = config['name'][iConfig]

ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]

"=====CODE====="
plt.close('all')
"import: and crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(drive,folder,nameI)
image =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
cmap = plt.cm.gray
"pre-processing: remove outliers"
#heightLimit = config['x4'][iConfig]+3*config['x5'][iConfig]
"pre-processing: detect ridges Steger"
#imageUnsharp = image-gaussian(image,sigma=np.sqrt(2)) #sigma = sqrt(sigma1**2+sigma**2)
#imageMask = imageUnsharp>=threshold_otsu(imageUnsharp*(imageUnsharp>0))

#imageHessian = hessian_matrix(skeletonize(imageMask),sigma=1)# hessian detection
#imagedy = prewitt_h(gaussian(skeletonize(imageMask),sigma=1))#prewitt is technically also a average filter
#imagedx = prewitt_v(gaussian(skeletonize(imageMask),sigma=1))#prewitt is technically also a average filter

from ridgeDetectionMPI import RidgeDetectionMPI

Ix, Iy, Ixx, Ixy, Iyy, contours, junctions = RidgeDetectionMPI(image)

plt.imshow(image,cmap)
for i in range(len(contours)):
    plt.plot(contours[i].col,contours[i].row)
'''
#plot preprocessing
###
fig = plt.figure(tight_layout=True)
fig.set_size_inches(15,6)
gs = gridspec.GridSpec(2, 3,width_ratios=[1,1,1],height_ratios= [4, 1])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[0, 1], sharex=ax1, sharey=ax1)
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[0, 2], sharex=ax1, sharey=ax1)
ax6 = fig.add_subplot(gs[1, 2])

ax1.imshow(image, cmap=cmap)
ax2.hist(image.ravel(),bins=100)
ax3.imshow(imageUnsharp,cmap=cmap)
ax4.hist(imageUnsharp.ravel(),bins=100)
ax4.axvline(threshold_otsu(imageUnsharp*(imageUnsharp>0)),color='k')
ax5.imshow(skeletonize(imageMask)*1+imageMask*1,cmap=cmap)
ax6.hist((imageMask*1).ravel(),bins=2)
###
fig = plt.figure(tight_layout=True)
fig.set_size_inches(12.5,5)
gs = gridspec.GridSpec(2, 5,width_ratios=[1,1,1,1,1],height_ratios= [1, 1])
ax7 = fig.add_subplot(gs[0, 0])
ax8 = fig.add_subplot(gs[0, 1], sharex=ax7, sharey=ax7)
ax9 = fig.add_subplot(gs[0, 2], sharex=ax7, sharey=ax7)
ax10 = fig.add_subplot(gs[1, 0], sharex=ax7, sharey=ax7)
ax11 = fig.add_subplot(gs[1, 1], sharex=ax7, sharey=ax7)
ax12 = fig.add_subplot(gs[1, 2], sharex=ax7, sharey=ax7)
ax13 = fig.add_subplot(gs[:,3:5], sharex=ax7, sharey=ax7)

ax7.imshow(skeletonize(imageMask)*1,cmap=cmap)
ax8.imshow(dx,cmap=cmap)
ax9.imshow(dy,cmap=cmap)
ax10.imshow(dxx,cmap=cmap)
ax11.imshow(dxy,cmap=cmap)
ax12.imshow(dyy,cmap=cmap)
ax13.imshow(skeletonize(imageMask)*1,cmap=cmap)
ax13.quiver(ridgePoint[:,0],ridgePoint[:,1],ridgeValue*ridgeDirection[:,0],ridgeValue*ridgeDirection[:,1],color='c')

#plot ridge detection
fig, axes = plt.subplots(2, 2)
result=meijering(image)
axes[0,0].imshow(result, cmap=cmap)
result=sato(image)
axes[0,1].imshow(result, cmap=cmap)
result=frangi(image)
axes[1,0].imshow(result, cmap=cmap)
result=hessian(image)
axes[1,1].imshow(result, cmap=cmap)

'''