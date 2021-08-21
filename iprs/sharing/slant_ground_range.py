#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np

from iprs.utils.const import *


def slantr2groundr(R, H, Ar, Xc):
    """slant range to ground range

    Convert slant range :math:`R` to ground range :math:`X`.

    Parameters
    ----------
    R : {1d-array}
        slant range array
    H : {float}
        sarplat height
    Ar : {float}
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : {1d-array}
        ground range

    """
    return np.sqrt(np.abs((R * np.cos(Ar))**2 - H * H) + EPS) - Xc
    # return np.sqrt(np.abs((R * np.cos(Ar))**2 - H * H) + EPS)


def slantt2groundr(tr, H, Ar):
    """slant time to ground range

    Convert slant range time :math:`t_r` to ground range :math:`X`.

    Parameters
    ----------
    tr : {1d-array}
        range time array
    H : {float}
        sarplat height
    Ar : {float}
        squint angle (unit, rad) in line geometry

    Returns
    -------
    X : {1d-array}
        ground range

    """

    return np.sqrt(np.abs(((tr * C / 2.) * np.cos(Ar))**2 - H * H) + EPS)


def groundr2slantr(X, H, Ar, Xc):
    """ground range to slant range

    Convert ground range :math:`R` to slant range :math:`X`.

    Parameters
    ----------
    X : {1d-array}
        ground range array
    H : {float}
        sarplat height
    Ar : {float}
        squint angle (unit, rad) in line geometry

    Returns
    -------
    R : {1d-array}
        slant range

    """

    return np.sqrt((X + Xc)**2 + H * H + EPS) / (np.cos(Ar) + EPS)
    # return np.sqrt((X)**2 + H * H + EPS) / (np.cos(Ar) + EPS)


def groundr2slantt(X, H, Ar):
    """ground range to slant time

    Convert ground range :math:`X` to slant time :math:`t_r`.

    Parameters
    ----------
    X : {1d-array}
        ground range
    H : {float}
        sarplat height
    Ar : {float}
        squint angle (unit, rad) in line geometry

    Returns
    -------
    tr : {1d-array}
        range time array

    """

    return 2. * np.sqrt(X**2 + H * H + EPS) / (np.cos(Ar) + EPS) / C


def min_slant_range(Fsr, Noff, Rnear):
    """minimum slant range from radar to target

    [description]

    Parameters
    ----------
    Fsr : {[type]}
        [description]
    Noff : {[type]}
        ``np.linspace(0, Nr, Nr)``
    Rnear : {[type]}
        [description]

    Returns
    -------
    [type]
        [description]
    """
    r = Rnear + Noff * (C / (2. * Fsr))
    return r


def min_slant_range_with_migration(Fsr, Noff, Rnear, Wl, Vr, fdc):
    r = Rnear + Noff * (C / (2. * Fsr))
    return r / np.sqrt(1. - (Wl * fdc / (Vr + Vr))**2)
