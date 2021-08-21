#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt


ftshift = True
eps = None

# == =Generate tansmitted and recieved signals
# ---Setting parameters
R = [1.e3, 2.e3, 3.e3]
A = [0.5, 1.0, 0.8]

C = 299792458.0
PI = np.pi
K = 4.1e+11
Tp = 37.e-06
B = np.abs(K) * Tp

alp = 1.24588
# 1.1 - 1.4
Fs = alp * B
# Fc = 5.3e9
Fc = 0.

Fsoff = 1e6
Fsoff = 0.
# Tpoff = 2.e-5
Tpoff = 0.
Koff = 1e10
Koff = 0.
Fcoff = 1e8
Fcoff = 0.

Ts = 2.1 * Tp
Ns = round(Fs * Ts)
Nh = round(Fs * Tp)
N = Ns + Nh - 1
Nfft = 2**iprs.nextpow2(N)

t = np.linspace(-Ts / 2., Ts / 2, Ns)
f = iprs.fftfreq(Fs, Ns, ftshift, 0)

# ---Transmitted signal
St = iprs.chirp_tran(t, Tp, K, Fc, 1.)

# ---Recieved signal
Sr = 0.
nTGs = len(R)
for n in range(nTGs):
    tau = 2. * R[n] / C
    Sr = Sr + iprs.chirp_recv(t, tau, Tp, K, Fc, A[n])

# Hc = exp(-2j * PI * Fc * t)
# Sr = Sr .* Hc

# ---Frequency domain
Yt = iprs.fft(St, n=None, axis=0, norm=None, shift=ftshift)
Yr = iprs.fft(Sr, n=None, axis=0, norm=None, shift=ftshift)

# Yt = chirp_spectrum(f, Tp, K, Fc, A)

# == =Matched filtering / Pulse compression in time domain

# ---Matched filtering in time domain
Sm1, tm1 = iprs.chirp_mf_td(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Ns=None, mod='conv')
S1 = iprs.fftconv1(Sr, Sm1, shape='same', axis=0, Nfft=Nfft, ftshift=ftshift, eps=None)

Sm2, tm2 = iprs.chirp_mf_td(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Ns=None, mod='corr')
S2 = iprs.fftcorr1(Sr, Sm2, shape='same', axis=0, Nfft=Nfft, ftshift=ftshift, eps=None)


plt.figure(1)
plt.subplot(341)
plt.plot(t * 1e6, np.real(St))
plt.plot(t * 1e6, np.abs(St))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Transmitted chirp')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(342)
plt.plot(t * 1e6, np.angle(St))
plt.grid()
plt.title('Transmitted chirp')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(343)
plt.plot(t * 1e6, np.real(Sr))
plt.plot(t * 1e6, np.abs(Sr))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Recieved chirp')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(344)
plt.plot(t * 1e6, np.angle(Sr))
plt.grid()
plt.title('Recieved chirp')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(345)
plt.plot(tm1 * 1e6, np.real(Sm1))
plt.plot(tm1 * 1e6, np.abs(Sm1))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Convolution filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(346)
plt.plot(tm1 * 1e6, np.angle(Sm1))
plt.grid()
plt.title('Convolution filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(347)
plt.plot(tm2 * 1e6, np.real(Sm2))
plt.plot(tm2 * 1e6, np.abs(Sm2))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Correlation filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(348)
plt.plot(tm2 * 1e6, np.angle(Sm2))
plt.grid()
plt.title('Correlation filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(349)
plt.plot(t * 1e6, np.abs(S1))
plt.grid()
plt.title('Filtered with convolution filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(3, 4, 10)
plt.plot(t * 1e6, np.angle(S1))
plt.grid()
plt.title('Filtered with convolution filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(3, 4, 11)
plt.plot(t * 1e6, np.abs(S2))
plt.grid()
plt.title('Filtered with correlation filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Amplitude')
plt.subplot(3, 4, 12)
plt.plot(t * 1e6, np.angle(S2))
plt.grid()
plt.title('Filtered with correlation filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.99, top=0.96, wspace=0.14, hspace=0.40)
plt.show()
