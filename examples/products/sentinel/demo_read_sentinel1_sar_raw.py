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


disk = '/mnt/d/'
disk = 'D:/'
filename = 'S1A_S1_RAW__0SDV_20180728T014255_20180728T014310_022988_027EB4_82C1'
filepath = disk + 'DataSets/sar/Sentinel1/data/' + filename + '.SAFE'

Description = {'Platform': 'Sentinel1', 'SensorType': 'SAR', 'SensorMode': 'SM', 'DataType': 'RAW', 'DataSize': ['Nlines×Nsamples×2(IQ)', 0]}

outfmt = '.pkl'
outfolder = disk + 'DataSets/sar/Sentinel1/' + outfmt[1::] + '/'

endian = '>'

offset = 0
# offset = 11644

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=offset, endian='>')

iprs.printrcd(D)

sl = 1
el = 28621
# el = 28651
# el = 28659
# el = 28000
# el = 30000

S = iprs.read_ers_sar_raw(filepath, sl=sl, el=el, rmbp=False)

print(S.shape)

Description['DataSize'][1] = S.shape

sensor_name = 'Sentinel1'
acquis_name = 'Sentinel1'
sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None

sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'Sentinel1_SAR_RAW=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + '(sl=' + str(sl) + 'el=' + str(el) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = S[:, :, 0] + 1j * S[:, :, 1]

iprs.showReImAmplitudePhase(S)
