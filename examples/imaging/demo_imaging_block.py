#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 09:55:34
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs

datafile = '/mnt/d/DataSets/zhi/SAR/geometry/disc/sensor=DIY4_acquisition=DIY4_640x640_disc6.pkl'

sardata, sarplat = iprs.load_data(datafile, way=0, which='all')

sarplat.printsp()

iprs.show_amplitude_phase(sardata.image[0])


sardata, sarplat = iprs.getblk(sardata, sarplat)
