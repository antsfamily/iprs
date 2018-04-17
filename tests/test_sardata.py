#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 23:40:56
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


import iprs

pklfile = '/home/liu/Desktop/Data/ws/dlimaging/data/sensor=DIY4_acquisition=DIY4_640x640_circle6.pkl'
matfile = '/home/liu/Desktop/Data/ws/dlimaging/data/sensor=DIY4_acquisition=DIY4_640x640_circle6.mat'
# pklfile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.pkl'
# matfile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.mat'


sardata, sarplat = iprs.sarread(pklfile)

iprs.sarstore(sardata, sarplat, matfile)

sardata, sarplat = iprs.sarread(matfile)
# print(sardata, sarplat)
