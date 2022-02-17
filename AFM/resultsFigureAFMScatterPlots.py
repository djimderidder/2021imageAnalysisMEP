# -*- coding: utf-8 -*-
"""
@author: djimderidder
"""
"import packages"
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

'This code is to makes the scatter plots of the mean area fraction and mean height from the height distrution.'

#353
paramA = np.array([11.19910282,1.2002686,0.16911733,17.54120297,5.42380608,0.03567409])
#796
paramA= np.append([paramA], [np.array([9.62492721,1.24621865,0.11770916,15.7280332,6.22423358,0.04061226])], axis=0)
#032
paramA= np.append(paramA, [np.array([5.80360662,0.96998403,0.2094195 ,12.1862264,4.92489743,0.039692])], axis=0)
#485
paramA= np.append(paramA, [np.array([13.48001671,1.28341639,0.16038759,19.4545735,5.17912772,0.03654903])], axis=0)
#057
paramA= np.append(paramA, [np.array([6.21412761,0.68249614,0.37157333,10.12148474,3.36768782,0.04121926])], axis=0)
#703
paramA= np.append(paramA, [np.array([5.56217313,0.74668397,0.33232805,10.65256759,4.37309336,0.03307047])], axis=0)

#417
paramB = np.array([ 5.440208,1.05788838,0.10049249,15.05736016,3.81101934,0.07732931])
#505
paramB= np.append([paramB], [np.array([ 9.21892189,1.05326138,0.11048401,19.00868996,3.81814498,0.07397215])], axis=0)
#981
paramB= np.append(paramB, [np.array([ 7.57941008, 1.23730244,0.10442431, 16.83035666, 4.0983825 ,0.06631246])], axis=0)

#Con120
param60 = np.array([ 8.23565264,1.02377543,0.26388837,12.28106163,5.1350234,0.02455821])
param60 = np.append([param60],[np.array([ 9.15609123,1.24188027,0.18820556,11.45072864,8.03727083,0.02218889])],axis=0)
param60 = np.append(param60,[np.array([5.38815938,0.68260987,0.39840815,7.03153733,3.3472428,0.03531165])],axis=0)
#Con60
param120 = np.array([2.03888155e+01,2.70920565e+00,8.84224550e-02,3.36506536e+01,7.44793234e+00,2.14919323e-02])
param120 = np.append([param120],[np.array([1.85568079e+01,1.80645572e+00,1.00565665e-01,2.93251515e+01,1.00839551e+01, 2.19091879e-02])],axis=0)
param120 = np.append(param120,[np.array([2.04950243e+01,1.88987223e+00,1.02200952e-01,3.07567829e+01,1.12001726e+01, 1.87433074e-02])],axis=0)

#paramA=param60
#paramB=param120

fig = plt.figure(tight_layout=True)
fig.set_size_inches(3.2,3.2)
gs2 = gridspec.GridSpec(1,1)
ax = fig.add_subplot(gs2[0, 0])

ax.scatter(2*np.ones(paramB.shape[0]),-paramB[:,0]+paramB[:,3],facecolor='0.5',s=75)
ax.scatter(np.ones(paramA.shape[0]),-paramA[:,0]+paramA[:,3],facecolor='0.5',s=75)

plt.ylim([0, 15])
plt.xlim([0, 3])

a=ax.get_xticks().tolist()
a[0]=''
a[1]='Medium \n denisty'
a[2]='Dense'
a[3]=''
ax.set_xticklabels(a)
plt.setp(ax.get_yticklabels(), fontsize=12);
plt.setp(ax.get_xticklabels(), fontsize=12);

ax.set_ylabel('Mean filament height [nm]',fontsize=13)
#-------------------
fig = plt.figure(tight_layout=True)
fig.set_size_inches(3.2,3.2)
gs2 = gridspec.GridSpec(1,1)
ax = fig.add_subplot(gs2[0, 0])

AA = np.sqrt(2*np.pi)*paramA[:,4]*paramA[:,5]
AB = np.sqrt(2*np.pi)*paramB[:,4]*paramB[:,5]

ax.scatter(2*np.ones(paramB.shape[0]),AB,facecolor='0.5',s=75)
ax.scatter(np.ones(paramA.shape[0]),AA,facecolor='0.5',s=75)

plt.ylim([0, 0.8])
plt.xlim([0, 3])

a=ax.get_xticks().tolist()
a[0]=''
a[1]='Medium \n denisty'
a[2]='Dense'
a[3]=''
ax.set_xticklabels(a)
plt.setp(ax.get_yticklabels(), fontsize=12);
plt.setp(ax.get_xticklabels(), fontsize=12);

ax.set_ylabel('Mean area fraction',fontsize=15)