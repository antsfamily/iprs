#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-1-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import copy
import iprs


disk = '/mnt/d/'
filename = 'E2_84690_STD_F137'
# filename = 'E2_84686_STD_F203'
# filename = 'E2_84699_STD_F303'
filepath = disk + 'DataSets/sar/ERS/data/' + filename + '/' + filename + '.D'

Description = {'Platform': 'ERS2', 'SensorType': 'SAR', 'SensorMode': 'STD', 'DataType': 'SLC', 'DataSize': ['Nlines×Nsamples×2(real imag)', 0]}

outfolder = disk + 'DataSets/sar/ERS/mat/'
outfmt = '.mat'

endian = '>'

D = copy.deepcopy(iprs.SarDataFileFileDescriptorRecordCEOS)
# D = copy.deepcopy(iprs.SarDataFileSignalDataRecordCEOS)

offset = 0
# offset = 11644

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=offset, endian='>')

iprs.printrcd(D)

sl = 1
el = 8192
# el = 28659

S = iprs.read_ers_sar_slc(filepath, sl=sl, el=el, rmbp=False)

print(S.shape, S.dtype)

Description['DataSize'][1] = S.shape

sensor_name = 'ERS'
acquis_name = 'ERS'
sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None

sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'ERS2_SAR_RAW=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + '(sl=' + str(sl) + 'el=' + str(el) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

iprs.imsave('./image' + sensor_name + '.tiff', sardata.rawdata)

iprs.showReImAmplitudePhase(S)
