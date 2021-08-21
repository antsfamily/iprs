#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

import logging
from iprs.utils.const import *
from iprs.utils.io import savemat, loadmat
from iprs.misc import visual as vis

from iprs.dsp import normalsignals as sig

from .share import zeros_padding, range_matched_filtering, \
    range_compression, second_range_compression2, \
    range_migration_factor, rcmc_sinc, rcmc_interp
import matplotlib.pyplot as plt

from iprs.dsp.fft import fft, ifft, fftfreq


def rda_adv(Sr, sarplat, zpadar=False, usesrc=False, usedpc=True, rcmc=8, ftshift=False, verbose=True):
    r"""Range Doppler Algorithm

    Range Doppler Algorithm for SAR

    see `Range Dopplor Algorithm <https://iridescent.ink/aitrace/Radar/SAR/Imaging/RangeDopplerAlgorithm.html>`_

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
        Second Range Compression (if As is larger, enable this) (default: {False})
    usedpc : {bool}, optional
        Dopplor Phase Correction: False-->no DPC (default: {True})
    rcmc : {bool, integer}, optional
        Range Migration Correction: integer-->kernel size, False-->no rcmc (default: {8})
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
    Ka = sarplat.params['Ka']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    PRT = sarplat.params['PRT']
    fadc = sarplat.params['fadc']
    Tp = sarplat.sensor['Tp']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
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

    logging.info("===In rda_adv...")

    # ==================Alignment to Zero Doppler Center in azimuth
    logging.info("---Align to zero Doppler Center(azimuth)...")

    Hazc = np.exp(-1j * 2.0 * PI * fadc * ta)
    # Hazc = np.matmul(Hazc, np.ones((1, Nr)))
    Hazc = np.repeat(Hazc, Nr).reshape((Na, Nr))
    # Sr = Sr * Hazc

    logging.info("---Done!")

    if zpadar is None:
        Za = int(np.ceil(Tp * Fsa * 1e4))
        Zr = int(np.ceil(Tp * Fsr))
        zpadar = (Za, Zr)

    if zpadar:
        Za, Zr = zpadar
        Sr, fa, fr, ta, tr = zeros_padding(
            Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=verbose)

    Na, Nr = Sr.shape
    fr = np.reshape(fr, (Nr, 1))
    fa = np.reshape(fa, (Na, 1)) + fadc

    fas = np.reshape(np.repeat(fa, Nr), (Na, Nr))
    # frs = np.reshape(np.repeat(fr, Na), (Nr, Na)).transpose()

    logging.info("---Do range compression (RC)...")

    logging.info("~~~Do FFT in range (range dopplor domain)...")
    Sr = fft(Sr, axis=1, shift=ftshift)
    logging.info("~~~Done!")

    # Sr = range_matched_filtering(Sr, fr, Kr)

    Hrs = iprs.rect(tr / Tp) * np.exp(-1j * PI * Kr * tr**2)
    Hrs = fft(Hrs, axis=0, shift=ftshift)
    Hrs = np.reshape(np.repeat(Hrs, Na), (Nr, Na)).transpose()

    Sr = Sr * Hrs

    logging.info("---Done!")

    if not usesrc:
        logging.info("~~~Do IFFT in range...")
        Sr = ifft(Sr, axis=1, shift=ftshift)
        logging.info("~~~Done!")
        if verbose:
            vis.show_amplitude_phase(Sr, Title='After RC')

        logging.info("---Do FFT in azimuth (range dopplor domain)...")
        Sr = fft(Sr, axis=0, shift=ftshift)
        logging.info("---Done!")

    D, Ds = range_migration_factor(fa, Fc, Vr, Nr, verbose=False)

    if usesrc:

        if verbose:
            Sr1 = ifft(Sr, axis=1, shift=ftshift)
            vis.show_amplitude_phase(Sr1, Title='After RC')

        logging.info("---Do FFT in azimuth (2D frequency domain)...")
        Sr = fft(Sr, axis=0, shift=ftshift)
        logging.info("---Done!")

        logging.info("---Do second range compression (SRC)...")
        Sr, _, _ = second_range_compression2(  # way 2, RFAF
            Sr, fa, fr, Ds, R0, Fc, Vr, Win=None, ftshift=ftshift, verbose=False)
        logging.info("---Done!")

        if verbose:
            vis.show_amplitude_phase(Sr, Title='After SRC')
    if usedpc:
        logging.info("---Do dopplor phase compensation (DPC)...")
        Hdp = np.exp(1j * 2 * PI * fas * Yc / Vs)
        Sr = Sr * Hdp
        logging.info("---Done!")

    if verbose:
        vis.show_amplitude_phase(Sr, Title='After DPC')

    if rcmc:
        logging.info("---Do Range Cell Migration Correction (RCMC)...")
        Rref = ((tnear + tfar) / 2.0) * C / 2.0

        deltaR = (1.0 / Fsr) * C / 2.0
        deltaRCMs = Rref * (1.0 / D - 1.0)
        deltaRCMs = deltaRCMs / deltaR  # Quantification

        # Sr = rcmc_sinc(Sr, deltaRCMs, r=rcmc, verbose=verbose)
        Sr = rcmc_interp(Sr, tr, D, verbose=verbose)

    # =================azimuth compression
    # -----------------Step6: Filter in azimuth
    logging.info("---Do azimuth compression...")

    Has = np.exp(1j * 4 * PI * R0 * Ds * Fc / C)
    Sr = Sr * Has

    logging.info('---Done!')

    # -----------------Step7: IFFT in azimuth
    logging.info('---Do IFFT in azimuth...')
    SI = ifft(Sr, axis=0, shift=ftshift)
    Sr = None
    logging.info('---Done!')

    if verbose:
        vis.show_amplitude_phase(SI, Title='After azimuth compression')

    if zpadar:
        logging.info("---Abort Invalid Data...")
        SI = SI[Za:Na - Za, Zr:Nr - Zr]
        logging.info("---Done!")
    logging.info("---out rda_adv.")

    return SI


def rda_ss(Sr, sarplat, zpadar=False, usesrc=False, rcmc=False, afa=None, ftshift=False, verbose=True):
    r"""Range Doppler Algorithm for small squint SAR

    Range Doppler Algorithm for small squint SAR.

    Parameters
    ----------
    Sr : {numpy array}
        The SAR rawdata
    sarplat : {sarplat Object}
        SAR platform contains various parameters
    zpadar : {bool}, optional
        Zeros Padding at the end and Abort after RDA (default: {False})
    usesrc : {bool}, optional
        Second Range Compression (if :math:`\theta_s` is larger, enable this) (default: {False})
    rcmc : {integer or bool}, optional
        Range Migration Correction (default: {False})
    afa : {integer or bool}, optional
        Autofocus algorithm, ``'PGA'`` for phase gradient algorithm
        ``'MD'`` for map drift, ``ENT`` for entropy based autofocus.
    ftshift : {bool}, optional
        fft shift?
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
    SubBC = sarplat.params['SubBeamCenter']
    SubSC = sarplat.params['SubSceneCenter']
    Tsr = sarplat.params['Tsr']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    PRT = sarplat.params['PRT']
    fadc = sarplat.params['fadc']
    Nsar = sarplat.params['Nsar']
    Tp = sarplat.sensor['Tp']
    Ka = sarplat.params['Ka']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    La = sarplat.sensor['La']
    As = sarplat.acquisition['As']
    tnear = sarplat.params['tnearSub']
    tfar = sarplat.params['tfarSub']
    Rnear = sarplat.params['SubRnear']
    SubTsar = sarplat.params['SubTsar']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        Yc = SubBC[1]
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        Yc = SubSC[1]

    logging.info("===In rda...")

    if zpadar is None:
        Za = int(np.ceil(Tp * Fsa * 1e4))
        Zr = int(np.ceil(Tp * Fsr))
        zpadar = (Za, Zr)

    if zpadar:
        Za, Zr = zpadar
        Sr, fa, fr, ta, tr = zeros_padding(
            Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=verbose)

    Na, Nr = Sr.shape
    # fr = np.reshape(fr, (Nr, 1))
    # fa = np.reshape(fa, (Na, 1))

    # =================range compression
    # -----------------Step1: FFT in range
    logging.info("---Range Compression...")
    Sr = fft(Sr, axis=1, shift=ftshift)
    fadc, _ = iprs.bdce_sf(Sr, Fsa, rdflag=True, isplot=False)
    print(np.mean(fadc), "bdce_sf--------------------------------")
    # -------------Estimate doppler centroid
    logging.info("---Estimate doppler centroid using WDA...")
    fadc, fbdc, Ma, _ = iprs.abdce_wda(Sr, Fsa, Fsr, Fc, rate=0.8, isplot=False)

    # Rp = iprs.min_slant_range_with_migration(Fsr, Nr, Rnear, Wl, Vr, fadc)
    Rp = iprs.min_slant_range(Fsr, Nr, Rnear)
    D = np.sqrt(1. - ((Wl * fa)**2) / ((2 * Vr)**2))
    # print(Km.shape, D.shape, Ksrc.shape, Rp.shape, fa.shape)
    # -----------------Step2: Matched Filtering in range
    # Hr, _, _, ZL, ZR = iprs.chirp_mf_fd(Km, Tp, Fsr, Fc=0., t=None, N=Nr, mod='way2', ftshift=ftshift)  # Fc=0. for demodulated
    # if ZL < 0:
    #     Sr = np.hstack((np.zeros((Na, abs(ZL))), Sr, np.zeros((Na, abs(ZR)))))

    # Hsrc = 1.
    # if usesrc:
    #     Hr = Hr * Hsrc
    for n in range(Na):
        Ksrc = 2 * (Vr**2) * (Fc**3) * (D[n]**3) / (C * Rp * (fa[n] ** 2))
        Km = Kr / (1. - Kr / Ksrc)
        Hr, _, _, ZL, ZR = iprs.chirp_mf_fd(
            Km, Tp, Fsr, Fc=0., t=None, N=Nr, mod='way2', ftshift=ftshift)  # Fc=0. for demodulated

        Sr[n, :] = Sr[n, :] * Hr
    # Hrs = np.reshape(np.repeat(Hrs, Na), (Nr, Na)).transpose()
    # Hrs = np.matmul(np.ones((Na, 1)), Hrs.transpose())
    # Sr = Sr * Hrs

    logging.info("---Done!")

    # -----------------Step3: IFFT in range
    logging.info("---Do IFFT in range...")

    Sr = ifft(Sr, axis=1, shift=ftshift)
    if ftshift is False:
        Sr = np.fft.ifftshift(Sr, axes=1)
    logging.info("---Done!")

    if verbose:
        vis.show_amplitude_phase(Sr, Title='After range compression')

    # fadc = iprs.bdce_api(Sr, Fsa, isplot=True)
    # print(fadc, "bdce_api--------------------------------")

    # =================azimuth FFT (range dopplor)
    logging.info("---Do FFT in azimuth...")

    Sr = fft(Sr, axis=0, shift=ftshift)
    print(Sr.shape, Vr)

    logging.info("---Done!")
    D = np.sqrt(1.0 - (Wl ** 2) * (fa ** 2) / (4.0 * Vr ** 2))
    # =================RCMC
    # -----------------Step5: RCMC

    if rcmc:
        logging.info("---Do Range Cell Migration Correction (RCMC)...")
        # Rref = ((tnear + tfar) / 2.0) * C / 2.0
        Rref = Rc
        print(Rref, "Rref")

        deltaR = (1.0 / Fsr) * C / 2.0
        deltaRCMs = Rref * (1.0 / D - 1.0)
        deltaRCMs = deltaRCMs / deltaR  # Quantification

        # Sr = rcmc_sinc(Sr, deltaRCMs, r=rcmc, verbose=verbose)
        Sr = rcmc_interp(Sr, tr, D, verbose=False)

        if verbose:
            vis.show_amplitude_phase(Sr, Title='After RCMC')

    # =================azimuth compression
    # -----------------Step6: Filter in azimuth
    logging.info("---Azimuth Compression...")
    fadr = iprs.dre_geo(Wl, Vr, Rp)
    FPa = iprs.azimuth_footprint(Rp, Wl, La)
    Tpa = FPa / Vr
    # fadc = fbdc
    # Tpa = SubTsar
    for n in range(Nr):
        # Ha, _, _, ZL, ZR = iprs.chirp_mf_fd(Ka, SubTsar, Fsa, Fc=fadc, t=None, f=None, N=Na, mod='way2', ftshift=ftshift)
        Ha, _, _, ZL, ZR = iprs.chirp_mf_fd(
            fadr[n], Tpa[n], Fsa, Fc=fadc, t=None, f=None, N=Na, mod='way2', ftshift=ftshift)
        Sr[:, n] = Sr[:, n] * Ha

    logging.info('---Done!')

    # -----------------Step7: IFFT in azimuth
    logging.info('---Do IFFT in azimuth...')
    SI = ifft(Sr, axis=0, shift=ftshift)
    if ftshift is False:
        SI = np.fft.ifftshift(SI, axes=0)

    logging.info('---Done!')

    savemat('./data/Image_NoDopplerCorrection.mat', {'SI': SI}, fmt='5')

    if verbose:
        vis.show_amplitude_phase(SI, Title='After azimuth compression')

    if zpadar:
        logging.info("---Abort Invalid Data...")
        SI = SI[Za:Na - Za, Zr:Nr - Zr]
        logging.info("---Done!")

    if afa in ['ENT', 'ent']:
        SI = iprs.entropyaf(SI, pfunc=None, pinit=None, emod='Natural', optm='Nelder-Mead')
    if afa in ['PGA', 'pga']:
        SI, ephi = iprs.pgaf_sm(SI, Nsar, Nsub=None, windb=None, est='ML', Niter=20, tol=1.e-6)
    logging.info("===out rda.")

    return SI


def rda_ls(Sr, sarplat, zpadar=False, rcmc=False, afa=None, ftshift=False, verbose=True):
    r"""Range Doppler Algorithm for large squint SAR

    Range Doppler Algorithm for large squint SAR.

    Parameters
    ----------
    Sr : {numpy array}
        The SAR rawdata
    sarplat : {sarplat Object}
        SAR platform contains various parameters
    zpadar : {bool}, optional
        Zeros Padding at the end and Abort after RDA (default: {False})
    usesrc : {bool}, optional
        Second Range Compression (if :math:`\theta_s` is larger, enable this) (default: {False})
    rcmc : {integer or bool}, optional
        Range Migration Correction (default: {False})
    afa : {integer or bool}, optional
        Autofocus algorithm, ``'PGA'`` for phase gradient algorithm
        ``'MD'`` for map drift, ``ENT`` for entropy based autofocus.
    ftshift : {bool}, optional
        fft shift?
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
    SubBC = sarplat.params['SubBeamCenter']
    SubSC = sarplat.params['SubSceneCenter']
    Tsr = sarplat.params['Tsr']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    PRT = sarplat.params['PRT']
    fadc = sarplat.params['fadc']
    Nsar = sarplat.params['Nsar']
    Tp = sarplat.sensor['Tp']
    Ka = sarplat.params['Ka']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    La = sarplat.sensor['La']
    As = sarplat.acquisition['As']
    tnear = sarplat.params['tnearSub']
    tfar = sarplat.params['tfarSub']
    Rnear = sarplat.params['SubRnear']
    SubTsar = sarplat.params['SubTsar']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        Yc = SubBC[1]
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        Yc = SubSC[1]

    logging.info("===In rda...")

    if zpadar is None:
        Za = int(np.ceil(Tp * Fsa * 1e4))
        Zr = int(np.ceil(Tp * Fsr))
        zpadar = (Za, Zr)

    if zpadar:
        Za, Zr = zpadar
        Sr, fa, fr, ta, tr = zeros_padding(
            Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=verbose)

    Na, Nr = Sr.shape
    # fr = np.reshape(fr, (Nr, 1))
    fa = np.reshape(fa, (Na, 1))

    # =================range compression
    # -----------------Step1: FFT in range
    logging.info("---Range Compression...")
    Sr = fft(Sr, axis=1, shift=ftshift)
    fadc, _ = iprs.bdce_sf(Sr, Fsa, rdflag=True, isplot=False)
    print(np.mean(fadc), "bdce_sf--------------------------------")
    # -------------Estimate doppler centroid
    logging.info("---Estimate doppler centroid using WDA...")
    fadc, fbdc, Ma, _ = iprs.abdce_wda(Sr, Fsa, Fsr, Fc, rate=0.8, isplot=False)

    Rp = iprs.min_slant_range_with_migration(Fsr, Nr, Rnear, Wl, Vr, fadc)
    Rp = iprs.min_slant_range(Fsr, Nr, Rnear)
    # -----------------Step2: Matched Filtering in range
    Hr, _, _, ZL, ZR = iprs.chirp_mf_fd(Kr, Tp, Fsr, Fc=0., t=None, N=Nr, mod='way2',
                                        ftshift=ftshift)  # Fc=0. for demodulated
    if ZL < 0:
        Sr = np.hstack((np.zeros((Na, abs(ZL))), Sr, np.zeros((Na, abs(ZR)))))
    Hsrc = 1.
    if usesrc:
        Hr = Hr * Hsrc
    for n in range(Na):
        Sr[n, :] = Sr[n, :] * Hr
    # Hrs = np.reshape(np.repeat(Hrs, Na), (Nr, Na)).transpose()
    # Hrs = np.matmul(np.ones((Na, 1)), Hrs.transpose())
    # Sr = Sr * Hrs

    logging.info("---Done!")

    # -----------------Step3: IFFT in range
    logging.info("---Do IFFT in range...")

    Sr = ifft(Sr, axis=1, shift=ftshift)
    if ftshift is False:
        Sr = np.fft.ifftshift(Sr, axes=1)
    logging.info("---Done!")

    if verbose:
        vis.show_amplitude_phase(Sr, Title='After range compression')

    # fadc = iprs.bdce_api(Sr, Fsa, isplot=True)
    # print(fadc, "bdce_api--------------------------------")

    # =================azimuth FFT (range dopplor)
    logging.info("---Do FFT in azimuth...")

    Sr = fft(Sr, axis=0, shift=ftshift)
    print(Sr.shape, Vr)

    logging.info("---Done!")
    D = np.sqrt(1.0 - (Wl ** 2) * (fa ** 2) / (4.0 * Vr ** 2))
    # =================RCMC
    # -----------------Step5: RCMC

    if rcmc:
        logging.info("---Do Range Cell Migration Correction (RCMC)...")
        # Rref = ((tnear + tfar) / 2.0) * C / 2.0
        Rref = Rc
        print(Rref, "Rref")

        deltaR = (1.0 / Fsr) * C / 2.0
        deltaRCMs = Rref * (1.0 / D - 1.0)
        deltaRCMs = deltaRCMs / deltaR  # Quantification

        # Sr = rcmc_sinc(Sr, deltaRCMs, r=rcmc, verbose=verbose)
        Sr = rcmc_interp(Sr, tr, D, verbose=False)

        if verbose:
            vis.show_amplitude_phase(Sr, Title='After RCMC')

    # =================azimuth compression
    # -----------------Step6: Filter in azimuth
    logging.info("---Azimuth Compression...")
    fadr = iprs.dre_geo(Wl, Vr, Rp)
    FPa = iprs.azimuth_footprint(Rp, Wl, La)
    Tpa = FPa / Vr
    print(Ka, fadc)
    print(fadr)
    # fadc = fbdc
    # Tpa = SubTsar
    for n in range(Nr):
        # Ha, _, _, ZL, ZR = iprs.chirp_mf_fd(Ka, SubTsar, Fsa, Fc=fadc, t=None, f=None, N=Na, mod='way2', ftshift=ftshift)
        Ha, _, _, ZL, ZR = iprs.chirp_mf_fd(
            fadr[n], Tpa[n], Fsa, Fc=fadc, t=None, f=None, N=Na, mod='way2', ftshift=ftshift)
        Sr[:, n] = Sr[:, n] * Ha

    logging.info('---Done!')

    # -----------------Step7: IFFT in azimuth
    logging.info('---Do IFFT in azimuth...')
    SI = ifft(Sr, axis=0, shift=ftshift)
    if ftshift is False:
        SI = np.fft.ifftshift(SI, axes=0)

    logging.info('---Done!')

    savemat('./data/Image_NoDopplerCorrection.mat', {'SI': SI}, fmt='5')

    if verbose:
        vis.show_amplitude_phase(SI, Title='After azimuth compression')

    if zpadar:
        logging.info("---Abort Invalid Data...")
        SI = SI[Za:Na - Za, Zr:Nr - Zr]
        logging.info("---Done!")

    if afa in ['ENT', 'ent']:
        SI = iprs.entropyaf(SI, pfunc=None, pinit=None, emod='Natural', optm='Nelder-Mead')
    if afa in ['PGA', 'pga']:
        SI, ephi = iprs.pgaf_sm(SI, Nsar, Nsub=None, windb=None, est='ML', Niter=20, tol=1.e-6)
    logging.info("===out rda.")

    return SI


def rda(Sr, sarplat, zpadar=False, rcmc=False, afa=None, ftshift=False, verbose=True):
    r"""Range Doppler Algorithm for zero squint SAR

    Range Doppler Algorithm for zero squint SAR.

    Parameters
    ----------
    Sr : {numpy array}
        The SAR rawdata
    sarplat : {sarplat Object}
        SAR platform contains various parameters
    zpadar : {bool}, optional
        Zeros Padding at the end and Abort after RDA (default: {False})
    rcmc : {integer or bool}, optional
        Range Migration Correction (default: {False})
    afa : {integer or bool}, optional
        Autofocus algorithm, ``'PGA'`` for phase gradient algorithm
        ``'MD'`` for map drift, ``ENT`` for entropy based autofocus.
    ftshift : {bool}, optional
        fft shift?
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
    SubBC = sarplat.params['SubBeamCenter']
    SubSC = sarplat.params['SubSceneCenter']
    SubSC = sarplat.params['SubSceneCenter']
    Tsr = sarplat.params['Tsr']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    PRT = sarplat.params['PRT']
    fadc = sarplat.params['fadc']
    Nsar = sarplat.params['Nsar']
    Tp = sarplat.sensor['Tp']
    Ka = sarplat.params['Ka']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    La = sarplat.sensor['La']
    As = sarplat.acquisition['As']
    tnear = sarplat.params['tnearSub']
    tfar = sarplat.params['tfarSub']
    Rnear = sarplat.params['SubRnear']
    SubTsar = sarplat.params['SubTsar']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        Yc = SubBC[1]
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        Yc = SubSC[1]

    logging.info("===In rda...")

    if zpadar is None:
        Za = int(np.ceil(Tp * Fsa * 1e4))
        Zr = int(np.ceil(Tp * Fsr))
        zpadar = (Za, Zr)

    if zpadar:
        Za, Zr = zpadar
        Sr, fa, fr, ta, tr = zeros_padding(
            Sr, fa, fr, ta, tr, Tp, Za, Zr, verbose=verbose)

    Na, Nr = Sr.shape
    # fr = np.reshape(fr, (Nr, 1))
    fa = np.reshape(fa, (Na, 1))

    # =================range compression
    # -----------------Step1: FFT in range
    logging.info("---Range Compression...")

    Nh = round(Fsr * Tp)
    Nfft = 2 ** iprs.nextpow2(Nr + Nh - 1)
    print(Sr.shape, Nfft, Nh)
    Sr = iprs.padfft(Sr, Nfft=Nfft, axis=1, shift=ftshift)
    Sr = fft(Sr, Nfft, axis=1, shift=ftshift)
    fadc, _ = iprs.bdce_sf(Sr, Fsa, rdflag=True, isplot=False)
    fadc = np.mean(fadc)
    print(np.mean(fadc), "bdce_sf--------------------------------")
    # -------------Estimate doppler centroid
    logging.info("---Estimate doppler centroid using WDA...")
    fadc, fbdc, Ma, _ = iprs.abdce_wda(Sr, Fsa, Fsr, Fc, rate=0.8, isplot=False)

    Noff = np.linspace(0, Nr, Nr)
    # Rp = iprs.min_slant_range_with_migration(Fsr, Noff, Rnear, Wl, Vr, fadc)
    Rp = iprs.min_slant_range(Fsr, Noff, Rnear)
    # -----------------Step2: Matched Filtering in range
    Hr, f = iprs.chirp_mf_fd(Kr, Tp, Fsr, Fc=0., Nfft=Nfft, mod='way1', win=None, ftshift=ftshift)  # Fc=0. for demodulated
    if verbose:
        plt.figure()
        plt.subplot(121)
        plt.plot(np.real(Hr))
        plt.title('real part of range matched filter')
        plt.subplot(122)
        plt.plot(np.imag(Hr))
        plt.title('imag part of range matched filter')
        plt.show()

    for n in range(Na):
        Sr[n, :] = Sr[n, :] * Hr

    logging.info("---Done!")

    # -----------------Step3: IFFT in range
    logging.info("---Do IFFT in range...")

    Sr = ifft(Sr, axis=1, shift=ftshift)
    Sr = iprs.mfpc_throwaway(Sr, Nr, Nh, axis=1, mffdmod='way1', ftshift=ftshift)

    if ftshift is False:
        Sr = np.fft.ifftshift(Sr, axes=1)
    logging.info("---Done!")

    if verbose:
        vis.show_amplitude_phase(Sr, Title='After range compression')

    # fadc = iprs.bdce_api(Sr, Fsa, isplot=True)
    # print(fadc, "bdce_api--------------------------------")

    # =================azimuth FFT (range dopplor)
    logging.info("---Do FFT in azimuth...")

    Sr = fft(Sr, axis=0, shift=ftshift)
    print(Sr.shape, Vr)

    logging.info("---Done!")
    D = np.sqrt(1.0 - (Wl ** 2) * (fa ** 2) / (4.0 * Vr ** 2))
    # =================RCMC
    # -----------------Step5: RCMC

    if rcmc:
        logging.info("---Do Range Cell Migration Correction (RCMC)...")
        # Rref = ((tnear + tfar) / 2.0) * C / 2.0
        Rref = Rc
        print(Rref, "Rref")

        deltaR = (1.0 / Fsr) * C / 2.0
        deltaRCMs = Rref * (1.0 / D - 1.0)
        deltaRCMs = deltaRCMs / deltaR  # Quantification

        # Sr = rcmc_sinc(Sr, deltaRCMs, r=rcmc, verbose=verbose)
        Sr = rcmc_interp(Sr, tr, D, verbose=False)

        if verbose:
            vis.show_amplitude_phase(Sr, Title='After RCMC')

    # =================azimuth compression
    # -----------------Step6: Filter in azimuth
    logging.info("---Azimuth Compression...")
    fadr = iprs.dre_geo(Wl, Vr, Rp)
    FPa = iprs.azimuth_footprint(Rp, Wl, La)
    Tpa = FPa / Vr / 4.
    print(Ka, fadc)
    print(np.mean(FPa))
    print(fadr)
    print(Tpa)
    # fadc = fbdc
    # fadc = 0.
    # Tpa = SubTsar
    for n in range(Nr):
        Ha, _ = iprs.chirp_mf_fd(fadr[n], Tpa[n], Fsa, Fc=fadc, Nfft=Na, mod='way2', win=None, ftshift=ftshift)
        Sr[:, n] = Sr[:, n] * Ha

    logging.info('---Done!')

    # -----------------Step7: IFFT in azimuth
    logging.info('---Do IFFT in azimuth...')
    SI = ifft(Sr, axis=0, shift=ftshift)
    if ftshift is False:
        SI = np.fft.ifftshift(SI, axes=0)

    logging.info('---Done!')

    savemat('./data/Image_NoDopplerCorrection.mat', {'SI': SI}, fmt='5')

    if verbose:
        vis.show_amplitude_phase(SI, Title='After azimuth compression')

    if zpadar:
        logging.info("---Abort Invalid Data...")
        SI = SI[Za:Na - Za, Zr:Nr - Zr]
        logging.info("---Done!")

    if afa in ['ENT', 'ent']:
        SI = iprs.entropyaf(SI, pfunc=None, pinit=None, emod='Natural', optm='Nelder-Mead')
    if afa in ['PGA', 'pga']:
        SI, ephi = iprs.pgaf_sm(SI, Nsar, Nsub=None, windb=None, est='ML', Niter=20, tol=1.e-6)
    logging.info("===out rda.")

    return SI


def rda0(Sr, sarplat, verbose=True):
    r"""Apply Range-Doppler imaging algorithm on raw data

    1. Range compression

    2. Range Cell Migration Correction

    3. Azimuth compression


    Parameters
    ----------
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

    if Sr is None:
        print("No raw data!")

    Na, Nr = Sr.shape
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']
    fa = sarplat.params['faSub']
    fr = sarplat.params['frSub']

    SubRb0 = sarplat.params['SubRb0']
    SubRbc = sarplat.params['SubRbc']
    SubRs0 = sarplat.params['SubRs0']
    SubRsc = sarplat.params['SubRsc']
    SubBC = sarplat.params['SubBeamCenter']
    SubSC = sarplat.params['SubSceneCenter']
    SubSC = sarplat.params['SubSceneCenter']
    Tsr = sarplat.params['Tsr']
    Fsr = sarplat.params['Fsr']
    Fsa = sarplat.params['Fsa']
    PRT = sarplat.params['PRT']
    fadc = sarplat.params['fadc']
    Nsar = sarplat.params['Nsar']
    Tp = sarplat.sensor['Tp']
    Ka = sarplat.params['Ka']
    Kr = sarplat.sensor['Kr']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    La = sarplat.sensor['La']
    As = sarplat.acquisition['As']
    tnear = sarplat.params['tnearSub']
    tfar = sarplat.params['tfarSub']
    Rnear = sarplat.params['SubRnear']
    SubTsar = sarplat.params['SubTsar']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        Yc = SubBC[1]
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        Yc = SubSC[1]

    etas = ta
    # ==================Alignment to Zero Doppler Center in azimuth
    if verbose:
        print("===Alignment to Zero Doppler Center in azimuth...")
    hh = np.exp(-1j * 2.0 * np.pi * fadc * etas)
    Has = np.reshape(np.repeat(hh, Nr), (Na, Nr))
    Sr = Sr * Has

    fr = np.array(np.linspace(-Fsr / 2.0, Fsr / 2.0, Nr))  # [Nr,]
    fa = np.array(np.linspace(-Fsa / 2.0, Fsa / 2.0, Na)) - fadc  # [Na,]
    # fa = np.array(np.linspace(-Fsa / 2.0, Fsa / 2.0, Na))  # [Na,]

    # =================Squint Processing=====================
    Rsq = -V * np.sin(As) * ta
    Hsq = np.zeros((Na, Nr), Sr.dtype)

    for n in range(Na):
        Hsq[n, :] = np.exp(1j * 4 * PI * Rsq[n] * (fr + Fc) / C)

    Sr = fft(Sr, axis=0, shift=True)
    Sr = Sr * Hsq
    Sr = ifft(Sr, axis=0, shift=True)

    # =================step1: range compression===========
    if verbose:
        print("Do Range Compression ...")

    hmf = sig.rect(fr / (np.abs(Kr) * Tp)) * np.exp(1j * PI * (fr ** 2) / Kr)

    Hrs = np.reshape(np.repeat(hmf, Na), (Nr, Na)).transpose()

    Sr = fft(Sr, axis=1, shift=True)

    Sr_rc = Sr * Hrs
    Sr_rc = ifft(Sr_rc, axis=1, shift=True)

    hmf = None
    if verbose:
        print("Range Compression done!")
        vis.show_response(Sr_rc, None, "After Range Compression")

    # =================step2: Azimuth FFT===============
    if verbose:
        print("Do Azimuth FFT ...")
    Sr_af = fft(Sr_rc, axis=0, shift=True)
    Sr_rc = None
    if verbose:
        print("Azimuth FFT done!")
        # showResponse(Sr_af, [self._tArray[0], self._tArray[-1], fArray[0],
        # fArray[-1]], 'Azimuth FFT')
        vis.show_response(Sr_af, None, 'After Azimuth FFT')

    # =======================step3: Range migration======================
    if verbose:
        print("Do Range Migration ...")
    Dfreq = np.sqrt(1.0 - (0.5 * Wl * fa / V) ** 2)
    # Sr_rm = range_migration2(Sr_af, tr, Dfreq)
    Sr_rm = Sr_af
    Sr_af = None

    if verbose:
        print("Range Migration Done!")
        # showResponse(Sr_rc, [self._tArray[0], self._tArray[-1], fArray[0],
        # fArray[-1]], 'RCMC')
        vis.show_response(Sr_rm, None, 'RCMC')

    # =======================step4: Azimuth compression====================
    if verbose:
        print("Do Azimuth Compression ...")

    etaZero = ta[len(ta) // 2] / V

    for i in range(Sr_rm.shape[1]):
        # Use H(f) = exp( 1j * 4 * pi * R0 * D(f) * f0 / c )
        # HMF = np.exp(2 * PI * 1j * C * tr[i] / Wl * Dfreq)
        # Multiply by a phase due to different azimuth zero time
        # HMF = HMF * np.exp(-1j * 2.0 * PI * fa * etaZero)
        Ka = (2 * V ** 2) / (Wl * R0)
        HMF = np.exp(-1j * (PI * fa ** 2) / Ka)

        # print("classical.py --> Sr_rm.shape, HMF.shape: ", Sr_rm.shape,
        # HMF.shape)
        Sr_rm[:, i] = Sr_rm[:, i] * HMF

    if verbose:
        print("Azimuth Compression Done!")
        vis.show_response(Sr_rm, None, 'After Azimuth compression')

    # =======================step5: Azimuth IFFT====================
    if verbose:
        print("Do Azimuth IFFT ...")

    Sr_af = np.zeros(Sr_rm.shape, dtype=complex)
    Sr_rd = ifft(Sr_af, axis=0, shift=True)
    Sr_af = None

    if verbose:
        print("Azimuth IFFT Done!")
        # vis.show_response(Sr_rd, None, 'After Azimuth IFFT')
        vis.show_response(Sr_rd, [tr[0], tr[-1], fa[0], fa[-1]],
                          'Reconstructed Image using RD', False)

    return Sr_rd
