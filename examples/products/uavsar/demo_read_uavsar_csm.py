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

filename = 'SaltnS_22001_18080_004_181105_L090_CX_01'
filepath = disk + 'DataSets/sar/UAVSAR/data/SaltnS_22001_18080_004_181105_L090_CX_01_stokes/' + filename + '.dat'
Description = {'Platform': 'UAVSAR', 'SensorType': 'POLSAR', 'SensorMode': 'STD', 'DataType': 'CSM', 'DataSize': ['Nlines×Nsamples×2(IQ)', 0]}

outfmt = '.pkl'
outfolder = disk + 'DataSets/sar/UAVSAR/'  + outfmt[1::] + '/'

endian = '>'

D = copy.deepcopy(iprs.SarDataFileFileDescriptorRecordCEOS)
# D = copy.deepcopy(iprs.SarDataFileSignalDataRecordCEOS)

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

S = iprs.read_uavsar_csm(filepath, sl=sl, el=el, rmbp=False)

print(S.shape)

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

outfile = outfolder + sardata.name + '(sl=' + str(sl) + 'el=' + str(el) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = S[:, :, 0] + 1j * S[:, :, 1]

iprs.showReImAmplitudePhase(S)
