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

plt.rcParams.update({'font.size': 22})
fig = plt.figure(tight_layout=True)
fig.set_size_inches(5,5)
gs2 = gridspec.GridSpec(1, 1)
ax1 = fig.add_subplot(gs2[0, 0])
ax1.boxplot([height1,np.zeros(5)], notch = True,whis = 0.75)
ax1.set_ylim([0, 10])
ax1.set_xlim([0.5,2.5])
ax1.set_ylabel('height [nm]')

a=ax1.get_xticks().tolist()
a[0]='hexamers'
a[1]='octamers'
ax1.set_xticklabels(a)
plt.setp(ax1.get_yticklabels(), fontsize=12);