#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

sarplat = iprs.SarPlat()
sarplat.name = 'DIY4'
sarplat.sensor = iprs.SENSORS[sarplat.name]
sarplat.acquisition = iprs.ACQUISITION['DIY4']
sarplat.params = None
sarplat.printsp()


SC = sarplat.acquisition['SceneCenter']
Xc = SC[0]
Yc = SC[1]

targets = [
    [100, 100, 0, 0, 0, 0, 1],
    [-150, -50, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [200, 0, 0, 0, 0, 0, 1],
]
print(targets)

Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets, verbose=True)


# visualize
iprs.show_amplitude_phase(Sr)

# do RD imaging
Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)
# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)


srate_a = 0.5
srate_r = 0.5

[Na, Nr] = Sr.shape

Na0 = int((1 - srate_a) * Na)
Nr0 = int((1 - srate_r) * Nr)
Nsr = Nr - Nr0
Nsa = Na - Na0
print("===========down sampling...")
print("num of samples in range: ", Nsr)
print("num of samples in azimuth: ", Nsa)

x = np.arange(0, Na, int(Na / Na0))
y = np.arange(0, Nr, int(Nr / Nr0))

Sr[x, :] = 0
Sr[:, y] = 0


Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)

# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD, with arate: ' + \
    str(round(srate_a, 4)) + ", rrate: " + str(round(srate_r, 4))
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)
