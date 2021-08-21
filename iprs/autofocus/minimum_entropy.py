#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-25 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.fft import *
from ..utils.const import *

from scipy.optimize import minimize
from iprs.misc.entropy import natural_entropy, shannon_entropy
from iprs.modeling.phase_error import pe_identity, pe_polynomial


def _entropy(X, phi):
    Na, Nr = X.shape

    for n in range(Nr):
        X[:, n] = X[:, n] * np.exp(1j * PI * phi)
    X = fft(X, axis=0)
    S = shannon_entropy(X)
    return S


def entropyaf(X, pfunc=None, pinit=None, emod='Natural', optm='Nelder-Mead'):
    r"""Entropy based autofocus

    Minimum entropy based autofocus

    Parameters
    ----------
    X : {2D numpy array}
        complex image with shape :math:`N_a×N_r`
    pfunc : {function handle}, optional
        modeling function of phase error :math:`\phi()` (the default is None, )
    pinit : {float}, optional
        initial value of :math:`\phi` (the default is None, which means zeros)
    emod : {str}, optional
        ``'Renyi'``, ``'Shannon'``(base 2), ``'Natural'``(base e)
        (the default is 'Natural')
    optm : {str}, optional
        optimization method (the default is 'Nelder-Mead', which [default_description])
    """

    raise TypeError("Not opened yet!")

    return X
