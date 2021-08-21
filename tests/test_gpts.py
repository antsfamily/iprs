#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-23 17:44:16
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $Id$

import iprs


sensor_name = 'DIY4'
acquis_name = 'DIY4'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.params = None
sarplat.printsp()

SA = sarplat.acquisition['SceneArea']

nTGs = 3
seed = 2018
print("=========++++++++================")
targets = iprs.gpts(SA, nTGs, seed=seed, verbose=True)

print("=================================")
print(targets)

Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets)

print(Sr)


# visualize
iprs.show_amplitude_phase(Sr)


Sr_img, ta, tr = iprs.rda(Sr, sarplat, verbose=False)

# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)
