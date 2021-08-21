#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

from ..utils.const import *

from ..misc import visual as vis

from ..dsp import normalsignals as sig
from .share import genRefPhase


def wka(Srx, sarplat, verbose=False):
    r"""Omega-K imaging algorithm

    1. FFT 2D
    2. Reference Function Multiplication
    3. Stolt interpolation
    4. IFFT 2D

    Sr : {numpy array}
        The SAR rawdata
    sarplat : {sarplat Object}
        SAR platform contains various parameters
    verbose : {bool}, optional
        display processing info (default: {True})

    Returns
    -------
    SI : complex ndarray
        compressed 2D array, azimuth positions, range time
    """

    if Srx is None:
        print("No raw data")

    H = sarplat.sensor['H']
    V = sarplat.sensor['V']
    Fc = sarplat.sensor['Fc']
    Tp = sarplat.sensor['Tp']
    Kr = sarplat.sensor['Kr']
    Wl = sarplat.sensor['Wl']
    PRF = sarplat.sensor['PRF']
    Tsa = sarplat.params['Tsa']
    Tsr = sarplat.params['Tsr']
    ta = sarplat.params['ta']
    tr = sarplat.params['tr']

    # Step1: 2D FFT
    if verbose:
        print("Step1: Do 2D FFT...")

    fr = tsfm.freq(Srx.shape[1], 1.0 / Tsr)
    fa = tsfm.freq(Srx.shape[0], V / Tsa)

    Sr = tsfm.fft2(Srx)
    Srx = None
    if verbose:
        print("Step1: 2D FFT done!")
        vis.show_response(Sr, None, '2D FFT')

    # Step2: Reference Function Multiplication
    if verbose:
        print("Step2: Do Reference Function Multiplication...")
    tZero = tr[len(tr) // 2]
    etaZero = ta[len(ta) // 2] / V
    Rref = 0.5 * C * tZero
    Vref = V
    phaseRef = genRefPhase(fa, fr, Fc, Rref, Vref, Kr, Tp, tZero, etaZero)

    Sr = Sr * phaseRef

    if verbose:
        print("Step2: RFM done!")
        vis.show_response(Sr, None, 'After RFM')

    # Step3: Stolt mapping
    if verbose:
        print("Step3: Do Stolt Mapping...")

    # For azimuth line :
    for i, f in enumerate(fa):
        #
        # Here we need analytical inverse of Stolt mapping :
        # f' + f0 = sqrt( (f0 + f)^2 - (c * fEta / (2*Vsat))^2 )
        #
        # f + f0 = + sqrt( (f0 + f')^2 + (c * fEta / (2*Vsat))^2 )
        #
        nfRangeArray = -Fc + \
            np.sqrt((Fc + fr)**2 - (C * f / (2.0 * V))**2)

        yRe = np.real(Sr[i, :])
        yIm = np.imag(Sr[i, :])
        yRe = np.interp(nfRangeArray, fr, yRe)
        yIm = np.interp(nfRangeArray, fr, yIm)
        Sr[i, :] = yRe + 1j * yIm

    if verbose:
        print("Step3: Stolt Mapping done!")
        vis.showReImAmplitudePhase(Sr, None, 'After Stolt mapping')

    # Step4: 2D IFFT
    if verbose:
        print("Step4: Do 2D IFFT...")

    Sr = tsfm.ifft2(Sr)

    if verbose:
        print("Step4: 2D IFFT done!")
        vis.show_response(Sr, None, 'After 2D IFFT')

    return Sr, ta, tr
