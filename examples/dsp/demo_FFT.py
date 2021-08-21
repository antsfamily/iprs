#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np


a = 1 + 2j
b = 3 + 4j
print(a * b)

rl = np.array([1, 2, 3, 4, 5, 6, 7, 8])
im = np.array([4, 5, 7, 8, 6, 1, 2, 3])

x = rl + 1j * im
z = rl + 1 + 1j * (im + 1)

print(x * z)

print(x.shape)
print(x)
print(np.fft.fftshift(x, axes=0))
print(np.fft.ifftshift(x, axes=0))

y = np.fft.fft(x)

y = iprs.fft(x, axis=0, shift=True)

y = iprs.ifft(x, axis=0, shift=True)
print(y)

y = np.fft.fftshift(np.fft.fft(np.fft.fftshift(x, axes=0), axis=0), axes=0)

print(y)


X = np.zeros((4, 8), dtype='complex128')
X[0] = x
X[1] = x + 1 + 1j
X[2] = x + 2 + 2j
X[3] = x + 3 + 3j

print("-------------")
print(X)

print(iprs.ifft(X, axis=1, shift=True))
