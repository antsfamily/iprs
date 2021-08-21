#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 22:37:58
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
import numpy as np
from scipy.misc import imread
import matplotlib.pyplot as plt


from iprs.dsp import noise as ns

# ==============================sin signal=================
# generates signals
f0 = 1000  # frequency
phi0 = np.pi / 2

T = 1.0 / f0

TL = 4 * T
Fs = 20 * f0
Ns = int(TL * Fs)
t = np.linspace(0, TL, Ns)

s = np.sin(2 * np.pi * f0 * t + phi0)

# add white Gaussian noise
SNR1 = 30
SNR2 = 5
y1 = ns.awgn(s, SNR1)
y2 = ns.awgn(s, SNR2)

plt.figure
plt.plot(s, '-r')
plt.plot(y1, '-b')
plt.plot(y2, '-g')
plt.legend(("original", "SNR: " + str(SNR1), "SNR: " + str(SNR2)))
plt.title("add white Gaussian noise with diff SNR")
plt.show()


# ============================ image =================

# imgfilepath = '../data/fig/zhi&yan.png'
imgfilepath = '../data/fig/Lena.bmp'

img = imread(imgfilepath)
# img = img[:,:,0]
SNR = 20
# imgns = ns.awgn(img, SNR)
imgns = ns.imnoise(img, SNR=SNR)


plt.figure
plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.subplot(122)
plt.imshow(imgns, cmap='gray')
plt.title("add wgn with SNR: " + str(SNR) + "dB")
plt.show()


# ============================ sar signal=================
