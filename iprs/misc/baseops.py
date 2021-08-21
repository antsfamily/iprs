#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-05 16:36:03
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import


def dmka(D, Ds):
    """Multi-key value assign

    Multi-key value assign

    Parameters
    ----------
    D : {[type]}
        [description]
    Ds : {[type]}
        [description]
    """

    for k, v in Ds.items():
        D[k] = v
    return D


if __name__ == '__main__':

    D = {'a': 1, 'b': 2, 'c': 3}
    Ds = {'b': 6}
    print(D)
    dmka(D, Ds)
    print(D)
