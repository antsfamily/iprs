#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 21:31:56
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def imnoise(img, noise='wgn', SNR=30):
    if np.ndim(img) == 3:
        img = np.sum(img, axis=2)
    imgns = awgn(img, SNR, imp=255, pMode='db', measMode='measured')
    return imgns


def awgn(sig, SNR=30, imp=1, pMode='db', measMode='measured'):
    """AWGN Add white Gaussian noise to a signal.
    Y = AWGN(X,SNR) adds white Gaussian noise to X.  The SNR is in dB.
    The power of X is assumed to be 0 dBW.  If X is complex, then
    AWGN adds complex noise.
    """

    # --- Set default values
    sigPower = 0
    reqSNR = SNR
    # print(sig.shape)
    # --- sig
    if sig is None:
        raise IOError('NoInput')
    elif sig.ndim > 2:
        raise TypeError("The input signal must have 2 or fewer dimensions.")
    # --- Check the signal power.
    # This needs to consider power measurements on matrices
    if measMode is 'measured':
        sigPower = np.sum((np.abs(sig.flatten()))**2) / sig.size
        if pMode is 'db':
            sigPower = 10 * np.log10(sigPower)

    # print(sig.shape)
    # --- Compute the required noise power
    if pMode is 'linear':
        noisePower = sigPower / reqSNR
    elif pMode is 'db':
        noisePower = sigPower - reqSNR
        pMode = 'dbw'

    # --- Add the noise
    if (np.iscomplex(sig).any()):
        opType = 'complex'
    else:
        opType = 'real'

    y = sig + wgn(sig.shape, noisePower, imp, pMode, opType)
    return y


def wgn(rowscols, p, imp=1, pMode='dbw', opType='real', seed=None):
    """WGN Generate white Gaussian noise.
       Y = WGN(M,N,P) generates an M-by-N matrix of white Gaussian noise. P
       specifies the power of the output noise in dBW. The unit of measure for
       the output of the wgn function is Volts. For power calculations, it is
       assumed that there is a load of 1 Ohm.
    """
    # print(rowscols)
    if pMode is 'linear':
        noisePower = p
    elif pMode is 'dbw':
        noisePower = 10 ** (p / 10)
    elif pMode is 'dbm':
        noisePower = 10 ** ((p - 30) / 10)

    # --- Generate the noise
    if seed is not None:
        np.random.seed(seed)

    if opType is 'complex':
        y = (np.sqrt(imp * noisePower / 2)) * \
            (_func(rowscols) + 1j * _func(rowscols))
    else:
        y = (np.sqrt(imp * noisePower)) * _func(rowscols)
    # print(y)
    return y


def _func(ab):
    if len(ab) == 1:
        n = np.random.randn(ab[0])
    else:
        n = np.random.randn(ab[0], ab[1])
    return n
