# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
"import packages"
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
    absolute_path_I = os.path.join(os.getcwd(), 'input', imgNameI)
    out=(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
    return out

#high denisty network
IM1 = importTxt(imgNameI = "2022.04.28-13.13.57.624__s2__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=0,ymax=100,xmin=256,xmax=512)
#lower denisty network
IM2 = importTxt(imgNameI = "2022.04.28-15.06.53.642__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_512px-10um.txt",ymin=52,ymax=152,xmin=25,xmax=281)
#isotropic network
IM3 = importTxt(imgNameI = "2022.05.24-12.14.46.827__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-5um.txt",ymin=0,ymax=171,xmin=0,xmax=512)

#denisity network
im1 =importTxt(imgNameI = "2022.06.09-12.23.00.222__s1__Si-SLB 5pip2 20dops-30 nM hex__QI_512px-5um.txt",ymin=0,ymax=500,xmin=170,xmax=290)
im2 =importTxt(imgNameI = "2022.04.26-13.40.39.612__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=60,ymax=130,xmin=20,xmax=80)
im3 =importTxt(imgNameI = "2022.04.28-14.27.34.852__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_768px-10um.txt",ymin=170,ymax=240,xmin=20,xmax=80)
im4 =importTxt(imgNameI = "2022.04.28-13.13.57.624__s2__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=150,ymax=220,xmin=20,xmax=80)

#blob
ag1 =importTxt(imgNameI = "2022.04.20-15.23.01.942__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt",ymin=0,ymax=86,xmin=0,xmax=256)
#denatured
ag2 =importTxt(imgNameI = "2022.05.17-16.37.27.660__s3__Si-SLB 5pip2 20dops-120 nM hex__QI_1024px-10um.txt",ymin=0,ymax=171,xmin=0,xmax=512)
#holes
ag3 =importTxt(imgNameI = "2022.05.18-15.20.19.617__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-5um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

##image distort
ia1 = importTxt(imgNameI = "2022.05.31-14.04.18.493__s1__Si-SLB 5pip2 20dops-60 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
#flat network
ia2 = importTxt(imgNameI = "2022.06.08-15.15.08.126__s2__Si-SLB 5pip2 20dops-60 nM hex__QI_1024px-6um.txt",ymin=0,ymax=114,xmin=300,xmax=641)
#copied artefacts
ia3 = importTxt(imgNameI = "2022.06.09-13.51.50.693__s1__Si-SLB 5pip2 20dops-30 nM hex__QI_512px-5um.txt",ymin=0,ymax=69,xmin=280,xmax=484)

#difficult
id1 = importTxt(imgNameI = "2022.04.28-12.01.55.152__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
id2 = importTxt(imgNameI = "2022.05.04-11.35.51.519__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

#oct zoom out
ioo1 = importTxt(imgNameI = "2022.07.26-15.18.51.971__s1__Si-SLB 5pip2 20dops-60 nM oct__QI_1024px-8um.txt",ymin=0,ymax=172,xmin=200,xmax=712)
ioo2 = importTxt(imgNameI = "2022.06.21-16.42.20.434__s4__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-4um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

#oct zoom in
ioi1 = importTxt(imgNameI = "2022.06.23-13.05.19.866__s2__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)
ioi2 = importTxt(imgNameI = "2022.06.28-14.00.36.398__s2__Si-SLB 5pip2 20dops-120 nM oct__QI_512px-2um.txt",ymin=0,ymax=172,xmin=0,xmax=512)

"===plot==="
def subplotgrid(fig,gs,y,x,I,clow,chigh,widthpx,widthnm):
    ax = fig.add_subplot(gs[y, x])
    cax=ax.imshow(I,'afmhot')
    cax.set_clim(clow, chigh)
    ax.axis('off')
    scalebar = ScaleBar(widthnm/widthpx, "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower right')#,label_formatter = lambda x, y:'')
    ax.add_artist(scalebar)
    cbar4 = plt.colorbar(cax, ax=ax,shrink=0.8,ticks=[clow,chigh])
    cbar4.set_ticklabels([str(clow)+" nm", str(chigh)+" nm"])
    cbar4.ax.tick_params(labelsize=15)

gs1 = gridspec.GridSpec(1,2)
gs2 = gridspec.GridSpec(1,4)
gs3 = gridspec.GridSpec(1,1)
gs4 = gridspec.GridSpec(2,1)
"""
fig1 = plt.figure(tight_layout=True)
fig1.set_size_inches(14,3) #width, height

subplotgrid(fig=fig1,gs=gs1,y=0,x=1,I=IM1,clow=0,chigh=30,widthpx=512,widthnm=10000)
subplotgrid(fig=fig1,gs=gs1,y=0,x=0,I=IM2,clow=0,chigh=30,widthpx=512,widthnm=10000)

fig2 = plt.figure(tight_layout=True)
fig2.set_size_inches(14,3) #width, height

subplotgrid(fig=fig2,gs=gs2,y=0,x=0,I=im1,clow=0,chigh=30,widthpx=512,widthnm=5000)
subplotgrid(fig=fig2,gs=gs2,y=0,x=3,I=im2,clow=0,chigh=30,widthpx=512,widthnm=10000)
subplotgrid(fig=fig2,gs=gs2,y=0,x=1,I=im3,clow=0,chigh=30,widthpx=512,widthnm=10000)
subplotgrid(fig=fig2,gs=gs2,y=0,x=2,I=im4,clow=0,chigh=30,widthpx=512,widthnm=10000)

fig3 = plt.figure(tight_layout=True)
fig3.set_size_inches(7,3) #width, height

subplotgrid(fig=fig3,gs=gs3,y=0,x=0,I=ag3,clow=0,chigh=20,widthpx=512,widthnm=5000)
"""
fig4 = plt.figure(tight_layout=True)
fig4.set_size_inches(7,6) #width, height

subplotgrid(fig=fig4,gs=gs4,y=1,x=0,I=IM1,clow=0,chigh=30,widthpx=512,widthnm=10000)
subplotgrid(fig=fig4,gs=gs4,y=0,x=0,I=IM2,clow=0,chigh=30,widthpx=512,widthnm=10000)
"""
subplotgrid(fig=fig4,gs=gs4,y=0,x=0,I=ia1,clow=0,chigh=25,widthpx=512,widthnm=2000)
subplotgrid(fig=fig4,gs=gs4,y=1,x=0,I=ia2,clow=0,chigh=30,widthpx=1024,widthnm=6000)

subplotgrid(fig=fig1,gs=gs1,y=0,x=0,I=ioo1,clow=0,chigh=30,widthpx=1024,widthnm=8000)
subplotgrid(fig=fig1,gs=gs1,y=0,x=1,I=ioo2,clow=0,chigh=30,widthpx=512,widthnm=4000)
"""