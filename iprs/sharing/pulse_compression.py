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
from iprs.dsp.convolution import cutfftconv1
from iprs.dsp.correlation import cutfftcorr1
from iprs.misc.mathops import nextpow2
from iprs.misc.arrayops import cut
from iprs.utils.const import *


def mfpc_throwaway(X, No, Nh, axis=0, mffdmod='way1', ftshift=False):
    r"""Throwaway invalid pulse compressed data

    Throwaway invalid pulse compressed data

    Parameters
    ----------
    X : {numpy.ndarray}
        Data after pulse compression.
    No : {number}
        Output size.
    Nh : {number}
        Filter size.
    axis : {number}, optional
        Throwaway dimension. (the default is 0)
    mffdmod : {str}, optional
        Frequency filter mode. (the default is 'way1')
    ftshift : {bool}, optional
        Whether to shift frequency (the default is False)
    """

    if axis is None:
        axis = 1
    if ftshift is None:
        ftshift = False

    Nfft = np.size(X, axis)
    Nfft, No, Nh = np.uint([Nfft, No, Nh])

    if No > Nfft:
        raise ValueError('Output size is bigger than input size!')
    elif No == Nfft:
        return X

    N = Nfft - No

    if ftshift:
        if mffdmod in ['way1', 'WAY1', 'Way1', 'way2', 'WAY2', 'Way2', 'way3', 'WAY3', 'Way3', 'way4', 'WAY4', 'Way4']:
            Nstart = np.uint(np.floor((N + 1) / 2.))
            Nend = np.uint(Nfft - (N - Nstart))
            X = cut(X, ((Nstart, Nend),), axis)
        else:
            raise ValueError('Unsupported frequency domain matched filter: ' + mfmod)

    else:
        if mffdmod in ['way1', 'WAY1', 'Way1']:
            Nstart = np.uint(np.fix(Nh / 2.))
            Nend = np.uint(Nstart + No)
            X = cut(X, ((Nstart, Nend),), axis)
        elif mffdmod in ['way2', 'WAY2', 'Way2']:
            Nend1 = Nfft
            Nstart1 = np.uint(Nend1 - (Nh - 1))
            X = cut(X, ((Nstart1, Nend1), (0, No)), axis)
            Nstart = np.uint(np.fix(Nh / 2.))
            Nend = np.uint(Nstart + No)
            X = cut(X, ((Nstart, Nend),), axis=axis)
        elif mffdmod in ['way3', 'WAY3', 'Way3']:
            Nstart = 0
            Nend = No
            X = cut(X, ((Nstart, Nend),), axis)
        elif mffdmod in ['way4', 'WAY4', 'Way4']:
            Nstart = 0
            Nend = No
            X = cut(X, ((Nstart, Nend),), axis)
        else:
            raise ValueError('Unsupported frequency domain matched filter: ' + mfmod)
    return X


if __name__ == '__main__':

    X = np.array(range(32))
    print(X, X.shape[0])

    No, Nh = (24, 7)
    X = mfpc_throwaway(X, No, Nh, axis=0, mffdmod='way1', ftshift=True)
    print(X)
