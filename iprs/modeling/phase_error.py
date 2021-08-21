#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-25 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def pe_identity(t, a):
    return t * a


def pe_polynomial(t, a, order=4):

    p = 0.
    for i in range(order):
        p += a[i] * (t[i])**i

    return p
