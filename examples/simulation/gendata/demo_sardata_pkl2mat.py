#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import scipy.io as scio

pklfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_Tokyoradarsat001_8bit.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_Tokyoradarsat001_8bit.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_Tokyoradarsat004_8bit.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_Tokyoradarsat004_8bit.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_gaoxiong001.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_gaoxiong001.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_IMAGE_HH_SAR001_8bit.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_IMAGE_HH_SAR001_8bit.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/geometry/circle/sensor=DIY4_acquisition=DIY4_640x640_circle6.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/geometry/circle/sensor=DIY4_acquisition=DIY4_640x640_circle6.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/noisy/sensor=DIY4_acquisition=DIY4_center_disc_Scene0.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/noisy/sensor=DIY4_acquisition=DIY4_center_disc_Scene0.mat'

pklfile = '/mnt/d/DataSets/zhi/SAR/noisy/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006_noisy.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/noisy/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006_noisy.mat'



sardata, sarplat = iprs.sarread(pklfile)


iprs.sarstore(sardata, sarplat, matfile)

data = scio.loadmat(matfile, struct_as_record=True)

sardata = data['sardata']
sarplat = data['sarplat']

