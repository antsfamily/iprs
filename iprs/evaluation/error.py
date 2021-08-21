#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 21:14:04
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np


def ampphaerror(orig, reco):
    r"""compute amplitude phase error

    compute amplitude phase error of two complex valued matrix

    Parameters
    ----------
    orig : {complex numpy array}
        orignal
    reco : {complex numpy array}
        reconstructed

    Returns
    -------
    amperror : float
        error of amplitude
    phaerror : float
        error of phase
    """

    amp_orig = np.abs(orig)
    amp_reco = np.abs(reco)
    pha_orig = np.angle(orig)
    pha_reco = np.angle(reco)

    # print(np.abs(amp_orig - amp_reco))
    # print(np.abs(pha_orig - pha_reco))
    # print(np.mean(np.abs(amp_orig - amp_reco)))
    # print(np.mean(np.abs(pha_orig - pha_reco)))

    amperror = np.mean(np.abs(amp_orig - amp_reco))
    phaerror = np.mean(np.abs(pha_orig - pha_reco))

    return amperror, phaerror


def mse(o, r):
    r"""Mean Squared Error

    The Mean Squared Error (MSE) is expressed as

    .. math::
        {\rm MSE} = \frac{1}{MN}\sum_{i=1}^{M}\sum_{j=0}^{N}[|{\bm I}(i,j)|, |\hat{\bm I}(i, j)|]^2

    Arguments
    ---------------
    o : ndarray
        Orignal signal matrix.

    r : ndarray
        Reconstructed signal matrix

    Returns
    ---------------
    MSE : float
        Mean Squared Error

    """

    return np.mean(np.square((np.abs(o).astype(float) - np.abs(r).astype(float))))
