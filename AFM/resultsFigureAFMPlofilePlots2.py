# -*- coding: utf-8 -*-
"""
@author: djimd
"""
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


"===import==="
namedata = "fitHeightDistributionshdn.xlsx"
drive = "D:\AFM_sorted"
folder = "5PIP2_20DOPS\hexamers\denseNetwork"

absolute_path_data = os.path.join(drive,folder,namedata)
data = pd.read_excel(absolute_path_data,skiprows=1)

namedata = "fitHeightDistributionshcn.xlsx"
folder = "5PIP2_20DOPS\hexamers\coveredNetwork"

absolute_path_data = os.path.join(drive,folder,namedata)
data = pd.concat([data,pd.read_excel(absolute_path_data,skiprows=1)],ignore_index=True)

height2 = np.empty((0,1))
height1 = np.empty((0,1))

for i, row in data.iterrows():
    if data['x3'][i]*1000>data['x6'][i]:
        height2 = np.append(height2,np.absolute(data['x4'][i]-data['x1'][i]))
    if data['x3'][i]*4>data['x6'][i]:
        height1 = np.append(height1,np.absolute(data['x4'][i]-data['x1'][i]))

fig1, ax1 = plt.subplots()
ax1.boxplot([height1,height2], notch = True,whis = 0.75)
ax1.set_ylim([0, 10])
ax1.set_ylabel('height [nm]')