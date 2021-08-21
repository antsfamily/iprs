#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

import logging
from ..utils.const import *
from ..misc import visual as vis
from ..dsp import normalsignals as sig
from iprs.dsp.fft import fft, ifft


def zeros_padding(Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=False):
    r"""pad zeros before and after data

    pad zeros before and after data

    ::

        0 0 0 0 0 0
        0 0  Sr 0 0
        0 0 0 0 0 0

    Parameters
    ----------
    Sr : ndarray
        orignal SAR signal matrix :math:`N_a×N_r`
    fa : 1darray
        frequency array :math:`N_a×1` in azimuth
    fr : 1darray
        frequency array :math:`N_r×1` in range
    ta : 1darray
        time array :math:`N_a×1` in azimuth
    tr : 1darray
        time array :math:`N_r×1` in range
    Tp : {float number}
        pulse width (s)
    Za : integer number
        padding numbers in azimuth
    Zr : integer number
        padding numbers in range
    verbose : {bool}, optional
        [description] (the default is False, which [default_description])

    Returns
    -------
    Sr : ndarray
        padded matrix :math:`(Z_a + N_a + Z_a) × (Z_r + N_r + Z_r)`
    """
    logging.info("---In zeros_padding...")

    logging.info("~~~Pad zeros before and after...")

    Na, Nr = Sr.shape

    # print(Sr.shape)
    Sr = np.concatenate((np.zeros((Za, Nr)), Sr), axis=0)
    # print(Sr.shape)
    Sr = np.concatenate((Sr, np.zeros((Za, Nr))), axis=0)
    # print(Sr.shape)
    Sr = np.concatenate((np.zeros((Na + Za * 2, Zr)), Sr), axis=1)
    # print(Sr.shape)
    Sr = np.concatenate((Sr, np.zeros((Na + Za * 2, Zr))), axis=1)
    # print(Sr.shape)

    print("~~~Data shape before zpa: ", (Na, Nr))
    print("~~~Data shape after zpa: ", Sr.shape)
    if verbose:
        print("~~~Frequency readjustment: ", Sr.shape)

    Na, Nr = Sr.shape
    # fr = np.linspace(fr[0], fr[-1], Nr)
    # fa = np.linspace(fa[0], fa[-1], Na)
    # tr = np.linspace(tr[0], tr[-1], Nr)
    # ta = np.linspace(ta[0], ta[-1], Na)

    print(fr.shape, np.zeros((Zr)).shape)
    print(ta.shape, np.zeros((Za)).shape)
    fr = np.hstack((np.zeros((Zr)), fr))
    fr = np.hstack((fr, np.zeros((Zr))))
    fa = np.hstack((np.zeros((Za)), fa))
    fa = np.hstack((fa, np.zeros((Za))))
    tr = np.hstack((np.zeros((Zr)), tr))
    tr = np.hstack((tr, np.zeros((Zr))))
    ta = np.hstack((np.zeros((Za)), ta))
    ta = np.hstack((ta, np.zeros((Za))))

    logging.info("---Done!")
    logging.info("---Out zeros_padding.")

    return Sr, fa, fr, ta, tr


def range_matched_filtering(Sr, fr, Kr):
    r"""Range matched filtering

    matched filtering in range direction

    .. math::
        H_r(f_\tau) = {\rm exp}\left\{j\frac{\pi f_\tau^2}{K_r}\right\},
        :label: equ-MatchedFilterRange



    Parameters
    ----------
    Sr : ndarray
        orignal SAR signal matrix :math:`N_a×N_r`
    fr : 1darray
        frequency array :math:`N_r×1` in range
    Kr : float number
        chirp rate in range direction

    Returns
    -------
    Sr : ndarray
        matched filtered data
    """
    logging.info("~~~In range_matched_filtering...")

    logging.info("~~~Generates range matched filtering...")
    Hrs = np.exp(1j * PI * (fr ** 2) / Kr)
    logging.info("~~~Done!")

    if Sr.shape != Hrs.shape:
        Na, Nr = Sr.shape
        Hrs = np.reshape(np.repeat(Hrs, Na), (Nr, Na)).transpose()

    logging.info("~~~Do range matched filtering...")
    Sr = Sr * Hrs
    logging.info("~~~Done!")

    logging.info("~~~Out range_matched_filtering.")

    return Sr


def range_compression(Sr, fr, Kr, verbose=False):
    r"""Range compression

    - Step1: Do FFT in range
    - Step2: Do matched filtering
    - Step3: Do IFFT in range

    .. math::
        H_r(f_\tau) = {\rm exp}\left\{j\frac{\pi f_\tau^2}{K_r}\right\},
        :label: equ-MatchedFilterRange


    Parameters
    ----------
    Sr : ndarray
        orignal SAR signal matrix :math:`N_a×N_r`
    fr : 1darray
        frequency array :math:`N_r×1` in range
    Kr : float number
        chirp rate in range direction
    verbose : {bool}, optional
        show more info (the default is False, which does not show)

    Returns
    -------
    Sr : ndarray
        Range compressed data
    """

    logging.info("---In range_compression...")

    logging.info("~~~Do FFT in range...")
    Sr = fft(Sr, axis=1, shift=True)
    logging.info("~~~Done!")

    Sr = range_matched_filtering(Sr, fr, Kr)

    logging.info("~~~Do IFFT in range...")
    Sr = ifft(Sr, axis=1, shift=True)
    logging.info("~~~Done!")

    if verbose:
        vis.show_amplitude_phase(Sr, Title='After range compression')

    logging.info("---Done!")
    logging.info("---Out range_compression.")

    return Sr


def second_range_compression2(Sr, fa, fr, Ds, Rb0, Fc, Vr, Win=None, ftshift=False, verbose=False):
    r"""Second Range Compression


    see `Second Range Compression <https://iridescent.ink/aitrace/Radar/SAR/Imaging/RangeDopplerAlgorithm.html#id11>`_

    Arguments
    ----------------------
    Sr : {ndarray}
        SAR raw data :math:`N_a×N_r` in time domain
    fa : {1darray}
        frequency array :math:`N_a×1` in zaimuth
    fr : {1darray}
        frequency array :math:`N_r×1` in range
    Ds : {ndarray}
        Migration factors :math:`N_a×N_r`
    Rb0 : {float number}
        smallest slant range (m) from radar to Scene Center
    Fc : {float number}
        center/carrier frequency (Hz)
    Vr : {float number}
        Velocity of radar platform
    Win : {string}, optional
        window type (the default is None, which [None])
    ftshift : {bool}, optional
        fft shift?
    verbose : {bool}, optional
        show more info (the default is False, which does not show)

    Returns
    -------
    Sr : {ndarray}
        data after second range compression
    """

    logging.info("---In second_range_compression...")

    Na, Nr = Sr.shape

    logging.info("~~~Generates filter...")

    fas = np.reshape(np.repeat(fa, Nr), (Na, Nr))
    frs = np.reshape(np.repeat(fr, Na), (Nr, Na)).transpose()

    FENMU = (C * Rb0 * (fas ** 2))
    FENMU = np.where(np.abs(FENMU) < EPS, EPS, FENMU)

    Ksrc = (2.0 * (Vr ** 2) * (Fc ** 3) * (Ds ** 3)) / FENMU
    Hsrc = np.exp(1j * PI * (frs ** 2) / Ksrc)
    logging.info("~~~Done!")

    logging.info("~~~Do second range compression...")

    Sr = Sr * Hsrc

    logging.info("~~~Done!")

    # field of range doppler
    logging.info("~~~Do IFFT in range...")

    Sr = ifft(Sr, axis=1, shift=ftshift)

    logging.info("~~~Done!")

    if verbose:
        vis.show_amplitude_phase(
            Sr, Title='After second range compression')

    logging.info("---Out second_range_compression.")

    return Sr, Ksrc, Hsrc


def range_migration_factor(fa, Fc, Vr, Nr, verbose=False):
    r"""range migration factor

    Compute range migration factor

    .. math::
        D(f_{\eta}, V_r) = \sqrt{1-\frac{c^2f_{\eta}^2}{4V_r^2f_0^2}} = \sqrt{1- \frac{\lambda^2f_{\eta}^2 }{4V_r^2}}
        :label: equ-RCMC_factor_RD

    Parameters
    ----------
    fa : {1darray}
        frequency array :math:`N_a×1` in zaimuth
    Fc : {float number}
        center/carrier frequency (Hz)
    Vr : {float number}
        Velocity of radar platform
    Nr : {float number}
        number of samples in range direction
    verbose : {bool}, optional
        show more info (the default is False, which does not show)

    Returns
    -------
    D : 1darray
        :math:`N_a×1` migration factor vector
    Ds : ndarray
        :math:`N_a×N_r` migration factor matrix
    """

    Wl = C / Fc
    Na = np.size(fa)

    D = np.sqrt(1.0 - ((Wl * fa) ** 2 / (4.0 * (Vr ** 2))))
    Ds = np.reshape(np.repeat(D, Nr), (Na, Nr))

    return D, Ds


def rcmc_sinc(Sr, deltaRCMs, r=None, verbose=False):
    r"""range migration correction with sinc interpolation

    range migration correction with sinc interpolation.

    see `sinc interpolation <https://iridescent.ink/aitrace/SignalProcessing/Digital/Basic/Interpolation/SincInterpolation.html>`_

    Parameters
    ----------
    Sr : {ndarray}
        SAR raw data :math:`N_a×N_r` in range dopplor domain
    deltaRCMs : {1darray}
        range migration :math:`N_r×1`
    r : {integer number}, optional
        kernel size for sinc interpolation (the default is None, which [r=8])
    verbose : {bool}, optional
        show more info, such as visualization (the default is False, which does not show)

    Returns
    -------
    Srrcmc
        data after range migration correction :math:`N_a×N_r`
    """
    logging.info("---In rcmc_sinc...")

    if r is None:
        r = 8
        logging.warning('~~~Using default kernel size %f' % r)

    Na, Nr = Sr.shape

    Srrcmc = np.zeros_like(Sr)

    M = deltaRCMs
    N = np.floor(M)
    P = M - N
    K = np.floor(N / (Nr / 2.0))
    N = np.mod(N, Nr / 2.0)

    K = K.astype('int')
    N = N.astype('int')

    deltaRCMs = None
    r2 = int(r / 2.0)
    offs = int(np.mean(N))
    maxN = np.max(N)
    NN = Nr - maxN - r2

    for i in range(Na):
        B = np.sinc(np.linspace(-P[i] - r2, -P[i] + r2, r))
        SB = np.sum(B)
        for j in range(r2, NN):
            k = j + N[i][0]
            kr2 = k - r2
            A = Sr[i, kr2:kr2 + r]
            Srrcmc[i, j + offs] = np.dot(A, B) / SB

    if verbose:
        vis.show_amplitude_phase(Srrcmc, Title='After RCMC')

    logging.info("~~~Done!")

    logging.info("---Out rcmc_sinc.")

    return Srrcmc


def rcmc_interp(Sr, tr, D, verbose=False):
    r"""range migration correction with linear interpolation

    [description]

    Parameters
    ----------
    Sr : {ndarray}
        SAR raw data :math:`N_a×N_r` in range dopplor domain
    tr : {1darray}
        time array :math:`N_r×1` in range
    D : 1darray
        :math:`N_a×1` migration factor vector
    verbose : {bool}, optional
        show more info (the default is False, which does not show)

    Returns
    -------
    Srrcmc
        data after range migration correction :math:`N_a×N_r`
    """

    logging.info("---In rcmc_interp...")

    if Sr.shape[1] != tr.shape[0]:
        raise ValueError('Sr has shape: ', Sr.shape,
                         'tr has shape: ', tr.shape)
    if Sr.shape[0] != D.shape[0]:
        raise ValueError('Sr has shape: ', Sr.shape,
                         'D has shape: ', D.shape)

    Srrcmc = np.zeros_like(Sr)

    logging.info("~~~Do linear interpolation...")

    for i in range(Srrcmc.shape[0]):
        tri = tr / D[i]
        Srrcmc[i, :] = np.interp(tri, tr, Sr[i, :])
        # Srrcmc[i, :] = iprs.interp(tri, tr, Sr[i, :])

    if verbose:
        vis.show_amplitude_phase(Srrcmc, Title='After RCMC')

    logging.info("~~~Done!")

    logging.info("---Out rcmc_interp.")
    return Srrcmc


def genRefPhase(fa, fr, f0, Rref, Vref, K, Tp, tZero=0, etaZero=0):
    r"""
    Phi_ref(f_eta, f_tau) = 4*pi*Rref/c * sqrt( (f0+f_tau)^2 - c^2 * f_eta^2 / (4*Vref^2) )
    - tZero corresponds to the 'zero' range time of the signal range time sampling. tZero = (tmax+tmin)/2
    - etaZero corresponds to the 'zero' azimuth time of the signal azimuth time sampling. etaZero = (etaMax+etaMin)/2

    """
    a = 4.0 * PI * Rref / C
    fRangeMax = np.abs(K) * Tp
    # fRangeMax = fr[-1]
    phase = np.zeros((len(fa), len(fr)), dtype=np.complex)
    for i, f in enumerate(fa):
        b = np.sqrt((f0 + fr)**2 - (0.5 * C * f / Vref)**2)
        c = PI * fr**2 / K
        d = 2.0 * PI * tZero * fr
        d2 = 2.0 * PI * etaZero * f
        phase[i, :] = sig.rect(fr / fRangeMax) * \
            np.exp(1j * a * b[:] + 1j * c[:] - 1j * d[:] - 1j * d2)
    return phase
