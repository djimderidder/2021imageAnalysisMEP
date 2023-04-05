# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
"import packages (make sure \2021imageAnalysisMEP\AFM\functions is in python path)"
import numpy as np
import pandas as pd
import os
import re
from ast import literal_eval

from scipy.optimize import curve_fit

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from whatExpected import WhatExpected

'This code is to fits the sum of two Gaussians on the height distrution.'

"====CONFIG==="
"1: define name of excel document and excel sheets"
nameconfig = "fitHeightDistributionshdn.xlsx"
drive = "D:\AFM_sorted"
folder = "5PIP2_20DOPS\hexamers\denseNetwork"

absolute_path_config = os.path.join(drive,folder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15

#nameI = "2022.04.26-13.40.39.612__s1__Si-SLB 5pip2 20dops-120 nM hex__QI_512px-10um.txt"
nameI = config['name'][iConfig]

#ymin = 0; ymax = 10000; xmin = 0; xmax= 10000;
ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]


"2: define crop region"
#ymin = 0; ymax = 204; xmin = 0; xmax= 512;
"3: define if you want a figure"
booleanFig = True
"optional: define expected value for the bimodal distribution, else leave curly brackets empty"
#expected = (6,1,0.1,10,1,0.2)
expected = literal_eval(config['params_estimation'][iConfig])

"=====CODE====="
plt.close('all')
"import crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(drive,folder,nameI)
I =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
print(I.shape)
"plot image"
y,x,_=plt.hist(I.ravel(),bins=100,density=True,color = "0.7")
plt.pause(0.1) #helps with showing image before asking questions
x=(x[1:]+x[:-1])/2 # correct hist data
"ask user questions"
if len(expected)!=6:
    expected = WhatExpected()
"fit"
def gauss(x,mu,sigma,A):
    return A*np.exp(-(x-mu)**2/2/sigma**2)

def bimodal(x,mu1,sigma1,A1,mu2,sigma2,A2):
    return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)
params,cov=curve_fit(bimodal,x,y,expected)

plt.plot(x,bimodal(x,*params),color='red',lw=3,label='model')

"plot image and histogram with fit"
maxHeightFig = np.round(params[3]+np.absolute(params[4])*2.5)
if booleanFig==True:
    fig = plt.figure(tight_layout=True)
    fig.set_size_inches(8,8)
    gs2 = gridspec.GridSpec(2, 2,width_ratios=[9,1],height_ratios= [3, 1])
    ax3 = fig.add_subplot(gs2[0, 0])
    ax2 = fig.add_subplot(gs2[1, 0])
    ax4 = fig.add_subplot(gs2[0, 1])
    
    
    y2,x2,_=ax2.hist(I.ravel()-params[0],bins=100,density=True,color = "0.7");
    x2=(x2[1:]+x2[:-1])/2
    
    ax2.plot(x2,gauss(x2,mu=0,sigma=params[1],A=params[2]),'k--',linewidth=2)
    ax2.plot(x2,gauss(x2,mu=params[3]-params[0],sigma=params[4],A=params[5]),'r--',linewidth=2)
    ax2.set_xlabel('Height above surface [nm]',fontsize=20)
    ax2.set_ylabel('Frequency',fontsize=25)
    ax2.set_ylim([0, 0.2])
    plt.setp(ax2.get_yticklabels(), fontsize=20);
    plt.setp(ax2.get_xticklabels(), fontsize=20);
    #============================
    cax = ax3.imshow(I,'afmhot')
    cax.set_clim(0,maxHeightFig)
    ax3.axis('off')
    ax4.axis('off')
    cbar = plt.colorbar(cax, ax=ax4,shrink=1,aspect=40,ticks=[0,maxHeightFig])
    cbar.set_ticklabels(["0 nm", str(maxHeightFig)+"nm"])
    cbar.ax.tick_params(labelsize=20)
    
    scalebar = ScaleBar(10/512, "um",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',label_formatter = lambda x, y:'')
    ax3.add_artist(scalebar)
    
    #dirName = os.path.join(os.getcwd(), 'output', 'resultsHeightAFM.png');
    #fig.savefig(dirName, format='png', dpi=720)

print(params)