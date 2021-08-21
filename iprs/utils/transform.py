#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
from iprs.utils.const import EPS


def db20(X):
    return 20. * np.log10(np.abs(X))


def scale(X, st=[0, 1], sf=None, istrunc=True, rich=False):
    r"""
    Scale data.

    .. math::
        x \in [a, b] \rightarrow y \in [c, d]

    .. math::
        y = (d-c)*(x-a) / (b-a) + c.

    Parameters
    ----------
    X : array_like
        The data to be scaled.
    st : tuple, list, optional
        Specifies the range of data after beening scaled. Default [0, 1].
    sf : tuple, list, optional
        Specifies the range of data. Default [min(X), max(X)].
    istrunc : bool
        Specifies wether to truncate the data to [a, b], For example,
        If sf == [a, b] and 'istrunc' is true,
        then X[X < a] == a and X[X > b] == b.
    rich : bool
        If you want to see what the data is scaled from and scaled to,
        then you should set it to true
    Returns
    -------
    out : ndarray
        Scaled data array.
    sf, st : list or tuple
        If rich is true, they will also be returned
    """

    if not(isinstance(st, (tuple, list)) and len(st) == 2):
        raise Exception("'st' is a tuple or list, such as (-1,1)")
    if sf is not None:
        if not(isinstance(sf, (tuple, list)) and len(sf) == 2):
            raise Exception("'sf' is a tuple or list, such as (0, 255)")
    else:
        sf = [np.min(X) + 0.0, np.max(X) + 0.0]
    if sf[0] is None:
        sf = (np.min(X) + 0.0, sf[1])
    if sf[1] is None:
        sf = (sf[0], np.max(X) + 0.0)

    a = sf[0] + 0.0
    b = sf[1] + 0.0
    c = st[0] + 0.0
    d = st[1] + 0.0

    X = X.astype('float')

    print(X.min(), X.max(), sf, st)

    if istrunc:
        X[X < a] = a
        X[X > b] = b

    print(X.min(), X.max(), sf, st)

    if rich:
        return (X - a) * (d - c) / (b - a + EPS) + c, sf, st
    else:
        return (X - a) * (d - c) / (b - a + EPS) + c
