"""
@author: djimderidder
"""
# -*- coding: utf-8 -*-
"""
@author: djimd
"""
"import packages (make sure \2021imageAnalysisMEP\AFM\functions is in python path)"
import numpy as np
import os

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib_scalebar.scalebar import ScaleBar

from skimage import io
from skimage.transform import resize
from skimage.filters import sobel_v, sobel_h, gaussian

from circularHist import circular_hist

"====CONFIG==="
"1: define name of image"
imageName = "holes_pip_hex_network_c_20210818_50nM_010-3.75.tif";


"=====CODE====="
"import images from \2021imageAnalysisMEP\TEM\input"
absolute_path_I = os.path.join(os.getcwd(), 'input', imageName);
I = io.imread(absolute_path_I);
"crop and rescale image"
I = I[round(I.shape[0]*3/8):round(I.shape[0]*5/8),round(I.shape[1]*3/8):round(I.shape[1]*5/8)]
I = resize(I, (I.shape[0] // 4, I.shape[1] // 4), anti_aliasing=True)
"process image"
I= gaussian(I, sigma=2)
"calculate gradient with sobel operator"
sobel_y = sobel_v(I)
sobel_x = sobel_h(I)
gradMag = np.hypot(sobel_x, sobel_y)
gradDir = np.arctan2(sobel_y,sobel_x)
gradDir = gradDir[1:gradDir.shape[0]-1,1:gradDir.shape[0]-1]

"plot figure"
fig = plt.figure(tight_layout=True)
fig.set_size_inches(7,7)
gs2 = gridspec.GridSpec(1, 1)
ax1 = fig.add_subplot(gs2[0, 0])

cax=ax1.imshow(gradDir)
ax1.set_title('Gradient direction',fontsize=25)
scalebar = ScaleBar(1/(3.75/4), "nm",length_fraction=0.3,width_fraction=1/30,color='w',frameon=False,location='lower left',font_properties={'size':20})
ax1.add_artist(scalebar)
ax1.axis('off')

cax.set_clim(-np.pi,np.pi)
cbar = plt.colorbar(cax, ax=ax1,shrink=0.75,ticks=[-np.pi,np.pi])
cbar.set_ticklabels(["-\u03C0", "\u03C0"])
cbar.ax.tick_params(labelsize=20)

fig, ax = plt.subplots(1,subplot_kw=dict(projection='polar'))
circular_hist(ax, gradDir.ravel(), bins=50, density=True, offset=0, gaps=True)