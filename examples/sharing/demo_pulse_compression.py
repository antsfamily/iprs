#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt

from iprs.utils.const import *
from iprs.dsp.fft import fft, ifft, fftfreq

mftdmod = 'conv'
mffdmod = 'way2'
ftshift = True

# ===Generate tansmit= ted and recieved signals
# ---Setting parameters
R = [1.e3, 2.e3, 3.e3]
A = [0.5, 1.0, 0.8]

EPS = 2.2e-32
K = 4.1e+11
Tp = 37.0e-06
B = np.abs(K) * Tp

alp = 1.24588  # 1.1-1.4
Fs = alp * B
Fc = 5.3e9
Fc = 0.

Koff = 0.
# Koff = 1.e10
Fcoff = 0.
# Fcoff = 1.e8

Ts = 2.1 * Tp
Ns = round(Fs * Ts)
Nh = round(Fs * Tp)
t = np.linspace(-Ts / 2., Ts / 2, Ns)
f = fftfreq(Fs, Ns, shift=ftshift)

N = Ns + Nh - 1
Nfft = 2**iprs.nextpow2(N)

# ---Transmitted signal
St = iprs.chirp_tran(t, Tp, K, Fc, A=1.)

# ---Recieved signal
Sr = 0.
for r, a in zip(R, A):
    tau = 2. * r / C
    Sr += iprs.chirp_recv(t, tau, Tp, K, Fc, A=a)

# ---Frequency domain
Yt = fft(St, axis=0, shift=ftshift)
Yr = fft(Sr, axis=0, shift=ftshift)

# ---Plot signals
plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.plot(t * 1e6, np.real(St))
plt.grid()
plt.title('Real part')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1e6, np.imag(St))
plt.grid()
plt.title('Imaginary part')
plt.xlabel(r'Time/$\mu s$')
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

print(np.sum(t), np.sum(St), np.sum(f))


plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.plot(t * 1e6, np.real(Sr))
plt.grid()
plt.title('Real part')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1e6, np.imag(Sr))
plt.grid()
plt.title('Imaginary part')
plt.xlabel(r'Time/$\mu s$')
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
plt.ylabel('Phase/rad')
plt.subplots_adjust(left=0.08, bottom=0.06, right=0.98, top=0.96, wspace=0.19, hspace=0.25)

plt.show()


# ===Matched filtering/Pulse compression in time domain

# ---Matched filtering in time domain
Sm, tm = iprs.chirp_mf_td(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Ns=None, mod=mftdmod)

if mftdmod in ['conv', 'Conv']:
    # S1 = np.convolve(Sr, Sm, mode='same')
    # S1 = iprs.conv1(Sr, Sm, shape='same')
    S1 = iprs.fftconv1(Sr, Sm, shape='same')

if mftdmod in ['corr', 'Corr']:
    # S1 = np.correlate(Sr, Sm, mode='same')
    # S1 = iprs.corr1(Sr, Sm, shape='same')
    S1 = iprs.fftcorr1(Sr, Sm, shape='same')

# ===Matched filtering/Pulse compression in frequency domain

# ---Matched filter in frequency domain
# ~~~Method 1-4
H, f = iprs.chirp_mf_fd(K + Koff, Tp, Fs, Fc=Fc + Fcoff, Nfft=Nfft,
                        mod=mffdmod, win=None, ftshift=ftshift)

print(H.shape, t.shape, Sm.shape, "=======")

# ---Tansform the recieved signal to frequency domain
Yr = fft(iprs.padfft(Sr, Nfft, 0, ftshift), Nfft, axis=0, shift=ftshift)

# ---Matched filtering/Pulse compression
Y = Yr * H

# ---Tansform back to time domain
S2 = ifft(Y, Nfft, axis=0, shift=ftshift)

S2 = iprs.mfpc_throwaway(S2, Ns, Nh, 0, mffdmod, ftshift)


print(np.sum(np.abs(S1 - S2)))
print(np.sum(np.abs(S1 - S2)))
print(np.argmax(np.abs(S1)), np.argmax(np.abs(S2)))


plt.figure(figsize=(12, 8))
plt.subplot(421)
plt.plot(t * 1e6, np.real(St))
plt.plot(t * 1e6, np.abs(St))
plt.grid()
plt.legend(('Real part', 'Amplitude'))
plt.title('Transmitted')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(422)
plt.plot(t * 1e6, np.real(Sr))
plt.plot(t * 1e6, np.abs(Sr))
plt.grid()
plt.legend(('Real part', 'Amplitude'))
plt.title('Recieved')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(423)
plt.plot(tm * 1e6, np.real(Sm))
plt.plot(tm * 1e6, np.abs(Sm))
plt.grid()
plt.legend(('Real part', 'Amplitude'))
plt.title('Filter (time domain)')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(424)
plt.plot(f, np.real(H))
plt.plot(f, np.abs(H))
plt.grid()
plt.legend(('Real part', 'Amplitude'))
plt.title('Filter (frequency domain,' + mffdmod + ')')
plt.xlabel('Frequency/Hz')
plt.ylabel('Amplitude')
plt.subplot(425)
plt.plot(t * 1e6, np.abs(S1))
plt.grid()
plt.title('Matched filtered with time domain filter')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(426)
plt.plot(t * 1e6, np.abs(S2))
plt.grid()
plt.title('Matched filtered with frequency domain filter')
plt.xlabel(r'Time/$\mu s$')
plt.ylabel('Amplitude')
plt.subplot(427)
plt.plot(t * 1e6, np.angle(S1))
plt.grid()
plt.title('Matched filtered with time domain filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplot(428)
plt.plot(t * 1e6, np.angle(S2))
plt.grid()
plt.title('Matched filtered with frequency domain filter')
plt.xlabel(r'Time/${\mu s}$')
plt.ylabel('Phase/rad')
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.99, top=0.96, wspace=0.14, hspace=0.40)
plt.show()
