#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

origfile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.mat'
recofile = 'D:/DataSets/zhi/sensor=DIY4_acquisition=DIY4_IMAGE_HH_SAR001_8bit.pkl'
orig_sardata, sarplat = iprs.load_data(datafile, way=0, which='all')
reco_sardata, sarplat = iprs.load_data(recofile, way=0, which='all')

amperror, phaerror = iprs.ampphaerror(orig_sardata, reco_sardata)
print("amperror: ", amperror, "phaerror: ", phaerror)
