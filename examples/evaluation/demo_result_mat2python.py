#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import scipy.io as scio


origfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006.pkl'


sardata, sarplat = iprs.sarread(origfile)

reconfile = '/home/liu/Desktop/Data/ws/reco.mat'
reconfile = '/mnt/d/ws/Matlab/Chapter3/alpha0.mat'
data = scio.loadmat(reconfile, struct_as_record=True)

reco = data['alpha']


isimgadj = True
figsize = (6, 5)


# axismod = 'Image'
axismod = 'SceneAbsolute'
# axismod = 'SceneRelative'
title = 'CSSAR'
# iprs.show_sarimage(reco, sarplat, cmap='gray')
iprs.show_sarimage(reco, sarplat, axismod=axismod, title=title, cmap='gray', isimgadj=isimgadj, figsize=figsize)
