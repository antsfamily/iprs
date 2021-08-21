#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-25 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import logging
import numpy as np

from progressbar import *
from iprs.utils.const import *
from iprs.utils.transform import db20
from iprs.misc.mathops import prevpow2
from iprs.dsp.fft import fft, ifft
import matplotlib.pyplot as plt


def spotlight_width(H, BWa, Lsar):
    return 2. * H * np.tan(BWa / 2.) - Lsar / (2. * H)


def remove_lpe(phase):
    r"""remove linear phase error

    Remove linear phase error based on linear fitting, the linear phase error
    will cause image shift.

    Parameters
    ----------
    phase : {numpy 1d-array}
        Phase with linear trend.

    Returns
    -------
    phase : {numpy 1d-array}
        Phase without linear trend.
    """
    Na = len(phase)
    taidx = np.linspace(0, Na, Na)
    linear_coefs = np.polyfit(taidx, phase, deg=1)
    linear_phase = np.polyval(linear_coefs, taidx)
    phase = np.unwrap(phase - linear_phase)
    # phase -= np.mean(phase)
    return phase


def phase_correction(SI, errp, Nsub=None):
    Na, Nr = SI.shape
    if Nsub is None:
        Nsub = Na
    # aa = 0
    for n in range(0, Na, Nsub):
        # aa += 1
        # if aa != 3:
        #     continue
        X = SI[n:n + Nsub, :]
        ephi = errp[n:n + Nsub]
        NN = X.shape[0]
        X = fft(X, axis=0, shift=True)
        X = X * (np.repeat(np.exp(-1j * ephi), Nr).reshape(NN, Nr))
        SI[n:n + Nsub] = ifft(X, axis=0, shift=True)
    return SI


def pgaf_sm_1iter(SI, windb=None, est='ML', isrmlinear=False, iscrct=False, isplot=False):
    r"""perform phase gradient autofocus 1 iter

    perform phase gradient autofocus 1 iter as described in [1].

    revised for stripmap SAR

    - [1] C.V. Jakowatz, D.E. Wahl, P.H. Eichel, D.C. Ghiglia, P.A. Thompson,
    {\em Spotlight-mode Synthetic Aperture Radar: A Signal Processing
    Approach.} Springer, 1996.

    - [2] D.E. Wahl, P.H. Eichel, D.C. Ghiglia, C.V. Jakowatz, "Phase
    gradient autofocus-a robust tool for high resolution SAR phase
    correction," IEEE Trans. Aero. & Elec. Sys., vol. 30, no. 3, 1994.

    Parameters
    ----------
    SI : {numpy ndarray}
        Complex SAR image :math:`{\bm X}\in {\mathbb C}^{N_a×N_r}`.
    windb : {None or float}, optional
        Cutoff for window (the default is None, which use the mean as the cutoff.)
    est : {str}, optional
        Estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
    isrmlinear : {bool}, optional
        Is remove linear phase error? (the default is False)
    iscrct : {bool}, optional
        Is corrected image? (the default is False)
    isplot : {bool}, optional
        Is plot estimated phase error? (the default is False)

    Returns
    ----------
    SI : {numpy ndarray}
        Corrected SAR image :math:`{\bm Y}\in {\mathbb C}^{N_a×N_r}`, only if :attr:`iscrct` is ``True``, SI is returned.
    errp : {numpy 1darray}
        Estimated phase error :math:`\phi\in {\mathbb R}^{N_a×1}`.


    """

    Na, Nr = SI.shape
    # ---Step 1: Samples selection
    maxpos = np.argmax(np.abs(SI), axis=0)
    midpos = int(Na / 2.)
    Nshift = midpos - maxpos

    # ---Step 2: Circular shifting in azimuth
    Z = np.zeros(SI.shape, dtype=SI.dtype)
    for n in range(Nr):
        Z[:, n] = np.roll(SI[:, n], Nshift[n])

    # plt.figure()
    # plt.imshow(np.abs(Z))
    # plt.show()

    # ---Step 3: Windowing
    ncoh_avg_win = np.sum(np.abs(Z)**2, 1)
    ncoh_avg_win_db20 = db20(ncoh_avg_win)
    if windb is None:
        win_cutoff = np.mean(ncoh_avg_win_db20)
    elif windb in ['mean', 'MEAN', 'Mean']:
        win_cutoff = np.mean(ncoh_avg_win_db20)
    elif windb in ['median', 'MEDIAN', 'Median']:
        win_cutoff = np.median(ncoh_avg_win_db20)
    else:
        win_cutoff = np.max(ncoh_avg_win_db20) - np.abs(windb)

    leftidx = midpos
    rightidx = midpos
    for i in range(midpos, 0, -1):
        if ncoh_avg_win_db20[i] < win_cutoff:
            leftidx = i
            break
    for i in range(midpos, Na, 1):
        if ncoh_avg_win_db20[i] < win_cutoff:
            rightidx = i
            break
    # print(win_cutoff, leftidx, rightidx)
    ncoh_avg_win = np.zeros(Na)
    ncoh_avg_win[leftidx:rightidx] = 1.
    Z = Z * (ncoh_avg_win.repeat(Nr).reshape(Na, Nr))

    # ---Step 4: FFT
    Z = fft(Z, axis=0, shift=True)

    # ---Step 5: Phase gradient estimate
    # ~~~Maximum-Likelihood (ML) phase gradient estimation
    if est in ['ML', 'ml']:
        gradp = np.angle(np.sum((Z[0:-1, :].conj()) * Z[1:, :], 1))
        errp = np.cumsum(np.real(gradp))
        errp = np.pad(errp, [0, 1], 'edge')

    # ~~~Linear unbiased minimum variance (LUMV) phase gradient estimation
    elif est in ['LUMV', 'lumv']:
        Zd = np.diff(Z, n=1, axis=0)
        Zd = np.append(Zd, np.array([Zd[-1, :]]), axis=0)
        gradp = np.sum(np.imag((Z.conj()) * Zd), 1) /\
            (np.sum(Z * Z.conj(), 1) + EPS)
        errp = np.cumsum(np.real(gradp))
    else:
        raise ValueError("Not supported estimator! Supported are ML and LUMV")

    if isrmlinear:
        # ~~~Remove linear trend in phase error, as suggested in [2], which will cause shift
        taidx = np.linspace(0, Na, Na)
        linear_coefs = np.polyfit(taidx, errp, deg=1)
        linear_phase = np.polyval(linear_coefs, taidx)
        errp = np.unwrap(errp - linear_phase)
    if isplot:
        plt.figure()
        plt.subplot(211)
        plt.plot(ncoh_avg_win_db20, 'b')
        plt.plot(win_cutoff * np.ones(Na), 'r')
        plt.plot(ncoh_avg_win, 'g')
        plt.legend(['non-coherent', 'cutoff', 'window'])
        plt.xlabel('sample index in azimuth direction')
        plt.ylabel('amplitude/dB')
        plt.title('window')
        plt.subplot(212)
        plt.plot(errp)
        plt.xlabel('sample index in azimuth direction')
        plt.ylabel('phase/rad')
        plt.title('estimated phase')
        plt.show()

    if iscrct:
        SI = fft(SI, axis=0, shift=True)
        SI = SI * (np.repeat(np.exp(-1j * errp), Nr).reshape(Na, Nr))
        SI = ifft(SI, axis=0, shift=True)
        return SI, errp
    else:
        return errp


def pgaf_sm(SI, Nsar, Nsub=None, windb=None, est='ML', Niter=None, tol=1.e-6, isplot=False):
    r"""Phase gradient autofocus for stripmap SAR.

    Phase gradient autofocus for stripmap SAR.

    Parameters
    ----------
    SI : {numpy ndarray}
        Complex SAR image :math:`N_a×N_r`.
    Nsar : {integer}
        Number of synthetic aperture pixels.
    Nsub : {integer}, optional
        Number of sub-aperture pixels. (the default is :math:`{\rm min}\{N_{sar}, N_a\}`)
    windb : {None or float}, optional
        cutoff for window (the default is None, which use the mean as the cutoff.)
    est : {str}, optional
        estimator, ``'ML'`` for Maximum Likelihood estimation, ``'LUMV'`` for Linear Unbiased Minimum Variance estimation (the default is 'ML')
    Niter : {integer}, optional
        Maximum iters (the default is None, which means using :attr:`tol` for stopping)
    tol : {float}, optional
        Tolerance phase error twice in a row. (the default is 1.e-6)
    isplot : {bool}, optional
        Plot estimated phase error or corrected image. (the default is False)

    Returns
    ----------
    SI : {numpy ndarray}
        Corrected SAR image :math:`{\bm X}\in {\mathbb C}^{N_a×N_r}`.
    errp : {numpy 1darray}
        Estimated phase error :math:`\phi\in {\mathbb R}^{N_a×1}`.

    Raises
    ------
    ValueError
        For stripmap SAR, processing sub aperture should be smaller than synthetic aperture!
    """

    logging.info("---In pgaf_sm...")

    Na, Nr = SI.shape
    if Nsub is None:
        Nsub = 2**prevpow2(Nsar / 2. + 1)
        Nsub = min(Nsub, Na)

    if Nsub > Nsar:
        print("Nsar, Nsub: ", Nsar, Nsub)
        raise ValueError(
            "For stripmap SAR, processing sub aperture should be smaller than synthetic aperture!")

    Noverlap = 0
    print(Nsub)

    if Niter is None:
        Niter = 100
    logging.info("~~~Do Phase Gradient Autofocus...")
    widgets = ['Progress: ', Percentage(), ' ', Bar('.'), ' ', Timer(), ' ', ETA(), ' ']
    pbar = ProgressBar(widgets=widgets, maxval=Niter).start()
    errp0, k = (1.e10, 0)
    errp = np.zeros(Na)
    # plt.figure(1)
    while (np.mean(np.abs(errp - errp0)) > tol) and (k < Niter):
        errp0 = np.copy(errp)
        for n in range(0, Na, Nsub):
            idx = n + Nsub + Noverlap
            ep = pgaf_sm_1iter(SI[n:idx, :], windb=windb, est=est,
                               isrmlinear=True, iscrct=False, isplot=isplot)
            # errp[n:n + Nsub] = errp[max(0, n - 1)] + ep[0:Nsub]
            errp[n:n + Nsub] = ep[0:Nsub]
        # plt.plot(errp)
        # plt.show()
        # errp = remove_lpe(errp)
        # plt.plot(errp)
        # plt.show()
        SI = phase_correction(SI, errp, Nsub)
        k = k + 1
        if isplot:
            XX = np.abs(SI)
            XX = iprs.imadjustlog(XX, None, (0, 255))
            XX = XX.astype('uint8')
            plt.figure(100)
            plt.imshow(XX, cmap='gray')
            plt.show()

        pbar.update(k)
    logging.info("~~~Done.")
    logging.info("---Out pgaf_sm.")

    return SI, errp


if __name__ == '__main__':
    import iprs
    import scipy.io as scio

    cmap = 'gray'

    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/NoPGA_GlobalAZF.mat'
    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/NoPGA_RefineAZF.mat'
    filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/alos/data/Image_NoDopplerCorrection.mat'
    # filename = '/mnt/e/ws/github/iprs3.0/iprs3.0/examples/imaging/products/ers/data/Image_NoDopplerCorrection.mat'
    data = scio.loadmat(filename)

    SI = data['SI']
    SI = SI[:, :, 0] + 1j * SI[:, :, 1]

    nlooks = (1, 1)
    maxp = 1e5
    N1, N2 = (0, 6000)
    # SI = SI[N1:N1 + 1024, N2:N2 + 1024]
    SI = SI[N1:N1 + 4096, N2:N2 + 2048]
    # nlooks = (4, 1)
    # maxp = 1e4
    # N1, N2 = (0, 0)
    # # N1, N2 = (2048, 1024)
    # SI = SI[N1:N1 + 4096, N2:N2 + 2048]
    # # SI = SI[N1:N1 + 8192, N2:N2 + 4096]

    X = SI.copy()
    Na, Nr = SI.shape
    print(Na, Nr)

    Nsar, H, BWa, Lsar = (6976, 691500., 0.0234996122966, 22983.1697693)
    # Nsar, H, BWa, Lsar = (1159, 780000., 0.0050116248639, 4832.8353993)
    Nsub = iprs.spotlight_width(H, BWa, Lsar)
    Nsub = int(Nsub / 4.45)
    Nsub = 256

    X, errp = iprs.pgaf_sm(X, Nsar, Nsub=Nsub, windb=None, est='LUMV',
                           Niter=50, tol=1.e-8, isplot=False)

    # SI = np.flipud(SI)
    # X = np.flipud(X)
    SI = iprs.multilook_spatial(SI, nlooks=nlooks)
    X = iprs.multilook_spatial(X, nlooks=nlooks)

    SI = np.abs(SI)
    SI = iprs.imadjust(SI, (None, maxp), (0, 255))
    SI = SI.astype('uint8')

    X = np.abs(X)
    X = iprs.imadjust(X, (None, maxp), (0, 255))
    X = X.astype('uint8')

    Na, Nr = X.shape
    iprs.imsave('./X.tif', X)
    iprs.imsave('./SI.tif', SI)

    if Na >= Nr:
        plt.figure()
        plt.subplot(121)
        plt.imshow(SI, cmap=cmap)
        plt.subplot(122)
        plt.imshow(X, cmap=cmap)
        plt.show()
    else:
        plt.figure()
        plt.subplot(211)
        plt.imshow(SI, cmap=cmap)
        plt.subplot(212)
        plt.imshow(X, cmap=cmap)
        plt.show()
