#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 23:40:56
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import scipy.io as scio

import iprs

pklfile = '/home/liu/Desktop/Data/ws/sci/radar/iprs/data/sar/sensor=DIY4_acquisition=DIY4_point.pkl'
matfile = '/home/liu/Desktop/Data/ws/sci/radar/iprs/data/sar/sensor=DIY4_acquisition=DIY4_point.mat'

sardata, sarplat = iprs.sarread(pklfile)
print(sardata, sarplat)

scio.savemat(matfile, {'sardata': sardata, 'sarplat': sarplat})

data = scio.loadmat(matfile)

print(data)
