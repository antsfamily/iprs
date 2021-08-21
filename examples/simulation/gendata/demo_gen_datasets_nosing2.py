#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import random

sensor_name = 'DIY4'
acquis_name = 'DIY4'

# sensor_name = 'DIY8'
# acquis_name = 'DIY8'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()


noise = 'wgn'
SNRs = [None, 50, 40, 30, 20, 15, 10, 5, 0, -5, -10, -15]


# outfolder = '../data/sar/'
outfolder = '../data/sar/noisy/'

datasetname = 'DIY4_MiniSAR20050524p0002image006'

datafile = "/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006.pkl"


imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK

verbose = True

cmap = None


sardata, sarplat = iprs.sarread(datafile)

X = np.array(sardata.rawdata)  # [N Na Nr] complex
I = np.array(sardata.image)

print(X.shape)


outfilename_prefix = outfolder + sarplat.name + "_" + datasetname

Srs = []
SrIrs = []
for SNR in SNRs:
    print("====================gen noisy(SNR=" + str(SNR) + ") sar raw data...")
    if SNR is not None:
        Sr = iprs.matnoise(X, noise=noise, imp=None, SNR=SNR)
        SrIr, ta, tr = iprs.rda(Sr, sarplat, verbose=False)
    else:
        Sr = X
        SrIr, ta, tr = iprs.rda(X, sarplat, verbose=False)


    Srs.append(Sr)
    SrIrs.append(SrIr)

print("====================save sar data...")
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Srs
sardata.image = SrIrs


outfile = datafile[0:-4] + '_noisy.pkl'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)
