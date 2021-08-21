#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from scipy import signal

from iprs.utils.const import *
import logging
from iprs.misc import visual as vis
from iprs.dsp.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt


def eve_npts_fit(txyz, vxyz, t, isplot=False):
    npoints = len(txyz)
    vr = []
    for v in vxyz:
        vr.append(np.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]))

    coef = np.polyfit(txyz, vr, 1)

    vr = np.polyval(coef, t)

    return vr
