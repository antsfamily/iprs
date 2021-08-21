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

# nlooks = (4, 1)
nlooks = (1, 1)
method = 'RDA'

sensor_name = 'ALOSPALSAR'
acquis_name = 'ALOSPALSAR'

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
    'SubEchoAnchor': [0, 0],
    # 'SubEchoAnchor': [3000, 3000],  # Airport
    # 'SubEchoAnchor': [6000, 3000],  # Ships
    # 'SubEchoAnchor': [8000, 4000],  # Ships
    'SubEchoSize': [32768, 8192],
    # 'SubEchoSize': [16384, 8192],
    # 'SubEchoSize': [8192, 4096],
}

sarplat.selection = ROI
SA = sarplat.acquisition['SceneArea']
SSA = sarplat.selection['SubSceneArea']
SSES = sarplat.selection['SubEchoSize']
print(SA, SSA, SSES)

(sa, sr) = ROI['SubEchoAnchor']

ea, er = iprs.ebeo((sa, sr), SSES, '+')
print(sa, sr, ea, er)
fmt = '.mat'


filefolder = 'ALPSRP050500980-L1.0'
filename = 'ALOS_PALSAR_RAW=IMG-HH-ALPSRP050500980-H1(sl=1el=35345)(sa0ea32768sr0er8192)_RDA_Imaging'
datafile = './data/' + filename + fmt

SI = scio.loadmat(datafile, struct_as_record=True)['SI']
SI = SI[:, :, 0] + 1j * SI[:, :, 1]
print(SI.shape)

SI = SI[sa:ea, sr:er]
# SI = np.flipud(SI)

SI = iprs.multilook_spatial(SI, nlooks=nlooks)

SI = np.abs(SI)


if nlooks > (1, 1):
    # SI = iprs.imadjustlog(SI, (0, 3), (0, 255))
    SI = iprs.imadjustlog(SI, None, (0, 255))
else:
    SI = iprs.imadjustlog(SI, None, (0, 255))

print(SI.min(), SI.max())

SI = SI.astype('uint8')

Na, Nr = SI.shape
SI = np.vstack((SI, np.zeros((35345 - Na, Nr))))

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
outfile = './data/image' + sensor_name + '_' + str(nlooks) + 'Looks_' + filename + '.tiff'
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
