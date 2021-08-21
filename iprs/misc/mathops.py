#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 16:36:03
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np


def nextpow2(x):
    if x == 0:
        y = 0
    else:
        y = int(np.ceil(np.log2(x)))

    return y


def prevpow2(x):
    if x == 0:
        y = 0
    else:
        y = int(np.floor(np.log2(x)))
    return y


def ebeo(a, b, op='+'):
    r"""element by element operation

    Element by element operation.

    Parameters
    ----------
    a : {list, tuple or nparray}
        The first list/tuple/nparray.
    b : {list, tuple or nparray}
        The second list/tuple/nparray.
    op : {str}, optional
        Supported operations are:
        - ``'+'`` or ``'add'`` for addition (default)
        - ``'-'`` or ``'sub'`` for substraction
        - ``'*'`` or ``'mul'`` for multiplication
        - ``'/'`` or ``'div'`` for division
        - ``'**'`` or ``pow`` for power
        - ``'<'``, or ``'lt'`` for less than
        - ``'<='``, or ``'le'`` for less than or equal to
        - ``'>'``, or ``'gt'`` for greater than
        - ``'>='``, or ``'ge'`` for greater than or equal to
        - ``'&'`` for bitwise and
        - ``'|'`` for bitwise or
        - ``'^'`` for bitwise xor
        - function for custom operation.

    Raises
    ------
    TypeError
        If the specified operator not in the above list, raise a TypeError.
    """
    if op in ['+', 'add']:
        return [i + j for i, j in zip(a, b)]
    if op in ['-', 'sub']:
        return [i - j for i, j in zip(a, b)]
    if op in ['*', 'mul']:
        return [i * j for i, j in zip(a, b)]
    if op in ['/', 'div']:
        return [i / j for i, j in zip(a, b)]
    if op in ['**', '^', 'pow']:
        return [i ** j for i, j in zip(a, b)]
    if isinstance(op, str):
        raise TypeError("Not supported operation: " + op + "!")
    else:
        return [op(i, j) for i, j in zip(a, b)]


def real2imag(X, axis=-1):

    if axis == -1:
        return X[..., 0] + 1j * X[..., 1]
    if axis == 1:
        return X[:, 0] + 1j * X[:, 1]
    if axis == 0:
        return X[0] + 1j * X[1]


def imag2real(X, axis=-1):

    return np.stack((X.real, X.imag), axis=axis)


if __name__ == '__main__':

    x = 120
    y = nextpow2(x)
    print(y)
