#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-23 19:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
from iprs.utils.arrayops import cut

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


