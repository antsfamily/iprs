#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-05 16:36:03
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np
from iprs.dsp.fft import fft, ifft, padfft
from iprs.misc.mathops import nextpow2
from iprs.misc.arrayops import cut


def conv1(f, g, shape='same'):
    r"""Convolution

    The convoltuion between f and g can be expressed as

    .. math::
       \begin{aligned}
       (f*g)[n] &= \sum_{m=-\infty}^{+\infty}f[m]g[n-m] \\
                &= \sum_{m=-\infty}^{+\infty}f[n-m]g[m]
       \end{aligned}
       :label: equ-1DConvDiscrete

    Parameters
    ----------
    f : {numpy array}
        data to be filtered
    g : {numpy array}
        convolution kernel
    shape : {str}, optional
        - 'full': returns the full convolution,
        - 'same': returns the central part of the convolution
                that is the same size as x (default).
        - 'valid': returns only those parts of the convolution
                that are computed without the zero-padded edges.
                LENGTH(y)is MAX(LENGTH(x)-MAX(0,LENGTH(g)-1),0).
    """

    Nf = len(f)
    Ng = len(g)
    N = Nf + Ng - 1

    f = np.hstack((np.zeros((Ng - 1)), f, np.zeros((Ng - 1))))
    g = g[::-1]
    y = []
    for n in range(N):
        y.append(np.dot(f[n:n + Ng], g))

    if shape in ['same', 'Same', 'SAME']:
        Ns = np.fix(Ng / 2.)
        Ne = Ns + Nf
    if shape in ['valid', 'Valid', 'VALID']:
        Ns = Ng - 1
        Ne = Ns + Nf - Ng + 1
    if shape in ['full', 'Full', 'FULL']:
        Ns = 0
        Ne = N
    Ns, Ne = np.int32([Ns, Ne])
    return np.array(y[Ns:Ne])


def cutfftconv1(y, Nfft, Nx, Nh, shape='same', axis=0, ftshift=False):
    r"""Throwaway boundary elements to get convolution results.

    Throwaway boundary elements to get convolution results.

    Parameters
    ----------
    y : {numpy.ndarray}
        array after ``iff``.
    Nfft : {number}
        number of fft points.
    Nx : {number}
        signal length
    Nh : {number}
        filter length
    shape : {str}
        output shape:
        1. ``'same' --> same size as input x``, :math:`N_x`
        2. ``'valid' --> valid convolution output``
        3. ``'full' --> full convolution output``, :math:`N_x+N_h-1`
        (the default is 'same')
    axis : {number}
        convolution axis (the default is 0)
    ftshift : {[type]}
        whether to shift the frequencies (the default is False)

    Returns
    -------
    y : {numpy.ndarray}
        array with shape specified by :attr:`same`.
    """

    Nfft, Nx, Nh = np.int32([Nfft, Nx, Nh])
    N = Nx + Nh - 1
    Nextra = Nfft - N

    if ftshift:
        if np.mod(Nx, 2) > 0 and np.mod(Nh, 2) > 0:
            if Nextra > 0:
                Nhead = np.int32(np.fix((Nextra + 1) / 2.))
                Ntail = Nextra - Nhead
                y = cut(y, ((Nhead, np.int32(Nfft - Ntail)),), axis=axis)
            else:
                y = cut(y, ((N - 1, N), (0, N - 1)), axis)
        else:
            Nhead = np.int32(np.fix(Nextra / 2.))
            Ntail = Nextra - Nhead
            y = cut(y, ((Nhead, np.int32(Nfft - Ntail)),), axis=axis)
    else:
        Nhead = 0
        Ntail = Nextra
        y = cut(y, ((Nhead, np.int32(Nfft - Ntail)),), axis=axis)

    if shape in ['same', 'SAME', 'Same']:
        Nstart = np.fix(Nh / 2.)
        Nend = Nstart + Nx
    elif shape in ['valid', 'VALID', 'Valid']:
        Nstart = Nh - 1
        Nend = N - (Nh - 1)
    elif shape in ['full', 'FULL', 'Full']:
        Nstart, Nend = (0, N)
    Nstart, Nend = np.int32([Nstart, Nend])
    y = cut(y, ((Nstart, Nend),), axis=axis)
    return y


def fftconv1(x, h, shape='same', axis=0, Nfft=None, ftshift=False, eps=None):
    """Convolution using Fast Fourier Transformation

    Convolution using Fast Fourier Transformation.

    Parameters
    ----------
    x : {numpy.ndarray}
        data to be convolved.
    h : {numpy.ndarray}
        filter array
    shape : {str}, optional
        output shape:
        1. ``'same' --> same size as input x``, :math:`N_x`
        2. ``'valid' --> valid convolution output``
        3. ``'full' --> full convolution output``, :math:`N_x+N_h-1`
        (the default is 'same')
    axis : {number}, optional
        convolution axis (the default is 0)
    Nfft : {number}, optional
        number of fft points (the default is :math:`2^nextpow2(N_x+N_h-1)`),
        note that :attr:`nfft` can not be smaller than :math:`N_x+N_h-1`.
    ftshift : {bool}, optional
        whether shift frequencies (the default is False)
    eps : {None or float}, optional
        x[abs(x)<eps] = 0 (the default is None, does nothing)

    Returns
    -------
    y : {numpy.ndarray}
        Convolution result array.

    """

    Nh = np.size(h, axis)
    Nx = np.size(x, axis)

    N = Nx + Nh - 1
    if Nfft is None:
        Nfft = 2**nextpow2(N)

    x = padfft(x, Nfft, axis, ftshift)
    h = padfft(h, Nfft, axis, ftshift)
    X = fft(x, Nfft, axis, norm=None, shift=ftshift)
    H = fft(h, Nfft, axis, norm=None, shift=ftshift)
    Y = X * H
    y = ifft(Y, Nfft, axis, norm=None, shift=ftshift)

    y = cutfftconv1(y, Nfft, Nx, Nh, shape, axis, ftshift)

    if eps is not None:
        y[abs(y) < eps] = 0.

    return y


if __name__ == '__main__':

    ftshift = False
    x = np.array([1, 2, 3, 4, 5])
    h = np.array([1 + 2j, 2, 3, 4, 5, 6, 7])

    y1 = conv1(x, h, shape='same')
    y2 = fftconv1(x, h, axis=0, Nfft=None, shape='same', ftshift=ftshift)
    # print(y1)
    # print(y2)
    print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))

    y1 = conv1(x, h, shape='valid')
    y2 = fftconv1(x, h, axis=0, Nfft=None, shape='valid', ftshift=ftshift)
    # print(y1)
    # print(y2)
    print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))

    y1 = conv1(x, h, shape='full')
    y2 = fftconv1(x, h, axis=0, Nfft=None, shape='full', ftshift=ftshift)
    # print(y1)
    # print(y2)
    print(np.sum(np.abs(y1 - y2)), np.sum(np.angle(y1) - np.angle(y2)))
