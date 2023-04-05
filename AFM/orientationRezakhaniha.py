# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:27:46 2023
@author: ridderdde
"""
import numpy as np
import pandas as pd
import os
import re

import skimage.io
from skimage.util import img_as_uint, img_as_ubyte
from skimage.filters import  gaussian,threshold_otsu, hessian
from skimage.morphology import skeletonize, thin, dilation, label
from skimage.feature import corner_harris, corner_subpix, corner_peaks, structure_tensor, canny
from skimage.transform import probabilistic_hough_line
from skimage.draw import line

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar
colorOI=['#000000','#E69F00','#56B4E9','#009E73','#F0E442','#0072B2','#D55E00','#CC79A7']
cmap = plt.cm.gray

#config
fileFolder = r"D:\AFM_sorted\5PIP2_20DOPS\hexamers\denseNetwork"
nameconfig = "fitHeightDistributionshdn.xlsx"

absolute_path_config = os.path.join(fileFolder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15

#load image
nameI = config['name'][iConfig]

ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]

absolute_path_I = os.path.join(fileFolder,nameI)
image =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]

#preprocessing
heightLimitUp = config['x4'][iConfig]+3*config['x5'][iConfig]
image[image>heightLimitUp]=heightLimitUp
heightLimitLow = config['x1'][iConfig]-3*config['x2'][iConfig]
image[image<heightLimitLow]=heightLimitLow

from ridge_detection.convol import convolve_gauss
def gaussDerivative(img,sigma):
    width=img.shape[0]
    height=img.shape[1]
    
    imgpxls2 = np.reshape(img,width*height)
    k = convolve_gauss(imgpxls2,width,height,sigma)
    
    r = {}
    r['ry'] = np.reshape(k[0],[width,height])
    r['rx'] = np.reshape(k[1],[width,height])
    r['ryy'] = np.reshape(k[2],[width,height])
    r['rxy'] = np.reshape(k[3],[width,height])
    r['rxx'] = np.reshape(k[4],[width,height])
                           
    return r

r = gaussDerivative(image,sigma=2) #rx = r['rx']

from numpy.linalg import eig
def  orderEigH(r):
    width=r['rx'].shape[0]
    height=r['rx'].shape[1]
    
    eigval = np.zeros([width,height,2])
    eigvec = np.zeros([width,height,2,2])
    for xx in range(height):
        for yy in range(width):
            kx = r['rx'][xx,yy]
            ky = r['ry'][xx,yy]
            kxx = r['rxx'][xx,yy]
            kxy = r['rxy'][xx,yy]
            kyy = r['ryy'][xx,yy]
            H = np.array([[kxx,kxy],[kxy,kyy]])
            w,v = eig(H)
            if abs(w[0])>abs(w[1]):
                eigval[xx,yy,0] = w[0]
                eigvec[xx,yy,0] = v[0]
                eigval[xx,yy,1] = w[1]
                eigvec[xx,yy,1] = v[1]
            elif abs(w[0])<abs(w[1]):
                eigval[xx,yy,0] = w[1]
                eigvec[xx,yy,0] = v[1]
                eigval[xx,yy,1] = w[0]
                eigvec[xx,yy,1] = v[0]
            else:
                if w[0]<w[1]:
                    eigval[xx,yy,0] = w[0]
                    eigvec[xx,yy,0] = v[0]
                    eigval[xx,yy,1] = w[1]
                    eigvec[xx,yy,1] = v[1]
                else:
                    eigval[xx,yy,0] = w[0]
                    eigvec[xx,yy,0] = v[0]
                    eigval[xx,yy,1] = w[1]
                    eigvec[xx,yy,1] = v[1]                    
    return eigval, eigvec

def circular_hist(ax, x, bins=16, density=True, offset=0, gaps=True):
    """
    Produce a circular histogram of angles on ax.
    Parameters
    ----------
    ax : matplotlib.axes._subplots.PolarAxesSubplot
        axis instance created with subplot_kw=dict(projection='polar').
    x : array
        Angles to plot, expected in units of radians.
    bins : int, optional
        Defines the number of equal-width bins in the range. The default is 16.
    density : bool, optional
        If True plot frequency proportional to area. If False plot frequency
        proportional to radius. The default is True.
    offset : float, optional
        Sets the offset for the location of the 0 direction in units of
        radians. The default is 0.
    gaps : bool, optional
        Whether to allow gaps between bins. When gaps = False the bins are
        forced to partition the entire [-pi, pi] range. The default is True.
    Returns
    -------
    n : array or list of arrays
        The number of values in each bin.
    bins : array
        The edges of the bins.
    patches : `.BarContainer` or list of a single `.Polygon`
        Container of individual artists used to create the histogram
        or list of such containers if there are multiple input datasets.
    """
    # Wrap angles to [-pi, pi)
    x = (x+np.pi) % (2*np.pi) - np.pi

    # Force bins to partition entire circle
    if not gaps:
        bins = np.linspace(-np.pi, np.pi, num=bins+1)

    # Bin data and record counts
    n, bins = np.histogram(x, bins=bins)

    # Compute width of each bin
    widths = np.diff(bins)

    # By default plot frequency proportional to area
    if density:
        # Area to assign each bin
        area = n / x.size
        # Calculate corresponding bin radius
        radius = (area/np.pi) ** .5
    # Otherwise plot frequency proportional to radius
    else:
        radius = n

    # Plot data on ax
    patches = ax.bar(bins[:-1], radius, zorder=1, align='edge', width=widths,
                     edgecolor='C0', fill=False, linewidth=1)

    # Set the direction of the zero angle
    ax.set_theta_offset(offset)

    # Remove ylabels for area plots (they are mostly obstructive)
    if density:
        ax.set_yticks([])

    return n, bins, patches

orientationI = np.nan_to_num(0.5*np.arctan(2*r['rxy']/(r['ryy']-r['rxx'])))
orientationI=orientationI[8:760,8:760]
#coherencyI = eigvalI[:,:,0]-eigvalI[:,:,1]/(eigvalI[:,:,0]+eigvalI[:,:,1])
coherencyI = np.sqrt((r['ryy']-r['rxx'])**2+5*r['rxy']**2)/(r['ryy']+r['rxx'])
coherencyI[coherencyI<0]=0
coherencyI[coherencyI>1]=1
coherencyI = coherencyI[8:760,8:760]
energyI = r['rxx']+r['ryy']
energyI = energyI[8:760,8:760]


from matplotlib.colors import hsv_to_rgb
hsvI = np.zeros([752,752,3])
hsvI[:,:,0] = (orientationI+np.pi)/(2*np.pi)
hsvI[:,:,1] = coherencyI
img = image[8:760,8:760]
hsvI[:,:,2] = img/25
fig = plt.figure()
plt.axis('off')
plt.imshow(hsv_to_rgb(hsvI))

filterOrientation = orientationI[(coherencyI>0.6)*(energyI>0.2)]
for i in range(filterOrientation.shape[0]):
    if filterOrientation[i]<0:
        filterOrientation[i]=filterOrientation[i]+np.pi
    
fig, ax = plt.subplots(1,subplot_kw=dict(projection='polar'))
circular_hist(ax, filterOrientation, bins=50,density =True,offset=0,gaps=True)

#test image
imagetest = np.array(skimage.io.imread(r"C:\Users\djimd\Downloads\chirp.tif"),dtype=np.uint8)
rtest = gaussDerivative(imagetest,sigma=1) #rx = r['rx']

orientationItest = np.nan_to_num(0.5*np.arctan(2*rtest['rxy']/(rtest['ryy']-rtest['rxx'])))
orientationItest=orientationItest[8:248,8:248]
coherencyItest = np.sqrt((rtest['ryy']-rtest['rxx'])**2+5*rtest['rxy']**2)/(rtest['ryy']+rtest['rxx'])
coherencyItest[coherencyItest<0]=0
coherencyItest[coherencyItest>1]=1
coherencyItest = coherencyItest[8:248,8:248]
energyItest = rtest['rxx']+rtest['ryy']
energyItest = energyItest[8:248,8:248]

hsvItest = np.zeros([240,240,3])
hsvItest[:,:,0] = (orientationItest+np.pi)/(2*np.pi)
hsvItest[:,:,1] = coherencyItest
imgtest = imagetest[8:248,8:248]
hsvItest[:,:,2] = imgtest
fig2 = plt.figure()
plt.imshow(hsv_to_rgb(hsvItest))
plt.axis('off')