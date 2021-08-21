#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-06 22:29:14
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np
from iprs.misc.mathops import nextpow2


def toimage(X, drange=(0., 255.), method='2Sigma'):
    r"""convert to image

    Convert data to image data :math:`\bm X` with dynamic range :math:`d=[min, max]`.

    Parameters
    ----------
    X : {numpy ndarray}
        data to be converted
    drange : {tuple}, optional
        dynamic range (the default is (0., 255.))
    method : {str}, optional
        converting method (the default is '2Sigma', which means two-sigma)

    Returns
    -------
    Y : {numpy ndarray}
        converted image data

    """

    if method in ['2Sigma', '2sigma', '2SIGMA', 'TwoSigma', 'twosigma', 'TWOSIGMA']:
        xmin, xmax = np.min(X), np.max(X)
        xmean, xstdv = np.mean(X), np.std(X)

        diff_min = xmean - 2 * xstdv
        diff_max = xmean + 2 * xstdv

        ymin, ymax = diff_min, diff_max

        if diff_min < xmin:
            ymin = xmin
        if diff_max > xmax:
            ymax = xmax

        dmin, dmax = drange
        slope = dmax / (ymax - ymin)
        offset = -slope * ymin
        # offset = -slope * ymin + dmin

        v = slope * X + offset
        idxltdmix = v < dmin
        idxgtdmax = v > dmax
        idxindrange = (~idxltdmix) & (~idxgtdmax)

        Y = X.copy()
        Y[idxltdmix] = dmin
        Y[idxgtdmax] = dmax
        Y[idxindrange] = v[idxindrange]

    if dmin >= 0:
        dtype = 'uint'
    else:
        dtype = 'int'
    dtype = nextpow2(drange[1] - drange[0])
    Y = Y.astype(dtype)

    return Y
