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

oshape = (8192, 7833)

oshape = (8192, 7924)

nlooks = (4, 1)
# nlooks = (1, 1)
method = 'RDA'

sensor_name = 'ERS'
acquis_name = 'ERS'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None
sarplat.printsp()

ROI = {
    'SubSceneArea': None,  # SceneArea
    # 'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
    # 'SubEchoSize': None,  # EchoSize
    # 'SubEchoSize': [1., 1.],  # 28659x5616
    # 'SubEchoSize': [28000, 5616],
    'SubEchoSize': [28603, 5616],
    # 'SubEchoSize': [28659, 5616],
    # 'SubEchoSize': [30000, 5616],
    # 'SubEchoSize': [8192, 5616],
    # 'SubEchoSize': [4096, 5616],
    # 'SubEchoSize': [2048, 5616],
    # 'SubEchoSize': [2048, 2048],
    # 'SubEchoSize': [1100, 1700],
    # 'SubEchoSize': [1024, 2048],
    # 'SubEchoSize': [1024, 1024],
}

sarplat.selection = ROI
SA = sarplat.acquisition['SceneArea']
SSA = sarplat.selection['SubSceneArea']
SSES = sarplat.selection['SubEchoSize']

rootfolder = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/'
folder = 'ers/'
filename = 'ERS2_SAR_RAW=E2_84690_STD_L0_F137(sl=1el=28603)(sa0ea28603sr0er5616)_CSA_Imaging'
# filename = 'ERS2_SAR_RAW=E2_84686_STD_L0_F203(sl=1el=28659)(sa0ea28659sr0er5616)_CSA_Imaging'
# filename = 'ERS2_SAR_RAW=ERS2_127_2907_23027(sl=1el=28000)(sa0ea28000sr0er5616)_CSA_Imaging'
datafile = rootfolder + folder + filename + '.mat'

SI = scio.loadmat(datafile, struct_as_record=True)['SI']
print(SI.shape)

(sa, sr) = (0, 0)
# (sa, sr) = (1801, 970)  # For coal & ferry terminals
# (sa, sr) = (5561, 1060)  # Vancouver airport
# (sa, sr) = (7097, 760)  # UBC and one ship
# (sa, sr) = (7769, 1050)  # English Bay ships
# (sa, sr) = (7657, 1850)  # Stanley Park & city
# (sa, sr) = (16169, 2640)  # Squamish & Garibaldi
# (sa, sr) = (17897, 2800)  # Brackendale

sa, ea, sr, er = (sa, sa + SSES[0], sr, sr + SSES[1])  # Stanley Park & city
SI = np.flipud(SI)
SI = SI[sa:ea, sr:er]
SI = np.flipud(SI)

SI = iprs.multilook_spatial(SI, nlooks=nlooks)

SI = np.abs(SI)


if nlooks > (1, 1):
    # SI = iprs.imadjustlog(SI, (0, 3), (0, 255))
    SI = iprs.imadjustlog(SI, (-5, 3), (0, 255))
else:
    SI = iprs.imadjustlog(SI, (3, 10), (0, 255))

print(SI.min(), SI.max())

SI = SI.astype('uint8')

print(SI.min(), SI.max())
print("SI.shape: ", SI.shape)

Title = 'Imaging Result of ' + method + '(' + str(nlooks) + ' looks)'


cmap = 'gray'
# cmap = 'hot'
# cmap = None

extent = SSA
# extent = None

# SI = iprs.imresize(SI, oshape, odtype=SI.dtype, preserve_range=True)
# print(SI.shape, SI.min(), SI.max(), "===")

print("save to tiff file!")
outfile = './image' + sensor_name + '_' + str(nlooks) + 'Looks_' + filename + '.tiff'
iprs.imsave(outfile, SI)
print("done!")


A = iprs.imread(outfile)

plt.figure()
plt.imshow(A, cmap='gray')
plt.show()

plt.figure()
plt.imshow(SI, extent=extent, cmap='gray')
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.title(Title)
plt.show()
