#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
import logging

from ..utils.const import *
from .geometry import rectangle, disc
from iprs.utils.image import imresize


def gpts(SceneArea, nTGs, seed=None, verbose=False):
    r"""Generates number of point targets.

    Generates number of point targets.

    Parameters
    ----------
    SceneArea : {list or tuple}
        Scene Area, [xmin,xmax,ymin,ymax]
    nTGs : {integer}
        number of targets
    seed : {integer}, optional
        random seed (the default is None, which different seed every time.)
    verbose : {bool}, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    targets : lists
        [tg1, tg2, ..., tgn], tgi = [x,y]
    """

    if verbose:
        print(SceneArea)
    (Xmin, Xmax, Ymin, Ymax) = SceneArea

    if seed is not None:
        np.random.seed(seed)

    x = np.random.randint(Xmin, Xmax, nTGs) * 1.0
    y = np.random.randint(Ymin, Ymax, nTGs) * 1.0
    # x = np.random.randint(Xmin/4.0, Xmax/4.0, nTGs) * 1.0
    # y = np.random.randint(Ymin/4.0, Ymax/4.0, nTGs) * 1.0

    vx = np.zeros(nTGs)
    vy = np.zeros(nTGs)
    ax = np.zeros(nTGs)
    ay = np.zeros(nTGs)
    rcs = np.random.rand(nTGs)
    # print(rcs)
    # rcs = np.ones(nTGs)
    # rcs[0] = 1

    targets = [x, y, vx, vy, ax, ay, rcs]
    targets = np.array(targets)

    if verbose:
        print(targets)

    targets = targets.transpose()

    return targets


def gdisc(SceneArea, nDiscs, centers=None, radius=None, radiusMin=None, radiusMax=None, amps=None, dx=None, dy=None, seed=None, verbose=False):
    r"""Generates number of Disc targets.

    Generates Disc targets.

    Parameters
    ----------
    SceneArea : {list or tuple}
        Scene Area, [xmin,xmax,ymin,ymax]
    nDiscs : {integer}
        number of disks
    centers : {lists}, optional
        disk centers (the default is None, which generate randomly)
    radius : {list}, optional
        disk radius (the default is None, which generate randomly)
    radiusMin : {integer}, optional
        minmun radius (the default is None, which generate randomly)
    radiusMax : {[type]}, optional
        maxmun radius (the default is None, which generate randomly)
    amps : {list}, optional
        amplitudes (the default is None, which generate randomly)
    dx : {float}, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : {float}, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    seed : {integer}, optional
        random seed (the default is None, which different seed every time.)
    verbose : {bool}, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    targets : lists
        [tg1, tg2, ..., tgn], tgi = [x,y]
    """

    if verbose:
        print(SceneArea)
    (Xmin, Xmax, Ymin, Ymax) = SceneArea

    if seed is not None:
        np.random.seed(seed)

    if centers is None:
        x0 = np.random.randint(Xmin, Xmax, nDiscs) * 1.0
        y0 = np.random.randint(Ymin, Ymax, nDiscs) * 1.0
    else:
        x0 = centers[0]
        y0 = centers[1]

    nDiscs = len(x0)

    if radiusMax is None:
        radiusMax = 20
    if radiusMin is None:
        radiusMin = 1

    if radius is None:
        radius = np.random.randint(radiusMin, radiusMax, nDiscs)
    if amps is None:
        amps = np.random.rand(nDiscs)

    r = radius

    targets = disc(SceneArea, x0[0], y0[0], r[0], a=amps[0], dx=dx, dy=dy, verbose=False)
    for n in range(1, nDiscs):
        target = disc(SceneArea, x0[n], y0[n], r[n], a=amps[n], dx=dx, dy=dy, verbose=False)
        print(target.shape, targets.shape)
        targets = np.concatenate((targets, target), axis=0)

    if verbose:
        print(targets)

    return targets


def grectangle(SceneArea, nRects, amps=None, h=None, w=None, dx=None, dy=None, seed=None, verbose=False):
    """Generates number of rectangle targets.

    Generates number of rectangle targets.

    Parameters
    ----------
    SceneArea : {list or tuple}
        Scene Area, [xmin,xmax,ymin,ymax]
    nRects : {integer}
        number of rectangles
    amps : {list}, optional
        amplitudes (the default is None, which generate randomly)
    height : {list}, optional
        height of each rectangle (the default is None, which generate randomly)
    width : {list}, optional
        width of each rectangle (the default is None, which generate randomly)
    dx : {float}, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : {float}, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    seed : {integer}, optional
        random seed (the default is None, which different seed every time.)
    verbose : {bool}, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    targets : ndarray
        [tg1, tg2, ..., tgn], tgi = [x,y]
    """

    if verbose:
        print(SceneArea)
    (Xmin, Xmax, Ymin, Ymax) = SceneArea

    if seed is not None:
        np.random.seed(seed)

    if amps is None:
        amps = np.random.rand(nRects)

    x0 = np.random.randint(Xmin, Xmax, nRects) * 1.0
    y0 = np.random.randint(Ymin, Ymax, nRects) * 1.0
    targets = rectangle(SceneArea, x0[0], y0[0], h, w, a=amps[0], dx=None, dy=None, verbose=False)
    for n in range(1, nRects):
        target = rectangle(SceneArea, x0[n], y0[n], h, w, a=amps[n], dx=None, dy=None, verbose=False)
        targets = np.concatenate((targets, target), axis=0)

    if verbose:
        print(targets)

    return targets


def img2tgs(grayimg, bg=0, noise=None, TH=None, SA=None, gdshape=None):
    r"""image to targets

    convert image to targets.


    Parameters
    ----------
    grayimg : {``numpy 2D-array``}
        gray image with size of (H, W), double [0, 1]
    bg : {``number``}, optional
        background value, 0:black, 1:white (default: {0})
    noise : {``str``}, optional
        noise type added to gray image, 'awgn': (default: {None})
    TH : {``number``}, optional
        threshold for obtain foreground targets (default: {None}, otsu)
    SA : {``list`` or ``tuple``}, optional
        scene area [xmin, xmax, ymin, ymax] (default: {None}, (-W / 2, W / 2, -H / 2, H / 2))
    gdshape : {``list`` or ``tuple``}, optional
        discreted scene size (default: {None}, (-W / 2, W / 2, -H / 2, H / 2))

    Returns
    -------
    targets : lists
        targets lists: [tg1, tg2, ..., tgn], tgi = [xi, yi, 0, 0, 0, 0, rcsi]
    """

    logging.info("---In img2tgs...")

    if np.ndim(grayimg) == 3:
        grayimg = np.mean(grayimg, axis=2)
    if noise is 'awgn':
        SNR = 3
        grayimg = matnoise(grayimg, noise='wgn', imp=1.0, SNR=SNR)

    if bg == 1.0:
        grayimg = 1.0 - grayimg

    if TH is None:
        TH = filters.threshold_otsu(grayimg)

    if SA is None:
        gY, gX = grayimg.shape
        SA = (-gX / 2.0, gX / 2.0, -gY / 2.0, gY / 2.0)

    gX = SA[1] - SA[0]
    gY = SA[3] - SA[2]

    if gdshape is None:
        dx = 1.0
        dy = 1.0
        gW = int(gX)
        gH = int(gY)
    else:
        gH, gW = gdshape
        dx = gX / (gW * 1.0)
        dy = gY / (gH * 1.0)

    [H, W] = grayimg.shape
    G = imresize(grayimg, oshape=(gH, gW), odtype=grayimg.dtype, preserve_range=True)
    grayimg = None

    xmin, xmax, ymin, ymax = SA

    logging.info('---convert image to targets...')

    # yy = np.linspace(ymin, ymax, gH, endpoint=True)
    yy = np.linspace(ymax, ymin, gH, endpoint=True)
    yy = np.repeat(yy, gW)
    yy = np.reshape(yy, (gH, gW))
    xx = np.linspace(xmin, xmax, gW, endpoint=True)
    xx = np.repeat(xx, gH)
    xx = np.reshape(xx, (gW, gH)).transpose()
    vx = np.zeros((gH, gW))
    vy = np.zeros((gH, gW))
    ax = np.zeros((gH, gW))
    ay = np.zeros((gH, gW))

    ii = (G > TH)

    targets = np.vstack(
        (xx[ii], yy[ii], vx[ii], vy[ii], ax[ii], ay[ii], G[ii]))
    targets = targets.transpose()

    # targets = []
    # for i in range(0, H):
    #     for j in range(0, W):
    #         G = grayimg[i, j]
    #         if G >= TH:
    #             # H:x-W:y
    #             # target = [i - H / 2, j - W / 2, 0, 0, 0, 0, G]
    #             # H:y-W:x
    #             # target = [xx[i, j], yy[i, j], 0, 0, 0, 0, G]
    #             target = [H - xx[i, j], yy[i, j], 0, 0, 0, 0, G]
    #             targets.append(target)
    #             # print(target)

    logging.info('---Done!')

    logging.info("---Out img2tgs.")

    return targets
