#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-11-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import copy
import iprs
import matplotlib.pyplot as plt


disk = '/mnt/d/'
disk = 'D:/'

filename = 'stlake_27129_20002_008_200131_L090HHHV_CX_01'
filepath = disk + \
    'DataSets/sar/UAVSAR/data/stlake_27129_20002_008_200131_L090_CX_01_mlc/' + \
    filename + '.mlc'
Description = {'Platform': 'UAVSAR', 'SensorType': 'POLSAR', 'SensorMode':
               '  ', 'DataType': 'MLC', 'DataSize': ['Nlines×Nsamples×2(IQ)', 0]}

outfmt = '.pkl'
outfolder = disk + 'DataSets/sar/UAVSAR/' + outfmt[1::] + '/'

endian = '<'
dshape = (3185, 5843)
S = iprs.read_uavsar_mlc(filepath, dshape=dshape, dtype='complex')


Description['DataSize'][1] = S.shape

sensor_name = 'UAVSAR'
acquis_name = 'UAVSAR'
sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None

sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'UAVSAR_STOKES_MATRIX=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + '(dshape=' + str(dshape) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = S[:, :, 0] + 1j * S[:, :, 1]

SI = np.abs(S)
print(SI.min(), SI.max())
SI = iprs.imadjustlog(SI, (-80, 20), (0, 255))
SI = SI.astype('uint8')

SI = np.fliplr(SI)

iprs.imsave('./image' + sensor_name + '.tiff', SI)

cmap = 'jet'
extent = None

plt.figure()
plt.imshow(SI, extent=extent, cmap=cmap)
plt.xlabel("Range/m")
plt.ylabel("Azimuth/m")
plt.title("UAVSAR MLC")
plt.show()
