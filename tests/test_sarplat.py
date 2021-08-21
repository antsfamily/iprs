#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 16:10:05
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from iprs.sarcfg.sensors import SENSORS
from iprs.sarcfg.acquis import ACQUISITION
from iprs.sarcfg.sarplat import *

sarplat = SarPlat()
# print(SR)
sarplat.name = 'DIY4'
sarplat.sensor = SENSORS[sarplat.name]
sarplat.acquisition = ACQUISITION['DIY4']
sarplat.params = None

sarplat.printsp()


# sarplat = SarPlat()
# # print(SR)
# sarplat.name = 'RADARSAT1'
# sarplat.sensor = SENSORS[sarplat.name]
# sarplat.acquisition = ACQUISITION['DIY4']
# sarplat.params = None

# sarplat.printsp()


# sarplat = SarPlat()
# # print(SR)
# sarplat.name = 'RADARSAT2'
# sarplat.sensor = SENSORS[sarplat.name]
# sarplat.acquisition = ACQUISITION['DIY4']
# sarplat.params = None

# sarplat.printsp()
