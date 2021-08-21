#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
from iprs.utils.const import PI
import numpy as np
import matplotlib.pyplot as plt

imagingMethod = 'RDA'
# imagingMethod = 'OmegaK'
# imagingMethod = 'CSA'

ftshift = True
zpadar = (256, 256)
# zpadar = None
zpadar = False
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 32
afa = None
# afa = 'PGA'
nlooks = (2, 2)
nlooks = (1, 1)
nlooks = (5, 1)

maxp = 1.8e4
minp = np.sqrt(maxp)
minp = None

sensor_name = 'ERS'
acquis_name = 'ERS'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}

fmt = '.mat'

disk = '/mnt/d/'
# disk = 'D:/'

# prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_50460_STD', 'F127', 1, 28636, [28636, 5616], 67.98 * PI / 180, 7.335008 * PI / 180, 5.3e9, 791640., 7100., 1679.9023438, 18959999.1, 3.70999985e-05, 834071.4111)
# prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_80406_STD', 'F123', 1, 28624, [28624, 5616], 68.03 * PI / 180, 7.359127 * PI / 180, 5.3e9, 791291., 7147., 1679.9023438, 18959999.1, 3.70999985e-05, 833359.9854)
prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_81988_STD', 'F327', 1, 28698, [28698, 5616], 68.02 * PI / 180, 7.355842 * PI / 180, 5.3e9, 791193., 7100., 1679.9023438, 18959999.1, 3.70999985e-05, 833367.9199)

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    'SubEchoAnchor': [0, 0],
    # 'SubEchoAnchor': [8192, 0],
    # 'SubEchoAnchor': [11000, 0],
    # 'SubEchoSize': [8192, 4096],
    # 'SubEchoSize': [16384, 4096],
    # 'SubEchoSize': [8192, 4096],
    # 'SubEchoSize': [4096, 2048],
    'SubEchoSize': ES,
}

sarplat.sensor = iprs.dmka(sarplat.sensor, {'H': H, 'V': V, 'PRF': PRF, 'Fc': Fc})

sarplat.acquisition = iprs.dmka(sarplat.acquisition, {'EchoSize': ES, 'Ad': Ad, 'Be': Be})
sarplat.params = None  # recompute parameters
sarplat.selection = ROI
sarplat.printsp()

SA = sarplat.acquisition['SceneArea']
SSA = sarplat.selection['SubSceneArea']
SSES = sarplat.selection['SubEchoSize']

(sa, sr) = ROI['SubEchoAnchor']

ea, er = iprs.ebeo((sa, sr), SSES, '+')
print(sa, sr, ea, er)

level = 'L0'
rootfolder = prefixname + '_' + frame
filefolder = prefixname + '_' + level + '_' + frame
filename = 'ERS2_SAR_RAW=' + filefolder + '(sl=' + str(sl) + 'el=' + str(el) + ')'

datafile = disk + '/DataSets/sar/ERS/' + fmt[1::] +\
    '/' + rootfolder + '/' + filefolder + '/' + filename + fmt

sardata, _ = iprs.sarread(datafile)
Sr = sardata.rawdata
Sr = Sr[sa:ea, sr:er, :]
sardata = None

Sr, Flag = iprs.iq_correction(Sr)

print(Sr.min(), Sr.max())
Sr = Sr[:, :, 0] + 1j * Sr[:, :, 1]

Na, Nr = Sr.shape
print("SAR raw data: ", Sr.shape, Sr.dtype)

real = np.real(Sr)
# imag = np.imag(Sr) * 0.0
imag = np.imag(Sr)

Sr = real + imag * 1j

cmap = 'jet'
extent = SSA

# plt.figure()
# plt.subplot(211)
# plt.imshow(np.abs(Sr), cmap=cmap)
# plt.title("SAR raw data(Amplitude)")
# plt.xlabel("Range")
# plt.ylabel("Azimuth")
# plt.subplot(212)
# plt.imshow(np.angle(Sr), cmap=cmap)
# # plt.imshow(SI, cmap=cmap)
# plt.title('SAR raw data(phase)')
# plt.tight_layout()
# plt.show()


if imagingMethod is 'RDA':
    # SI = iprs.rda0(Sr, sarplat, verbose=True)
    SI = iprs.rda(Sr, sarplat, zpadar=zpadar, rcmc=rcmc, ftshift=ftshift, verbose=False)
    # SI = iprs.rda_adv(Sr, sarplat, zpadar=zpadar,
    # usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, verbose=False)
if imagingMethod is 'CSA':
    # SI = iprs.csa(Sr, sarplat, verbose=True)
    SI = iprs.csa_adv(Sr, sarplat, zpadar=zpadar,
                      usesrc=usesrc, rcmc=rcmc, usedpc=usedpc, verbose=False)

SI = np.flipud(SI)

outfile = './data/' + filename + '(sa' + str(sa) + 'ea' + str(ea) + 'sr' + \
    str(sr) + 'er' + str(er) + ')_' + imagingMethod + '_Imaging'
iprs.savemat(outfile + '.mat', {'SI': SI}, fmt='5')

print("SI.shape: ", SI.shape)

SI = np.abs(SI)

SI = iprs.multilook_spatial(SI, nlooks=nlooks)

print("SI.shape: ", SI.shape)

extent = SSA
cmap = 'gray'
axismod = 'SceneAbsoluteSlantRange'
axismod = 'SceneRelativeSlantRange'
axismod = 'Image'
iprs.sarshow(SI, sarplat, maxp=maxp, axismod=axismod,
             title=None, cmap=cmap, outfile=None, newfig=True)

print("SI.min(), SI.max(): ", SI.min(), SI.max())


SI = iprs.imadjust(SI, (minp, maxp), (0, 255))
# SI = iprs.imadjustlog(SI, (7, 15), (0, 255))
# SI = iprs.imadjustlog(SI, (40, 100), (0, 255))

# SI = iprs.histeq(SI, nbins=256)

SI = SI.astype('uint8')

iprs.imsave('./data/image' + imagingMethod + '_' + sensor_name + "_" + str(nlooks) + 'Looks_' +
            '(sa' + str(sa) + 'ea' + str(ea) + 'sr' + str(sr) + 'er' + str(er) + ')' + '.tiff', SI)

exit()

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

extent = SSA

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
