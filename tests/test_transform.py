#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 20:18:44
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
import matplotlib.pyplot as plt
from iprs.dsp import transform as tsfm

f0 = 1000  # frequency
phi0 = np.pi / 2

T = 1.0 / f0

TL = 4 * T
Fs = 20 * f0
Ns = int(TL * Fs)
t = np.linspace(0, TL, Ns)

s = np.sin(2 * np.pi * f0 * t + phi0)
y = tsfm.fft(s)
# print(y)
# f = tsfm.freq(Ns, Fs)
f = tsfm.freq(Ns, Fs)
print(f)
plt.figure
plt.subplot(121)
plt.plot(t, s)
plt.title('Original sig')
plt.subplot(122)
plt.plot(f, abs(y))
plt.title('fft of s')
plt.show()
