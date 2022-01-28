# -*- coding: utf-8 -*-
"""
@author: djimd
"""
import os
import time

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from skimage.filters import gaussian
#---
def FigureSplinesOverImage(I,lineCoord,x1,y1,booleanBlur=True,booleanSave=False,booleanScalebar=False):
    """
    Plot
    inputs
        lineCoord: arrays of x-y coordinates of linear splines
        I
        x1
        y1
        lineCoord
        
        booleanBlur
        booleanSave
        booleanScalebar
    returns
        discreteLines: list of x-y coordinates for pixels
            list: [N]
                N = amount of filaments
        K
            int
        kplus
            int
        kmin
            int
        
    """
    if booleanBlur==True:
        I= gaussian(I, sigma=4)
        
    fig = plt.figure(tight_layout=True)
    fig.set_size_inches(5,5)
    gs = gridspec.GridSpec(1, 1)
    ax = fig.add_subplot(gs[0, 0])

    ax.imshow(I,origin='upper',cmap='gray')
    for i in range(0,int(lineCoord.shape[1]/2)): #line
        ax.plot(lineCoord[:,i*2]-x1,lineCoord[:,i*2+1]-y1,'y.-',linewidth=2)
        ax.text(lineCoord[1,i*2]-x1,lineCoord[1,i*2+1]-y1,s=str(i), c='w',fontsize=12)
            
    if booleanScalebar==True:
        scalebar = ScaleBar(1/3.75, "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',font_properties={'size':15})
        ax.add_artist(scalebar)    
    
    ax.axis('off')
    
    if booleanSave==True:
        dirName = os.path.join(os.getcwd(), 'output', 'FigureSplinesOverImage.png');
        fig.savefig(dirName, format='png', dpi=720)
    plt.pause(0.1)