#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.fft import fft, fftshift, ifftshift

from iprs.utils.const import *
import logging

from iprs.dsp.normalsignals import rect


def sar_tran(t, Tp, Kr, Fc, A=1.):

    return A * rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * Kr * t**2)


def sar_recv(t, tau, Tp, Kr, Fc, A=1.):

    t = t - tau
    return A * rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * Kr * t**2)


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    Kr = 4.1e+11
    Tp = 37.0e-06
    Br = abs(Kr) * Tp

    alpha = 1.24588  # 1.1-1.4
    Fsr = alpha * Br
    # Fc = 5.3e9
    Fc = 0.

    Tsr = 1.1 * Tp
    Nsr = int(Fsr * Tsr)
    t = np.linspace(-Tsr / 2., Tsr / 2, Nsr)
    f = np.linspace(-Fsr / 2., Fsr / 2, Nsr)

    St = sar_tran(t, Tp, Kr, Fc)

    Yt = fftshift(fft(fftshift(St, axes=0), axis=0), axes=0)

    plt.figure(1)
    plt.subplot(221)
    plt.plot(t * 1e6, np.real(St))
    plt.plot(t * 1e6, np.abs(St))
    plt.grid()
    plt.legend({'Real part', 'Amplitude'})
    plt.title('Matched filter')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, np.angle(St))
    plt.grid()
    plt.subplot(223)
    plt.plot(f, np.abs(Yt))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, np.angle(Yt))
    plt.grid()
    plt.show()
