#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-13 10:34:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
from scipy.misc import imread as scipyimread
from scipy.misc import imsave as scipyimsave


def imread(imgfile):
    return scipyimread(imgfile)


def imsave(outfile, img):
    return scipyimsave(img, outfile)
