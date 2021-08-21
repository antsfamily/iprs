#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-23 19:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import logging
import numpy as np


def cut(A, pos, axis=None):
    """Cut array at given position.

    Cut array at given position.

    Parameters
    ----------
    A : {numpy.ndarray}
        [description]
    pos : {tulpe or list}
        cut positions: ((cpstart, cpend), (cpstart, cpend), ...)
    axis : {number, tulpe or list}, optional
        cut axis (the default is None, which means nothing)
    """

    if axis is None:
        return A
    if type(axis) == int:
        axis = tuple([axis])
    nDims = np.ndim(A)
    idx = [None] * nDims

    if len(axis) > 1 and len(pos) != len(axis):
        error('You should specify cut axis for each cut axis!')
    elif len(axis) == 1:
        axis = tuple(list(axis) * len(pos))

    uqaixs = np.unique(axis)
    for a in uqaixs:
        idx[a] = []

    for i in range(len(axis)):
        idx[axis[i]] += range(pos[i][0], pos[i][1])

    for a in uqaixs:
        idxall = [slice(None)] * nDims
        idxall[a] = idx[a]
        A = A[tuple(idxall)]
    return A



if __name__ == '__main__':

    X = np.random.randint(0, 100, 90).reshape(9, 10)
    print('X')
    print(X)
    Y = cut(X, ((1, 4), (5, 8)), axis=0)
    print('Y = cut(X, ((1, 4), (5, 8)), axis=0)')
    print(Y)
    Y = cut(X, ((1, 4), (7, 9)), axis=(0, 1))
    print('Y = cut(X, ((1, 4), (7, 9)), axis=(0, 1))')
    print(Y)
    Y = cut(X, ((1, 4), (1, 4), (5, 8), (7, 9)), axis=(0, 1, 0, 1))
    print('cut(X, ((1, 4), (1, 4), (5, 8), (7, 9)), axis=(0, 1, 0, 1))')
    print(Y)


