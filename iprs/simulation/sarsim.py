#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.fft import fft, fftshift, ifftshift, fft2, ifft, ifft2

import logging
from ..utils.const import *

from ..dsp.normalsignals import rect, chirp
from ..dsp.noise import imnoise, matnoise
from iprs.sharing.range_azimuth_beamwidth_footprint import azimuth_footprint
from .sar_impulse_response import sarir
from .gentargets import img2tgs
from skimage import filters

import matplotlib.pyplot as plt

from iprs.utils.image import imresize


def tgs2rawdata(sarplat, targets, noise=None, SNR=None, verbose=False):
    r"""Generates echoes of point targets.

    Generates SAR raw data of point targets.

    Parameters
    ----------
    sarplat : {``SarPlat``}
        sar plat class, see `sarplat.py` or documentation
    targets : {``ndarray`` or ``lists``}
        targets: [[x1, y1, vx1, vy1, ax1, ay1, rcs1], ..., [xn, yn, vxn, vyn, axn, ayn, rcsn]], target: [x, y, vx, vy, ax, ay, rcs].
    noise : {``str``}, optional
        noise type added to gray image, 'awgn': (default: {None})
    SNR : {``number``}, optional
        signal to noise level (default: {None})
    verbose : {bool}, optional
        display log info (default: {False})

    Returns
    -------
    Sr : { ``2-darray`` }
        [azimuth, range], raw data signal of point targets.
    """

    logging.info("---In tgs2rawdata...")

    if targets is None:
        raise ValueError("targets should not be empty！")
        return None

    Na = sarplat.params['SubNa']
    Nr = sarplat.params['SubNr']
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']

    SubRb0 = sarplat.params['SubRb0']
    SubRbc = sarplat.params['SubRbc']
    SubRs0 = sarplat.params['SubRs0']
    SubRsc = sarplat.params['SubRsc']
    SubSC = sarplat.params['SubSceneCenter']
    SubBC = sarplat.params['SubBeamCenter']

    DX = sarplat.params['DX']
    DY = sarplat.params['DY']
    FPr = sarplat.params['FPr']
    FPa = sarplat.params['FPa']
    BWa = sarplat.params['BWa']
    tac = sarplat.params['tac']
    V = sarplat.sensor['V']
    Vs = sarplat.sensor['Vs']
    Vr = sarplat.sensor['Vr']
    Vg = sarplat.sensor['Vg']
    H = sarplat.sensor['H']
    Tp = sarplat.sensor['Tp']
    Fc = sarplat.sensor['Fc']
    Kr = sarplat.sensor['Kr']
    La = sarplat.sensor['La']
    Wl = sarplat.sensor['Wl']
    As = sarplat.acquisition['As']
    GM = sarplat.params['GeometryMode']

    if GM == 'BG':
        R0 = SubRb0
        Rc = SubRbc
        SC = SubBC
    if GM == 'SG':
        R0 = SubRs0
        Rc = SubRsc
        SC = SubSC

    FPa = azimuth_footprint(Rc, Wl, La)
    Sr = np.zeros((Na, Nr), dtype=complex)

    targets = np.array(targets)
    targets = targets.astype('float')
    targets[:, 0] = targets[:, 0] + SC[0]
    targets[:, 1] = targets[:, 1] + SC[1]

    trs = np.repeat(tr, Na).reshape(Nr, Na).transpose()  # [Na, Nr]
    # tas = np.repeat(ta, Nr).reshape(Na, Nr)  # [Na, Nr]

    BWa = iprs.azimuth_beamwidth(Wl, La)

    cnt = 0

    nTGs = np.size(targets, 0)
    # t2s = 0.5 * (tas ** 2)
    t2 = 0.5 * (ta ** 2)

    logging.info('---Generates SAR echo data...')
    for target in targets:
        cnt = cnt + 1
        if cnt % ((nTGs // 10) + 1) == 0:
            logging.info("~~~%d-th target of %d total targets" % (cnt, nTGs))

        x0, y0, vx, vy, ax, ay, G0 = target

        x = x0 + vx * ta + ax * t2  # [Na, 1]
        y = y0 + vy * ta + ay * t2 - Vr * ta  # [Na, 1]

        # print(vx, vy)
        R = np.sqrt(x ** 2 + y ** 2 + H ** 2)  # [Na, 1]
        # R = np.sqrt(R0**2 + (Vr * ta)**2)

        RC2 = 2 * R / C
        RC2 = np.repeat(RC2, Nr).reshape(Na, Nr)  # [Na, Nr]

        phase1 = -2j * PI * Fc * RC2
        phase2 = 1j * PI * Kr * (trs - RC2) ** 2  # [Na, Nr]

        FPa = azimuth_footprint(R, Wl, La)

        Wa = np.sinc((ta * Vr - y0) / FPa)  # [Na, 1]
        # Wa = np.sinc(0.886 * np.arctan((ta - tac) * Vr / Rc) / BWa)  # unwork, azimuth shift
        # Wa = np.sinc(0.886 * np.arctan((ta * Vg - y0) / R0) / BWa)
        Wa = Wa ** 2
        Wa = np.repeat(Wa, Nr).reshape(Na, Nr)  # [Na, Nr]

        Wr = rect((trs - RC2) / Tp)  # [Na, Nr]

        G = G0 * Wa * Wr
        # G = G0 * Wa

        # plt.figure()
        # plt.subplot(121)
        # plt.imshow(np.abs(Wa * Wr))
        # plt.subplot(122)
        # plt.imshow(20 * np.log10(np.abs(np.fft.fft(Wa * Wr))))
        # plt.show()

        # demodulated signal
        Sr += G * np.exp(phase1 + phase2)

    if(noise is not None) and (SNR is not None):
        logging.info('~~~Add %s noise to echo...')

        Sr = matnoise(Sr, noise=noise, imp=None, SNR=SNR)

        logging.info('~~~Done!')

    logging.info('---Done!')

    logging.info("---Out tgs2rawdata.")

    return Sr, ta, tr


def img2echo(sarplat, grayimg, bg=0., TH=None, noise=None, SNR=30, h=None, verbose=None):
    """image to SAR echo

    image to SAR echo (frequency domain method)

    Parameters
    ----------
    sarplat : {``SarPlat``}
        see `sarplat.py` or documentation
    grayimg : {``2d-array``}
        gray image with size of (H, W)
    TH : {float}, optional
        threshold for obtain foreground targets (default: {None}, otsu)
    noise : {``string``}, optional
        'awgn': white Gaussian noise (default: {None})
    SNR : {``float``}, optional
        signal to noise ratio (default: 30dB)
    h : {1d or 2d array}, optional
        impulse response, (default None, auto-generated)
    verbose : {bool}, optional
        show log info (default: {False})
    """

    logging.info("---In img2echo...")

    har = sarir(sarplat, mod='ar', ver=verbose)

    SA = sarplat.selection['SubSceneArea']

    gdshape = sarplat.selection['SubEchoSize']

    grayimg = np.flipud(grayimg)

    if np.ndim(grayimg) == 3:
        grayimg = np.mean(grayimg, axis=2)
    if noise is 'awgn':
        grayimg = matnoise(grayimg, noise='wgn', imp=1.0, SNR=SNR)

    if bg == 1.0:
        grayimg = 1.0 - grayimg

    if TH is None:
        TH = filters.threshold_otsu(grayimg)

    # grayimg[grayimg <= TH] = 0.

    grayimg = imresize(grayimg, har.shape)

    M, N = grayimg.shape
    grayimg = np.pad(grayimg, ((int(M / 2), int(M / 2)), (int(N / 2), int(N / 2))), 'constant')
    har = np.pad(har, ((int(M / 2), int(M / 2)), (int(N / 2), int(N / 2))), 'constant')

    H = fftshift(fft(fftshift(har, axes=0), axis=0), axes=0)
    # H = fftshift(fft(fftshift(har, axes=1), axis=1), axes=1)
    # H = fftshift(fft(fftshift(H, axes=1), axis=1), axes=1)
    # H = fftshift(fft(fftshift(H, axes=0), axis=0), axes=0)

    G = fftshift(fft(fftshift(grayimg, axes=0), axis=0), axes=0)
    # G = fftshift(fft(fftshift(grayimg, axes=1), axis=1), axes=1)
    # G = fftshift(fft(fftshift(G, axes=1), axis=1), axes=1)
    # G = fftshift(fft(fftshift(G, axes=0), axis=0), axes=0)

    S = G * H
    Sr = ifftshift(ifft(ifftshift(S, axes=0), axis=0), axes=0)
    # Sr = ifftshift(ifft(ifftshift(Sr, axes=1), axis=1), axes=1)

    # G = fft(grayimg)
    # H = fft(har)
    # S = G * H
    # Sr = ifft(S)

    plt.figure()
    plt.subplot(231)
    plt.imshow(grayimg)
    plt.title('G')
    plt.subplot(234)
    plt.imshow(20 * np.log10(np.abs(G) + 1e-16))
    plt.title('fft(G)')
    plt.subplot(232)
    plt.imshow(np.abs(har))
    plt.title('h')
    plt.subplot(235)
    plt.imshow(np.abs(H))
    plt.title('H')
    plt.subplot(233)
    plt.imshow(20 * np.log10(np.abs(Sr) + 1e-16))
    plt.title('Sr')
    plt.subplot(236)
    plt.imshow(np.abs(S))
    plt.title('S')
    plt.show()

    # G = fftshift(fft(fftshift(grayimg, axes=0)))
    # H = fftshift(fft(fftshift(har, axes=0)))
    # S = G * H
    # Sr = ifft(ifftshift(S, axes=0))
    # Sr = ifftshift(Sr, axes=1)

    Sr = Sr[int(M / 2):M + int(M / 2), int(N / 2):N + int(N / 2)]

    targets = img2tgs(grayimg, bg=bg, noise=noise, TH=TH, SA=SA, gdshape=gdshape)

    logging.info("---Out img2echo.")
    return Sr, targets


def img2rawdata(sarplat, grayimg, bg=0, TH=None, noise=None, gdshape=None, mod='time', verbose=False):
    r"""Generates sar raw data of an image scene.

    Generates SAR raw data of gray image.

    Arguments
    -----------------------
    sarplat : { ``SarPlat`` }
            see `sarplat.py` or documentation

    grayimg : { ``2d-array`` }
            gray image with size of (H, W)

    Keyword Arguments
    -----------------------
    bg : { ``number`` }
            background color value, 1:white, 0:black. (default: {0})

    TH : { ``number`` }
            threshold for obtain foreground targets (default: {None}, otsu)

    noise : { ``string`` }
            'awgn': white Gaussian noise (default: {None})

    gdshape : { ``list`` or ``tuple`` }
            discreted scene size (default: {None}, (-W / 2, W / 2, -H / 2, H / 2))

    mod : { ``string`` }
            simulation mode, ``'time'`` --> time domain, ``'conv'`` --> using convolution,
            ``'freq'`` --> frequency domain (default: 'time')

    verbose : { ``bool`` }
            show log info (default: {False})

    Returns
    -----------------------
    Sr : `2d-array`
        [azimuth, range] raw data response of gray image.
    targets : lists
        targets lists: [tg1, tg2, ..., tgn], tgi = [xi, yi, 0, 0, 0, 0, rcsi]
    """

    logging.info('---In img2rawdata...')

    # SA = sarplat.acquisition['SceneArea']
    SA = sarplat.selection['SubSceneArea']

    if mod is 'time':
        targets = img2tgs(grayimg, bg=bg, noise=noise, TH=TH, SA=SA, gdshape=gdshape)
        logging.info('~~~There are total %d targets.' % len(targets))
        Sr, ta, tr = tgs2rawdata(sarplat, targets, noise=None, verbose=verbose)

    if mod is 'freq':
        Sr, targets = img2echo(sarplat, grayimg, TH=None, noise=noise, verbose=verbose)

    logging.info('---Out img2rawdata.')
    return Sr, targets
