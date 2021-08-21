#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-01-15 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def intesity(S):
    r"""compute intensity of S

    Denotes :math:`|{\bm S}|` as the amplitude of :math:`\bm S`, which can be expressed as

    .. math::
       |{\bm S}|_{ij} = \sqrt{{\rm real}^2({\bm S}_{ij}) + {\rm imag}^2({\bm S}_{ij})}


    Parameters
    ----------
    S : {ndarray}
        complex data matrix.

    Returns
    -------
    |S| : ndarray
        intensity of the input.
    """

    return np.abs(S)


def power(S):
    r"""compute power of S


    Parameters
    ----------
    S : {ndarray}
        complex data matrix.

    Returns
    -------
    |S|^2 : ndarray
        power of the input.
    """

    return np.real(S * np.conj(S))


# see  https://github.com/asfadmin/ASF_MapReady/blob/devel/src/libasf_ardop/calibration.c


def sigma_naught(noise, noise_factor, linear_conversion_factor, DNsquared):

    return 10 * np.log10(linear_conversion_factor * (DNsquared - noise_factor * noise))


def gamma_naught(noise, noise_factor, linear_conversion_factor, DNsquared, incidAngle):

    return 10 * np.log10((linear_conversion_factor * (DNsquared - noise_factor * noise)) / np.cos(incidAngle))


def beta_naught(noise, noise_factor, linear_conversion_factor, DNsquared, incidAngle):
    """[summary]

    [description]

    Parameters
    ----------
    noise : {[type]}
        [description]
    noise_factor : {[type]}
        [description]
    linear_conversion_factor : {[type]}
        [description]
    DNsquared : {[type]}
        [description]
    incidAngle : {[type]}
        [description]

    Returns
    -------
    number
        [description]
    """


    return 10 * np.log10((linear_conversion_factor * (DNsquared - noise_factor * noise)) / np.sin(incidAngle))




