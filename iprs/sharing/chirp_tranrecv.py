#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

import logging
from iprs.utils.const import *

from iprs.dsp.normalsignals import rect


def chirp_tran(t, Tp, K, Fc, A=1.):

    return A * rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * K * t**2)


def chirp_recv(t, tau, Tp, K, Fc, A=1.):

    t = t - tau
    return A * rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * K * t**2)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from numpy.fft import fft, fftshift, ifft, ifftshift


    # ===Generate tansmitted and recieved signals
    # ---Setting parameters
    R = [1.e3, 2.e3, 3.e3]
    A = [0.5, 1.0, 0.8]

    EPS = 2.2e-32
    K = 4.1e+11
    Tp = 37.0e-06
    Br = abs(K) * Tp

    alp = 1.24588  # 1.1-1.4
    Fsr = alp * Br
    Fc = 5.3e9
    Fc = 0.

    Tsr = 2.1 * Tp
    Nsr = int(Fsr * Tsr)
    t = np.linspace(-Tsr / 2., Tsr / 2, Nsr)
    f = np.linspace(-Fsr / 2., Fsr / 2, Nsr)

    # ---Transmitted signal
    St = chirp_tran(t, Tp, K, Fc, A=1.)

    # ---Recieved signal
    Sr = 0.
    for r, a in zip(R, A):
        tau = 2. * r / C
        Sr += chirp_recv(t, tau, Tp, K, Fc, A=a)

    # ---Frequency domain
    Yt = fftshift(fft(fftshift(St, axes=0), axis=0), axes=0)
    Yr = fftshift(fft(fftshift(Sr, axes=0), axis=0), axes=0)

    # ---Plot signals
    plt.figure(figsize=(10, 8))
    plt.subplot(221)
    plt.plot(t * 1e6, np.real(St))
    plt.grid()
    plt.title('Real part')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, np.imag(St))
    plt.grid()
    plt.title('Imaginary part')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, np.abs(Yt))
    plt.grid()
    plt.title('Spectrum')
    plt.xlabel('Frequency/Hz')
    plt.ylabel('Amplitude')
    plt.subplot(224)
    plt.plot(f, np.angle(Yt))
    plt.grid()
    plt.title('Spectrum')
    plt.xlabel('Frequency/Hz')
    plt.ylabel('Phase')
    plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

    plt.show()

    plt.figure(figsize=(10, 8))
    plt.subplot(221)
    plt.plot(t * 1e6, np.real(Sr))
    plt.grid()
    plt.title('Real part')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, np.imag(Sr))
    plt.grid()
    plt.title('Imaginary part')
    plt.xlabel('Time/μs')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, np.abs(Yr))
    plt.grid()
    plt.title('Spectrum')
    plt.xlabel('Frequency/Hz')
    plt.ylabel('Amplitude')
    plt.subplot(224)
    plt.plot(f, np.angle(Yr))
    plt.grid()
    plt.title('Spectrum')
    plt.xlabel('Frequency/Hz')
    plt.ylabel('Phase')
    plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

    plt.show()
