#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np

from iprs.utils.const import *


def compute_range_beamwidth(Nr, Fsr, H, Ad, Tp):
    r"""computes beam angle in range direction

    .. math::
       {\rm sin}\frac{\theta_e}{2} = \frac{2H{\rm cos}\theta_d}{a} \pm \sqrt{{\rm sin}^2\theta_d + \frac{4H^2{\rm cos}^2 \theta_d}{a^2}}

    where :math:`a=\frac{cN_s}{F_s}`.

    Parameters
    ----------
    Nr : {integer}
        Number of samples in range direction.
    Fsr : {float}
        Sampling rate in range direction.
    H : {float}
        Height of the platform.
    Ad : {float}
        The depression angle (unit: rad).
    Tp : {float}
        Pulse width (unit: s).

    Returns
    -------
    float
        The beam angle (unit, rad) in range direction.

    """

    # Np = int(Fsr * Tp)
    Np = 0
    a = C * (Nr - Np) / Fsr
    b = 2 * H * np.cos(Ad) / a
    x1 = -b + np.sqrt(np.sin(Ad)**2 + b**2)
    x2 = -b - np.sqrt(np.sin(Ad)**2 + b**2)

    if x1 >= -1 and x1 <= 1:
        return 2. * np.arcsin(x1)
    if x2 >= -1 and x2 <= 1:
        return 2. * np.arcsin(x2)
    return None


def azimuth_beamwidth(Wl, La):
    BWa = 0.886 * Wl / La
    return BWa


def antenna_pattern_azimuth(Wl, La, A):

    BWa = 0.886 * Wl / La

    Pa = np.sinc(0.886 * A / BWa)

    return Pa


def azimuth_footprint(R, Wl, La):

    BWa = 0.886 * Wl / La
    return R * BWa


def range_footprint(R, Wl, La):

    pass
    return None


def cr_footprint(Wl, H, La, Ad):
    r"""cross range (azimuth) foot print

    .. math::
       R_{CR} \approx \frac{\lambda}{L_a}\frac{H}{{\rm cos}\theta_d}

    Parameters
    ----------
    Wl : {float}
        wave length
    H : {float}
        height of SAR platform
    La : {float}
        length of antenna aperture (azimuth)
    Ad : {float}
        depression angle

    Returns
    -------
    float
        foot print size in azimuth
    """

    FPa = (Wl * H) / (La * np.cos(Ad))

    return FPa


def ar_footprint(Wl, H, Lr, Ad):
    r"""along range (range) foot print

    .. math::
       R_{AR} \approx \frac{\lambda}{L_r}\frac{H}{{\rm cos}\theta_d}

    Parameters
    ----------
    Wl : {float}
        wave length
    H : {float}
        height of SAR platform
    Lr : {float}
        length of antenna aperture (range)
    Ad : {float}
        depression angle

    Returns
    -------
    float
        foot print size in range
    """

    print("===", Wl, H, Lr, Ad)
    FPr = (Wl * H) / (Lr * np.cos(Ad)**2)

    return FPr


if __name__ == "__main__":

    H = 793000
    Nr = 9288
    Ad = 53.3 * PI / 180.0
    Fsr = 32.317e+6
    Tp = 2.5e-6
    Ae = compute_range_beamwidth(Nr, Fsr, H, Ad, Tp)
    print(Ae * 180 / PI)
