#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-26 09:51:56
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from __future__ import division, print_function, absolute_import
import numpy as np

from ..utils.const import *
from ..dsp import normalsignals as sig

from iprs.sharing.range_azimuth_beamwidth_footprint import azimuth_footprint


import sys
import pickle as pkl
from skimage import transform

import matplotlib.pyplot as plt


def sarmodel(sarplat, mod=None, gdshape=None, normrc=None, verbose=True):
    r"""model sar imaging process.

    SAR imaging model

    Parameters
    ----------
    sarplat: {SarPlat object}
        SAR platform class
    mod: {str}, optional
        mod type(default: {'2D1'})

            if mod is '2D1':
                the model will be in vector mode:
                    s = A      g
                    MNx1      MNxHW  HWx1(M: Na, N: Nr, MN << HW)
            if mod is '2D2':
                the model will be in mat mode:
                    S = Aa     G     Be
                    MxN       MxH    HxW   WxN(M: Na, N: Nr, M << H, N << W)
            if mod is '1Da':
                    S = A      G
                    MxW       MxH    HxW(M: Na, N: Nr, M << H)
            if mod is '1Dr':
                    S'    =   A      G'
                    NxH       NxW    WxH(M: Na, N: Nr, N << W)

    gdshape: {tuple}, optional
        discrete scene size of G (default: {None}, sarplat.acquisition['SceneArea'], dx=dy=1)

    normrc: {[type]}, optional
        [description](the default is None, which[default_description])
    verbose : { ``bool`` }
        show log info (default: {True})

    Returns
    -------
    A : numpy array
        Imaging mapping matrix.
    """

    print("================in sarmodel================")

    H = sarplat.sensor['H']
    V = sarplat.sensor['V']
    Tp = sarplat.sensor['Tp']
    Kr = sarplat.sensor['Kr']
    Fc = sarplat.sensor['Fc']
    Wl = sarplat.sensor['Wl']
    La = sarplat.sensor['La']
    # Fs = sarplat.sensor['Fs']
    # PRF = sarplat.sensor['PRF']
    Na = sarplat.params['SubNa']
    Nr = sarplat.params['SubNr']
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']
    Xc = sarplat.params['Xc']
    Yc = sarplat.params['Yc']
    Rbc = sarplat.params['Rbc']
    SA = sarplat.acquisition['SceneArea']

    gX = SA[1] - SA[0]
    gY = SA[3] - SA[2]

    if gdshape is None:
        dx = 1.0
        dy = 1.0
        gW = gX
        gH = gY
    else:
        gH, gW = gdshape
        dx = gX / (gW * 1.0)
        dy = gY / (gH * 1.0)

    if verbose:
        print("===Generates mapping matirx...")
        print("---gY, gX; gH, gW; dy, dx: ", gY, gX, gH, gW, dy, dx)
        print("---Na, Nr: ", Na, Nr)

    yFootPrint = azimuth_footprint(Rbc, Wl, La)

    if mod is None:
        mod = '2D1'

    if mod is '2D1':
        print((Na * Nr, gH * gW))
        NaNr = int(Na * Nr)
        gHgW = int(gH * gW)
        A = np.zeros((NaNr, gHgW), dtype='complex')

        # tau = np.repeat(tr, Na).reshape(Nr, Na).transpose()  # [Na, Nr]

        cnt = 0
        for m in range(Na):
            for n in range(Nr):
                R, _, yy = __computeRmn(ta[m], tr[n], H, V, Yc, Xc, SA, gH, gW)
                yy = yy.flatten()
                RC2 = 2 * R / C
                phase = -2 * Fc * RC2 + Kr * (tr[n] - RC2) ** 2
                wr = sig.rect((tr[n] - RC2) / Tp)
                wa = np.sinc(yy / yFootPrint)
                A[cnt, :] = wr * wa * np.exp(1j * PI * phase)
                cnt = cnt + 1
    if mod is '2D2':
        pass
    # if mod is '1Da':
    #         S     =   A      G
    #         MxW       MxH    HxW   (M:Na, N:Nr, M<<H)
    if mod is '1Da':
        A = np.zeros((Na, gW), dtype='complex')

        # for m in range(Na):
        #     for n in range(gY):

        #         PhiAzimuth(i,k)=exp(j*pi*Ka*(ta(i)-ta_Nyquist(k))^2).*...
        #     (abs(ta(i)-ta_Nyquist(k))<=Tsar/2);
        #         R = __computeRmn(m, n, ta[m], tr[n], H, V, Xc, Yc, gY, gX)
        #         print(R, R.shape)
        #         RC2 = 2 * R / C
        #         phase = -2 * Fc * RC2 + Kr * (tr[n] - RC2)**2

        #         A[Na, :] = sig.rect((tr[n] - RC2) / Tp) * \
        #             np.exp(1j * PI * phase)
        #         cnt = cnt + 1

    # if mod is '1Dr':
    #         S'    =   A      G'
    #         NxH       NxW    WxH   (M:Na, N:Nr, N<<W)
    if mod is '1Dr':
        A = np.zeros((Nr, gY), dtype='complex')

    if verbose:
        print("===Done!")

    return A


def __computeRmn(ta, tr, H, V, Yc, Xc, SA, gH, gW):
    r"""compute range at g(i, j)

    compute range at g(i, j)

    Arguments
    ------------
    m {integer}
        current y coordinate of H
    n {integer}
        current x coordinate of W
    ta {time in azimuth}
        azimuth time
    tr {numpy array}
        range time
    H {integer}
        height of SAR platform
    V {float}
        velocity of SAR platform
    Yc {float}
        center coordinate in Y axis
    Xc {float}
        center coordinate in X axis
    SA {list}
        scene area: [xmin, xmax, ymin, ymax]
    H {integer}
        height of scene(Y)
    W {integer}
        width of scene(X)
    """

    xmin = SA[0] + Xc
    xmax = SA[1] + Xc
    ymin = SA[2] + Yc
    ymax = SA[3] + Yc

    yy = np.linspace(ymin, ymax, gH, endpoint=False)
    yy = np.repeat(yy, gW)
    yy = np.reshape(yy, (gH, gW))
    xx = np.linspace(xmin, xmax, gW, endpoint=False)
    xx = np.repeat(xx, gH)
    xx = np.reshape(xx, (gW, gH)).transpose()

    # print("===========***==========")
    # print(xx, xx.shape)
    # print(yy, yy.shape)
    # print(xx.min(), xx.max(), yy.min(), yy.max())
    # print(xx[0:6], xx[0:6], yy[0:6], yy[0:6])

    yy = yy - V * ta

    R = np.sqrt(xx ** 2 + yy ** 2 + H ** 2)  # [gY, gX]
    R = R.flatten()
    return R, xx, yy


def load_sarmodel(datafile, mod='AinvA'):
    r"""load sarmodel file

    load sarmodel file (``.pkl``)

    Parameters
    ----------
    datafile : {str}
        Model data file path.
    mod : {str}, optional
        Specify load which variable, ``A``, ``invA``, ``AinvA``
        (the default is 'AinvA', which :math:`\bm A`, :math:`{\bm A}^{-1}` )

    Returns
    -------
    A : numpy array
        Imaging mapping matrix.
    invA : numpy array
        Inverse of imaging mapping matrix.

    Raises
    ------
    ValueError
        wrong mod
    """
    print("===reading model file: ", datafile, "...")
    if datafile is not "":
        # get map
        f = open(datafile, 'rb')
        # for python2
        if sys.version_info < (3, 1):
            if mod is 'A':
                A = pkl.load(f)
                f.close()
                return A
            if mod is 'invA':
                pkl.load(f)
                invA = pkl.load(f)
                f.close()
                return invA
            if mod is 'AinvA':
                A = pkl.load(f)
                invA = pkl.load(f)
                f.close()
                return A, invA
            if mod is 'AAH':
                A = pkl.load(f)
                pkl.load(f)
                AH = pkl.load(f)
                f.close()
                return A, AH
            if mod is 'AinvAAH':
                A = pkl.load(f)
                invA = pkl.load(f)
                AH = pkl.load(f)
                f.close()
                return A, invA, AH
            f.close()
            raise ValueError("mod: 'A', 'invA', 'AinvA', 'AAH', 'AinvAAH'")

        # for python3
        else:
            if mod is 'A':
                A = pkl.load(f, encoding='latin1')
                f.close()
                return A
            if mod is 'invA':
                pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                f.close()
                return invA
            if mod is 'AinvA':
                A = pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                f.close()
                return A, invA
            if mod is 'AAH':
                A = pkl.load(f, encoding='latin1')
                pkl.load(f, encoding='latin1')
                AH = pkl.load(f, encoding='latin1')
                f.close()
                return A, AH
            if mod is 'AinvAAH':
                A = pkl.load(f, encoding='latin1')
                invA = pkl.load(f, encoding='latin1')
                AH = pkl.load(f, encoding='latin1')
                f.close()
                return A, invA, AH
            f.close()
            raise ValueError("mod: 'A', 'invA', 'AinvA', 'AAH', 'AinvAAH'")
    else:
        return None


def save_sarmodel(A, invA=None, AH=None, datafile='./model.pkl'):
    r"""save model mapping matrix

    save model mapping matrix to a file.


    Parameters
    ----------
    A : {numpy array}
        Imaging mapping matrix
    invA : {numpy array}, optional
        Moore - Penorse inverse of A(default: {None})
    AH : {numpy array}, optional
        The Hermite :math:`{\bm A}^H` of the Imaging mapping matrix :math:`\bm A`
        (the default is None, which does not store)
    datafile : {str}, optional
        save file path(default: {'./model.pkl'})
    """

    f = open(datafile, 'wb')

    pkl.dump(A, f, 0)
    if invA is not None:
        pkl.dump(invA, f, 0)
    if AH is not None:
        pkl.dump(AH, f, 0)
    f.close()


def sarmodel_genecho(A, g, mod=None, gdshape=None, verbose=True):
    r"""Generates SAR raw echoes by SAR Imaging model

    .. math::
       {\bm s} = {\bm A}{\bm g}

    Arguments
    -------------------
    A {2d numpy array}
        SAR Imaging matrix.
    g {2d numpy array}
        The scene.

    Keyword Arguments
    -------------------
    mod {str}
        mod type(default: {'2D1'})

        if mod is '2D1':
            the model will be in vector mode:
                s = A      g
                MNx1      MNxHW  HWx1(M: Na, N: Nr, MN << HW)
        if mod is '2D2':
            the model will be in mat mode:
                S = Aa     G     Be
                MxN       MxH    HxW   WxN(M: Na, N: Nr, M << H, N << W)
        if mod is '1Da':
                S = A      G
                MxW       MxH    HxW(M: Na, N: Nr, M << H)
        if mod is '1Dr':
                S'    =   A      G'
                NxH       NxW    WxH(M: Na, N: Nr, N << W)

    gdshape {tuple}
        discrete scene size of G(default: {None}, size of g, dx=dy=1)

    verbose {bool
        show more log info (default: {True})

    Returns
    -------
    s : numpy array
        SAR raw data
    g : 1d numpy array
        The scene.
    """

    H, W = g.shape
    if gdshape is None:
        dx = 1.0
        dy = 1.0
        gW = W
        gH = H
    else:
        gH, gW = gdshape
        dx = W / (gW * 1.0)
        dy = H / (gH * 1.0)

    if mod is '2D1':
        g = transform.resize(g, (gH, gW), preserve_range=True)
        g = g.flatten()
        g = g / np.max(g)
        print(A.shape, g.shape, gH, gW, g.min(), g.max())
        s = np.matmul(A, g)
        return s, g
