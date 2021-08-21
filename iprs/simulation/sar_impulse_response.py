#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

import logging
from iprs.utils.const import *

from iprs.dsp.normalsignals import rect, chirp
from iprs.dsp.noise import imnoise, matnoise
from iprs.sharing.range_azimuth_beamwidth_footprint import azimuth_footprint


from skimage import filters, transform
import matplotlib.pyplot as plt


def sarir(sarplat, mod='ar', ver=False):
    r"""SAR impulse response

    2D impulse response in both directions

    .. math::
       h(\eta, \tau) = h_a(\eta,\tau) h_r(\eta,\tau) = h_r(\eta,\tau) h_a(\eta,\tau)

    1D impulse response in azimuth

    .. math::
       \begin{aligned}
           h_a(\eta, \tau) &= w_a(\eta-\eta_c) \\
                & {\rm exp}\left\{ -j4\pi f_0 R(\eta)/c \right\}
       \end{aligned}
       :label: equ-SARImpulseResponse1Da

    1D impulse response in range

    .. math::
       \begin{aligned}
         h_r(\eta, \tau) &= w_r\left(\tau-2R(\eta)/c\right) \\
         & {\rm exp}\left\{j\pi K_r\left(\tau-2R(\eta)/c\right)^2 \right\}
       \end{aligned}
       :label: equ-SARImpulseResponse1Dr


    Parameters
    ----------
    sarplat : {SarPlat}
        SAR platform object
    mod : {str}, optional
        mode for generating the impulse response. ``'ar'`` --> 2D impulse response in both directions,
        ``'a'`` --> 1D impulse response in azimuth, ``'r'`` --> 1D impulse response in range,
        (the default is 'ar')
    ver : {bool}, optional
        show more information (the default is False)
    """

    logging.info("---In sar_impulse_response...")

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

    trs = np.repeat(tr, Na).reshape(Nr, Na).transpose()  # [Na, Nr]
    tas = np.repeat(ta, Nr).reshape(Na, Nr)  # [Na, Nr]

    t2 = 0.5 * (tas ** 2)

    vx = 0.
    vy = 0.
    ax = 0.
    ay = 0.

    logging.info('---Generates impulse response(' + mod + ')...')

    Xc, Yc, Zc = SC
    SA = sarplat.selection['SubSceneArea'] + [Xc, Xc, Yc, Yc]

    x0 = np.linspace(SA[0], SA[1], Nr)
    x0 = np.repeat(x0, Na).reshape(Nr, Na).transpose()
    y0 = np.linspace(SA[2], SA[3], Na)
    y0 = np.repeat(y0, Nr).reshape(Na, Nr)
    x0 = np.flipud(x0)

    x = x0 + vx * tas + ax * t2  # [Na, Nr]
    y = y0 + vy * tas + ay * t2 - Vr * tas  # [Na, Nr]

    R = np.sqrt(x ** 2 + y ** 2 + H ** 2)  # [Na, Nr]

    print(R.min(), R.max(), ta.shape, y0.shape)
    RC2 = 2 * R / C
    # print(RC2.shape)
    # RC2 = np.repeat(RC2, Nr).reshape(Na, Nr)  # [Na, Nr]

    phase1 = -2j * PI * Fc * RC2
    phase2 = 1j * PI * Kr * (trs - RC2) ** 2  # [Na, Nr]

    # Wa = np.sinc((tas * V - y0) / FPa)  # [Na, 1]
    Wa = np.sinc(0.886 * np.arctan((tas - tac) * Vg / R0) / BWa)
    # Wa = np.sinc(0.886 * np.arctan((tas * Vg - y0) / R0) / BWa)
    Wa = Wa ** 2
    # Wa = np.repeat(Wa, Nr).reshape(Na, Nr)  # [Na, Nr]

    Wr = rect((trs - RC2) / Tp)  # [Na, Nr]

    ha = Wa * np.exp(phase1)

    hr = Wr * np.exp(phase2)

    logging.info("---Done!")
    logging.info("---Out sar_impulse_response.")
    if mod is 'a':
        return ha
    if mod is 'r':
        return hr
    if mod is 'ar':
        return ha * hr


if __name__ == '__main__':

    import iprs

    sensor_name = 'Air1'
    acquis_name = 'Air1'

    # sensor_name = 'Air2'
    # acquis_name = 'Air2'

    sarplat = iprs.SarPlat()
    sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
    sarplat.sensor = iprs.SENSORS[sensor_name]
    sarplat.acquisition = iprs.ACQUISITION[acquis_name]
    sarplat.selection = iprs.SELECTION['ROI1']
    sarplat.params = None
    sarplat.select()

    sarplat.printsp()

    har = sarir(sarplat, mod='ar', ver=True)

    print(har.shape, "=======")

    imgfile = '../../data/img/000002AirPlane128.png'
    imgfile = '../../data/img/pointsx128.png'
    imgRGB = iprs.imread(imgfile)

    if np.ndim(imgRGB) > 2:
        img = imgRGB[:, :, 0]
    else:
        img = imgRGB

    Sr = iprs.img2echo(sarplat, img, TH=0., noise=None, SNR=30, h=har, verbose=True)

    print(Sr.shape, "--------")

    SI = iprs.rda_adv(Sr, sarplat, zpadar=(256, 256),
                      usesrc=True, usedpc=True, rcmc=32, verbose=False)

    plt.figure()
    plt.subplot(121)
    plt.imshow(np.abs(Sr))
    plt.subplot(122)
    plt.imshow(np.abs(SI))
    plt.show()
