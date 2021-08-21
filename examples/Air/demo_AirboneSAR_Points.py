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

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None
# GM = 'BG'

sarplat.printsp()

SC = sarplat.acquisition['SceneCenter']
SA = sarplat.selection['SubSceneArea']
SS = [int(SA[1] - SA[0]), int(SA[3] - SA[2])]
Xc = SC[0]
Yc = SC[1]

datasetname = 'point'
outfolder = '../../data/sar/point/'

imagingMethod = 'RangeDoppler'
# imagingMethod = 'ChirpScaling'
# imagingMethod = 'OmegaK'

ftshift = True
zpadar = (256, 256)
zpadar = False
# zpadar = None
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 4


targets = [
    [200, 60, 0, 0, 0, 0, 1],
    # [200, 0, 0, 0, 0, 0, 1],
    # [0, 0, 0, 0, 0, 0, 1],
    [-200, -60, 0, 0, 0, 0, 1],

    # [0, 0, 0, 0, 0, 0, 1],
    # [-6, -6, 0, 0, 0, 0, 1],
    # [-6, 6, 0, 0, 0, 0, 1],
    # [6, -6, 0, 0, 0, 0, 1],
    # [6, 6, 0, 0, 0, 0, 1],
    # [9, 9, 0, 0, 0, 0, 1],

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

imgshape = (256, 320)
imgshape = SS
print("SS: ", SS)
print("SA: ", SA)
SrI = iprs.show_targets(targets, SA=SA, extent=SA, imgshape=imgshape)

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

plt.figure(figsize=(6, 7.5))
plt.subplot(321)
plt.imshow(np.absolute(Sr), cmap=cmap)
plt.xlabel('Range\n(a)')
plt.ylabel('Azimuth')
plt.title('Time domain (amplitude)')
plt.subplot(322)
plt.imshow(np.angle(Sr), cmap=cmap)
plt.xlabel('Range\n(b)')
plt.ylabel('Azimuth')
plt.title('Time domain (phase)')

plt.subplot(323)
plt.imshow(np.absolute(RD), cmap=cmap)
plt.xlabel('Range\n(c)')
plt.ylabel('Azimuth')
plt.title('RD domain (amplitude)')
plt.subplot(324)
plt.imshow(np.angle(RD), cmap=cmap)
plt.xlabel('Range\n(d)')
plt.ylabel('Azimuth')
plt.title('RD domain (phase)')


plt.subplot(325)
plt.imshow(np.absolute(F2D), cmap=cmap)
plt.xlabel('Range\n(e)')
plt.ylabel('Azimuth')
plt.title('2D frequency domain (amplitude)')
plt.subplot(326)
plt.imshow(np.angle(F2D), cmap=cmap)
plt.xlabel('Range\n(f)')
plt.ylabel('Azimuth')
plt.title('2D frequency domain (phase)')
plt.subplots_adjust(left=0.05, bottom=0.09, right=1.0, top=0.97, wspace=0.12, hspace=0.52)
plt.show()

# store
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Sr
sardata.image = SrI
sardata.description = sensor_name + '_' + datasetname


outfilename_prefix = outfolder + sarplat.name + \
    "_" + datasetname + str(len(targets))

outfile = outfilename_prefix + '.mat'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

# --------------------------------------------
# do RD imaging
verbose = True
verbose = False

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
# axismod = 'SceneAbsoluteSlantRange'
axismod = 'SceneRelativeSlantRange'
# axismod = 'SceneAbsoluteGroundRange'
axismod = 'SceneRelativeGroundRange'

Title = 'Imaging result of ' + imagingMethod + '\n ('


if usesrc:
    Title = Title + 'SRC+'
if rcmc:
    Title = Title + 'RCMC+'
if usedpc:
    Title = Title + 'DPC'

Title = Title + ")"

iprs.show_sarimage(SrIr, sarplat, axismod=axismod, title=Title, isimgadj=isimgadj)
