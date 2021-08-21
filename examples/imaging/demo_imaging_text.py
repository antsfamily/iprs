#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt

# isSave = False
isSave = True

sensor_name = 'DIY1'
acquis_name = 'DIY1'
# sensor_name = 'DIY5'
# sensor_name = 'DIY6'
# acquis_name = 'DIY6'

# sensor_name = 'DIY7'
# acquis_name = 'DIY7'

# sensor_name = 'DIY8'
# acquis_name = 'DIY8'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

# ========================================================
# datasetname = 'SAR64'
# datasetname = 'SAR128'
# datasetname = 'SAR512'
# datasetname = 'ellipse256'
# datasetname = 'ellipse512'
# datasetname = 'zhi&yan'
# datasetname = 'iridescent'
# datasetname = 'Lena'
# datasetname = 'SAR&ellipse1024'
# datasetname = 'SAR&ellipse256'
# datasetname = 'ellipse1024'
# datasetname = 'randdisc'
# datasetname = 'disc1024'
# datasetname = 'strip1024'
# datasetname = 'strip2'
# datasetname = 'stripslim1024'
# datasetname = 'line1024'
# datasetname = 'line256'
# datasetname = 'SARDL'
# datasetname ='gaoxiong001'


# datasetname = 'MiniSAR20050816p0005image006'
# datasetname = 'MiniSAR20050816p0005image012_256'
# datasetname = 'MiniSAR20050816p0006image012'
# datasetname = 'MiniSAR20050519p0001image008'
# datasetname = 'MiniSAR20050519p0002image005'
# datasetname = 'MiniSAR20050519p0003image003'
# datasetname = 'MiniSAR20050519p0003image006'
# datasetname = 'MiniSAR20050519p0004image005'
# datasetname = 'MiniSAR20050519p0004image008'
# datasetname = 'MiniSAR20050519p0005image003'
# datasetname = 'MiniSAR20050519p0006image004'
# datasetname = 'MiniSAR20050519p0006image005'
# datasetname = 'MiniSAR20050519p0006image008'
# datasetname = 'MiniSAR20050519p0009image003'
# datasetname = 'MiniSAR20050519p0009image005'
# datasetname = 'MiniSAR20050519p0010image002'
# datasetname = 'MiniSAR20050519p0010image003'
# datasetname = 'MiniSAR20050524p0002image006'
# datasetname = 'MiniSAR20050525p0002image009'
# datasetname = 'MiniSAR20050525p0002image011'


# datasetname = 'IMAGE_HH_SAR001_8bit_256'
# datasetname = 'IMAGE_HH_SAR002_8bit_256'
# datasetname = 'Tokyoradarsat001_8bit_256'
# datasetname = 'Tokyoradarsat004_8bit_256'
# datasetname = 'Tokyoradarsat004_128'
# datasetname = 'Tokyoradarsat004_128'
# datasetname = '000010'
# datasetname = '000009'

datasetname = 'MSTAR_HB06159'
# datasetname = 'MSTAR_HB06167'
# datasetname = 'MSTAR_HB06175'
# datasetname = 'MSTAR_HB06181'
# datasetname = 'MSTAR_HB06183'
# datasetname = 'MSTAR_HB06185'


datasetname = 'Lotus128'
# datasetname = 'SAR&ellipse256'


# imgfolder = '../../data/fig/MinSAR/'
# imgfolder = '../../data/fig/radarsat/'
imgfolder = '../../data/img/'
# imgfolder = '../../data/fig/'


imgfilepath = imgfolder + datasetname + '.png'

grayimg = iprs.imread(imgfilepath)
grayimg = grayimg[:, :, 0]


SNR = 30
imgns = iprs.imnoise(grayimg, SNR=SNR)
img = iprs.scale(grayimg, [0.0, 255.0], [0.0, 1.0])

# ==========================================================
outfolder = '../../data/sar/image/'


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
TH = 0
targets = iprs.img2tgs(grayimg, bg=bgv, TH=TH, noise=None)

imgshape = grayimg.shape
SrI = iprs.show_targets(targets, imgshape, outfile)


Sr, targets = iprs.img2rawdata(
    sarplat, grayimg, bg=bgv, noise=None, verbose=True)

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


if imagingMethod is 'RangeDoppler':
    # do RD imaging
    Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)
elif imagingMethod is 'OmegaK':
    Sr_img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)
elif imagingMethod is 'ChirpScaling':
    Sr_img = iprs.chirp_scaling(Sr, sarplat, verbose=False)


axismod = 'Image'
# axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
title = 'Reconstructed Image using ' + imagingMethod
# title = 'Reconstructed Image using omega-k'
outfile = outfilename_prefix + "_" + imagingMethod + '.png'

iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None, outfile=outfile)
