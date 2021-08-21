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
# nlooks = (2, 1)

maxp = 5e4
minp = np.sqrt(maxp)
# minp = None

sensor_name = 'ALOSPALSAR'
acquis_name = 'ALOSPALSAR'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}

fmt = '.mat'

disk = '/mnt/d/'
# disk = 'D:/'

rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP020160970', 1, 31358, [31358, 11944], 45.618 * PI / 180, 3.323950 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 703222., 7147.64, 1912.046, 32.00e+6, 957190.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP050500980', 1, 35345, [35345, 10344], 53.480 * PI / 180, 4.283521 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 702025., 7166.00, 2155.172, 32.00e+6, 850614.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP115120970', 1, 35345, [35345, 10344], 53.478 * PI / 180, 4.284679 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 701765., 7166.40, 2155.172, 32.00e+6, 850314.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP258510980', 1, 35344, [35344, 5194], 53.462 * PI / 180, 4.298634 * PI / 180, 1.27e9, -14.e6 / 27.0e-6, 701828., 7165.42, 2155.172, 16.00e+6, 850464.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP262740970', 1, 35193, [35193, 5194], 53.480 * PI / 180, 4.303387 * PI / 180, 1.27e9, -14.e6 / 27.0e-6, 701744., 7166.22, 2145.923, 16.00e+6, 850164.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP162320920', 1, 35224, [35224, 10344], 53.470 * PI / 180, 4.284614 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 701498., 7169.28, 2155.17, 32.00e+6, 850014.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP166550550', 1, 35421, [35421, 10344], 53.460 * PI / 180, 4.303236 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 698105., 7184.88, 2159.827, 32.00e+6, 845967.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP273680670', 1, 35345, [35345, 10344], 53.453 * PI / 180, 4.297680 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 698769., 7179.24, 2155.17, 32.00e+6, 846866.)

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    'SubEchoAnchor': [0, 0],
    # 'SubEchoAnchor': [3000, 3000],  # Airport
    # 'SubEchoAnchor': [3000, 6000],  # Airport
    # 'SubEchoAnchor': [6000, 3000],  # Ships
    # 'SubEchoAnchor': [6000, 6000],
    # 'SubEchoAnchor': [8000, 4000],  # Ships
    # 'SubEchoAnchor': [3000, 0],  # Ships
    # 'SubEchoAnchor': [10000, 0],
    # 'SubEchoSize': [35345, 10344],
    'SubEchoSize': [8192, 8192],
    # 'SubEchoSize': [32768, 8192],
    # 'SubEchoSize': [16384, 8192],
    # 'SubEchoSize': [8192, 4096],
    # 'SubEchoSize': [4096, 2048],
    # 'SubEchoSize': ES,
}

sarplat.sensor = iprs.dmka(sarplat.sensor, {'H': H, 'V': V, 'PRF': PRF, 'Fc': Fc, 'Kr': Kr, 'Fs': Fs})

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

rootfolder = rootfilename
filefolder = rootfilename + '-L1.0'
# filefolder = rootfilename + '-L1.1'
# filename = 'ALOS_PALSAR_SLC=IMG-HH-' + rootfilename + \
filename = 'ALOS_PALSAR_RAW=IMG-HH-' + rootfilename + \
    '-H1(sl=' + str(sl) + 'el=' + str(el) + ')'

datafile = disk + '/DataSets/sar/ALOSPALSAR/' + fmt[1::] +\
    '/' + rootfolder + '/' + filefolder + '/' + filename + fmt

sardata, _ = iprs.sarread(datafile)
Sr = sardata.rawdata
Sr = Sr[sa:ea, sr:er, :]
sardata = None

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

# SI = np.flipud(SI)

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
