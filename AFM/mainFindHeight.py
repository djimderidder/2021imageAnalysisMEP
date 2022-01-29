# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
"import packages (make sure \2021imageAnalysisMEP\AFM\functions is in python path)"
import numpy as np
import pandas as pd
import os

from scipy.optimize import curve_fit

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from whatExpected import WhatExpected

"====CONFIG==="
"1: define name of excel document and excel sheets"
excelNameI = "height.xlsx"
imageSheet = "resultsHexConcentrationAFM120_3"
"2:  difine if you want a figure"
booleanFig = True
maxHeightFig = 60
"optional: define expected value for the bimodal distribution, else leave curly brackets empty"
expected = (20,2,0.11,35,8,0.01)



"=====CODE====="
"import crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(os.getcwd(), 'input', excelNameI)
I = pd.read_excel(absolute_path_I, sheet_name=imageSheet).to_numpy()
I = (I-min(I.ravel()))*10**9
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
if booleanFig==True:
    fig = plt.figure(tight_layout=True)
    fig.set_size_inches(12,8)
    gs2 = gridspec.GridSpec(2, 2,width_ratios=[7,1],height_ratios= [3, 1])
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
    cbar = plt.colorbar(cax, ax=ax4,shrink=1,ticks=[0,maxHeightFig])
    cbar.set_ticklabels(["0 nm", maxHeightFig+"nm"])
    cbar.ax.tick_params(labelsize=20)
    
    scalebar = ScaleBar(10/512, "um",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',label_formatter = lambda x, y:'')
    ax3.add_artist(scalebar)
    
    dirName = os.path.join(os.getcwd(), 'output', 'resultsHeightAFM.png');
    fig.savefig(dirName, format='png', dpi=720)