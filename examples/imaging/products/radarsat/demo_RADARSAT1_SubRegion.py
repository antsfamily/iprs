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

imagingMethod = 'RDA'
# imagingMethod = 'OmegaK'
imagingMethod = 'CSA'

zpadar = (512, 512)
# zpadar = False
# zpadar = None
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 32

fulltime = False
fulltime = True

usemask = False
# usemask = True

sensor_name = 'RADARSAT1'
acquis_name = 'RADARSAT1'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None


ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    # 'SubEchoSize': None,  # EchoSize
    # 'SubEchoSize': [1., 1.], # 19438x9288
    # 'SubEchoSize': [1. / 12.65, 1. / 2.267], # 1536x4096
    'SubEchoSize': [1. / 12.65, 1. / 4.535], # 1536x2048
}

sarplat.selection = ROI
ROIY = sarplat.selection['SubEchoSize'][0]
ROIX = sarplat.selection['SubEchoSize'][1]

NstartX = int(sarplat.acquisition['EchoSize'][1] / 2. - ROIX / 2.)
NstartY = int(sarplat.acquisition['EchoSize'][0] / 2. - ROIY / 2.)


# disk = 'D:/'
disk = '/mnt/d/'
filename = 'RADARSAT1_SAR_RAW=Vancouver(sl=1el=19438)'
datafile = disk + '/DataSets/sar/RADARSAT/frombooks/Vancouver/mat/' + filename + '.mat'

sardata, _ = iprs.sarread(datafile)

Sr = sardata.rawdata

print(np.min(np.abs(Sr.real)), np.max(np.abs(Sr.real)))
print(np.min(np.abs(Sr.imag)), np.max(np.abs(Sr.imag)))

sa = 7657
ea = 9193
sr = 1850
er = 5946


if fulltime:
    mask = np.zeros(sarplat.acquisition['EchoSize'])
    sarplat.selection = None

sarplat.select()
sarplat.printsp()

SA = sarplat.selection['SubSceneArea']


NendY = NstartY + ROIY
NendX = NstartX + ROIX

temp = Sr
if fulltime:
    Sr = np.zeros_like(temp)
    Sr[NstartY:NendY, NstartX:NendX] = temp[NstartY:NendY, NstartX:NendX]
    # Sr = temp
    mask[NstartY:NendY, NstartX:NendX] = 1
else:
    Sr = temp[NstartY:NendY, NstartX:NendX]

print(NstartY, NstartX, NendY, NendX)


Na, Nr = Sr.shape
print("SAR raw data: ", Sr.shape, Sr.dtype)


if imagingMethod is 'RDA':
    # SI, _, _ = iprs.rda(Sr, sarplat, verbose=True)
    SI = iprs.rda_adv(Sr, sarplat, zpadar=zpadar,
                      usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, verbose=False)
if imagingMethod is 'CSA':
    # SI = iprs.csa(Sr, sarplat, verbose=True)
    SI = iprs.csa_adv(Sr, sarplat, zpadar=zpadar,
                      usesrc=usesrc, rcmc=rcmc, usedpc=usedpc, verbose=False)

SI = np.abs(SI)

data = {'SI': SI}
scio.savemat('./SI.mat', data)

# SI = iprs.imadjust(SI, (0, 20), (0, 255))

SI = iprs.imadjustlog(SI, (20, 255), (0, 255))

SI = np.flipud(SI)

if fulltime and usemask:
    SI = SI * mask

print("SI.shape: ", SI.shape)

Title = 'Imaging result of RDA('

Title = 'Imaging Result of ' + imagingMethod


if usesrc or rcmc:
    Title = Title + '\n ('
    if usesrc:
        Title = Title + 'SRC+'
    if rcmc:
        Title = Title + 'RCMC+'
if usedpc:
    Title = Title + 'DPC'

Title = Title + ")"


cmap = 'gray'
# cmap = 'hot'
# cmap = None

extent = SA
extent = None

plt.figure()
plt.subplot(211)
plt.imshow(np.abs(Sr), cmap=cmap)
plt.title("SAR raw data(Amplitude)")
plt.xlabel("Range")
plt.ylabel("Azimuth")
plt.subplot(212)
plt.imshow(SI, extent=extent, cmap=cmap)
plt.title(Title)
plt.xlabel("Range")
plt.ylabel("Azimuth")
plt.tight_layout()
plt.show()

plt.figure()
plt.imshow(SI, extent=extent, cmap='gray')
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.title(Title)
plt.show()


EchoSize = sarplat.acquisition['EchoSize']

ROIYs = (1024, 512, 256, 128)
ROIXs = (1024, 512, 256, 128)

plt.figure()
cnt = 1
for ROIY, ROIX in zip(ROIYs, ROIXs):
    plt.subplot(2, 2, cnt)
    cnt = cnt + 1

    NstartX = int(EchoSize[1] / 2. - ROIX / 2.)
    NstartY = int(EchoSize[0] / 2. - ROIY / 2.)

    II = SI[NstartY:NstartY + ROIY, NstartX:NstartX + ROIX]
    print(ROIY, ROIX, II.shape)
    plt.imshow(II, cmap=cmap)
    plt.title("%s x %s" % (ROIY, ROIX))
    plt.xlabel("Range")
    plt.ylabel("Azimuth")

plt.tight_layout()
plt.show()
