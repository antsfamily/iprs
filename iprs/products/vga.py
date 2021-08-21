#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  :2018-12-24 12:03:00
# @Author  :Zhi Liu(zhiliu.mind@gmail.com)
# @Link  :http://iridescent.ink
# @Verson :$1.0$
# @Note  :https://crisp.nus.edu.sg/ers/ers.html
#

import logging
import numpy as np


def vga_gain_compensation(S, V, mod='linear', fact=1.0):
    r"""vga gain compensation

    vga gain compensation

    .. math::
       \begin{aligned}
       {\bm F} &= (λ 10^{{\bm V}/20})\\
       {\bm S}_{c} &= {\bm F} \odot {\bm S}
       \end{aligned}

    Parameters
    ----------
    S : {numpy array}
        :attr:`S` is an :math:`N_a×N_r×2` array, where, :math:`S[:,:,0]` is the I signal
        and :math:`S[:,:,1]` is the Q signal.
    V : {numpy array}
        :attr:`S` is an :math:`N_a×N_r` or :math:`N_a×1` VGA gain array, the gain values are in
        ``dB`` unit.
    mod : {str}, optional
        compensation mode (the default is 'linear')
    fact : {number}, optional
        fact is the factor :math:`\lambda` (the default is 1.0)

    Returns
    -------
    {numpy array}
        compensated signal, :math:`N_a×N_r×2` array.
    """

    logging.info("===In vga_gain_compensation...")

    Na, Nr, _ = S.shape
    S = np.array(S).astype('float')
    V = np.array(V)[0:Na, :]

    linear_gain_factor = (fact * 10.**(V / 20.0)).astype('float')

    if np.ndim(V) == 3:
        S = S * linear_gain_factor
    elif np.ndim(V) == 2 and V.shape[1] + V.shape[0] > 2:
        S[:, :, 0] = S[:, :, 0] * linear_gain_factor
        S[:, :, 1] = S[:, :, 1] * linear_gain_factor
    else:
        # A = np.repeat(linear_gain_factor, Nr*2).reshape(Na, Nr, 2)
        # S = A * S

        for n in range(Na):
            S[n, :, :] = linear_gain_factor[n] * S[n, :, :]

    logging.info("===Out vga_gain_compensation.")

    return S



