#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from __future__ import division, print_function, absolute_import
import os
import numpy as np
import scipy.io as scio


def loadmat(filename):

    return scio.loadmat(filename)


def savemat(filename, mdict, fmt='5', dtype=None):
    for k, v in mdict.items():
        if np.iscomplex(v).any():
            mdict[k] = np.array(
                [np.real(v), np.imag(v)]).transpose(1, 2, 0)
            mdict[k] = mdict[k].astype('float32')
    scio.savemat(filename, mdict, format=fmt)

    return 0


if __name__ == '__main__':
    pass


