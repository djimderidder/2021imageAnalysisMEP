# -*- coding: utf-8 -*-
"""
@author: djimd
"""
"import packages (make sure \2021imageAnalysisMEP\TEM\functions is in python path)"
import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from skimage import io

from splineCoordinatesToPixels import SplineCoordinatesToPixels
from figureSplinesOverImage import FigureSplinesOverImage
from whichFilament import WhichFilament
from distanceFilaments import DistanceFilaments



"====CONFIG==="
"1: define name of image"
imageName = "holes_pip_hex_network_c_20210818_50nM_010-3.75.tif";
"2: define pixel scale [pixel/nm]"
pxpnm = 3.75;
"3: define name of excel document and excel sheets"
excelName = "manualLines.xlsx";
cropcoordSheet = "crops"
indexCropcoord = 7;
filamentSheet="TEM010"



"=====CODE====="
"import crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_e = os.path.join(os.getcwd(), 'input', excelName);
x1,y1,x2,y2= pd.read_excel(absolute_path_e, sheet_name=cropcoordSheet).to_numpy()[indexCropcoord,1:5]*pxpnm;
del cropcoordSheet, indexCropcoord
"import manual filaments from \2021imageAnalysisMEP\TEM\input"
lineCoord= pd.read_excel(absolute_path_e, sheet_name=filamentSheet).to_numpy()*pxpnm
del excelName, absolute_path_e, filamentSheet
"import images from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(os.getcwd(), 'input', imageName);
I = io.imread(absolute_path_I);
I = I[round(y1):round(y2),round(x1):round(x2)]
del imageName, absolute_path_I

"plot image"
FigureSplinesOverImage(I,lineCoord,x1,y1,booleanSave=False)
"ask user questions"
K,kmin,kplus = WhichFilament(lineCoord)
"get pixel values for each filament"
discreteLines= SplineCoordinatesToPixels(lineCoord)
"calculate distance"
Out1, Out2 = DistanceFilaments(discreteLines,K,kmin,kplus,pxpnm)
print('Code is ready')