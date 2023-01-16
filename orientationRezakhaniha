import numpy as np
import pandas as pd
import os

import skimage.io
import re

nameconfig = "fitHeightDistributionshdn.xlsx"
drive = "F:\AFM_sorted"
folder = "5PIP2_20DOPS\hexamers\denseNetwork"
absolute_path_config = os.path.join(drive,folder,nameconfig)
config = pd.read_excel(absolute_path_config,skiprows=1)
iConfig = 15
nameI = config['name'][iConfig]
ymin,ymax,xmin,xmax=[int(s) for s in re.findall(r'\b\d+\b',config['crop'][iConfig])]
absolute_path_I = os.path.join(drive,folder,nameI)
image =(np.loadtxt(absolute_path_I)*10**9)[ymin:ymax,xmin:xmax]
cmap = plt.cm.gray
heightLimitUp = config['x4'][iConfig]+3*config['x5'][iConfig]
image[image>heightLimitUp]=heightLimitUp
heightLimitLow = config['x1'][iConfig]-3*config['x2'][iConfig]
image[image<heightLimitLow]=heightLimitLow
img = img_as_ubyte((image-np.min(image))/(np.max(image)-np.min(image)))


#I = gaussian(I,sigma=2)#we blur first to remove oulier noise
#I = (I-np.min(I))/(np.max(I)-np.min(I)) #norm image before conversion
#img = img_as_ubyte(image) #since 8 bit converstion is stupid for x<256 np.uint8(np.array([254,255,256],dtype=np.uint16))
#img = img[1000:1500,1000:1500]


#estimate derivatives
from ridge_detection.convol import convolve_gauss
def gaussDerivative(img,sigma):
    width=img.shape[0]
    height=img.shape[1]
    
    imgpxls2 = np.reshape(img,width*height)
    k = convolve_gauss(imgpxls2,width,height,sigma)
    
    r = {}
    r['rx'] = np.reshape(k[0],[width,height])
    r['ry'] = np.reshape(k[1],[width,height])
    r['rxx'] = np.reshape(k[2],[width,height])
    r['rxy'] = np.reshape(k[3],[width,height])
    r['ryy'] = np.reshape(k[4],[width,height])
                           
    return r

r = gaussDerivative(img,sigma=2) #rx = r['rx']

#compute line points
from numpy.linalg import eig
def  orderEigH(r):
    width=img.shape[0]
    height=img.shape[1]
    
    eigval = np.zeros([width,height,2])
    eigvec = np.zeros([width,height,2,2])
    for xx in range(height):
        for yy in range(width):
            kxx = r['rxx'][xx,yy]
            kxy = r['rxy'][xx,yy]
            kyy = r['ryy'][xx,yy]
            H = np.array([[kxx,kxy],[kxy,kyy]])
            w,v = eig(H)
            if abs(w[0])>abs(w[1]):
                eigval[xx,yy,0] = w[0]
                eigvec[xx,yy,0] = v[0]
                eigval[xx,yy,1] = w[1]
                eigvec[xx,yy,1] = v[1]
            elif abs(w[0])<abs(w[1]):
                eigval[xx,yy,0] = w[1]
                eigvec[xx,yy,0] = v[1]
                eigval[xx,yy,1] = w[0]
                eigvec[xx,yy,1] = v[0]
            else:
                if w[0]<w[1]:
                    eigval[xx,yy,0] = w[0]
                    eigvec[xx,yy,0] = v[0]
                    eigval[xx,yy,1] = w[1]
                    eigvec[xx,yy,1] = v[1]
                else:
                    eigval[xx,yy,0] = w[0]
                    eigvec[xx,yy,0] = v[0]
                    eigval[xx,yy,1] = w[1]
                    eigvec[xx,yy,1] = v[1]                    
    return eigval, eigvec

eigval, eigvec = orderEigH(r)
c = (eigval[:,:,0]-eigval[:,:,1])/(eigval[:,:,0]+eigval[:,:,1])
E = r['rxx']+r['ryy']
