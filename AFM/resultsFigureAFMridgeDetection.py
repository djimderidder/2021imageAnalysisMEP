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

import skimage.io
from skimage.filters import meijering, sato, frangi, hessian, gaussian, threshold_otsu, prewitt_h, prewitt_v
from skimage.morphology import skeletonize, thin, binary_erosion
from skimage.feature import hessian_matrix, hessian_matrix_eigvals

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
"import: and crop coordinates"
absolute_path_I = os.path.join(drive,folder,nameI)
#absolute_path_Isim = os.path.join(r"D:\AFM_sorted\simulated\structure_1.tif")
image =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
#imagesim = np.array(skimage.io.imread(absolute_path_Isim),dtype=np.uint8)
cmap = plt.cm.gray
"pre-processing: remove outliers"
heightLimitUp = config['x4'][iConfig]+3*config['x5'][iConfig]
image[image>heightLimitUp]=heightLimitUp
heightLimitLow = config['x1'][iConfig]-3*config['x2'][iConfig]
image[image<heightLimitLow]=heightLimitLow
"pre-processing: detect ridges Steger"
#imageUnsharp = image-gaussian(image,sigma=np.sqrt(2)) #sigma = sqrt(sigma1**2+sigma**2)
#imageMask = imageUnsharp>=threshold_otsu(imageUnsharp*(imageUnsharp>0))

#imageHessian = hessian_matrix(skeletonize(imageMask),sigma=1)# hessian detection
#imagedy = prewitt_h(gaussian(skeletonize(imageMask),sigma=1))#prewitt is technically also a average filter
#imagedx = prewitt_v(gaussian(skeletonize(imageMask),sigma=1))#prewitt is technically also a average filter
from ridge_detection.lineDetector import LineDetector
from ridge_detection.params import Params,load_json
from skimage.util import img_as_ubyte

config_filename = os.path.join(os.getcwd(), 'input', "params.json")
json_data=load_json(config_filename)
params = Params(config_filename)

img = img_as_ubyte((image-np.min(image))/(np.max(image)-np.min(image)))
test=np.reshape(img, img.shape[0]*img.shape[1])
test=np.reshape(img, [img.shape[1],img.shape[0]])

detect = LineDetector(params=config_filename)
result = detect.detectLines(test)

plt.imshow(img,cmap)
for i in range(len(result)):
    plt.plot(result[i].col,result[i].row,'r')

angles = []
for i in range(len(result)):
    for j in result[i].angle:
        if j<np.pi:
            angles.append(j)
        else:
            angles.append(j-np.pi)

from circularHist import circular_hist
angles=np.asarray(angles)
fig, ax = plt.subplots(1,subplot_kw=dict(projection='polar'))
circular_hist(ax, angles, bins=50, density=True, offset=0, gaps=True)

    
H = hessian_matrix(img,sigma=1)
eigH = hessian_matrix_eigvals(H)
E = H[0]+H[2] #energy
c = (eigH[0]-eigH[1])/(eigH[0]+eigH[1]+0.000000001)#coherency
o = 1/2*np.arctan(2*H[1]/(H[1])-H[0])
o[np.isnan(o)]=0.554

from matplotlib.colors import hsv_to_rgb
hsvImage = np.empty([768,768,3])
hsvImage[:,:,0] = (o-np.ones(image.shape)*np.min(o))/(np.ones(image.shape)*(np.max(o))-np.ones(image.shape)*np.min(o))
hsvImage[:,:,1] = (image-np.ones(image.shape)*np.min(image))/(np.ones(image.shape)*np.max(image)-np.ones(image.shape)*np.min(image))
hsvImage[:,:,2] = (image-np.ones(image.shape)*np.min(image))/(np.ones(image.shape)*np.max(image)-np.ones(image.shape)*np.min(image))
plt.imshow(hsv_to_rgb(hsvImage))
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