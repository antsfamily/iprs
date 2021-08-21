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
from iprs.utils.const import *
import matplotlib.pyplot as plt


sensor_name = 'ALOSPALSAR'
acquis_name = 'ALOSPALSAR'
sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = {'GeometryMode': 'SG'}

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

# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP156110750', 1, 35345, [35345, 10344], 53.453 * PI / 180, 4.297680 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 698769., 7179.24, 2155.17, 32.00e+6, 846866.)
# rootfilename, sl, el, ES, Ad, Be, Fc, Kr, H, V, PRF, Fs, Rnear = ('ALPSRP148670980', 1, 35345, [35345, 10344], 53.453 * PI / 180, 4.297680 * PI / 180, 1.27e9, -28.e6 / 27.0e-6, 698769., 7179.24, 2155.17, 32.00e+6, 846866.)

sarplat.sensor = iprs.dmka(
    sarplat.sensor, {'H': H, 'V': V, 'PRF': PRF, 'Fc': Fc, 'Kr': Kr, 'Fs': Fs})

sarplat.acquisition = iprs.dmka(sarplat.acquisition, {'EchoSize': ES, 'Ad': Ad, 'Be': Be})
sarplat.params = None  # recompute parameters
sarplat.selection = None
sarplat.printsp()

Description = {'Platform': 'ALOS', 'SensorType': 'PALSAR',
               'SensorMode': 'Fine(FBS)', 'DataType': 'SLC', 'DataSize': ['Nlines×Nsamples×2(RI)', 0]}

level = 'L1.1'
ext = '.1__A'
rootfolder = rootfilename
filefolder = rootfilename + '-' + level
filename = 'IMG-HH-' + rootfilename + '-H1'

filepath = disk + 'DataSets/sar/ALOSPALSAR/data/' + \
    rootfolder + '/' + filefolder + '/' + filename + ext

outfmt = '.mat'
outfolder = disk + 'DataSets/sar/ALOSPALSAR/' + \
    outfmt[1::] + '/' + rootfolder + '/' + filefolder + '/'

endian = '>'

# ------------------demo of reading record, start
D = copy.deepcopy(iprs.SarImageFileFileDescriptorRecordALOSPALSAR)
# D = copy.deepcopy(iprs.SarDataFileSignalDataRecordALOSPALSAR)

offset = 0
# offset = 11644

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=offset, endian='>')
nLines = D['Number of lines per data set (nominal)'][2][0]

iprs.printrcd(D)
# ------------------demo of reading record, end

sl = 1
el = 81
el = 256
# el = nLines

S = iprs.read_alos_palsar_slc(filepath, sl=sl, el=el, rmbp=False)

print(S.shape, S.dtype)

Description['DataSize'][1] = S.shape


sardata = iprs.SarData()
sardata.rawdata = S
sardata.name = 'ALOS_PALSAR_SLC=' + filename
sardata.image = []
sardata.description = Description

outfile = outfolder + sardata.name + '(sl=' + str(sl) + 'el=' + str(el) + ')' + outfmt

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

S = sardata.rawdata[:, :, 0] + 1j * sardata.rawdata[:, :, 1]

SI = np.abs(S)

SI = iprs.toimage(SI, drange=(0, 255), method='2sigma')
print(SI.min(), SI.max(), SI.shape)

SI = SI[0:256, 0:256]
iprs.imsave('./' + rootfilename + '-L1.1' + '-2SigmaMapping' + '.tiff', SI)


plt.figure()
plt.imshow(SI, cmap='gray')
plt.show()
