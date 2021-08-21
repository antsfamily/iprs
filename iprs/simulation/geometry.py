#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 10:28:33
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np


def rectangle(SceneArea, x0, y0, h, w, a=None, dx=None, dy=None, verbose=False):
    r"""rectangle area

    generates rectangle area

    Parameters
    ----------
    SceneArea : {list or tuple}
        Scene Area, unit m, [xmin,xmax,ymin,ymax]
    x0 : {float}
        x center of rectangle, unit m (x: horizontal, y: vertical)
    y0 : {float}
        y center of rectangle, unit m (x: horizontal, y: vertical)
    h : {float}
        height of rectangle, unit m (the default is None, which generates randomly)
    w : {float}
        width of rectangle, unit m (the default is None, which generates randomly)
    a : {float}, optional
        amplitude (the default is None, which generates randomly)
    dx : {float}, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : {float}, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    verbose : {bool}, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    rects : ndarray
        rectangle area
    """

    if verbose:
        print(SceneArea)
    (Xmin, Xmax, Ymin, Ymax) = SceneArea
    if dx is None:
        dx = 1. / (Xmax - Xmin)
    if dy is None:
        dy = 1. / (Ymax - Ymin)

    if h is None:
        h = np.random.rand() * 100.
    if w is None:
        w = np.random.rand() * 100.

    if a is not None:
        g = a.copy()
    rects = []
    for x in np.linspace(max(x0 - w / 2., Xmin), min(x0 + w / 2., Xmax), int(w)):
        for y in np.linspace(max(y0 - h / 2., Ymin), min(y0 + h / 2., Ymax), int(h)):
            if a is None:
                g = np.random.rand()
            rects.append([x, y, 0, 0, 0, 0, g])

    rects = np.array(rects)

    if verbose:
        print(rects, rects.shape, "===++===")
    return rects


def disc(SceneArea, x0, y0, r, a=None, dx=None, dy=None, verbose=False):
    r"""disc area

    generates disc area


    Parameters
    ----------
    SceneArea : {list or tuple}
        Scene Area, [xmin,xmax,ymin,ymax]
    x0 : {number}
        x center of disc (x: horizontal, y: vertical)
    y0 : {number}
        y center of disc (x: horizontal, y: vertical)
    r : {number}
        radius of disc
    a : {number}, optional
        amplitude of disc (default: {None})
    dx : {float}, optional
        resolution in range (default: {1 / (xmax-xmin)})
    dy : {float}, optional
        resolution in azimuth (default: {1 / (ymax-ymin)})
    verbose : {bool}, optional
        show more log info (the default is False, which means does not show)

    Returns
    -------
    ccas : ndarray
        disk area
    """

    if verbose:
        print(SceneArea)
    (Xmin, Xmax, Ymin, Ymax) = SceneArea
    if dx is None:
        dx = 1. / (Xmax - Xmin)
    if dy is None:
        dy = 1. / (Ymax - Ymin)
    # print("disc: x0, y0, r, a, dx, dy --> ", x0, y0, r, a, dx, dy)
    r2 = r * r
    ccas = []
    if a is not None:
        g = a.copy()
    for x in np.linspace(max(x0 - r, Xmin), min(x0 + r, Xmax), int(2 * r)):
        for y in np.linspace(max(y0 - r, Ymin), min(y0 + r, Ymax), int(2 * r)):
            d = (x - x0) ** 2 + (y - y0) ** 2
            if d <= r2:
                if a is None:
                    g = np.random.rand()
                ccas.append([x, y, 0, 0, 0, 0, g])

    ccas = np.array(ccas)
    if verbose:
        print(ccas, ccas.shape, "===++===")
    return ccas

