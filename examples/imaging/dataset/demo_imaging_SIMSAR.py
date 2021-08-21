#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import os
import iprs
import numpy as np
import random

sensor_name = 'SIMSARv1a'
acquis_name = 'SIMSARv1a'

sensor_name = 'SIMSARv1a'
acquis_name = 'SIMSARv1a'

sensor_name = 'SIMSARv1a'
acquis_name = 'SIMSARv1a'


sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquis=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()


infolder = "/mnt/d/DataSets/zhi/SAR/SIMSARv1/samples/"

outfolder = '/mnt/d/DataSets/zhi/SAR/SIMSARv1/'

datasetname = "MSTAR"

outfilename_prefix = outfolder + sarplat.name + "_" + datasetname + "nScenes"

outfile = outfilename_prefix + '.png'

imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK

verbose = True


infiles = os.listdir(infolder)

nScenes = len(infiles)

print("nScenes: ", str(nScenes))

bgv = 0
Srs = []
SrIs = []
for infile in infiles:
    imgfile = infolder + infile
    print(imgfile)
    grayimg = iprs.imread(imgfile)
    print("====================gen targets...")
    targets = iprs.img2tgs(grayimg, bg=bgv, noise=None)

    imgshape = grayimg.shape
    print(imgshape)
    SrI = iprs.show_targets(targets, imgshape, outfile=None, isshow=False)

    print("====================gen sar raw data...")
    Sr, targets = iprs.img2rawdata(
        sarplat, grayimg, bg=bgv, noise=None, verbose=True)

    Srs.append(Sr)
    SrIs.append(SrI)

print("====================save sar data...")
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Srs
sardata.image = SrIs

outfile = outfilename_prefix + str(nScenes) + '.pkl'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

Srs = sardata.rawdata
SrIs = sardata.image


nImagesForShow = 6

idxImageShow = random.sample(range(nScenes), nImagesForShow)
print("show image: ", idxImageShow)

for n in idxImageShow:
    if verbose:
        outfile = outfilename_prefix + \
            "_Scene" + str(n) + '.png'
        iprs.show_image(SrIs[n], outfile=outfile, isshow=True)
        # print("9999999999")
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
