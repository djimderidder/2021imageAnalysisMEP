# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

def DistanceFilaments(discreteLines,K,kmin,kplus,pxpnm):
    """
    Plot
    inputs
        discreteLines
        K
        kmin
        kplus
        pxnm
    returns
        Out1
        Out2    
    """
    kk = discreteLines[K].shape[0]
    gumin = np.zeros((kk,kmin+kplus+1))
    gdmin = np.zeros((kk,kmin+kplus+1))
    
    fig = plt.figure(tight_layout=True)
    fig.set_size_inches(5,5)
    gs = gridspec.GridSpec(1, 1)
    ax = fig.add_subplot(gs[0, 0])
    
    for i in range(0,kk): #measured line length
        for h in range(K-kmin,K+kplus+1): #amount of lines
            ll = discreteLines[h].shape[0]
            gup = np.zeros((kk,ll))
            gdown = np.zeros((kk,ll))
            for j in range(0,ll): #lenght of comparing line
                if not h==K:
                    if K<=h:
                        gup[i,j] = np.linalg.norm(discreteLines[K][i]-discreteLines[h][j])
                        gdown[i,j] = np.inf
                    if K>=h:
                        gdown[i,j]= np.linalg.norm(discreteLines[K][i]-discreteLines[h][j])
                        gup[i,j] = np.inf
                else:
                    gdown[i,j] = np.inf
                    gup[i,j] = np.inf
            gumin[i,h-(K-kmin)] = np.min(gup[i,:])/pxpnm
            gdmin[i,h-(K-kmin)] = np.min(gdown[i,:])/pxpnm
            ax.plot(discreteLines[h][:,0],discreteLines[h][:,1],'r')
            
            del gup, gdown
    
    ax.plot(discreteLines[K][:,0],discreteLines[K][:,1], 'b')
    
    Out1=np.min(gdmin,axis=1)
    Out2=np.min(gumin,axis=1)
    
    fig = plt.figure(tight_layout=True)
    plt.plot(Out1,'m') #high
    plt.plot(Out2,'c') #low
    plt.xlabel('distance along filament [pixels]',fontsize=20)
    plt.ylabel('distance to closest filament [nm]',fontsize=20)
    
    return Out1,Out2