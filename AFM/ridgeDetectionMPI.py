# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 14:52:38 2022

@author: djimd
"""

#from ridge_detection.gui import create_win

#if __name__ == "__main__":
#    create_win()
#C:\Users\djimd\Documents\GitHub\2021imageAnalysisMEP\AFM\input\2022.04.28-14.27.34.852__s3__Si-SLB 5pip2 20dops-120 nM hex__PF_768px-10um.tif

from ridge_detection.position import compute_line_points
from ridge_detection.convol import convolve_gauss
from ridge_detection.link import compute_contours

import numpy as np

def RidgeDetectionMPI(image):
    width = image.shape[0]
    height = image.shape[1]
    
    k=convolve_gauss(np.reshape(image, width*height),width,height,sigma=2)
    ismax = [0 for i in range(width * height)]
    ev = [0 for i in range(width * height)]
    n1 = [0 for i in range(width * height)]
    n2 = [0 for i in range(width * height)]
    p1 = [0 for i in range(width * height)]
    p2 = [0 for i in range(width * height)]
    
    contours= list()
    junctions = list()
    
    compute_line_points(
            ku=k, 
            ismax=ismax, 
            ev=ev, 
            nx=n1, 
            ny=n2, 
            px=p1, 
            py=p2, 
            width=width, 
            height=height, 
            low=0.34, 
            high=1.02, 
            mode='MODE_LIGHT')
    
    compute_contours(
            ismax=ismax, 
            eigval=ev, 
            normx=n1, 
            normy=n2, 
            posx=p1, 
            posy=p2, 
            gradx=k[0], 
            grady=k[1], 
            contours=contours , 
            sigma=2, 
            extend_lines=True, 
            mode='MODE_LIGHT', 
            width=width, 
            height=height, 
            junctions=junctions )
    Ix=np.reshape(k[0],[width,height])
    Iy=np.reshape(k[1],[width,height])
    Ixx=np.reshape(k[2],[width,height])
    Ixy=np.reshape(k[3],[width,height])
    Iyy=np.reshape(k[4],[width,height])
    #ismax, ev
    #subpixel postions (p1,p2)
    #line direction (n1,n2)
    return Ix, Iy, Ixx, Ixy, Iyy, contours, junctions