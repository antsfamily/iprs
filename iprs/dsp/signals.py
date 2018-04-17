#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 10:45:23
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def hs(x):
    """
    Heavyside function :
        hv(x) = {1, if x>=0; 0, otherwise}
    """
    return 0.5 * (np.sign(x) + 1.0)


def ihs(x):
    """
    Inverse Heavyside function:
        ihv(x) = {0, if x>=0; 1, otherwise}
    """
    # print(x)
    # print(np.sign(x))
    return 0.5 * (1.0 - np.sign(x))


def rect(x):
    """
    Rectangle function:
        rect(x) = {1, if |x|<= 0.5; 0, otherwise}
    """
    # print(hs(x + 0.5))
    return hs(x + 0.5) * ihs(x - 0.5)


def chirp(t, tau_p, K_r):
    """
    Create a chirp signal :
        S_{tx}(t) = rect(t/tau_p) * exp(1j*pi*K_r*t^2)
    """
    return rect(t / tau_p) * np.exp(1j * np.pi * K_r * t**2)


def pulse(t, tau, T, delayTime=0):
    """
    Create a pulse signal

             _______
      ______|       |_______

    -T/2 -tau/2+d tau/2+d T/2

    time = -T*0.5 + step*index

    """
    tArray = t
    sArray = rect((t - delayTime) / tau)
    return sArray, tArray


def pulse2(tau, T, N, delayTime=0):
    """
    Create a pulse signal

             _______
      ______|       |_______

    -T/2 -tau/2+d tau/2+d T/2

    time = -T*0.5 + step*index

    """
    step = T * 1.0 / N
    tArray = np.arange(-T * 0.5, T * 0.5, step)
    sArray = rect((tArray - delayTime) / tau)
    return sArray, tArray
