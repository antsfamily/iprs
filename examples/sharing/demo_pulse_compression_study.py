#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

from numpy.fft import fft, fftshift, ifft, ifftshift

from iprs.utils.const import *

from iprs.dsp.normalsignals import rect

import matplotlib.pyplot as plt

# ===Generate tansmitted and recieved signals
# ---Setting parameters
R = [1.e3, 2.e3, 3.e3]
A = [0.5, 1.0, 0.8]

EPS = 2.2e-32
Kr = 4.1e+11
Tp = 37.0e-06
Br = np.abs(Kr) * Tp

alp = 1.24588  # 1.1-1.4
Fsr = alp * Br
Fc = 5.3e9
# Fc = 0.


Tsr = 2.1 * Tp
Nsr = int(Fsr * Tsr)
t = np.linspace(-Tsr / 2., Tsr / 2, Nsr)
f = np.linspace(-Fsr / 2., Fsr / 2, Nsr)
fr = np.linspace(-Fsr / 2., Fsr / 2, Nsr)
tc = -Fc / Kr

# ---Transmitted signal
St = rect(t / Tp) * np.exp(2j * PI * Fc * t + 1j * PI * Kr * t**2)

# ---Recieved signal
Sr = 0.
for r, a in zip(R, A):
    tau = 2. * r / C
    ttau = t - tau
    Sr += a * rect(ttau / Tp) * np.exp(2j * PI * Fc * ttau + 1j * PI * Kr * ttau ** 2)


# ---Frequency domain
Yt = fftshift(fft(fftshift(St, axes=0), axis=0), axes=0)
Yr = fftshift(fft(fftshift(Sr, axes=0), axis=0), axes=0)

# ---Plot signals
plt.figure(figsize=(10, 8))
plt.subplot(221)
plt.plot(t * 1000, np.real(St))
plt.grid()
plt.title('Real part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1000, np.imag(St))
plt.grid()
plt.title('Imaginary part')
plt.xlabel('Time/ms')
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
plt.plot(t * 1000, np.real(Sr))
plt.grid()
plt.title('Real part')
plt.xlabel('Time/ms')
plt.ylabel('Amplitude')
plt.subplot(222)
plt.plot(t * 1000, np.imag(Sr))
plt.grid()
plt.title('Imaginary part')
plt.xlabel('Time/ms')
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

# ===Matched filtering/Pulse compression in time domain

# ---Matched filtering signal
Sm = rect(t / Tp) * np.exp(-1j * PI * Kr * (-t - tc)**2)

# S1 = np.convolve(Sr, Sm, mode='same')
print(Fc, tc, Kr, Tp, "====]]]]")
print(t[0:10])
print(t[-10:-1])

N = len(Sr)
M = len(Sm)
K = int(np.floor(M / 2))
Ma = K
Mb = K
if np.mod(M, 2) == 0:
    Mb = K - 1
S1 = np.zeros((N), dtype='complex')
Sp = np.hstack((np.zeros((Mb)), Sr, np.zeros((Ma))))
for n in range(N):
    S1[n] = np.dot(Sp[n:n + M][::-1], Sm)

# ===Matched filtering/Pulse compression in frequency domain
# ---Tansform the recieved signal to frequency domain

Yr = fftshift(fft(fftshift(Sr, axes=0), axis=0), axes=0)
# Yr = fft(Sr, 1)
# Yr = fftshift(fft(fftshift(Sp, axes=0)), 1)

# ---Matched filter in frequency domain
# ~~~Method 1
H = fftshift(fft(fftshift(Sm, axes=0), axis=0), axes=0)
# ~~~Method 2
H = np.conj(fftshift(fft(fftshift(St, axes=0), axis=0), axes=0))
# ~~~Method 3
# H = rect((fr + Kr * tc) / Br) * np.exp(1j * PI * fr**2 / Kr)

# ---Matched filtering/Pulse compression
Y = Yr * H
# ---Tansform back to time domain
S2 = ifftshift(ifft(ifftshift(Y, axes=0), axis=0), axes=0)

plt.figure(figsize=(12, 8))
plt.subplot(321)
plt.plot(t * 1e6, np.real(St))
plt.plot(t * 1e6, np.abs(St))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Transmitted')
plt.xlabel('Time/μs')
plt.ylabel('Amplitude')
plt.subplot(322)
plt.plot(t * 1e6, np.real(Sr))
plt.plot(t * 1e6, np.abs(Sr))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Recieved')
plt.xlabel('Time/μs')
plt.ylabel('Amplitude')
plt.subplot(323)
plt.plot(t * 1e6, np.real(Sm))
plt.plot(t * 1e6, np.abs(Sm))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Filter (time domain)')
plt.xlabel('Time/μs')
plt.ylabel('Amplitude')
plt.subplot(324)
plt.plot(f, np.real(H))
plt.plot(f, np.abs(H))
plt.grid()
plt.legend({'Real part', 'Amplitude'})
plt.title('Filter (frequency domain)')
plt.xlabel('Frequency/Hz')
plt.ylabel('Amplitude')
plt.subplot(325)
plt.plot(t * 1e6, np.abs(S1))
plt.grid()
plt.title('Matched filtered with time domain filter')
plt.xlabel('Time/μs')
plt.ylabel('Amplitude')
plt.subplot(326)
plt.plot(t * 1e6, np.abs(S2))
plt.grid()
plt.title('Matched filtered with frequency domain filter')
plt.xlabel('Time/μs')
plt.ylabel('Amplitude')
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.99, top=0.96, wspace=0.14, hspace=0.40)
plt.show()
