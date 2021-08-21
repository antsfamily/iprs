#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt
from skimage import transform

# isSave = False
isSave = True


sensor_name = 'DIY1'
acquis_name = 'DIY1'

# sensor_name = 'DIY8'
# acquis_name = 'DIY8'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

# ========================================================
datasetname = 'Lotus128'
# datasetname = 'points128'
# datasetname = 'ship128'
# datasetname = '000002AirPlane128'
datasetname = '000003Ground128'
# datasetname = 'Lotus64'
# datasetname = 'points64'
# datasetname = 'ship64'
# datasetname = '000002AirPlane64'
# datasetname = '000003Ground64'


imgfolder = '../../data/img/'


imgfilepath = imgfolder + datasetname + '.png'

grayimg = iprs.imread(imgfilepath)


SNR = 30
imgns = iprs.imnoise(grayimg, SNR=SNR)
img = iprs.scale(grayimg, [0.0, 255.0], [0.0, 1.0])

# ==========================================================
outfolder = '../../data/diysar/'


outfilename_prefix = outfolder + sarplat.name + "_" + datasetname

outfile = outfilename_prefix + "_input" + '.png'

# ==========================================================
imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK


plt.figure
plt.subplot(121)
plt.imshow(grayimg, cmap='gray')
plt.title('Original')
plt.subplot(122)
plt.imshow(imgns, cmap='gray')
plt.title("add wgn with SNR: " + str(SNR) + "dB")
plt.show()

bgv = 0  # bg color : white
TH = 0  # Threshhold
targets = iprs.img2tgs(grayimg, bg=bgv, TH=TH, noise=None)

SA = sarplat.acquisition['SceneArea']
imgshape = grayimg.shape
print(SA)
SrI = iprs.show_targets(targets, SA, imgshape, outfile)


Sr, targets = iprs.img2rawdata(
    sarplat, grayimg, bg=bgv, TH=TH, noise=None, verbose=True)

# store
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Sr
sardata.image = SrI

outfile = outfilename_prefix + '.pkl'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)


# visualize
iprs.show_amplitude_phase(Sr)


usesrc = False
usermc = False

if imagingMethod is 'RangeDoppler':
    # do RD imaging
    Sr_img = iprs.rda_adv(
        Sr, sarplat, usezpa=True, usesrc=usesrc, usermc=usermc, verbose=True)
    # Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)

elif imagingMethod is 'OmegaK':
    Sr_img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)
elif imagingMethod is 'ChirpScaling':
    Sr_img = iprs.chirp_scaling(Sr, sarplat, verbose=False)


# axismod = 'Image'
axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
title = 'Reconstructed Image using ' + imagingMethod
# title = 'Reconstructed Image using omega-k'
outfile = outfilename_prefix + "_" + imagingMethod + '.png'

iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None, outfile=outfile)
