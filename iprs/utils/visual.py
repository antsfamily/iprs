#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-13 10:34:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

from __future__ import division, print_function, absolute_import
import numpy as np
import matplotlib.pyplot as plt
from iprs.utils.const import *


def show_targets(targets, imgshape, outfile=None, isshow=True):
    W = imgshape[1]
    H = imgshape[0]
    I = np.zeros((H, W))
    # print(I.shape, "++++++==")

    if targets is None:
        raise ValueError("targets should not be None")
    targets = np.array(targets)
    targets[:, 0] = targets[:, 0] + H / 2.0
    targets[:, 1] = targets[:, 1] + W / 2.0
    # print(targets)
    for target in targets:
        # print(int(target[0]), int(target[1]))
        I[int(target[0]), int(target[1])] = target[-1]

    extent = [-W / 2.0, W / 2.0, H / 2.0, -H / 2.0]
    # extent = [0, W, H, 0]
    plt.close()
    plt.figure()
    plt.imshow(I, extent=extent,
               aspect=None, interpolation='none')
    plt.colorbar()

    if outfile is not None:
        plt.savefig(outfile)
        print("target image has been saved to: ", outfile)
    if isshow:
        plt.show()
        plt.close()
    else:
        plt.close()
    return I


def show_amplitude_phase(Srx, Title=None, keepAspectRatio=True):
    if Title is None:
        Title = 'SAR raw data, '

    plt.figure()
    plt.subplot(121)
    plt.imshow(np.absolute(
        Srx), aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.title(Title + "amplitude")

    plt.subplot(122)
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.angle(Srx), interpolation='none')
    plt.title(Title + "phase")
    # plt.colorbar()
    plt.show()


def show_response(Srx, extent=None, title="Figure", keepAspectRatio=True):
    print(np.absolute(Srx))
    plt.figure()
    # f.suptitle(title)
    plt.title(title)
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.absolute(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.show()


def showReImAmplitudePhase(Srx, extent=None, title="Figure", keepAspectRatio=True, ):
    f = plt.figure()
    f.suptitle(title)
    plt.subplot(221)
    plt.title("SAR response, module")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.absolute(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(222)
    plt.title("SAR response, phase")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.angle(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(223)
    plt.title("SAR response, Re")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.real(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(224)
    plt.title("SAR response, Im")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.imag(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.show()


def show_image(img, Title=None, keepAspectRatio=True, outfile=None, isshow=True):
    H = img.shape[0]
    W = img.shape[1]

    if Title is None:
        Title = "Image"
    extent = [-W / 2.0, W / 2.0, H / 2.0, -H / 2.0]
    # extent = [0, W, H, 0]

    plt.figure()
    plt.title(Title)
    plt.imshow(img, extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')

    plt.colorbar()

    if outfile is not None:
        plt.savefig(outfile)
        print("image has been saved to: ", outfile)

    if isshow:
        plt.show()
    else:
        plt.close()
    # print("666666666666666666666")
    return img


def show_sarimage(Sr_img, sarplat, axismod=None, title=None, aspect=None, outfile=None):
    """
    axismod
    """

    xmin = sarplat.params['xmin']  # amin
    xmax = sarplat.params['xmax']  # amax
    ymin = sarplat.params['ymin']  # rmin
    ymax = sarplat.params['ymax']  # rmax
    Rmin = sarplat.params['Rmin']
    Rmax = sarplat.params['Rmax']
    rmin = sarplat.params['rmin']
    rmax = sarplat.params['rmax']
    SC = sarplat.acquisition['SceneCenter']
    ta = sarplat.params['ta']
    tr = sarplat.params['tr']
    da = sarplat.params['da']
    dr = sarplat.params['dr']
    Na = sarplat.params['Na']
    Nr = sarplat.params['Nr']
    Ad = sarplat.acquisition['Ad']
    V = sarplat.sensor['V']

    # for plt x: horizontal --> range, y: vertical --> azimuth
    if axismod is None:
        axismod = 'Image'

    if axismod is 'Image':
        [amax, rmax] = Sr_img.shape
        extent = [1, rmax, amax, 1]
    elif axismod is 'SceneAbsolute':
        extent = [ymin, ymax, xmax, xmin]
    elif axismod is 'SceneRelative':
        extent = [ymin - SC[1], ymax - SC[1], xmax - SC[0], xmin - SC[0]]
    else:
        extent = [ta[0] * V, ta[-1] * V, tr[0] * C, tr[-1] * C]

    # print(extent)
    extent = np.array(extent)

    plt.figure()
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.title(title)
    plt.imshow(np.absolute(Sr_img), extent=extent,
               aspect=aspect, interpolation='none')
    plt.colorbar()
    if outfile is not None:
        plt.savefig(outfile)
        print("sar image has been saved to: ", outfile)

    plt.show()
