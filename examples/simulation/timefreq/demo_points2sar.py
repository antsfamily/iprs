#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt

sensor_name = 'Air1'
acquis_name = 'Air1'
# sensor_name = 'Air2'
# acquis_name = 'Air2'
# sensor_name = 'Air3'
# acquis_name = 'Air3'


sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    # 'SubEchoSize': None,  # EchoSize
    # 'SubEchoSize': [256, 320],  # 256x256
    'SubEchoSize': [512, 640],  # 128x128
    # 'SubEchoSize': [1024, 1280],  # 128x128
    # 'SubEchoSize': [2048, 2560],  # 128x128
}
sarplat.selection = ROI
sarplat.printsp()

SC = sarplat.acquisition['SceneCenter']
SA = sarplat.selection['SubSceneArea']
SE = sarplat.selection['SubEchoSize']
SS = [int(SA[1] - SA[0]), int(SA[3] - SA[2])]
Xc = SC[0]
Yc = SC[1]

outfolder = '../../../data/sar/point/'

datasetname = 'points'


imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
imagingMethod = 'ChirpScaling'


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

H, W = SE

G = np.zeros((H, W))
G[int(H / 2) + 1, int(W / 2) + 1] = 1

gdshape = (H, W)
gdshape = (256, 320)
# gdshape = (2 * H, 2 * W)
# gdshape = None
bgv = 0.

Sr, targets = iprs.img2rawdata(sarplat, G, bg=bgv, TH=0.5, noise=None, gdshape=None, mod='time', verbose=False)

# Sr, targets = iprs.img2rawdata(sarplat, G, bg=bgv, TH=0., noise=None, gdshape=None, mod='freq', verbose=False)

iprs.show_amplitude_phase(Sr)
plt.show()

imgshape = (H, W)
SrI = iprs.show_targets(targets, SA, imgshape)


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
sardata.description = sarplat.name + sensor_name + '_' + datasetname
outfilename_prefix = outfolder + sarplat.name + \
    "_" + datasetname + '_' + str(len(targets)) + 'Tgs'

outfile = outfilename_prefix + '.mat'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)
Sr = sardata.rawdata[:, :, 0] + sardata.rawdata[:, :, 1] * 1j

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
