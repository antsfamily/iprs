#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2018-11-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import copy
import iprs
import scipy.io as scio

useVGACPS = False
# useVGACPS = True

disk = '/mnt/d/'
# disk = 'D:/'
filename = 'Vancouver'

filepath = disk + 'DataSets/sar/RADARSAT/frombooks/' + filename + '/data/DAT_01.001'
vgagainfilepath = disk + 'DataSets/sar/RADARSAT/frombooks/' + \
    filename + '/data/AGC_attenuation_values.mat'

Description = {'Platform': 'RADARSAT1', 'SensorType': 'SAR', 'SensorMode': 'STD',
               'DataType': 'RAW', 'DataSize': ['Nlines×Nsamples×2(IQ)', 0]}

outfmt = '.mat'
outfolder = disk + 'DataSets/sar/RADARSAT/frombooks/' + filename + '/' + outfmt[1::] + '/'

endian = '>'

D = copy.deepcopy(iprs.SarDataFileFileDescriptorRecordRADARSAT)
offset = 0

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=offset, endian='>')

nLines = D['Number of lines per data set (nominal)'][2][0]

sl = 1
el = nLines
# el = 19

print(sl, el)

# 19438 x 9288
S = iprs.read_radarsat_sar_raw(filepath, sl=sl, el=el)

if useVGACPS:
    data = scio.loadmat(vgagainfilepath, struct_as_record=True)
    V = data['nom_attenuation']
    print(S.shape, V.shape)
    S = iprs.vga_gain_compensation(S, V, mod='linear', fact=1.5)

S = S.astype('int8')

Description['DataSize'][1] = S.shape
print(S.shape)


sensor_name = 'RADARSAT1'
acquis_name = 'RADARSAT1'
sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}
sarplat.params = None
sarplat.selection = None

sarplat.printsp()

sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'RADARSAT1_SAR_RAW=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + \
    '(sl=' + str(sl) + 'el=' + str(el) + ')_VGACPS=' + str(useVGACPS) + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = S[:, :, 0] + 1j * S[:, :, 1]

iprs.showReImAmplitudePhase(S)
