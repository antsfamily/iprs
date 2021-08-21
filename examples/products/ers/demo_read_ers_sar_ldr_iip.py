#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2019-11-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import copy
import iprs


disk = '/mnt/d/'
filename = 'E2_80406_STD_L0_F123'
# filename = 'E2_82446_STD_L0_F327'
# filename = 'E2_84690_STD_L0_F137'
# filename = 'E2_84686_STD_L0_F203'
# filename = 'E2_84699_STD_L0_F303'
# filename = 'E2_02558_STD_L0_F327'
# filepath = disk + 'DataSets/sar/ERS/data/' + filename + '/' + filename + '.000.ldr'
filepath = disk + 'DataSets/sar/ERS/data/' + filename + '/' + filename + '.000.ldr'

D = copy.deepcopy(iprs.LeaderFileImportantImagingParametersRecordERS)

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=0, endian='>')

iprs.printrcd(D)
