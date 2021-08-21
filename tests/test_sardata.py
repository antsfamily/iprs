#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 23:40:56
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import h5py
import iprs
import numpy as np


pklfile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.pkl'
matfile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.mat'
hf5file = '../data/sar/sensor=DIY4_acquisition=DIY4_point.hdf5'

pklfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006.pkl'
matfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006.mat'
hf5file = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_MiniSAR20050524p0002image006.hd5'

sardata, sarplat = iprs.sarread(pklfile)
iprs.show_amplitude_phase(sardata.image)
image0 = sardata.image

sardata.store(sarplat, hf5file)

iprs.sarstore(sardata, sarplat, matfile)
sardata, sarplat = iprs.sarread(matfile)

image1 = sardata.image

image0 = sardata.image
print(np.sum(np.sum(image0-image1)))

iprs.show_amplitude_phase(sardata.image)
iprs.show_amplitude_phase(sardata.rawdata)
