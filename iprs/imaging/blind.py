#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 21:08:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.fft import *
from iprs.utils.const import *
import matplotlib.pyplot as plt


def blindsar_svd(Sr, verbose=False):
    Na, Nr = Sr.shape
    U, S, Vh = np.linalg.svd(Sr, full_matrices=True, compute_uv=True)

    print(U.shape, S.shape, Vh.shape, "====")

    print(U[:, 0], S, Vh[:, 0])

    V = np.conj(Vh).transpose()

    aRef = U[:, 0]
    rRef = V[:, 0]

    plt.figure()
    plt.subplot(221)
    plt.plot(np.real(aRef))
    plt.subplot(222)
    plt.plot(np.real(rRef))

    S = np.fft.fft2(Sr)
    # aRef = np.fft.fft(aRef)
    aRef = fftshift(np.fft.fft(fftshift(aRef)))
    plt.subplot(223)
    plt.plot(np.real(aRef))
    aRef = np.repeat(aRef, Nr).reshape(Na, Nr)

    # rRef = np.fft.fft(rRef)
    rRef = fftshift(np.fft.fft(fftshift(rRef)))
    plt.subplot(224)
    plt.plot(np.real(rRef))
    rRef = np.repeat(rRef, Na).reshape(Nr, Na).transpose()
    print(rRef.shape, aRef.shape)
    plt.show()

    Sr = fftshift(fft(fftshift(Sr, axes=1), axis=1), axes=1)
    Sr = Sr * rRef
    Sr = ifftshift(ifft(ifftshift(Sr, axes=1), axis=1), axes=1)

    Sr = fftshift(fft(fftshift(Sr, axes=0), axis=0), axes=0)
    Sr = Sr * aRef
    SI = ifftshift(ifft(ifftshift(Sr, axes=0), axis=0), axes=0)

    return SI


if __name__ == '__main__':

    Sr = np.random.randn(128, 256)
    SI = blindsar_svd(Sr)

    print(SI.shape, SI.dtype)
