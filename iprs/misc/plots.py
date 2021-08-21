#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def cplot(ca, lmod=None):
    N = len(ca)
    if lmod is None:
        lmod = '-b'
    r = np.real(ca)
    i = np.imag(ca)
    # x = np.hstack((np.zeros(N), r))
    # y = np.hstack((np.zeros(N), i))
    for n in range(N):
        plt.plot([0, r[n]], [0, i[n]], lmod)
    plt.xlabel('real')
    plt.ylabel('imag')


if __name__ == '__main__':

    N = 3

    r = np.random.rand(N)
    i = -np.random.rand(N)

    print(r)
    print(i)
    x = r + 1j * i

    cplot(x)
