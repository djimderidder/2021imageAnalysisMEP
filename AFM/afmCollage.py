# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:19:33 2023

@author: ridderdde
"""

import numpy as np
import pandas as pd
import os

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.colors import LightSource

"===import==="
def importTxt(imgNameI,ymin,ymax,xmin,xmax):
    absolute_path_I = os.path.join(r'F:\AFM_sorted\5PIP2_20DOPS', imgNameI)
    out=(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
    return out

#high denisty network
IM1 = importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-13.13.57.624__s2__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=0,ymax=100,xmin=256,xmax=512)
IM1 = IM1-7.6 #7.6, 1.10 ,0.07, 12.10, 1.65, 0.19
#lower denisty network
IM2 = importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-15.06.53.642__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_512px-10um.txt",ymin=52,ymax=152,xmin=25,xmax=281)
IM2 = IM2-10.46#10.46, 1.34, 0.06, 16.12, 2.48, 0.12
#zoom out
IM3 =importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-14.27.34.852__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_768px-10um.txt",ymin=0,ymax=600,xmin=0,xmax=768)
IM3 = IM3-9.89#9.89, 1.50, 0.06, 16.65, 2.76, 0.10
#isotropic network
IM4 = importTxt(imgNameI = r"hexamers\isotropicNetwork\2022.05.24-12.14.46.827__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-5um.txt",ymin=0,ymax=171,xmin=0,xmax=512)

#denisity network
im1 =importTxt(imgNameI = r"hexamers\denseNetwork\2022.06.09-12.23.00.222__s1__Si-SLB 5pip2 20dops-30 nM hex__QI_512px-5um.txt",ymin=0,ymax=500,xmin=170,xmax=290)
im2 =importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.26-13.40.39.612__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=60,ymax=130,xmin=20,xmax=80)
im3 =importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-14.27.34.852__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_768px-10um.txt",ymin=170,ymax=240,xmin=20,xmax=80)
im4 =importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-13.13.57.624__s2__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=150,ymax=220,xmin=20,xmax=80)

#no lipids
ii = (np.loadtxt(r"F:\AFM_sorted\no\hexamers\2021.10.20-16.35.37.806__s2__Si-120 nM hex__QI_512px-10um.txt")*10**9)[0:300,0:512]

#blob
ag1 =importTxt(imgNameI = r"hexamers\other\blobAndBundle\2022.04.20-15.23.01.942__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=0,ymax=86,xmin=0,xmax=256)
#denatured
ag2 =importTxt(imgNameI = r"hexamers\other\denatured\2022.05.17-16.37.27.660__s3__Si-SLB 5pip2 20dops-120 nM hex__QI_1024px-10um.txt",ymin=0,ymax=171,xmin=0,xmax=512)
#holes
ag3 =importTxt(imgNameI = r"hexamers\other\denaturedWithHoles\2022.05.18-15.20.19.617__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-5um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

##image distort
ia1 = importTxt(imgNameI = r"hexamers\coveredNetwork\2022.05.31-14.04.18.493__s1__Si-SLB 5pip2 20dops-60 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
#flat network
ia2 = importTxt(imgNameI = r"hexamers\other\network\2022.06.08-15.15.08.126__s2__Si-SLB 5pip2 20dops-60 nM hex__QI_1024px-6um.txt",ymin=0,ymax=114,xmin=300,xmax=641)
#copied artefacts
ia3 = importTxt(imgNameI = r"hexamers\denseNetwork\2022.06.09-13.51.50.693__s1__Si-SLB 5pip2 20dops-30 nM hex__QI_512px-5um.txt",ymin=0,ymax=69,xmin=280,xmax=484)

#difficult
id1 = importTxt(imgNameI = r"hexamers\denseNetwork\2022.04.28-12.01.55.152__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
id2 = importTxt(imgNameI = r"hexamers\other\denatured\2022.05.04-11.35.51.519__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

#oct zoom out
ioo1 = importTxt(imgNameI = r"octamers\coveredNetwork\2022.07.26-15.18.51.971__s1__Si-SLB 5pip2 20dops-60 nM oct__QI_1024px-8um.txt",ymin=0,ymax=172,xmin=200,xmax=712)
ioo2 = importTxt(imgNameI = r"octamers\other\denatured\2022.06.21-16.42.20.434__s4__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-4um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

#oct zoom in
ioi1 = importTxt(imgNameI = r"octamers\other\denatured\2022.06.23-13.05.19.866__s2__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
ioi2 = importTxt(imgNameI = r"octamers\other\denatured\2022.06.28-14.00.36.398__s2__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

"===plot==="
def subplotgridScalebar(fig,gs,y,x,I,clow,chigh,widthpx,widthnm):
    ax = fig.add_subplot(gs[y, x])
    cax=ax.imshow(I,'afmhot')
    cax.set_clim(clow, chigh)
    ax.axis('off')
    scalebar = ScaleBar(widthnm/widthpx, "nm",length_fraction=0.3,width_fraction=1/30,color='w',box_color='k',frameon=True,location='lower right')#,label_formatter = lambda x, y:'')
    ax.add_artist(scalebar)
    cbar4 = plt.colorbar(cax, ax=ax,shrink=0.8,ticks=[clow,chigh])
    cbar4.set_ticklabels([str(clow)+" nm", str(chigh)+" nm"])
    cbar4.ax.tick_params(labelsize=15)

def subplotgrid(fig,gs,y,x,I,clow,chigh,widthpx,widthnm):
    ax = fig.add_subplot(gs[y, x])
    cax=ax.imshow(I,'afmhot')
    cax.set_clim(clow, chigh)
    ax.axis('off')
    scalebar = ScaleBar(widthnm/widthpx, "nm",length_fraction=0.3,width_fraction=1/30,color='w',box_color='k',frameon=True,location='lower right')#,label_formatter = lambda x, y:'')
    ax.add_artist(scalebar)

gs1 = gridspec.GridSpec(1,2)
gs2 = gridspec.GridSpec(1,4)
gs3 = gridspec.GridSpec(2,1,height_ratios= [4, 0.5])
gs4 = gridspec.GridSpec(4,1,height_ratios= [4, 1, 4, 1])

fig1 = plt.figure(tight_layout=True)
fig1.set_size_inches(7,7) #width, height
subplotgrid(fig=fig1,gs=gs4,y=0,x=0,I=IM2,clow=0,chigh=20,widthpx=512,widthnm=10000)
ax = fig1.add_subplot(gs4[1,0])
ax.hist(IM2.ravel(),bins=200,density=True,color = "0.7")
ax.set_xlim(-10,30)
ax.set_ylabel('Frequency')
subplotgrid(fig=fig1,gs=gs4,y=2,x=0,I=IM1,clow=0,chigh=20,widthpx=512,widthnm=10000)
ax = fig1.add_subplot(gs4[3,0])
ax.hist(IM1.ravel(),bins=200,density=True,color = "0.7")
ax.set_xlim(-10,30)
ax.set_xlabel('Height (nm)')
ax.set_ylabel('Frequency')

#----
fig2 = plt.figure(tight_layout=True)
fig2.set_size_inches(7,6) #width, height

subplotgridScalebar(fig=fig2,gs=gs3,y=0,x=0,I=IM3,clow=0,chigh=20,widthpx=768,widthnm=10000)
ax = fig2.add_subplot(gs3[1,0])
ax.hist(IM3.ravel(),bins=200,density=True,color = "0.7")
ax.set_xlim(-10,30)
ax.set_xlabel('Height (nm)')
ax.set_ylabel('Frequency')

#---
fig3 = plt.figure(tight_layout=True)
fig3.set_size_inches(7,3.5) #width, height

subplotgrid(fig=fig3, gs=gs3,y=0,x=0,I=ii,clow=0,chigh=20,widthpx=512,widthnm=10000)
ax = fig3.add_subplot(gs3[1,0])
ax.hist(ii.ravel(),bins=200,density=True,color="0.7")
ax.set_xlim(-10,30)
ax.set_xlabel('Height (nm)')
ax.set_ylabel('Frequency')