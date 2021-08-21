#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import scipy.io as scio
from skimage import exposure
import matplotlib.pyplot as plt

imagingMethod = 'RDA'
# imagingMethod = 'OmegaK'
imagingMethod = 'CSA'

zpadar = (256, 256)
# zpadar = None
# zpadar = False
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 32


sensor_name = 'Sentinel1'
acquis_name = 'Sentinel1'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None
sarplat.printsp()

SA = sarplat.acquisition['SceneArea']

disk = '/mnt/d/'
# disk = 'D:/'

datafile = disk + '/DataSets/sar/Sentinel/S12019/Sentinel.mat'

data = scio.loadmat(datafile, struct_as_record=True)

temp = data['sardata']
Sr = temp['rawdata'][0][0]
Na, Nr = Sr.shape
print("SAR raw data: ", Sr.shape, Sr.dtype)
# Sr = Sr.transpose()

real = np.real(Sr)
# imag = np.imag(Sr) * 0.0
imag = np.imag(Sr)


Sr = real + imag * 1j

cmap = 'jet'
extent = SA

plt.figure()
plt.subplot(211)
plt.imshow(np.abs(Sr), cmap=cmap)
plt.title("SAR raw data(Amplitude)")
plt.xlabel("Range")
plt.ylabel("Azimuth")
plt.subplot(212)
plt.imshow(np.angle(Sr), cmap=cmap)
# plt.imshow(SI, cmap=cmap)
plt.title('SAR raw data(phase)')
plt.tight_layout()
plt.show()


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

print(SI.min(), SI.max())

# SI = iprs.imadjust(SI, (0, 20), (0, 255))
SI = iprs.imadjustlog(SI, (0, 40), (0, 255))

print("SI.shape: ", SI.shape)

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

plt.figure()
plt.subplot(211)
plt.imshow(np.abs(Sr), cmap=cmap)
plt.title("SAR raw data(Amplitude)")
plt.xlabel("Range")
plt.ylabel("Azimuth")
plt.subplot(212)
plt.imshow(SI, extent=extent, cmap=cmap)
# plt.imshow(SI, cmap=cmap)
plt.title(Title)
plt.tight_layout()
plt.show()

plt.figure()
plt.imshow(SI, extent=extent, cmap=cmap)
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.title(Title)
plt.show()
