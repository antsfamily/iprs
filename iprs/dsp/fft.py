#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:38:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import math
import numpy as np
import numpy.fft as npfft


def padfft(X, Nfft=None, axis=0, shift=False):
    r"""PADFT Pad array for doing FFT or IFFT

    PADFT Pad array for doing FFT or IFFT

    Parameters
    ----------
    X : {numpy.ndarray}
        Data to be padded.
    Nfft : {number or None}
        Padding size.
    axis : {number}, optional
        Padding dimension. (the default is 0)
    shift : {bool}, optional
        Whether to shift the frequency (the default is False)
    """

    if axis is None:
        axis = 0

    Nx = np.size(X, axis)

    if Nfft < Nx:
        raise ValueError('Output size is smaller than input size!')

    Nd = np.ndim(X)
    Np = int(np.uint(Nfft - Nx))
    PS = np.zeros((Nd, 2), dtype='int32')
    PV = [0]
    if shift:
        PS[axis, 0] = int(np.fix((Np + 1) / 2.))
        X = np.pad(X, PS, 'constant', constant_values=PV)
        PS[axis, :] = [0, Np - PS[axis, 0]]
        X = np.pad(X, PS, 'constant', constant_values=PV)
    else:
        PS[axis, 1] = Np
        X = np.pad(X, PS, 'constant', constant_values=PV)

    return X


def fft(a, n=None, axis=-1, norm=None, shift=False):
    N = np.size(a, axis)
    if (n is not None) and (n > N):
        a = padfft(a, n, axis, shift)
    if shift:
        return npfft.fftshift(npfft.fft(npfft.fftshift(a, axes=axis), n=n, axis=axis, norm=norm), axes=axis)
    else:
        return npfft.fft(a, n=n, axis=axis, norm=norm)


def ifft(a, n=None, axis=-1, norm=None, shift=False):
    if shift:
        return npfft.ifftshift(npfft.ifft(npfft.ifftshift(a, axes=axis), n=n, axis=axis, norm=norm), axes=axis)
    else:
        return npfft.ifft(a, n=n, axis=axis, norm=norm)


def fftfreq(fs, n, shift, norm=False):
    r"""Return the Discrete Fourier Transform sample frequencies

    Return the Discrete Fourier Transform sample frequencies.

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start).  For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`, if shift is ``True`` and ``norm`` is True::

      f = [-n/2, ..., -1,     0, 1, ...,   n/2-1] / (d*n)   if n is even
      f = [-(n-1)/2, ..., -1, 0, 1, ..., (n-1)/2] / (d*n)   if n is odd

    Given a window length `n` and a sample spacing `d`, if shift is ``False``::

      f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)   if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)   if n is odd

    where :math:`d = 1/f_s`.

    Parameters
    ----------
    fs : {float}
        Sampling rate.
    n : {integer}
        Number of samples.
    shift : {bool}
        Does shift the zero frequency to center.

    Returns
    -------
    numpy array
        frequency array with size :math:`n×1`.
    """
    d = 1. / fs
    if n % 2 == 0:
        N = n
        N1 = n / 2.
        N2 = n / 2.
        endpoint = False
    else:
        N = n - 1
        N1 = (n + 1) / 2
        N2 = (n - 1) / 2
        endpoint = True

    if shift:
        f = np.linspace(-N / 2., N / 2., n, endpoint=endpoint)
    else:
        f = np.hstack((np.linspace(0, N / 2., N1, endpoint=endpoint),
                       np.linspace(-N / 2., 0, N2, endpoint=False)))
    if norm:
        return f / n
    else:
        return f / (d * n)


def fft2(img):
    r"""
    Improved 2D fft
    """
    out = np.zeros(img.shape, dtype=complex)
    for i in range(out.shape[1]):
        # get range fixed column
        out[:, i] = fft(img[:, i])
    for j in range(out.shape[0]):
        out[j, :] = fft(out[j, :])
    return out


def ifft2(img):
    r"""
    Improved 2D ifft
    """
    out = np.zeros(img.shape, dtype=complex)
    for i in range(out.shape[1]):
        out[:, i] = ifft(img[:, i])
    for j in range(out.shape[0]):
        out[j, :] = ifft(out[j, :])
    return out


def fftx(x, n=None):

    return npfft.fftshift(npfft.fft(npfft.fftshift(x, n)))


def ffty(x, n=None):
    return (npfft.fftshift(npfft.fft(npfft.fftshift(x.transpose(), n)))).transpose()


def ifftx(x, n=None):
    return npfft.fftshift(npfft.ifft(npfft.fftshift(x), n))


def iffty(x, n=None):
    return (npfft.fftshift(npfft.ifft(x.transpose(), n))).transpose()


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fs = 1000.
    n = 16

    print(np.fft.fftfreq(n, 1. / fs))

    f = fftfreq(fs, n, shift=False, norm=False)
    print(f)
    f = fftfreq(fs, n, shift=False, norm=True)
    print(f)
    f = fftfreq(fs, n, shift=True, norm=True)
    print(f)

    print(np.linspace(-fs / 2., fs / 2., n))

    Ts = 2.
    f0 = 100.
    Fs = 1000.
    Ns = int(Fs * Ts)
    t = np.linspace(0., Ts, Ns)
    # f = np.linspace(-Fs / 2., Fs / 2., Ns)
    f = fftfreq(Fs, Ns, shift=True)
    print(f)

    x = np.sin(2. * np.pi * f0 * t)
    y = fft(x, shift=True)
    y = np.abs(y)

    plt.figure()
    plt.subplot(121)
    plt.grid()
    plt.plot(t, x)
    plt.subplot(122)
    plt.grid()
    plt.plot(f, y)
    plt.show()

    X = np.array([[1, 2, 3], [4, 5, 6]])
    print(X)
    X = padfft(X, Nfft=8, axis=0, shift=False)
    print(X)
    X = padfft(X, Nfft=8, axis=1, shift=False)
    print(X)
