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
from iprs.utils.const import *

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

prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_50460_STD', 'F127', 1, 28636, [28636, 5616], 67.98 * PI / 180, 7.335008 * PI / 180, 5.3e9, 791640., 7100., 1679.9023438, 18959999.1, 3.70999985e-05, 834071.4111)
# prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_80406_STD', 'F123', 1, 28624, [28624, 5616], 68.03 * PI / 180, 7.359127 * PI / 180, 5.3e9, 791291., 7100., 1679.9023438, 18959999.1, 3.70999985e-05, 833359.9854)
prefixname, frame, sl, el, ES, Ad, Be, Fc, H, V, PRF, Fs, Tp, Rnear = ('E2_81988_STD', 'F327', 1, 28698, [28698, 5616], 68.02 * PI / 180, 7.355842 * PI / 180, 5.3e9, 791193., 7100., 1679.9023438, 18959999.1, 3.70999985e-05, 833367.9199)

sarplat.sensor = iprs.dmka(sarplat.sensor, {'H': H, 'V': V, 'PRF': PRF, 'Fc': Fc})

sarplat.acquisition = iprs.dmka(sarplat.acquisition, {'EchoSize': ES, 'Ad': Ad, 'Be': Be})
sarplat.params = None  # recompute parameters
sarplat.selection = None
sarplat.printsp()

Description = {'Platform': 'ERS2', 'SensorType': 'SAR', 'SensorMode': 'STD', 'DataType': 'RAW', 'DataSize': ['Nlines×Nsamples×2(IQ)', 0]}

level = 'L0'
ext = '.000.raw'
rootfolder = prefixname + '_' + frame
filefolder = prefixname + '_' + level + '_' + frame
filename = prefixname + '_' + level + '_' + frame

filepath = disk + 'DataSets/sar/ERS/data/' + \
    rootfolder + '/' + filefolder + '/' + filename + ext

outfmt = '.mat'
outfolder = disk + 'DataSets/sar/ERS/' + \
    outfmt[1::] + '/' + rootfolder + '/' + filefolder + '/'

endian = '>'

# ------------------demo of reading record, start
D = copy.deepcopy(iprs.SarDataFileFileDescriptorRecordCEOS)

offset = 0
# offset = 11644

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=offset, endian='>')
nLines = D['Number of lines per data set (nominal)'][2][0]

iprs.printrcd(D)
# ------------------demo of reading record, end

sl = 1
el = 32
el = nLines
print(sl, el)

S = iprs.read_ers_sar_raw(filepath, sl=sl, el=el, rmbp=False)

print(S.shape)

Description['DataSize'][1] = S.shape


sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'ERS2_SAR_RAW=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + '(sl=' + str(sl) + 'el=' + str(el) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = S[:, :, 0] + 1j * S[:, :, 1]

iprs.showReImAmplitudePhase(S)
