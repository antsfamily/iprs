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


# datasetname = "128x128_disc"
datasetname = "center_disc"


imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK

verbose = True

nScenes = 2
nTGsEachSceneMax = 2

# nScenes = 4
# nTGsEachSceneMax = 5

nImagesForShow = 2
cmap = 'Spectral'
cmap = None

rmax = 12

nTGsAll = np.random.randint(1, nTGsEachSceneMax, nScenes)

SA = sarplat.acquisition['SceneArea']
scenShape = (SA[1] - SA[0], SA[3] - SA[2])

outfilename_prefix = outfolder + sarplat.name + "_" + datasetname

for n in range(nScenes):
    nTGs = nTGsAll[n]
    print("====================gen targets...")
    targets = iprs.gdisc(SA, nTGs, radiusMax=rmax, seed=None, verbose=False)
    SrI = iprs.show_targets(targets, scenShape, outfile=None, isshow=False)

    Srs = []
    SrIs = []
    for SNR in SNRs:
        print("====================gen noisy(SNR=" + str(SNR) + ") sar raw data...")
        Sr, ta, tr = iprs.tgs2rawdata(
            sarplat, targets, noise=noise, SNR=SNR, verbose=False)

        SrIr, ta, tr = iprs.rda(Sr, sarplat, verbose=False)

        Srs.append(Sr)
        SrIs.append(SrI)

        # axismod = 'Image'
        # axismod = 'SceneAbsolute'
        axismod = 'SceneRelative'
        # axismod = 'ddd'
        Title = 'Reconstructed Image using ' + imagingMethod
        # Title = 'Reconstructed Image using omega-k'

        iprs.show_sarimage(
            SrIr, sarplat, axismod=axismod, title=Title, cmap=cmap,
            aspect=None)

    print("====================save sar data...")
    sardata = iprs.SarData()
    sardata.name = datasetname
    sardata.rawdata = Srs
    sardata.image = SrIs

    outfile = outfilename_prefix + "_Scene" + str(n) + '.pkl'

    iprs.sarstore(sardata, sarplat, outfile)
    sardata, sarplat = iprs.sarread(outfile)
