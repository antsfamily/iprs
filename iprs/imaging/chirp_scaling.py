#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.fft import *

import logging
from ..utils.const import *
from ..misc import visual as vis
from .share import zeros_padding


def printmmv(name, value):
    print(name, value.shape, value[0:4], value.min(), value.max())


def csa_adv(Sr, sarplat, zpadar=False, usesrc=True, rcmc=None, usedpc=True, verbose=False):
    r"""Chirp Scaling Algorithm

    Chirp Scaling Imaging for SAR

    see `Chirp Scaling Algorithm <https://iridescent.ink/aitrace/Radar/SAR/Imaging/ChirpScalingAlgorithm.html>`_

    Parameters
    ----------
    Sr : {numpy array}
        The SAR rawdata
    sarplat : {sarplat Object}
        SAR platform contains various parameters
    zpadar : {bool, tulpe, None}, optional
        Zeros Padding at the end and Abort after RDA:
        zpadar=(Za, Zr), None-->auto compute, False-->no padding (default: {False})
    usesrc : {bool}, optional
        Second Range Compression (if As is larger, enable this) (default: {True})
    rcmc : {bool, integer}, optional
        Range Migration Correction: integer-->kernel size, False-->no rcmc (default: {False})
    usedpc : {bool}, optional
        Dopplor Phase Correction: False-->no DPC (default: {True})
    verbose : {bool}, optional
        display processing info (default: {True})

    Returns
    -------
    SI : numpy array
        Image of complex value.
    """

    Na, Nr = Sr.shape
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']
    fa = sarplat.params['faSub']
    fr = sarplat.params['frSub']

    SubRb0 = sarplat.params['SubRb0']
    SubRbc = sarplat.params['SubRbc']
    SubRs0 = sarplat.params['SubRs0']
    SubRsc = sarplat.params['SubRsc']
    SubSC = sarplat.params['SubSceneCenter']
    SubBC = sarplat.params['SubBeamCenter']
    Bdop = sarplat.params['Bdop']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    Ka = sarplat.params['SubKa']
    fadc = sarplat.params['fadc']
    Tp = sarplat.sensor['Tp']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vg = sarplat.sensor['Vg']
    Vr = sarplat.sensor['Vr']
    Vs = sarplat.sensor['Vs']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    As = sarplat.acquisition['As']
    tnear = sarplat.params['tnearSub']
    tfar = sarplat.params['tfarSub']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        Yc = SubBC[1]
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        Yc = SubSC[1]

    ta = np.reshape(ta, (Na, 1))

    logging.info("===In csa_adv")

    if zpadar is None:
        Za = int(np.ceil(Tp * Fsa * 1e4))
        Zr = int(np.ceil(Tp * Fsr))
        zpadar = (Za, Zr)

    if zpadar:
        Za, Zr = zpadar
        Sr, fa, fr, ta, tr = zeros_padding(
            Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=verbose)

    Na, Nr = Sr.shape
    # ta = ta + ta[-1]
    # fa = fa + fa[-1]
    # fr = fr + fr[-1]
    ta = np.reshape(ta, (Na, 1))
    fr = np.reshape(fr, (Nr, 1))
    fa = np.reshape(fa, (Na, 1)) + fadc
    # print(fr.shape, fa.shape, ta.shape, tr.shape)

    # ==================Align to Zero Doppler Center in azimuth
    logging.info("---Align to zero Doppler Center(azimuth)...")
    Haz = np.exp(-1j * 2.0 * PI * fadc * np.matmul(ta, np.ones((1, Nr))))
    Sr = Sr * Haz
    # printmmv("Sr", Sr)

    logging.info("---Done!")

    # print(fadc, Vr)

    # =================Step1: FFT in azimuth (In RD domain)
    logging.info("---Do FFT in azimuth...")

    # Sr = fft(Sr, axis=0)
    Sr = fftshift(fft(fftshift(Sr, axes=0), axis=0), axes=0)
    logging.info("---Done!")

    # -----------------Step2: Chirp Scaling
    logging.info("---Do Chirp Scaling...")
    Rref = ((tnear + tfar) / 2.0) * C / 2.0
    Rref = Rc
    Vref = Vr
    faref = fadc
    # print(fa.shape, faref.shape)

    print("Rref", Rref)
    print("Vref", Vref)
    print("faref", faref)

    DfaV = np.sqrt(1. - ((Wl * fa)**2) / (4.0 * (V**2)))
    DfaVref = np.sqrt(1. - ((Wl * fa)**2) / (4.0 * (Vref**2)))
    DfarefV = np.sqrt(1. - ((Wl * faref)**2) / (4.0 * (V**2)))
    DfarefVref = np.sqrt(1. - ((Wl * faref)**2) / (4.0 * (Vref**2)))
    # printmmv("DfaV", DfaV)
    # printmmv("DfaVref", DfaVref)
    # print(faref.shape, DfarefVref.shape, "+++++")

    FENMU = (C * R0 * (fa ** 2))
    FENMU = np.where(np.abs(FENMU) < EPS, EPS, FENMU)
    Ksrc = (2.0 * (V ** 2) * (Fc ** 3) * (DfaV ** 3)) / FENMU
    Km = Kr / (1.0 - Kr / Ksrc)
    RCMbulk = Rref / DfaVref - Rref / DfarefVref
    # printmmv("DfaV", DfaV)
    # printmmv("Ksrc", Ksrc)
    # printmmv("Km", Km)
    # printmmv("RCMbulk", RCMbulk)

    tau = (2. / C) * (R0 / DfarefV + RCMbulk)
    taudiff = tau - (2. * Rref) / (C * DfaVref)
    alpha = DfarefVref / DfaVref - 1.0

    Hsrc = np.exp(1j * PI * Km * alpha * (taudiff**2))
    # printmmv("tau", tau)
    # printmmv("alpha", alpha)
    # printmmv("Hsrc", Hsrc)
    # print(Sr.shape, Hsrc.shape, Km.shape, alpha.shape, taudiff.shape, Ksrc.shape, fa.shape, DfaVref.shape, "+++++")
    Sr = Sr * (np.matmul(Hsrc, np.ones((1, Nr))))
    Hsrc = None
    logging.info('---Done!')

    # -----------------Step3: FFT in range
    logging.info("---Do FFT in range...")
    # Sr = fft(Sr, axis=1)
    Sr = fftshift(fft(fftshift(Sr, axes=1), axis=1), axes=1)
    logging.info("---Done!")

    # -----------------Step4: RC, SRC, RCMC
    logging.info("---Do RC, SRC...")
    Hm = np.exp(1j * PI * np.matmul(np.ones((Na, 1)), fr.transpose())**2 /
                (np.matmul(Km, np.ones((1, Nr))) *
                    (1 + np.matmul(alpha, np.ones((1, Nr))))))

    Sr = Sr * Hm
    Hm = None

    logging.info("---Done!")

    Title = 'After RC, SRC'
    if rcmc:
        Hrcmc = np.exp(1j * 4 * PI * (np.matmul(RCMbulk, np.ones((1, Nr)))) *
                       (np.matmul(np.ones((Na, 1)), fr.transpose())) / C)
        logging.info("---Do RCMC...")
        Sr = Sr * Hrcmc
        Hrcmc = None
        logging.info("---Done!")
        Title = 'After RC, SRC and RCMC'

    # -----------------Step5: IFFT in range
    logging.info("---Do IFFT in range...")

    # Sr = ifft(Sr, axis=1)
    Sr = ifftshift(ifft(ifftshift(Sr, axes=1), axis=1), axes=1)

    logging.info("---Done!")
    if verbose:
        vis.show_amplitude_phase(Sr, Title=Title)

    if usedpc:
        logging.info("---Do dopplor phase compensation (DPC)...")
        Hdp = np.exp(1j * 2 * PI * fa * Yc / Vr)
        Sr = Sr * np.matmul(Hdp, np.ones((1, Nr)))
        logging.info("---Done!")

        if verbose:
            vis.show_amplitude_phase(Sr, Title='After DPC')

    # -----------------Step6: azimuth compression
    logging.info("---Do azimuth compression...")

    Hac = np.exp(1j * 4 * PI * R0 * Fc * DfaV / C)
    Hpc = np.exp(-1j * 4 * PI * (Km / (C**2)) *
                 (1.0 - DfaVref / DfarefVref) * (R0 / DfaV - Rref / DfaV)**2)

    Sr = Sr * np.matmul(Hac, np.ones((1, Nr)))
    Sr = Sr * np.matmul(Hpc, np.ones((1, Nr)))

    logging.info("---Done!")

    # -----------------Step7: IFFT in azimuth
    logging.info("---Do IFFT in azimuth...")

    # SI = ifft(Sr, axis=0)
    SI = ifftshift(ifft(ifftshift(Sr, axes=0), axis=0), axes=0)
    Sr = None

    logging.info("---Done!")

    if verbose:
        vis.show_amplitude_phase(SI, Title='After azimuth compression')

    if zpadar:
        logging.info("---Abort Invalid Data...")
        SI = SI[Za:Na - Za, Zr:Nr - Zr]
        logging.info("---Done!")

    logging.info("===Out csa_adv!")

    return SI


def csa(Sr, sarplat, verbose=True):

    V = sarplat.sensor['V']
    Wl = sarplat.sensor['Wl']
    Wl = sarplat.sensor['Wl']
    Kr = sarplat.sensor['Kr']
    Fc = sarplat.sensor['Fc']

    Rb0 = sarplat.params['Rb0']
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']
    fa = sarplat.params['faSub']
    fr = sarplat.params['frSub']
    Fs = sarplat.params['Fs']
    PRF = sarplat.params['PRF']

    Na, Nr = Sr.shape

    R = np.array([tr]) * C / 2

    D = 1.0 / np.sqrt(1 - (Wl * fa / 2.0 / V)**2)  # [1, Na]
    alp = 1.0 / D - 1  # [1, Na]
    Km = Kr / (1 - Kr * Wl * Rb0 * (fa**2) / 2.0 /
               (V * V) / (Fc * Fc) / (D**3))  # [1, Na]
    # print(Na, tr.shape, D.shape, "====")
    tau = np.ones((Na, 1)) * tr - \
        (2 * Rb0 / C / D.transpose()) * np.ones((1, Nr))
    Ssc = np.exp(1j * PI * (Km * alp).transpose() *  # [Na, Nr]
                 np.ones((1, Nr)) * (tau**2))
    Sr_rA = tsfm.fftx(Sr)  # [Na, Nr]
    Sr_sc = Sr_rA * Ssc  # [Na, Nr]

    Sr_RA = tsfm.ffty(Sr_sc)  # [Na, Nr]
    # print(Ssc.shape, Sr_rA.shape, Sr_sc.shape, Sr_RA.shape)

    # [Na, Nr]
    rangeMod_phase = PI * (D / Km).transpose() * \
        np.ones((1, Nr)) * (np.ones((Na, 1)) * (fr**2))
    # [Na, Nr]
    cs_bulk_phase = (4.0 * PI * Rb0 / C) * alp.transpose() * \
        np.ones((1, Nr)) * (np.ones((Na, 1)) * fr)
    # [Na, Nr]
    Sr_RA_cor = Sr_RA * np.exp(1j * (rangeMod_phase + cs_bulk_phase))
    # print(rangeMod_phase.shape, cs_bulk_phase.shape, Sr_RA_cor.shape)
    Sr_rA1 = tsfm.iffty(Sr_RA_cor)  # [Na, Nr]

    # [Na, Nr]
    dop_phase = (-4 * PI / Wl) * (np.ones((Na, 1)) * R) * \
        (D.transpose() * np.ones((1, Nr)))
    phase_cor = (-4 * PI / (C * C)) * (Km * (1 - D) / (D**2)).transpose() * \
        np.ones((1, Nr)) * (np.ones((Na, 1)) * (Rb0 - R)**2)
    Sr_rA_cor = Sr_rA1 * np.exp(1j * (dop_phase + phase_cor))
    # Sr_rA_cor = Sr_rA1 * np.exp(1j * (dop_phase))
    Sr_ra = tsfm.ifftx(Sr_rA_cor)  # [Na, Nr]
    return Sr_ra
