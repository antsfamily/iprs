#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt

imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
# imagingMethod = 'ChirpScaling'
ftshift = True
zpadar = (256, 256)
zpadar = False
# zpadar = None
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 32

sensor_name = 'ERS'
acquis_name = 'ERS'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None

ROI = {
    'SubSceneArea': None,  # SceneArea
    'SubEchoAnchor': [0, 0],
    # 'SubEchoSize': None,  # EchoSize
    # 'SubEchoSize': [1., 1.],  # 28603x5616
    # 'SubEchoSize': [8192, 5616],
    # 'SubEchoSize': [4096, 5616],
    # 'SubEchoSize': [2048, 5616],
    # 'SubEchoSize': [2048, 2048],
    # 'SubEchoSize': [1024, 2048],
    'SubEchoSize': [1024, 1024],
    # 'SubEchoSize': [2286, 2297],
}
sarplat.selection = ROI

sarplat.printsp()

SC = sarplat.selection['SubSceneCenter']
# SC = sarplat.selection['SubBeamCenter']
SA = sarplat.selection['SubSceneArea']
SS = [int(SA[1] - SA[0]), int(SA[3] - SA[2])]
Xc = SC[0]
Yc = SC[1]

datasetname = 'point'
outfolder = '../../../../data/sar/point/'

a = 32
# a = -32
a = 5000
# a = -100
targets = [
    # [-700, -400, 0, 0, 0, 0, 1],
    # [a, a, 0, 0, 0, 0, 1],
    [a, 0, 0, 0, 0, 0, 1],
    # [0, 0, 0, 0, 0, 0, 1],
    # [0, a, 0, 0, 0, 0, 1],
    # [-a, -a, 0, 0, 0, 0, 1],

    # [-100, -50, 0, 0, 0, 0, 1],
    # [-100, -51, 0, 0, 0, 0, 1],
    # [-100, -52, 0, 0, 0, 0, 1],
    # [-100, 50, 0, 0, 0, 0, 1],
    # [-100, 51, 0, 0, 0, 0, 1],
    # [-100, 52, 0, 0, 0, 0, 1],
    # [0, 0, 0, 0, 0, 0, 1],
    # [0, 1, 0, 0, 0, 0, 1],
    # [0, 2, 0, 0, 0, 0, 1],
    # [100, -50, 0, 0, 0, 0, 3],
    # # [100, -51, 0, 0, 0, 0, 1],
    # # [100, -52, 0, 0, 0, 0, 1],
    # [100, 50, 0, 0, 0, 0, 3],
    # # [100, 51, 0, 0, 0, 0, 1],
    # # [100, 52, 0, 0, 0, 0, 1],

]

# imgshape = SS
# print("SS: ", SS)
# print("SA: ", SA)
# SrI = iprs.show_targets(targets, SA=SA, extent=SA, imgshape=imgshape)

Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets, verbose=True)

print(Sr.shape)
# visualize
# Sr = np.flipud(Sr)

RD = np.fft.fftshift(np.fft.fft(
    np.fft.fftshift(Sr, axes=(0,)), axis=0), axes=0)

# F2D = np.fft.fft2(Sr)
F2D = np.fft.fft(RD, axis=1)

isimgadj = False
cmap = 'jet'
# cmap = 'gray'

plt.figure()
plt.subplot(121)
plt.imshow(np.absolute(Sr), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('Time domain (amplitude)')
plt.subplot(122)
plt.imshow(np.angle(Sr), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Azimuth')
plt.title('Time domain (phase)')

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
sardata.image = []
sardata.description = sensor_name + '_' + datasetname

outfilename_prefix = outfolder + sarplat.name + \
    "_" + datasetname + str(len(targets))

outfile = outfilename_prefix + '.mat'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)
# --------------------------------------------
# do RD imaging
verbose = True

if imagingMethod is 'RangeDoppler':
    # do RD imaging
    # SrIr = iprs.rda_adv(Sr, sarplat, zpadar=zpadar,
    #                     usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, verbose=verbose)
    SrIr = iprs.rda(Sr, sarplat, zpadar=zpadar, rcmc=rcmc, ftshift=ftshift, verbose=verbose)

elif imagingMethod is 'OmegaK':
    SrIr, ta, tr = iprs.wka(Sr, sarplat, verbose=verbose)
elif imagingMethod is 'ChirpScaling':
    SrIr = iprs.csa_adv(Sr, sarplat, zpadar=zpadar,
                        usesrc=False, rcmc=rcmc, usedpc=usedpc, verbose=verbose)
    # SrIr = iprs.csa(Sr, sarplat, verbose=verbose)


axismod = 'Image'
# axismod = 'SceneAbsoluteGroundRange'
axismod = 'SceneRelativeGroundRange'
# axismod = 'SceneAbsoluteSlantRange'
# axismod = 'SceneRelativeSlantRange'

Title = 'Imaging result of ' + imagingMethod + '\n ('


if usesrc:
    Title = Title + 'SRC+'
if rcmc:
    Title = Title + 'RCMC+'
if usedpc:
    Title = Title + 'DPC'

Title = Title + ")"

iprs.show_sarimage(SrIr, sarplat, axismod=axismod, title=Title, isimgadj=isimgadj, aspect=None)
