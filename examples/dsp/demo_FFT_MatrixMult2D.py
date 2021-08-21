#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt

X = iprs.imread('../../data/img/Lighthouse.png')
X = X[:, :, 0]
H, W = X.shape

ftshift = True

Y1 = iprs.fft(X, axis=0, shift=ftshift)
Y1 = iprs.fft(Y1, axis=1, shift=ftshift)

MH = iprs.fft(np.eye(H, H), axis=0, shift=ftshift)
MW = iprs.fft(np.eye(W, W), axis=1, shift=ftshift)

Y2 = np.matmul(MH, X)
Y2 = np.matmul(Y2, MW)

residual = np.abs(Y1 - Y2)


plt.figure(1)
plt.subplot(221)
plt.imshow(X)
plt.title('Orignal signal')
plt.colorbar()

plt.subplot(222)
plt.imshow(residual)
plt.title('Residual of 2D-FT results')
plt.colorbar()

plt.subplot(223)
plt.imshow(20 * np.log10(abs(Y1)))
plt.title('2D-FT results with matlab''s function fft')
plt.colorbar()
plt.subplot(224)
plt.imshow(20 * np.log10(abs(Y2)))
plt.title('2D-FT results with matrix multiplication')
plt.colorbar()
plt.show()
