# -*- coding: utf-8 -*-
"""
@author: djimd
"""
"import packages"
import numpy as np
import pandas as pd
import os

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from skimage import io
from skimage.filters import gaussian

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
distanceSheet="distances"
"4: define starting index of shown filaments"
istart = 2


"=====CODE====="
"import crop coordinates from \2021imageAnalysisMEP\TEM\input"
absolute_path_e = os.path.join(os.getcwd(), 'input', excelName);
x1,y1,x2,y2= pd.read_excel(absolute_path_e, sheet_name=cropcoordSheet).to_numpy()[indexCropcoord,1:5]*pxpnm;
del cropcoordSheet, indexCropcoord
"import manual filaments from \2021imageAnalysisMEP\TEM\input"
lineCoord= pd.read_excel(absolute_path_e, sheet_name=filamentSheet).to_numpy()*pxpnm
del filamentSheet
"import filament distance data"
data= pd.read_excel(absolute_path_e, sheet_name=distanceSheet).to_numpy()
del excelName, absolute_path_e,distanceSheet
"import images from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(os.getcwd(), 'input', imageName);
I = io.imread(absolute_path_I);
I = I[round(y1):round(y2),round(x1):round(x2)]
del imageName, absolute_path_I

"select data"
dataList=data.ravel()
#dataList=data[:,0:53].ravel()
#dataList=data[:,53:92].ravel()
#dataList=data[:,92:151].ravel()
#dataList=data[:,151:203].ravel()
#dataList=data[:,203:229].ravel()
#dataList=data[:,229:267].ravel()
#dataList=data[:,267:281].ravel()
#dataList=data[:,281:293].ravel()

dataList = dataList[~np.isnan(dataList)]

"initiate plot"
fig = plt.figure(tight_layout=True)
fig.set_size_inches(10,4)
gs2 = gridspec.GridSpec(1, 2)
ax1 = fig.add_subplot(gs2[0, 0])
ax2 = fig.add_subplot(gs2[0, 1])
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 15}
plt.rc('font',**font)

"show blurred image"
ax1.imshow(gaussian(I, sigma=4),origin='upper',cmap='gray')
"show TEM image"
discreteLines =[]
for i in range(istart,int(lineCoord.shape[1]/2)): #line
    ax1.plot(lineCoord[:,i*2]-x1,lineCoord[:,i*2+1]-y1,'y.-',linewidth=2)
scalebar = ScaleBar(1/3.75, "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',font_properties={'size':15})
ax1.add_artist(scalebar)
ax1.axis('off')
"show histogram"
ax2.hist(dataList,bins=100,weights=np.zeros_like(dataList) + 1. / dataList.size)
ax2.set_xlabel('distance between filaments [nm]',fontsize=20)
ax2.set_ylabel('frequency',fontsize=20)
plt.setp(ax2.get_yticklabels(), fontsize=15);
plt.setp(ax2.get_xticklabels(), fontsize=15);