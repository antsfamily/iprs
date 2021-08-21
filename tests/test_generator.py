#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 03:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs


sensor_name = 'DIY'
acquis_name = 'DIY3'

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


Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets)

print(Sr)


# visualize
iprs.show_amplitude_phase(Sr)
