#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 21:31:56
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def matnoise(mat, noise='wgn', PEAK=None, SNR=30):
    r"""add noise to an matrix

    Add noise to an matrix (real or complex)

    Arguments
    --------------------
    mat : {numpy array}
        can be real or complex valued

    Keyword Arguments
    --------------------
    noise : {string}
        type of noise (default: {'wgn'})
    SNR : {float number}
        Signal-to-noise ratio (default: {30})
    """
    print(mat.dtype)
    if mat.dtype in ('complex128', 'complex64', 'complex32', 'complex'):
        matreal = np.real(mat)
        matimag = np.imag(mat)
        if PEAK is None:
            imptempr = np.max(matreal.flatten())
            imptempi = np.max(matimag.flatten())
        else:
            imptempr, imptempi = PEAK
        matreal = awgn(
            matreal, SNR=SNR, PEAK=imptempr, pMode='db', measMode='measured')
        matimag = awgn(
            matimag, SNR=SNR, PEAK=imptempi, pMode='db', measMode='measured')
        mat = matreal + matimag * 1j
    else:
        if PEAK is None:
            PEAK = np.max(mat.flatten())
        mat = awgn(mat, SNR=SNR, PEAK=PEAK, pMode='db', measMode='measured')
    return mat


def imnoise(img, noise='wgn', SNR=30):
    """Add noise to image

    Add noise to image

    Parameters
    ----------
    img : {numpy ndarray}
        image aray
    noise : {string}, optional
        noise type (the default is 'wgn', which [default_description])
    SNR : {float number}, optional
        Signal-to-noise ratio (the default is 30, which [default_description])

    Returns
    -------
    {numpy array}
        Images with added noise.

    """
    if np.ndim(img) == 3:
        img = np.sum(img, axis=2)
    imgns = awgn(img, SNR, PEAK=255, pMode='db', measMode='measured')
    return imgns


def awgn(sig, SNR=30, PEAK=1, pMode='db', measMode='measured'):
    """AWGN Add white Gaussian noise to a signal.

    Y = AWGN(X,SNR) adds white Gaussian noise to X.  The SNR is in dB.
    The power of X is assumed to be 0 dBW.  If X is complex, then
    AWGN adds complex noise.

    Parameters
    ----------
    sig : {numpy array}
        Signal that will be noised.
    SNR : {float number}, optional
        Signal Noise Ratio (the default is 30)
    PEAK : {float number}, optional
        Peak value (the default is 1)
    pMode : {string}, optional
        [description] (the default is 'db')
    measMode : {string}, optional
        [description] (the default is 'measured', which [default_description])

    Returns
    -------
    {numpy array}
        noised data

    Raises
    ------
    IOError
        No input signal
    TypeError
        Input signal shape wrong
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
        sigPower = np.sum((np.abs(sig.flatten())) ** 2) / sig.size
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
        dtype = 'complex'
    else:
        dtype = 'real'

    y = sig + wgn(sig.shape, noisePower, PEAK, pMode, dtype)
    return y


def wgn(shape, p, PEAK=1, pMode='dbw', dtype='real', seed=None):
    """WGN Generate white Gaussian noise.

    Y = WGN((M,N),P) generates an M-by-N matrix of white Gaussian noise. P
    specifies the power of the output noise in dBW. The unit of measure for
    the output of the wgn function is Volts. For power calculations, it is
    assumed that there is a load of 1 Ohm.

    Parameters
    ----------
    shape : {tulpe}
        Shape of noising matrix
    p : {float number}
        P specifies the power of the output noise in dBW.
    PEAK : {float number}, optional
        Peak value (the default is 1)
    pMode : {string}, optional
        Power mode of the output noise (the default is 'dbw')
    dtype : {string}, optional
        data type, real or complex (the default is 'real', which means real-valued)
    seed : {integer}, optional
        Seed for random number generator. (the default is None, which means different each time)

    Returns
    -------
    numpy array
        Matrix of white Gaussian noise (real or complex).
    """

    # print(shape)
    if pMode is 'linear':
        noisePower = p
    elif pMode is 'dbw':
        noisePower = 10 ** (p / 10)
    elif pMode is 'dbm':
        noisePower = 10 ** ((p - 30) / 10)

    # --- Generate the noise
    if seed is not None:
        np.random.seed(seed)

    if dtype is 'complex':
        y = (np.sqrt(PEAK * noisePower / 2)) * \
            (_func(shape) + 1j * _func(shape))
    else:
        y = (np.sqrt(PEAK * noisePower)) * _func(shape)
    # print(y)
    return y


def _func(ab):
    if len(ab) == 1:
        n = np.random.randn(ab[0])
    else:
        n = np.random.randn(ab[0], ab[1])
    return n
