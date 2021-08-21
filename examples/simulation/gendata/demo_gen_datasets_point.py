#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

sensor_name = 'DIY4'
acquis_name = 'DIY4'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

outfolder = '../data/sar/'

datasetname = "point"
# datasetname = "disc"

outfilename_prefix = outfolder + sarplat.name + "_" + datasetname

outfile = outfilename_prefix + '.png'

imagingMethod = 'RangeDoppler'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'ChirpScaling'  # 'RangeDoppler'  ChirpScaling  OmegaK
# imagingMethod = 'OmegaK'  # 'RangeDoppler'  ChirpScaling  OmegaK


nTGs = 5
SA = sarplat.acquisition['SceneArea']
print("====================gen targets...")
if datasetname is "point":
    targets = iprs.gpts(SA, nTGs, seed=None, verbose=True)
elif datasetname is "disc":
    targets = iprs.gdisc(SA, nTGs, radiusMax=10, seed=None, verbose=False)

iprs.show_targets(targets, (SA[1] - SA[0], SA[3] - SA[2]), outfile)

print("====================gen sar raw data...")
Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets)

# visualize
iprs.show_amplitude_phase(Sr)

if imagingMethod is 'RangeDoppler':
    # do RD imaging
    Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)
elif imagingMethod is 'OmegaK':
    Sr_img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)
elif imagingMethod is 'ChirpScaling':
    Sr_img = iprs.chirp_scaling(Sr, sarplat, verbose=False)

print(Sr_img[0:10, 0:10])
# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
# axismod = 'ddd'
title = 'Reconstructed Image using ' + imagingMethod
# title = 'Reconstructed Image using omega-k'
outfile = outfilename_prefix + imagingMethod + '.png'

iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None, outfile=outfile)

sardata = iprs.SarData()

sardata.name = datasetname
sardata.rawdata = Sr
sardata.image = Sr_img

outfile = outfilename_prefix + '.pkl'
iprs.sarstore(sardata, sarplat, outfile)
outfile = outfilename_prefix + '.mat'
iprs.sarstore(sardata, sarplat, outfile)

# sardata, sarplat = iprs.sarread(outfile)


Sr_img = sardata.image


iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None, outfile=None)
