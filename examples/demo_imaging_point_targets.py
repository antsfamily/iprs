#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs

sensor_name = 'DIY4'
acquis_name = 'DIY4'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
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
    [200, 0, 0, 0, 0, 0, 1],
    [500, -500, 0, 0, 0, 0, 1],
]
print(targets)

Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets, verbose=False)

print(Sr.shape)
# visualize
iprs.show_amplitude_phase(Sr)

# do RD imaging
Sr_img, ta, tr = iprs.range_doppler(Sr, sarplat, verbose=False)
# iprs.show_img(img)


# Sr_img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=True)

axismod = 'Image'
# axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(Sr_img, sarplat, axismod=axismod, title=title, aspect=None)
