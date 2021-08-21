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

rootfilename = 'ALPSRP020160970'
# rootfilename = 'ALPSRP050500980'
# rootfilename = 'ALPSRP115120970'


level = 'L1.0'
rootfolder = rootfilename
filefolder = rootfilename + '-' + level
filename = 'IMG-HH-' + rootfilename + '-H1'
ext = '.0__A'

filepath = disk + 'DataSets/sar/ALOSPALSAR/data/' + rootfolder + '/' + filefolder + '/' + filename + ext

D = copy.deepcopy(iprs.LeaderFileImportantImagingParametersRecordALOS)

iprs.readrcd(filepath, iprs.decfmtfceos, D, offset=0, endian='>')

iprs.printrcd(D)
