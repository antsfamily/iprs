#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-13 23:39:36
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs


EXTS = [".jpg", ".jpeg", ".bmp", ".png"]

infolder = '/mnt/d/DataSets/zhi/SAR/MiniSAR/'

filelists = iprs.listxfile(listdir=infolder, exts=EXTS, issubdir=None)

print("number of files: ", len(filelists))
for file in filelists:
    print(file)
