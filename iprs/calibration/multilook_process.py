#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-05 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def multilook_spatial(Sslc, nlooks):
    """spatial multilook processing

    spatial averaging in azimuth or range direction.

    Parameters
    ----------
    Sslc : {complex or float}
        Processed single look complex (or intensity) sar data matrix with size of :math:`N_a×N_r`.
    nlooks : {tuple or list}
        number of looks in azimuth and range direction, [na, nr] or (na, nr).

    Returns
    -------
    Smlc : {complex}
        Processed multi-look complex.

    """

    Na, Nr = Sslc.shape
    if nlooks is None:
        return Sslc

    # spatial averaging
    if nlooks[0] > 1:
        Smlca = np.zeros((int(Na / nlooks[0]), Nr), dtype=Sslc.dtype)
        index = 0
        for a in range(0, Na - nlooks[0], nlooks[0]):
            Smlca[index, :] = np.mean(Sslc[a:a + (nlooks[0] - 1), :], axis=0)
            index += 1
    else:
        Smlca = Sslc

    Na, Nr = Smlca.shape

    if nlooks[1] > 1:
        Smlc = np.zeros((Na, int(Nr / nlooks[1])), dtype=Sslc.dtype)
        index = 0
        for r in range(0, Nr - nlooks[1], nlooks[1]):
            Smlc[:, index] = np.mean(Smlca[:, r:r + (nlooks[1] - 1)], axis=1)
            index += 1
    else:
        Smlc = Smlca

    return Smlc


if __name__ == '__main__':

    Na, Nr = (1025, 256)
    real = np.random.rand(Na, Nr)
    imag = np.random.rand(Na, Nr)
    print(real.shape, imag.shape)
    Sslc = real + 1j * imag
    Smlc = multilook_spatial(Sslc, nlooks=4)

    print(Smlc.shape)
