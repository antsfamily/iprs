#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

from iprs.utils.const import *
import logging
from iprs.misc import visual as vis
from iprs.dsp.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt


def bdce_sf(Sr, Fsa, rdflag=False, Nroff=0, isplot=False):
    r"""Baseband doppler centroid estimation by spectrum fitting

    Baseband doppler centroid estimation by spectrum fitting.

    Parameters
    ----------
    Sr : {numpy array}
        SAR signal :math:`N_a×N_r` in range-doppler domain (range frequency domain).
    Fsa : {float}
        Sampling rate in azimuth
    rdflag : {bool}
        Specifies whether the input SAR signal is in range-doppler domain. If not, :fun:`dce_sf` excutes FFT in range direction.
    isplot : {bool}
        Whether to plot the estimated results.(Default: False)
    """
    Na, Nr = Sr.shape

    # Change to range - Doppler domain
    if not rdflag:
        Sr = fft(Sr, axis=1, shift=True)
    # Get power
    Sr = Sr * (Sr.conj())

    # Search for each column peak power(position of centroid)
    dpidx = np.argmax(Sr, axis=0)

    # Map found indexes into frequencies
    dpf = np.linspace(-Fsa / 2., Fsa / 2., Na)
    rgidx = np.linspace(0, Nr, Nr)
    dpcv = dpf[dpidx[Nroff:]]
    dpp_deg = 1
    # Polynomial fit of Doppler centroid
    dc_coef = np.polyfit(rgidx, dpcv, dpp_deg)

    # Handler to evaluate Doppler centroid[Hz] as function of range pixel number
    fbdc = np.polyval(dc_coef, rgidx)
    if isplot:
        plt.figure()
        plt.plot(dpcv, '-b')
        plt.plot(fbdc, '-r')
        plt.xlabel('Range cell')
        plt.ylabel('Frequency/Hz')
        plt.title('Baseband doppler centroid estimation based on spectrum fitting')
        plt.show()

    return fbdc, dc_coef


def bdce_api(Sr, Fsa, isplot=False):
    """Baseband doppler centroid estimation by average phase increment

    Baseband doppler centroid estimation by average phase increment.

    Parameters
    ----------
    Sr : {numpy array}
        SAR raw data or range compressed data
    Fsa : {float}
        Sampling rate in azimuth
    isplot : {bool}
        Whether to plot the estimated results.(Default: False)
    """
    Na, Nr = Sr.shape
    cccv = np.sum(np.conj(Sr[1:, :]) * Sr[0:-1, :], 0)
    cccv = np.angle(cccv)
    acccv = np.mean(cccv)
    fbdc = acccv * (Fsa / (2. * PI))
    if isplot:
        plt.figure()
        # plt.plot(np.real(acccv), '-b')
        # plt.plot(np.imag(acccv), '-g')
        plt.plot(cccv, '-r')
        plt.plot([0, Nr], [acccv, acccv], '-b')
        plt.text(Nr / 2., acccv, str(fbdc), fontsize=16, ha='left', rotation=0, wrap=True)
        plt.xlabel('Range cell')
        plt.ylabel('Phase/rad')
        plt.title('Baseband doppler centroid estimation based on average phase increment')
        plt.show()

    return fbdc


def bdce_madsen(Sr, Fsa, isplot=False):
    """Baseband doppler centroid estimation by madsen

    Baseband doppler centroid estimation bymadsen.

    Parameters
    ----------
    Sr : {numpy array}
        SAR raw data or range compressed data
    Fsa : {float}
        Sampling rate in azimuth
    isplot : {bool}
        Whether to plot the estimated results.(Default: False)
    """

    # Sr fuhao chuli
    acccv = np.sum(np.conj(Sr[1:, :]) * Sr[0:-1, :], 0)
    fbdc = (Fsa / (2. * PI)) * np.angle(acccv)

    if isplot:
        plt.figure()
        # plt.plot(np.real(acccv), '-b')
        # plt.plot(np.imag(acccv), '-g')
        plt.plot(fbdc, '-r')
        plt.xlabel('Range cell')
        plt.ylabel('Frequency/Hz')
        plt.title('Baseband doppler centroid estimation based on average phase increment')
        plt.show()
        fbdc = np.unwrap(fbdc)
    return fbdc


def adce_wda(Sr, Fsa, Fsr, Fc):
    """Absolute doppler centroid estimation by wavelength diversity algorithm

    Absolute doppler centroid estimation by Wavelength Diversity Algorithm (WDA).

    Parameters
    ----------
    ----------
    Sr : {numpy array}
        SAR signal :math:`N_a×N_r` in range-doppler domain (after range compression).
    Fsa : {float}
        Sampling rate in azimuth.
    Fsr : {float}
        Sampling rate in range.
    """

    Na, Nr = Sr.shape

    Sr = fft(Sr, axis=1, shift=True)
    cccv = accc(Sr)
    cccv = np.angle(cccv)
    coef = np.polyfit(np.linspace(0, Fsr, Nr), cccv, deg=1)
    alpha = coef[0]

    return (Fsa / (2 * PI)) * Fc * alpha


def abdce_wda(Sr, Fsa, Fsr, Fc, rate=0.9, isplot=False):
    """Absolute and baseband doppler centroid estimation by wavelength diversity algorithm

    Absolute and baseband doppler centroid estimation by Wavelength Diversity Algorithm (WDA).

    <<合成孔径雷达成像_算法与实现>> p350.

    Parameters
    ----------
    ----------
    Sr : {numpy array}
        SAR signal :math:`N_a×N_r` in range frequency domain.
    Fsa : {float}
        Sampling rate in azimuth.
    Fsr : {float}
        Sampling rate in range.
    """

    logging.info("---In abdce_wda...")

    Na, Nr = Sr.shape

    acccv = np.sum(np.conj(Sr[1:, :]) * Sr[0:-1, :], 0)
    phi_acccv = np.angle(acccv)

    N = int(rate * Nr)
    NN = Nr - N
    if NN % 2 == 0:
        N1 = int(NN / 2)
    else:
        N1 = int((NN + 1) / 2)
    Fs = rate * Fsr
    fidx = fftfreq(Fs, N, shift=True, norm=False)
    phi_acccv = phi_acccv[N1:N1 + N]
    coef = np.polyfit(fidx, phi_acccv, deg=1)
    alpha = coef[0]

    if isplot:
        fit_phi_acccv = np.polyval(coef, fidx)
        posx = 0
        posy = np.min(phi_acccv)
        plt.figure()
        plt.plot(fidx / 1.e6, phi_acccv, '-b')
        plt.plot(fidx / 1.e6, fit_phi_acccv, '-r')
        plt.text(posx, posy,
                 "slop: " + str(round(alpha * 1.e9, 4)) + "mrad/MHz" +
                 "\nbias: " + str(round(coef[1] * 1.e3, 4)) + "mrad", fontsize=12)
        plt.xlabel('Range Frequency/MHz')
        plt.ylabel('ACCC/rad')
        plt.legend(['ACCC', 'Fitted'])
        plt.title('Absolute doppler centroid estimation based on WDA')
        plt.show()

    fadc = (Fsa / (2 * PI)) * Fc * alpha
    fbdc = np.angle(np.mean(acccv)) * (Fsa / (2. * PI))

    Ma = int((fadc - fbdc) / Fsa)
    # residual frequency to azimuth sampling rate
    rf = (Ma * Fsa - (fadc - fbdc))
    rfc = rf / Fsa
    if rfc < 0.33:
        yesno = 'Yes!'
    else:
        yesno = 'No!'
    fadc = fbdc + Ma * Fsa
    logging.info("~~~Estimated absolute DC: " + str(fadc))
    logging.info("~~~Estimated baseband DC: " + str(fbdc))
    logging.info("~~~Estimated ambiguity number: " + str(Ma))
    logging.info("~~~Residual (unit Hz): " + str(rf) + "=" + str(rfc) + "PRF < 0.33PRF? " + yesno)
    logging.info("---Done.")
    logging.info("---Out abdce_wda.")

    return fadc, fbdc, Ma, rf


def dce_wda(Sr, Fsr, Fsa, Fc, ncpb=None, tr=None, isplot=False, isfftr=False):

    Na, Nr = Sr.shape
    if tr is None:
        tr = np.linspace(0, Nr, Nr)

    ftshift = True

    if ncpb is None:
        ncpb = [Na, Nr]
    nblks = np.int32(np.ceil([Na / ncpb[0], Nr / ncpb[1]]))

    if isfftr:
        Sr = fft(Sr, n=None, axis=1, norm=None, shift=ftshift)

    fr = fftfreq(Fsr, n=nblks[1], shift=ftshift, norm=False)

    dNa, dNr = np.int32(ncpb)
    rngAvgACCC = np.zeros(nblks, dtype='complex64')
    alpha = np.zeros((nblks[0], 1))
    phiokfit = np.zeros((nblks[0], Nr))
    frall = fftfreq(Fsr, Nr, ftshift, False)

    idxa = 0
    for n in range(0, Na, dNa):
        idxae = min(n + dNa, Na - 1)
        ACCC = np.sum(np.conj(Sr[n:idxae, :]) * Sr[n + 1:idxae + 1, :], 0)
        idxr = 0
        for m in range(0, Nr, dNr):
            rngAvgACCC[idxa, idxr] = np.mean(ACCC[m:min(m + dNr, Nr)])
            idxr = idxr + 1
        phi = np.angle(rngAvgACCC[idxa, 0:nblks[1]])  # ACCC phase angle
        c = np.polyfit(fr, phi, 1)
        alpha[idxa] = c[0]
        bias = c[1]

        # Remove the outliers
        phifit = alpha[idxa] * fr + bias
        p_pf = (phi - phifit)**2
        idxok = p_pf <= np.mean(p_pf)

        c = np.polyfit(fr[idxok], phi[idxok], 1)
        alpha[idxa] = c[0]
        bias = c[1]

        # for all range cells.
        phiokfit[idxa, :] = alpha[idxa] * frall + bias

        if isplot:
            plt.figure()
            plt.grid()
            plt.plot(fr / 1e6, phi, '-b')
            plt.plot(fr[idxok] / 1e6, phi[idxok], '-g')
            plt.plot(frall / 1e6, phiokfit[idxa, :], '-r')
            plt.xlabel('Range frequency/MHz')
            plt.ylabel('ACCC phase angle/rad')
            plt.legend(('Original', 'Cleaned', 'Fitted'))

        idxa = idxa + 1

    fadc = Fsa * Fc * alpha / (2 * PI)

    # phiokfit = np.unwrap(phiokfit)

    fbdc = Fsa * phiokfit / (2 * PI)

    if isplot:
        plt.figure()
        plt.grid()
        legendstr = []
        # plot(frall, fadc, '-b')
        for n in range(nblks[0]):
            legendstr.append('Azimuth block ' + str(n + 1))
            plt.plot(frall / 1e6, fbdc[n])
        plt.xlabel('Range frequency/MHz')
        plt.ylabel('Estimated doppler centoid/Hz')
        plt.legend(legendstr)
        plt.show()

    Ma = np.round((fadc - fbdc) / Fsa)

    dfres = Ma * Fsa - (fadc - fbdc)

    R = dfres / Fsa

    fadc = fbdc + Ma * Fsa

    return fadc, fbdc, Ma


def fullfadc(fdc, shape):
    nblks = fdc.shape
    Na, Nr = shape

    NBa = nblks[0]
    NBr = nblks[1]
    Na1b = int(np.uint(Na / NBa))
    Nr1b = int(np.uint(Nr / NBr))

    fc = np.zeros((Na, Nr))

    for a in range(NBa):
        for r in range(NBr):
            fc[int(a * Na1b):min(int((a + 1) * Na1b), Na), int(r * Nr1b):min(int((r + 1) * Nr1b), Nr)] = fdc[a, r]
    return fc


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import iprs

    datafile = '/mnt/d/DataSets/sar/ALOSPALSAR/mat/ALPSRP050500980-L1.0/ALOS_PALSAR_RAW=IMG-HH-ALPSRP050500980-H1(sl=1el=35345).mat'
    # datafile = '/mnt/d/DataSets/sar/ERS/mat/ERS2_SAR_RAW=E2_02558_STD_L0_F327(sl=1el=28682).mat'

    sardata, sarplat = iprs.sarread(datafile)

    Fsa = sarplat.params['Fsa']
    Fsr = sarplat.params['Fsr']
    fr = sarplat.params['fr']
    Kr = sarplat.params['Kr']
    Fc = sarplat.sensor['Fc']
    Sr = sardata.rawdata[:, :, 0] + 1j * sardata.rawdata[:, :, 1]

    Sr = Sr[0:1024, 0:2048]
    # Sr = Sr[1024:4096, 0:2048]
    fr = np.linspace(-Fsr / 2.0, Fsr / 2.0, Sr.shape[1])

    # Sr = fftshift(fft(fftshift(Sr, axes=1), axis=1), axes=1)

    # Sr = iprs.range_matched_filtering(Sr, fr, Kr)

    # Sr = ifftshift(ifft(ifftshift(Sr, axes=1), axis=1), axes=1)

    # aa = iprs.doppler_center_estimation(Sr, Fsa)
    # print(aa)

    # Sr = Sr[512:-512, 512:-512]
    # Sr = Sr[:, 512:512+1024]
    # Sr = Sr[0:512, 0:512]

    # Sr = fftshift(fft(fftshift(Sr, axes=1), axis=1), axes=1)
    # Sr = fftshift(fft(Sr, axis=1), axes=1)
    # Sr = fft(Sr, axis=1)

    print(Sr.shape)

    accc(Sr, isplot=True)

    _, dc_coef = bdce_sf(Sr, Fsa, rdflag=False, isplot=True)
    print(dc_coef)
    bdce_api(Sr, Fsa, isplot=True)

    fadc = adce_wda(Sr, Fsa, Fsr, Fc)

    print(fadc)
