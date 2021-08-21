#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-23 19:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
import logging
from iprs.dsp.fft import fft, ifft, fftfreq, padfft
from iprs.utils.const import *
from iprs.misc.mathops import nextpow2
from iprs.dsp.normalsignals import rect
import matplotlib.pyplot as plt


def chirp_mf_td(K, Tp, Fs, Fc=0., Ns=None, mod='conv'):

    tc = -Fc / K
    if Ns is None:
        t = np.linspace(-Tp / 2., Tp / 2., round(Fs * Tp))
    else:
        Ts = Ns / Fs
        t = np.linspace(-Ts / 2., Ts / 2., Ns)

    if mod in ['conv', 'Conv']:
        # mf = rect(t / Tp) * np.exp(-1j * PI * K * (-t - tc)**2)
        mf = rect(t / Tp) * np.exp(2j * PI * Fc * t - 1j * PI * K * t**2)
        # mf = rect(t / Tp) * ne.evaluate('exp(2j * PI * Fc * t - 1j * PI * K * (t**2))')
    if mod in ['corr', 'Corr']:
        # mf = rect(t / Tp) * np.exp(1j * PI * K * (t - tc)**2)
        mf = rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * K * t**2)
        # mf = rect(t / Tp) * ne.evaluate('exp(2j * PI * Fc * t + 1j * PI * K * (t**2))')

    return mf, t


def chirp_mf_fd(K, Tp, Fs, Fc=0., Nfft=None, mod='way1', win=None, ftshift=False):

    Nh = round(Fs * Tp)
    if Nfft is None:
        Nfft = 2 ** nextpow2(Nh)
    t = np.linspace(-Tp / 2., Tp / 2., Nh)
    # t = np.linspace(-Ts / 2., Ts / 2., Nfft)
    f = fftfreq(Fs, Nfft, ftshift, norm=False)

    if mod in ['way1', 'Way1', 'WAY1']:
        mf = rect(t / Tp) * np.exp(2j * PI * Fc * t - 1j * PI * K * t**2)
        mf = padfft(mf, Nfft, 0, ftshift)
        mf = fft(mf, Nfft, axis=0, shift=ftshift)

    if mod in ['way2', 'Way2', 'WAY2']:
        mf = rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * K * t**2)
        mf = padfft(mf, Nfft, 0, ftshift)
        mf = fft(mf, Nfft, axis=0, shift=ftshift)
        mf = np.conj(mf)

    if mod in ['way3', 'Way3', 'WAY3']:
        mf = rect(f / (K * Tp)) * np.exp(1j * PI * f**2 / K)

    if mod in ['way4', 'Way4', 'WAY4']:
        mf = np.exp(1j * PI * f**2 / K)
        # mf = np.exp(1j * PI * (f + Fc)**2 / K)

    if win is not None:
        mf = mf * win(Nfft)

    return mf, f


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    Kr = 4.1e+11
    Tp = 37.0e-06
    Br = np.abs(Kr) * Tp

    alpha = 1.24588  # 1.1-1.4
    Fsr = alpha * Br
    Fc = 5.3e9
    # Fc = 0.

    Tsr = 2.1 * Tp
    Nsr = int(Fsr * Tsr)
    tr = np.linspace(-Tsr / 2., Tsr / 2., Nsr)
    fr = np.linspace(-Fsr / 2., Fsr / 2., Nsr)
    t = np.linspace(-Tsr / 2., Tsr / 2., Nsr)

    Sm1, t = chirp_mf_td(Kr, Tp, Fsr, Fc=Fc, N=Nsr, mod='conv')
    Sm2, t = chirp_mf_td(Kr, Tp, Fsr, Fc=Fc, N=Nsr, mod='corr')

    f = np.linspace(-Fsr / 2., Fsr / 2., len(Sm1))
    Ym1 = fft(Sm1, axis=0, shift=True)

    f = np.linspace(-Fsr / 2., Fsr / 2., len(Sm2))
    Ym2 = fft(Sm2, axis=0, shift=True)

    plt.figure(1)
    plt.subplot(221)
    plt.plot(t * 1e6, np.real(Sm1))
    plt.plot(t * 1e6, np.abs(Sm1))
    plt.grid()
    plt.legend(['Real part', 'Amplitude'])
    plt.title('Convolution matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, np.imag(Sm1))
    plt.plot(t * 1e6, np.abs(Sm1))
    plt.grid()
    plt.legend(['Imaginary part', 'Amplitude'])
    plt.title('Convolution matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, np.abs(Ym1))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, np.angle(Ym1))
    plt.grid()

    plt.figure(2)
    plt.subplot(221)
    plt.plot(t * 1e6, np.real(Sm2))
    plt.plot(t * 1e6, np.abs(Sm2))
    plt.grid()
    plt.legend(['Real part', 'Amplitude'])
    plt.title('Correlation matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(222)
    plt.plot(t * 1e6, np.imag(Sm2))
    plt.plot(t * 1e6, np.abs(Sm2))
    plt.grid()
    plt.legend(['Imaginary part', 'Amplitude'])
    plt.title('Correlation matched filter')
    plt.xlabel(r'Time/$\mu s$')
    plt.ylabel('Amplitude')
    plt.subplot(223)
    plt.plot(f, np.abs(Ym2))
    plt.grid()
    plt.subplot(224)
    plt.plot(f, np.angle(Ym2))
    plt.grid()
    plt.show()
