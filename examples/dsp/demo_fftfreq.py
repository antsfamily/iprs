#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

ftshift = True
ftshift = False

Fs = 32.e6

N = 256


f1 = np.fft.fftfreq(N, 1. / Fs)

f2 = iprs.fftfreq(Fs, N, ftshift, norm=False)
# f2 = iprs.fftfreq(Fs, N, ftshift, norm=True)

print(f1)
print(f2)
