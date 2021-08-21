#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 16:36:03
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
from iprs.utils.const import *

SINC_TABLE_Nq16Ns8 = [
    [-0.003, 0.010, -0.024, 0.062, 0.993, -0.054, 0.021, -0.009],
    [-0.007, 0.021, -0.049, 0.131, 0.973, -0.098, 0.040, -0.017],
    [-0.012, 0.032, -0.075, 0.207, 0.941, -0.134, 0.055, -0.023],
    [-0.016, 0.043, -0.101, 0.287, 0.896, -0.160, 0.066, -0.027],
    [-0.020, 0.054, -0.125, 0.371, 0.841, -0.176, 0.074, -0.030],
    [-0.024, 0.063, -0.147, 0.457, 0.776, -0.185, 0.078, -0.031],
    [-0.027, 0.071, -0.165, 0.542, 0.703, -0.185, 0.079, -0.031],
    [-0.030, 0.076, -0.178, 0.625, 0.625, -0.178, 0.076, -0.030],
    [-0.031, 0.079, -0.185, 0.703, 0.542, -0.165, 0.071, -0.027],
    [-0.031, 0.078, -0.185, 0.776, 0.457, -0.147, 0.063, -0.024],
    [-0.030, 0.074, -0.176, 0.841, 0.371, -0.125, 0.054, -0.020],
    [-0.027, 0.066, -0.160, 0.896, 0.287, -0.101, 0.043, -0.016],
    [-0.023, 0.055, -0.134, 0.941, 0.207, -0.075, 0.032, -0.012],
    [-0.017, 0.040, -0.098, 0.973, 0.131, -0.049, 0.021, -0.007],
    [-0.009, 0.021, -0.054, 0.993, 0.062, -0.024, 0.010, -0.003],
    [-0.000, 0.000, -0.000, 1.000, 0.000, -0.000, 0.000, -0.000],
]


def sinc_table(Nq, Ns):

    X = np.zeros((Nq, Ns))
    # for q in range(Nq, 0, -1):
    #     NN = Ns / (2.0 * q)
    #     X[q - 1, :] = np.linspace(-NN, NN, Ns)

    for q in range(Nq, 0, -1):
        X[q - 1, :] = np.linspace(0, Ns, Ns * q, endpoint=True)[0::q] - Ns / 2.
        # X[q - 1, :] = np.round(X[q - 1, :]) - Ns / 2.
        print(X[q - 1, :])

    kasier_window = np.kaiser(Ns, 2.5).repeat(Nq).reshape(Ns, Nq).transpose()
    # return sinc(X) * kasier_window
    return sinc(X)


def sinc_interp(xin, r=1.0):
    xin = np.array(xin)
    N = xin.size
    M = int(N * r)

    u = np.linspace(0, N, M)
    v = np.linspace(0, N, N)
    xout = []
    for i in u:
        xout.append(np.sum(xin * sinc(v - i)))
    return np.array(xout), np.array(u)


def interp(x, xp, yp, mod='sinc'):
    """interpolation

    interpolation

    Parameters
    ----------
    x : array_like
        The x-coordinates of the interpolated values.

    xp : 1-D sequence of floats
        The x-coordinates of the data points, must be increasing if argument
        `period` is not specified. Otherwise, `xp` is internally sorted after
        normalizing the periodic boundaries with ``xp = xp % period``.

    yp : 1-D sequence of float or complex
        The y-coordinates of the data points, same length as `xp`.

    mod : {str}, optional
        ``'sinc'`` : sinc interpolation (the default is 'sinc')

    Returns
    -------
    y : float or complex (corresponding to fp) or ndarray
        The interpolated values, same shape as `x`.

    """

    xp = np.array(xp)
    yp = np.array(yp)
    N = yp.size
    M = x.size

    x = np.linspace(0., N, M)
    xp = np.linspace(0., N, N)

    y = []
    for i in x:
        y.append(np.sum(yp * sinc(xp - i)))
    return np.array(y)


def sinc(x):
    x = np.array(x)
    eps = 1.0e-8
    y = np.where(np.abs(PI * x) < eps, 1.0,
                 np.sin(PI * x + eps) / (PI * x + eps))
    return y


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    Ns = 16.0

    t = np.linspace(-Ns / 2., Ns / 2., Ns)
    x = np.sinc(t)
    plt.figure()
    plt.plot(t, x)
    plt.show()

    SINC_TABLE_Nq16Ns8_1 = np.array(SINC_TABLE_Nq16Ns8)
    SINC_TABLE_Nq16Ns8_2 = sinc_table(16, 8)
    plt.figure()
    plt.subplot(121)
    for n in range(16):
        plt.plot(SINC_TABLE_Nq16Ns8_1[n, :])

    plt.subplot(122)
    for n in range(16):
        plt.plot(SINC_TABLE_Nq16Ns8_2[n, :])
    plt.show()

    Ns = 100.0
    T = 64.0
    Fs = Ns / T
    Ts = 1.0 / Fs

    t0 = np.linspace(0, T, Ns)

    a = 0.9
    x0 = t0 * a**t0

    r = 4.0
    t1 = np.linspace(0, T, Ns * r)

    x1 = np.interp(t1, t0, x0)

    x2, _ = sinc_interp(x0, r=r)

    t2 = np.linspace(0, T, Ns * r)
    x2 = interp(t2, t0, x0)

    print(np.sinc(2.3), sinc(2.3), np.sinc(2.3 / np.pi), np.sin(2.3) / 2.3)

    plt.figure()
    plt.plot(t0, x0, '-ob')
    plt.plot(t1, x1, '-g')
    plt.plot(t2, x2, '-r')
    plt.grid()
    plt.xlabel('Time/s')
    plt.ylabel('Amplitude')
    plt.title('interpolation')
    plt.legend(['original', 'np.interp', 'sinc_interp'])

    plt.show()
