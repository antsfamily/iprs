#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt

sensor_name = 'RADARSAT1'
acquis_name = 'RADARSAT1'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.params = {'GeometryMode': 'SG'}
sarplat.selection = None
sarplat.printsp()

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    # 'SubEchoSize': None,  # EchoSize
    'SubEchoSize': [1., 1.],  # 19438x9288
    # 'SubEchoSize': [1. / 18.98, 1. / 9.070],  # 1024x1024
    # 'SubEchoSize': [1536, 9288],
    # 'SubEchoSize': [1536, 4096],
    # 'SubEchoSize': [1536, 2048],
    # 'SubEchoSize': [1536, 1024],
    # 'SubEchoSize': [4096, 4096],
    # 'SubEchoSize': [2048, 2048],
    # 'SubEchoSize': [1024, 1024],
    # 'SubEchoSize': [512, 512],
    'SubEchoSize': [256, 256],
    # 'SubEchoSize': [1536, 256],
}
sarplat.selection = ROI

SA = sarplat.acquisition['SceneArea']
SSA = sarplat.selection['SubSceneArea']
SSES = sarplat.selection['SubEchoSize']
SS = [int(SA[1] - SA[0]), int(SA[3] - SA[2])]


outfolder = '../../../../data/sar/image/'
datasetname = 'image'

# datasetname = 'points32'
# datasetname = 'Lotus32'
# datasetname = 'ship32'
# datasetname = 'points64'
# datasetname = 'Lotus64'
# datasetname = 'ship64'
datasetname = 'Lotus128'
# datasetname = 'Lotus256'
# datasetname = 'ship128'
# datasetname = 'points128'
# datasetname = 'pointsx128'
# datasetname = '000043'
# datasetname = '000010'
# datasetname = '000237'
# datasetname = '000066'
# datasetname = '000002AirPlane128'

imgfilepath = '../../../../data/' + 'img/' + datasetname + '.png'

imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
# imagingMethod = 'ChirpScaling'


zpadar = (256, 256)
# zpadar = False
# zpadar = None
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 32


# ------------------------------------------------------------

imgRGB = iprs.imread(imgfilepath)

if np.ndim(imgRGB) > 2:
    grayimg = imgRGB[:, :, 0]
else:
    grayimg = imgRGB

SNR = 30
imgns = iprs.imnoise(grayimg, SNR=SNR)
img = iprs.scale(grayimg, [0.0, 255.0], [0.0, 1.0])
print("img.shape: ", img.shape)
H, W = img.shape

gdshape = (H, W)
# gdshape = (2 * H, 2 * W)
# gdshape = None

bgv = 0
grayimg = grayimg / 255.0
Sr, targets = iprs.img2rawdata(sarplat, grayimg, bg=bgv, noise=None,
                               TH=0., gdshape=gdshape, verbose=True)

print(targets)
imgshape = (H, W)
SrI = iprs.show_targets(targets, SA, imgshape)

iprs.show_amplitude_phase(Sr)
plt.show()


RD = np.fft.fftshift(np.fft.fft(
    np.fft.fftshift(Sr, axes=(0,)), axis=0), axes=0)

# F2D = np.fft.fft2(Sr)
F2D = np.fft.fft(RD, axis=1)

cmap = 'jet'
# cmap = 'gray'

plt.figure()
plt.subplot(321)
plt.imshow(np.absolute(Sr), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('Time domain (amplitude)')
plt.subplot(322)
plt.imshow(np.angle(Sr), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('Time domain (phase)')

plt.subplot(323)
plt.imshow(np.absolute(RD), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('RD domain (amplitude)')
plt.subplot(324)
plt.imshow(np.angle(RD), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('RD domain (phase)')


plt.subplot(325)
plt.imshow(np.absolute(F2D), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('2D frequency domain (amplitude)')
plt.subplot(326)
plt.imshow(np.angle(F2D), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('2D frequency domain (phase)')
plt.tight_layout()
plt.show()

# store
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Sr
sardata.image = SrI
sardata.description = sensor_name + '_' + datasetname

outfilename_prefix = outfolder + sarplat.name + \
    "_" + datasetname + '_' + str(len(targets)) + 'Tgs'

outfile = outfilename_prefix + '.mat'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

# --------------------------------------------
# do RD imaging
verbose = True

if imagingMethod is 'RangeDoppler':
    # do RD imaging
    SrIr = iprs.rda_adv(Sr, sarplat, zpadar=zpadar, usesrc=usesrc,
                        usedpc=usedpc, rcmc=rcmc, verbose=verbose)
    # SrIr = iprs.rda(Sr, sarplat, usezpa=False,
    #                 usermc=False, verbose=verbose)

elif imagingMethod is 'OmegaK':
    SrIr, ta, tr = iprs.wka(Sr, sarplat, verbose=verbose)
elif imagingMethod is 'ChirpScaling':
    SrIr = iprs.csa_adv(Sr, sarplat, zpadar=zpadar, usesrc=False,
                        rcmc=rcmc, usedpc=usedpc, verbose=verbose)
    # SrIr = iprs.csa(Sr, sarplat, verbose=verbose)

axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'

Title = 'Imaging result of ' + imagingMethod + '\n ('


if usesrc:
    Title = Title + 'SRC+'
if rcmc:
    Title = Title + 'RCMC+'
if usedpc:
    Title = Title + 'DPC'

Title = Title + ")"

iprs.show_sarimage(SrIr, sarplat, axismod=axismod, title=Title, aspect=None)
