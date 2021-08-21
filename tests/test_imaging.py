#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs

sensor_name = 'DIY3'
acquis_name = 'DIY4'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

targets = [
    [100, 100, 0, 0, 0, 0, 0.3],
    [0, 0, 0, 0, 0, 0, 0.9],
    [150, 100, 0, 0, 0, 0, 0.5],
    [200, 100, 0, 0, 0, 0, 0.6],
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
iprs.show_sarimage(Sr_img, sarplat, axismod=axismod, title=title, aspect=None)

# exit()

# Sr_img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)

# # axismod = 'Image'
# # axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
# title = 'Reconstructed Image using omega-k'
# iprs.show_sarimage(Sr_img, sarplat, axismod=axismod, title=title, aspect=None)


Sr_img = iprs.chirp_scaling(Sr, sarplat, verbose=True)

# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using chirp scaling'
iprs.show_sarimage(Sr_img, sarplat, axismod=axismod, title=title, aspect=None)
