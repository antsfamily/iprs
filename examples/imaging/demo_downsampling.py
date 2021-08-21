#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

srate_a = 0.5
srate_r = 0.5
# srate_a = 0.25
# srate_r = 0.25
datafile = '../data/sar/image/sensor=Air3_acquisition=Air3_00006672554Tgs.mat'

sardata, sarplat = iprs.load_data(datafile, way=0, which='all')
print(sardata)
sarplat.selection = None
sarplat.select()
sarplat.printsp()

# iprs.show_amplitude_phase(sardata.image[0])
# X = sardata.rawdata[0]

X = sardata.rawdata[0]
# print(type(X), X.shape)

Sr, obmat = iprs.sparse_observation(
    np.array([X]), way=0, mode='uniformly', rsample=(srate_a, srate_r))


# visualize
iprs.show_amplitude_phase(Sr[0])

# do RD imaging
Sr_img, ta, tr = iprs.rda(X, sarplat, verbose=False)
# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)

print(Sr[0].shape, "==============")
sarplat = iprs.process_sarplat(sarplat, rsample=(srate_a, srate_r))
# sarplat.printsp()
Sr_img, ta, tr = iprs.rda(Sr[0], sarplat, verbose=False)

# axismod = 'Image'
axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
# title = 'Reconstructed Image using RD, with arate: ' + \
#     str(round(srate_a, 4)) + ", rrate: " + str(round(srate_r, 4))
# title = 'Reconstructed Image using omega-k'
# iprs.show_sarimage(
#     Sr_img, sarplat, axismod=axismod, title=title, aspect=None)


title = 'CPRD'
iprs.show_sarimage3d(Sr_img, sarplat, axismod=axismod,
                     title=title, cmap='gray', isimgadj=True, figsize=(6, 5))
