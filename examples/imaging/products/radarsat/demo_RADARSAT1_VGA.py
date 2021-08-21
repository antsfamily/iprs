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

# imagingMethod = 'RDA'
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
rcmc = 12


sensor_name = 'RADARSAT1'
acquis_name = 'RADARSAT1'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.selection = None
sarplat.params = None
sarplat.select()
sarplat.printsp()

SA = sarplat.acquisition['SceneArea']

# disk = 'D:/'
disk = '/mnt/d/'
filename = 'RADARSAT1_SAR_RAW=Vancouver(sl=1el=19438)'
datafile = disk + '/DataSets/sar/RADARSAT/frombooks/Vancouver/mat/' + filename + '.mat'
vgagainfilepath = disk + 'DataSets/sar/RADARSAT/frombooks/Vancouver/data/AGC_attenuation_values.mat'

V = scio.loadmat(vgagainfilepath, struct_as_record=True)['nom_attenuation']
sardata, _ = iprs.sarread(datafile)
Sr = sardata.rawdata

sa, ea, sr, er = (0, 1536, 0, 2048)
sa, ea, sr, er = (7657, 9193, 1850, 5946)

Sr = Sr[sa:ea, sr:er, :]
V = V[sa:ea, :]

Sr0 = Sr[:, :, 0] + 1j*Sr[:, :, 1]

Sr1 = iprs.vga_gain_compensation(Sr, V, mod='linear', fact=1.5)

Na, Nr, _ = Sr.shape
print("SAR raw data: ", Sr.shape, Sr.dtype)

Sr1 = Sr1[:, :, 0] + 1j*Sr1[:, :, 1]


cmap = 'jet'
extent = SA


if imagingMethod is 'RDA':
    # SI, _, _ = iprs.rda(Sr, sarplat, verbose=True)
    SI0 = iprs.rda_adv(Sr0, sarplat, zpadar=zpadar,
                      usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, verbose=False)
    SI1 = iprs.rda_adv(Sr1, sarplat, zpadar=zpadar,
                      usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, verbose=False)
if imagingMethod is 'CSA':
    # SI = iprs.csa(Sr, sarplat, verbose=True)
    SI0 = iprs.csa_adv(Sr0, sarplat, zpadar=zpadar,
                      usesrc=usesrc, rcmc=rcmc, usedpc=usedpc, verbose=False)
    SI1 = iprs.csa_adv(Sr1, sarplat, zpadar=zpadar,
                      usesrc=usesrc, rcmc=rcmc, usedpc=usedpc, verbose=False)

SI0 = np.abs(SI0)
SI0 = np.flipud(SI0)
SI0 = iprs.imadjustlog(SI0, (2, 255), (0, 255))

SI1 = np.abs(SI1)
SI1 = np.flipud(SI1)
SI1 = iprs.imadjustlog(SI1, (20, 255), (0, 255))

print("SI0.shape: ", SI0.shape)

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
plt.imshow(SI0, extent=extent, cmap='gray')
plt.title(Title + '(without VGA)')
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.subplot(212)
plt.imshow(SI1, extent=extent, cmap=cmap)
# plt.imshow(SI, cmap=cmap)
plt.title(Title + '(with VGA)')
plt.tight_layout()
plt.show()

