#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def shannon_entropy(X):

    X = np.conj(X) * X

    P = np.sum(X)

    p = X / P

    S = - np.sum(p * np.log2(p))

    return S


def natural_entropy(X):

    X = np.conj(X) * X

    P = np.sum(X)

    p = X / P

    S = - np.sum(p * np.log(p))

    return S
