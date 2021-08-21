#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-08-05 17:39:38
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $Id$

import sys
import iprs
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt


sensor_name = 'DIY8'
acquis_name = 'DIY8'

sarplat8 = iprs.SarPlat()
sarplat8.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat8.sensor = iprs.SENSORS[sensor_name]
sarplat8.acquisition = iprs.ACQUISITION[acquis_name]
sarplat8.params = None
sarplat8.printsp()


A = iprs.sarmodel(sarplat8, model='1Da', nmod=None)

print(A.shape)
