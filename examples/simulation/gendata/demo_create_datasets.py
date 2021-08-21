#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-12 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import random

sensor_name = 'DIY4'
acquis_name = 'DIY4'

sarplat = iprs.SarPlat()


outfolder = '../data/sar/'

sarplatname = 'sensor=DIY4_acquisition=DIY4_'
datasetname = 'MinSARs21+Disc32'

outfilename_prefix = outfolder + sarplatname + datasetname

infolder = '/mnt/d/DataSets/zhi/SAR/MiniSAR/'
dataformat = '.pkl'

filelists = iprs.listxfile(listdir=infolder, exts=dataformat)


# exit()
Srs = []
SrIs = []

nScenes = 0
for sarfile in filelists:
    print("reading... ", sarfile)
    sardata, sarplat = iprs.sarread(sarfile)
    Sr = sardata.rawdata
    SrI = sardata.image

    print("====================combine sar raw data")
    if isinstance(Sr, list):
        nScenesN = len(Sr)
        print("---------- ", nScenesN, " scenes in: ", sarfile)
        for n in range(nScenesN):
            print(type(Sr[n]))
            print(Sr[n].shape)
            Srs.append(Sr[n])
            SrIs.append(SrI[n])
            nScenes = nScenes + 1
    else:
        print(Sr.shape)
        Srs.append(Sr)
        SrIs.append(SrI)
        nScenes = nScenes + 1


outfile = outfilename_prefix + "_nScenes" + str(nScenes) + '.pkl'

print("====================save sar data to...")
print(outfile)

DataSet = iprs.SarData()
DataSet.name = datasetname
DataSet.rawdata = Srs
DataSet.image = SrIs

outfile = outfilename_prefix + "_nScenes" + str(nScenes) + '.pkl'

iprs.sarstore(DataSet, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

Srs = sardata.rawdata
SrIs = sardata.image


# ----------------------------valid------------------------
verbose = True
imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK


nImagesForShow = 6

idxImageShow = random.sample(range(nScenes), nImagesForShow)
idxImageShow = range(nImagesForShow)
print("show image: ", idxImageShow)

for n in idxImageShow:
    if verbose:
        outfile = outfilename_prefix + \
            "_Scene" + str(n) + '.png'
        iprs.show_image(SrIs[n], outfile=outfile, isshow=True)
        # visualize
        iprs.show_amplitude_phase(Srs[n])

    if imagingMethod is 'RangeDoppler':
        # do RD imaging
        SrIr, ta, tr = iprs.rda(Srs[n], sarplat, verbose=False)
    elif imagingMethod is 'OmegaK':
        SrIr, ta, tr = iprs.omega_k(Srs[n], sarplat, verbose=False)
    elif imagingMethod is 'ChirpScaling':
        SrIr = iprs.chirp_scaling(Srs[n], sarplat, verbose=False)

    if verbose:
        # axismod = 'Image'
        # axismod = 'SceneAbsolute'
        axismod = 'SceneRelative'
        # axismod = 'ddd'
        Title = 'Reconstructed Image using ' + imagingMethod
        # Title = 'Reconstructed Image using omega-k'
        outfile = outfilename_prefix + "_" + \
            imagingMethod + "_Scene" + str(n) + '.png'

        iprs.show_sarimage(
            SrIr, sarplat, axismod=axismod, title=Title,
            aspect=None, outfile=outfile)
