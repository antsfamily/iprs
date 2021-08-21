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

Nx, Nh = (5, 3)
Nx, Nh = (5, 8)
Nx, Nh = (8, 5)
Nx, Nh = (8, 4)
Nx, Nh = (8, 8)
Nx, Nh = (9, 9)

Nfft = Nx + Nh - 1
# Nfft = None  # 2^nextpow2(Nx + Nh - 1)

x = np.random.rand((Nx)) + 1j * np.random.rand((Nx))
h = np.random.rand((Nh)) + 1j * np.random.rand((Nh))

print(x)
print(h)
print('---------------------------')
# np.convolve gives wrong results, matlab's conv1 gives correct results.

# y1 = np.convolve(x, h, mode='same')
y1 = iprs.conv1(x, h, shape='full')
y2 = iprs.fftconv1(x, h, axis=0, Nfft=Nfft, shape='full', ftshift=ftshift)

print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))

# y1 = np.convolve(x, h, mode='valid')
y1 = iprs.conv1(x, h, shape='valid')
y2 = iprs.fftconv1(x, h, axis=0, Nfft=Nfft, shape='valid', ftshift=ftshift)
print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))

# y1 = np.convolve(x, h, mode='full')
y1 = iprs.conv1(x, h, shape='full')
y2 = iprs.fftconv1(x, h, axis=0, Nfft=Nfft, shape='full', ftshift=ftshift)
print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))
