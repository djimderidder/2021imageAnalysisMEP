import matplotlib
import matplotlib.colors

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

##########################################
# Loading libraries and data
##########################################
#
import numpy
import orientationpy
from skimage.draw import disk
import skimage.io
import os
import re
import pandas as pd

from CircularHist import circular_hist, weighted_circular_hist

#pip install orientationpy

# Load the greyscale image (and convert it to float)
fileFolder = r"F:\AFM_sorted\5PIP2_20DOPS\hexamers\denseNetwork"
nameconfig = "fitHeightDistributionshdn.xlsx"

absolute_path_config = os.path.join(fileFolder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15

#load image
nameI = config['name'][iConfig]
ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]
absolute_path_I = os.path.join(fileFolder,nameI)
im =(numpy.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]

#preprocessing
heightLimitUp = config['x4'][iConfig]+3*config['x5'][iConfig]
im[im>heightLimitUp]=heightLimitUp
heightLimitLow = config['x1'][iConfig]-3*config['x2'][iConfig]
im[im<heightLimitLow]=heightLimitLow
im = (im-heightLimitLow)/(heightLimitUp-heightLimitLow)*255

# Show image
plt.imshow(im, cmap="Greys_r")
plt.title("Original image")
plt.show()

#set up figures
fig1 = plt.figure(tight_layout=True)
fig1.set_size_inches(15,10) #height, width
gs6 = gridspec.GridSpec(3,2)

fig2 = plt.figure(tight_layout=True)
fig2.set_size_inches(5,15) #width, height
gs3 = gridspec.GridSpec(3,1)

fig3 = plt.figure(tight_layout=True)
fig3.set_size_inches(5,15) #width, height

fig4 = plt.figure(tight_layout=True)
fig4.set_size_inches(7,6) #width, height
gs1 = gridspec.GridSpec(1,1)
cmap = matplotlib.cm.hsv
norm = matplotlib.colors.Normalize(vmin=-90, vmax=90)

fig5, ax5 = plt.subplots(1,subplot_kw=dict(projection='polar'))
fig6, ax6 = plt.subplots(1,subplot_kw=dict(projection='polar'))

##########################################
# Parameters
##########################################
sig = 2

##########################################
# Computing Image Gradients
##########################################
mask = numpy.zeros(im.shape, dtype=numpy.uint8)
rr, cc = disk((im.shape[0]/2, im.shape[1]/2), (im.shape[0]/2)-2, shape=im.shape)
mask[rr, cc] = 1
mask= mask>0


for n, mode in enumerate(["finite_difference", "splines", "gaussian"]):
    #estimation gradient
    Gy, Gx = orientationpy.computeGradient(im, mode=mode)
    
    ax = fig1.add_subplot(gs6[n,0])
    ax.set_title(f"{mode}-Gy")
    ax.imshow(Gy, cmap="coolwarm", vmin=-64, vmax=64)

    ax = fig1.add_subplot(gs6[n,1])
    ax.set_title(f"{mode}-Gx")
    ax.imshow(Gx, cmap="coolwarm", vmin=-64, vmax=64)
    
    #structure tensor
    structureTensor = orientationpy.computeStructureTensor([Gy, Gx], sigma=sig)
    
    #orientation, energy and coherency
    orientations = orientationpy.computeOrientation(structureTensor, computeEnergy=True, computeCoherency=True)
        
    ax = fig2.add_subplot(gs3[n,0])
    cax = ax.imshow(orientations["energy"] / orientations["energy"].max(), vmin=0, vmax=1)
    cbar = plt.colorbar(cax, ax=ax,shrink=0.8)
    ax.set_title("Energy Normalised")
    
    orientations["coherency"][im == 0] = 0
    
    ax = fig3.add_subplot(gs3[n,0])
    cax = ax.imshow(orientations["coherency"], vmin=0, vmax=1)
    cbar = plt.colorbar(cax, ax=ax,shrink=0.8)
    ax.set_title("Coherency")

##########################################
# Computing Pixel-level orientations
##########################################
# Output is a dictionary
orientations = orientationpy.computeOrientation(structureTensor, computeEnergy=True, computeCoherency=True)
orientations['theta'][~mask]=0
orientations['coherency'][~mask]=0
orientations['energy'][~mask]=0

# Ignore orientations where image is too low value
orientations["theta"][im < 10] = 0

# Alternative composition, start as HSV
imageDisplayHSV = numpy.zeros((orientations["theta"].shape[0], orientations["theta"].shape[1], 3), dtype=float)
# Hue is the orientation (nice circular mapping)
imageDisplayHSV[:, :, 0] = (orientations["theta"] + 90) / 180
# Saturation is coherency
imageDisplayHSV[:, :, 1] = orientations["coherency"] / orientations["coherency"].max()
# Value is original image ;)
imageDisplayHSV[:, :, 2] = im / im.max()

ax = fig4.add_subplot(gs1[0,0])
fig4.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation="vertical",ticks=[-90,90])
ax.imshow(matplotlib.colors.hsv_to_rgb(imageDisplayHSV))

axins = ax.inset_axes([0.5, 0.5, 0.47, 0.47])
axins.imshow(matplotlib.colors.hsv_to_rgb(imageDisplayHSV))
# subregion of the original image
x1, x2, y1, y2 = 200, 300, 600, 500
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])

ax.indicate_inset_zoom(axins, linewidth=5,edgecolor="black")

ax.axis('off')

##########################################
# Histogram without filter
##########################################
orientationHist = numpy.pi/180 *orientations['theta'][mask]
for i in range(orientationHist.shape[0]):
    if orientationHist[i]<0:
        orientationHist[i]=orientationHist[i]+2*numpy.pi


circular_hist(ax5, orientationHist, bins=90,density =True,offset=0,gaps=True)


##########################################
# Histogram wit >2% normalized energy, weighted with coherency
##########################################
normEnergy = (orientations['energy']-numpy.min(orientations['energy']))/(numpy.max(orientations['energy'])-numpy.min(orientations['energy']))
filOrientationHist = numpy.pi/180*orientations['theta'][normEnergy>0.02] #to know what part is ignored use plt.imshow(normEnergy>0.02)
for i in range(filOrientationHist.shape[0]):
    if filOrientationHist[i]<0:
        filOrientationHist[i]=filOrientationHist[i]+2*numpy.pi

weighted_circular_hist(ax6, filOrientationHist, orientations['coherency'][normEnergy>0.02], bins=90,density =True,offset=0,gaps=True)

# import skimage.feature
#structureTensorSK = numpy.array(skimage.feature.structure_tensor(im, sigma=2, order="rc"))
'''
boxSizePixels = 20
structureTensorBoxes = orientationpy.computeStructureTensorBoxes(
    [Gy, Gx],
    [boxSizePixels, boxSizePixels],
)

# The structure tensor in boxes is passed to the same function to compute
# The orientation
orientationsBoxes = orientationpy.computeOrientation(
    structureTensorBoxes,
    mode="fiber",
    computeEnergy=True,
    computeCoherency=True,
)

# We normalise the energy, to be able to hide arrows in the subsequent quiver plot
orientationsBoxes["energy"] /= orientationsBoxes["energy"].max()

# Compute box centres
boxCentresY = numpy.arange(orientationsBoxes["theta"].shape[0]) * boxSizePixels + boxSizePixels // 2
boxCentresX = numpy.arange(orientationsBoxes["theta"].shape[1]) * boxSizePixels + boxSizePixels // 2

# Compute X and Y components of the vector
boxVectorsYX = orientationpy.anglesToVectors(orientationsBoxes)

# Vectors with low energy reset
boxVectorsYX[:, orientationsBoxes["energy"] < 0.05] = 0.0

plt.title("Local orientation vector in boxes")
plt.imshow(im, cmap="Greys_r", vmin=0)

# Warning, matplotlib is XY convention, not YX!
plt.quiver(
    boxCentresX,
    boxCentresY,
    boxVectorsYX[1],
    boxVectorsYX[0],
    angles="xy",
    scale_units="xy",
    # scale=energyBoxes.ravel(),
    color="r",
    headwidth=0,
    headlength=0,
    headaxislength=1,
)
plt.show()
''' 
