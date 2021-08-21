#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2018-11-01 12:54:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import numpy as np
import copy
import iprs
import scipy.io as scio

useVGACPS = False
# useVGACPS = True

disk = '/mnt/d/'
filename = 'Vancouver'

filepath = disk + 'DataSets/sar/RADARSAT/frombooks/Vancouver/data/LEA_01.001'

endian = '>'

D = copy.deepcopy(iprs.SarDataFileFileDescriptorRecordRADARSAT)
# D = copy.deepcopy(iprs.SarDataFileSignalDataRecordRADARSAT)


LengthRecord = iprs.readrcd1item(filepath, iprs.decfmtfceos, fmt='1B4', offset=0, addr=(9, 12), endian='>')[0]
print(LengthRecord)

LengthRecord = iprs.readrcd1item(filepath, iprs.decfmtfceos, fmt='1B4', offset=720, addr=(9, 12), endian='>')[0]
print(LengthRecord)

SamplingRate = iprs.readrcd1item(filepath, iprs.decfmtfceos, fmt='1F16', offset=720, addr=(711, 726), endian='>')[0]
