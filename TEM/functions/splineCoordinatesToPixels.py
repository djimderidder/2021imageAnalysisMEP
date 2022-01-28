# -*- coding: utf-8 -*-
"""
@author: djimd
"""
import numpy as np
from skimage.draw import line

#---
def SplineCoordinatesToPixels(lineCoord):
    """
    Get pixel coordinates for each filament from spline points
    inputs
        lineCoord: arrays of x-y coordinates of linear splines
            NumPy array: [max(M_i)x2N]
                N = amount of filaments
                i = 1,2,...,N
                M_i = number of spline points for filament i
    returns
        discreteLines: list of x-y coordinates for pixels
            list: [N]
                N = amount of filaments
        
    """
    discreteLines =[]
    for i in range(0,int(lineCoord.shape[1]/2)): #line
        #ax.text(lineCoord[1,i*2]-x1,lineCoord[1,i*2+1]-y1,s=str(i), c='w',fontsize=12)
        discreteLine = np.empty((0,2))
        for j in range(0,sum((~np.isnan(lineCoord[:,i*2])*1))-1): #for loop of segement
            p1,p2=lineCoord[j:(j+2),i*2].astype(int)
            q1,q2=lineCoord[j:(j+2),i*2+1].astype(int)
            discreteLine=np.append(discreteLine,np.array(list(zip(*line(p1,q1,p2,q2)))),axis=0)
            del p1,q1,p2,q2,j
        discreteLines.append(discreteLine)
    return discreteLines
