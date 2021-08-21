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

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

outfolder = '../data/sar/'
# outfolder = './data/'

datasetname = "point"
datasetname = "640x640_disc_cross"

outfilename_prefix = outfolder + sarplat.name + "_" + datasetname

outfile = outfilename_prefix + '.png'

imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK

verbose = True

SA = sarplat.acquisition['SceneArea']
scenShape = (SA[1] - SA[0], SA[3] - SA[2])

nScenes = 2

rmin = 5

rmax = 8

(Xmin, Xmax, Ymin, Ymax) = SA

print(Xmin, Xmax)

x0 = [0, 0, 0, -Xmin / 5, 0, Xmin / 5]
y0 = [-Ymin / 5, 0, Ymin / 5, 0, 0, 0]
centers = [x0, y0]
amps = [0.8, 1, 0.9, 0.7, 1, 0.6]
# amps = [0.8, 1, 0.9, 0.7, 1, 0.6]

Srs = []
SrIs = []
for n in range(nScenes):
    print("====================gen targets...")
    targets = iprs.gdisc(SA, nDiscs=len(x0), centers=centers, radiusMin=rmin,
                         radiusMax=rmax, amps=amps, seed=None, verbose=False)
    SrI = iprs.show_targets(targets, scenShape, outfile=None, isshow=False)

    print("====================gen sar raw data...")
    Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets)
    Srs.append(Sr)
    SrIs.append(SrI)

print("====================save sar data...")
sardata = iprs.SarData()
sardata.name = datasetname
sardata.rawdata = Srs
sardata.image = SrIs

outfile = outfilename_prefix + "_rmax" + \
    str(rmax) + "_nScenes" + str(nScenes) + '.pkl'

iprs.sarstore(sardata, sarplat, outfile)
sardata, sarplat = iprs.sarread(outfile)

Srs = sardata.rawdata
SrIs = sardata.image


nImagesForShow = 1

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
