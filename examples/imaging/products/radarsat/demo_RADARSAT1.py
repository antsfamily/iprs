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

isSaveImagingResult = True

maxp = 1.5e5
# maxp = 1.e4
# maxp = 5e3
# maxp = 2.5e2
ftshift = True
# zpadar = (512, 512)
zpadar = False
# zpadar = None
usesrc = True
# usesrc = False
usedpc = True
# usedpc = False
rcmc = False
rcmc = 64
afa = None
# afa = 'PGA'
nlooks = (1, 1)
# nlooks = None

useVGACPS = False
useVGACPS = True

sensor_name = 'RADARSAT1'
acquis_name = 'RADARSAT1'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    'SubEchoAnchor': [0, 0],
    # 'SubEchoAnchor': [1801, 970],  # For coal & ferry terminals
    # 'SubEchoAnchor': [5561, 1060],  # Vancouver airport
    # 'SubEchoAnchor': [7097, 760],  # UBC and one ship
    # 'SubEchoAnchor': [7769, 1050],  # English Bay ships
    # 'SubEchoAnchor': [4096, 0],  # Blaine, Washington, USA
    # 'SubEchoAnchor': [7657, 1850],  # Stanley Park & city
    # 'SubEchoAnchor': [16169, 2640], # Squamish & Garibaldi
    # 'SubEchoAnchor': [17897, 2800], # Brackendale
    # 'SubEchoSize': [2048, 2048],
    # 'SubEchoSize': [4096, 4096],
    # 'SubEchoSize': [8192, 8192],
    'SubEchoSize': [16384, 8192],

}

sarplat.selection = ROI
sarplat.printsp()

SA = sarplat.acquisition['SceneArea']
SSA = sarplat.selection['SubSceneArea']
SSES = sarplat.selection['SubEchoSize']
SubRsc = sarplat.params['SubRsc']
SubRnear = sarplat.params['SubRnear']
SubRfar = sarplat.params['SubRfar']
print(SA, SSA, SSES)

(sa, sr) = ROI['SubEchoAnchor']

ea, er = iprs.ebeo((sa, sr), SSES, '+')
print(sa, sr, ea, er)

# disk = 'D:/'
disk = '/mnt/d/'
filefmt = '.mat'
# filefmt = '.pkl'
filename = 'RADARSAT1_SAR_RAW=Vancouver(sl=1el=19438)_VGACPS=True'
filename = 'RADARSAT1_SAR_RAW=Vancouver(sl=1el=19438)_VGACPS=False'
datafile = disk + '/DataSets/sar/RADARSAT/frombooks/Vancouver/' + \
    filefmt[1::] + '/' + filename + filefmt
vgagainfilepath = disk + 'DataSets/sar/RADARSAT/frombooks/Vancouver/data/AGC_attenuation_values.mat'

sardata, _ = iprs.sarread(datafile)
Sr = sardata.rawdata
Sr = Sr[sa:ea, sr:er, :]

print("min max", Sr.min(), Sr.max())


if useVGACPS:
    V = scio.loadmat(vgagainfilepath, struct_as_record=True)['nom_attenuation']
    Sr = iprs.vga_gain_compensation(Sr, V[sa:ea, :], mod='linear', fact=1.5)
# scio.savemat('radarsat_vancouver.mat', {'Sr': Sr})
Na, Nr, _ = Sr.shape
print("SAR raw data: ", Sr.shape, Sr.dtype)

Sr = Sr[:, :, 0] + 1j * Sr[:, :, 1]

real = np.real(Sr)
# imag = np.imag(Sr) * 0.0
imag = np.imag(Sr)

# Sr = imag + real * 1j
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
    SI = iprs.rda(Sr, sarplat, zpadar=zpadar, rcmc=rcmc, afa=afa, ftshift=ftshift, verbose=False)
    # SI = iprs.rda_ss(Sr, sarplat, zpadar=zpadar, rcmc=rcmc, afa=afa, ftshift=ftshift, verbose=False)

    # SI = iprs.rda_adv(Sr, sarplat, zpadar=zpadar, usesrc=usesrc, usedpc=usedpc, rcmc=rcmc, ftshift=ftshift, verbose=False)
if imagingMethod is 'CSA':
    # SI = iprs.csa(Sr, sarplat, verbose=True)
    SI = iprs.csa_adv(Sr, sarplat, zpadar=zpadar,
                      usesrc=usesrc, rcmc=rcmc, usedpc=usedpc, verbose=False)

SI = np.flipud(SI)

if isSaveImagingResult:
    outfile = './data/Vancouver(sa' + str(sa) + 'ea' + str(ea) + 'sr' + \
        str(sr) + 'er' + str(er) + ')_' + imagingMethod + '_Imaging'
    scio.savemat(outfile + '.mat', {'SI': iprs.imag2real(SI)})

SI = iprs.multilook_spatial(SI, nlooks=nlooks)
print("SI.shape: ", SI.shape)

SI = np.abs(SI)
print("SI.min(), SI.max(): ", SI.min(), SI.max())

cmap = 'gray'
axismod = 'SceneAbsoluteSlantRange'
axismod = 'SceneRelativeSlantRange'
axismod = 'SceneRelativeGroundRange'
# axismod = 'Image'
extent = [SubRnear - SubRsc, SubRfar - SubRsc, SSA[2], SSA[3]]

iprs.sarshow(SI, sarplat, maxp=maxp, axismod=axismod,
             title=None, cmap=cmap, outfile=None, newfig=True)

# exit()
# SI = iprs.imadjust(SI, (None, maxp), (0, 255))
# SI = iprs.imadjust(SI, (10, 300), (0, 255))
# SI = iprs.imadjust(SI, (20, 255), (0, 255))
# SI = iprs.imadjustlog(SI, (20, 50), (0, 255))
# SI = iprs.imadjustlog(SI, None, (0, 255))
# SI = iprs.imadjustlog(SI, (5, 255), (0, 255))
# SI = SI.astype('uint8')

SI = iprs.mapping(SI)

iprs.imsave('./data/image' + sensor_name + "_" + str(nlooks) + 'Looks_' +
            '(sa' + str(sa) + 'ea' + str(ea) + 'sr' + str(sr) + 'er' + str(er) + ')' '.tiff', SI)

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

Title = Title + ")" + str(nlooks) + 'Looks'

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
plt.imshow(SI, extent=extent, cmap='gray')
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.title(Title)
plt.show()
