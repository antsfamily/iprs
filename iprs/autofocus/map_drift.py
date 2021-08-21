#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-25 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

import logging
from iprs.utils.const import *
from iprs.dsp.fft import fft, ifft
import matplotlib.pyplot as plt


def mda_sm(SI, Ka, Fsa, Nsar, fadr, Tpa, fadc, isplot=False):

    Na, Nr = SI.shape

    # ---Step 1: Fourier transform (azimuth)
    # SI = fft(SI, axis=0, shift=True)
    SI = np.abs(SI)

    Nc = int(Na / 2.)
    C = iprs.xcorr(A=SI[:Nc], B=SI[Nc:], shape='same', axis=0)
    # C = np.abs(C)
    # dtidx = np.argmax(C, axis=0)

    idx = np.linspace(0, Nc, Nc)
    fitC = C.copy()
    dtidx = np.zeros(Nr)
    for n in range(Nr):
        coef = np.polyfit(idx, C[:, n], 3)
        fitC[:, n] = np.polyval(coef, idx)
        dtidx[n] = np.argmax(fitC[:, n], axis=0)

    if isplot:
        plt.figure()
        plt.plot(np.abs(C[:, 0]), '-b')
        plt.plot(np.abs(C[:, int(Nr / 2)]), '-k')
        plt.plot(np.abs(C[:, Nr - 1]), '-g')
        plt.plot(np.abs(fitC[:, 0]), '-.b')
        plt.plot(np.abs(fitC[:, int(Nr / 2)]), '-.k')
        plt.plot(np.abs(fitC[:, Nr - 1]), '-.g')
        plt.legend(['range cell ' + str(0),
                    'range cell ' + str(int(Nr / 2)),
                    'range cell ' + str(Nr - 1)])
        plt.show()

    # ---Step 2:
    print("dtidx", dtidx)
    dt = (dtidx - Nc / 2.) / Fsa
    print("dt", dt)
    dKa = -fadr * fadr * dt / (Fsa / 2.)

    return fadr + dKa


if __name__ == '__main__':
    import iprs
    import scipy.io as scio

    cmap = 'gray'

    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/NoPGA_GlobalAZF.mat'
    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/NoPGA_RefineAZF.mat'
    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/Image_NoDopplerCorrection.mat'
    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/ers/data/Image_NoDopplerCorrection.mat'
    data = scio.loadmat(filename)

    SI = data['SI']
    SI = SI[:, :, 0] + 1j * SI[:, :, 1]

    # nlooks = (2, 1)
    # maxp = 1e5
    # N1, N2 = (3000, 3000)
    # SI = SI[N1:N1 + 1024, N2:N2 + 1024]
    # SI = SI[N1:N1 + 4096, N2:N2 + 2048]
    nlooks = (4, 1)
    maxp = 1e4
    N1, N2 = (0, 0)
    # N1, N2 = (2048, 1024)
    SI = SI[N1:N1 + 4096, N2:N2 + 2048]
    # SI = SI[N1:N1 + 8192, N2:N2 + 4096]
    X = SI.copy()
    Na, Nr = SI.shape
    print(Na, Nr)

    # Nsar, H, BWa, Lsar = (6976, 691500., 0.0234996122966, 22983.1697693)
    Nsar, H, BWa, Lsar, Ka = (1159, 780000., 0.0050116248639, 4832.8353993, -2032.125161)
    Nsub = iprs.spotlight_width(H, BWa, Lsar)
    Nsub = int(Nsub / 4.45)
    Nsub = None

    X = iprs.mda_sm(SI, Ka, None, Nsar, isplot=True)
