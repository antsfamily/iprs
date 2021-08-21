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
from iprs.sharing.slant_ground_range import slantr2groundr, groundr2slantr
from skimage import exposure
from mpl_toolkits.mplot3d import Axes3D
# import mayavi.mlab as mlab


def show_targets(targets, SA, imgshape, extent=None, outfile=None, isshow=True):
    r"""show targets

    Show targets in an image.

    Arguments
    --------------
    targets {[type]}
        [description]
    imgshape {[type]}
        [description]

    Keyword Arguments
    --------------
    outfile {[type]}
        [description] (default: {None})
    isshow {bool}
        [description] (default: {True})

    Returns
    --------------
        [type] -- [description]

    Raises
    --------------
        ValueError -- [description]
    """
    H = imgshape[0]
    W = imgshape[1]
    II = np.zeros((H, W))
    # print(II.shape, "++++++==")

    if targets is None:
        raise ValueError("targets should not be None")
    targets = np.array(targets)

    Lx = SA[1] - SA[0]
    Ly = SA[3] - SA[2]
    dX = Lx / (W * 1.0)
    dY = Ly / (H * 1.0)

    targets[:, 0] = (targets[:, 0] - SA[0]) / dX - 1
    targets[:, 1] = (targets[:, 1] - SA[2]) / dY - 1

    # print(targets)
    for target in targets:
        II[int(target[1]), int(target[0])] = target[-1]  # W:x, H:y

    if extent is None:
        extent = SA

    II = np.flipud(II)
    plt.close()
    plt.figure()
    plt.imshow(II, extent=extent, aspect=None, interpolation='none')
    # plt.imshow(II)
    plt.colorbar()

    if outfile is not None:
        plt.savefig(outfile)
        print("target image has been saved to: ", outfile)
    if isshow:
        plt.show()
        plt.close()
    else:
        plt.close()
    return II


def show_amplitude_phase(Srx, Title=None, cmap=None, extent=None, keepAspectRatio=True, outfile=None, isshow=True):
    r"""[summary]

    [description]

    Parameters
    ----------
    Srx : {[type]}
        [description]
    Title : {[type]}, optional
        [description] (the default is None, which [default_description])
    cmap : {[type]}, optional
        [description] (the default is None, which [default_description])
    extent : {[type]}, optional
        [description] (the default is None, which [default_description])
    keepAspectRatio : {bool}, optional
        [description] (the default is True, which [default_description])
    outfile : {[type]}, optional
        [description] (the default is None, which [default_description])
    isshow : {bool}, optional
        [description] (the default is True, which [default_description])
    """
    if Title is None:
        Title = 'SAR raw data'

    plt.figure()
    plt.subplot(121)
    plt.imshow(np.absolute(
        # Srx), aspect='auto' if not keepAspectRatio else None,
        # interpolation='none')
        Srx), extent=extent, aspect='auto' if not keepAspectRatio else None, interpolation='none', cmap=cmap)
    # plt.xlabel("Range (m)")
    # plt.ylabel("Azimuth (m)")
    plt.xlabel("Range\n(a)")
    plt.ylabel("Azimuth")
    plt.title(Title + " (amplitude)")

    plt.subplot(122)
    # plt.xlabel("Range (m)")
    # plt.ylabel("Azimuth (m)")
    plt.xlabel("Range\n(b)")
    plt.ylabel("Azimuth")
    plt.imshow(np.angle(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none', cmap=cmap)
    plt.title(Title + " (phase)")
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)
        print("image has been saved to: ", outfile)
    # plt.colorbar()
    if isshow:
        plt.show()
    else:
        plt.close()


def show_response(Srx, extent=None, title="Figure", keepAspectRatio=True, outfile=None, isshow=True):
    r"""show SAR response

    [description]

    Arguments
    ------------------
    Srx {[type]}
        [description]

    Keyword Arguments
    ------------------
    extent {[type]}
        [description] (default: {None})
    title {str}
        [description] (default: {"Figure"})
    keepAspectRatio {bool}
        [description] (default: {True})
    outfile {[type]}
        [description] (default: {None})
    isshow {bool}
        [description] (default: {True})
    """

    plt.figure()
    plt.title(title)
    plt.xlabel("Range (m)")
    plt.ylabel("Azimuth (m)")
    extent = [27844.409098089047, 28868.409098089047, 512.0, -512.0]
    plt.imshow(np.absolute(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    if outfile is not None:
        plt.savefig(outfile)
        print("image has been saved to: ", outfile)
    if isshow:
        plt.show()
    else:
        plt.close()


def showReImAmplitudePhase(Srx, extent=None, title="Figure", keepAspectRatio=True):
    r"""[summary]

    [description]

    Parameters
    ----------
    Srx : {[type]}
        [description]
    extent : {[type]}, optional
        [description] (the default is None, which [default_description])
    title : {str}, optional
        [description] (the default is "Figure", which [default_description])
    keepAspectRatio : {bool}, optional
        [description] (the default is True, which [default_description])
    """

    f = plt.figure()
    f.suptitle(title)
    plt.subplot(221)
    plt.title("SAR response, module")
    # plt.xlabel("Range (m)")
    # plt.ylabel("Azimuth (m)")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.absolute(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(222)
    plt.title("SAR response (phase)")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.angle(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(223)
    plt.title("SAR response (real part)")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.real(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.subplot(224)
    plt.title("SAR response (imaginary part)")
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    plt.imshow(np.imag(Srx), extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none')
    plt.colorbar()
    plt.show()


def show_image(img, Title=None, cmap=None, keepAspectRatio=True, outfile=None, isshow=True):
    H = img.shape[0]
    W = img.shape[1]

    if Title is None:
        # Title = "Image"
        Title = "Intensity"
    extent = [-W / 2.0, W / 2.0, -H / 2.0, H / 2.0]
    # extent = [0, W, H, 0]

    plt.figure()
    ax = plt.subplot(111)
    plt.title(Title)
    plt.xlabel("Range")
    plt.ylabel("Azimuth")
    # plt.xticks(fontsize=17)
    # plt.yticks(fontsize=17)
    # ax.set_xlabel("Range", fontsize=17)
    # ax.set_ylabel("Azimuth", fontsize=17)
    # ax.legend(fontsize=17)
    plt.imshow(img, extent=extent,
               aspect='auto' if not keepAspectRatio else None, interpolation='none', cmap=cmap)

    plt.colorbar()

    if outfile is not None:
        plt.savefig(outfile)
        print("image has been saved to: ", outfile)

    if isshow:
        plt.show()
        pass
    else:
        plt.close()
    return img


def sarshow(SI, sarplat, maxp=None, axismod=None, title=None, cmap=None, aspect=None, outfile=None, newfig=True, figsize=None):
    r"""show sar image

    show sar image

    Arguments:
        SI {[type]} -- [description]
        sarplat {[type]} -- [description]

    Keyword Arguments:
        axismod {[type]} -- [description] (default: {None})
        title {[type]} -- [description] (default: {None})
        cmap {[type]} -- [description] (default: {None})
        maxp {bool} -- [description] (default: {False})
        aspect {[type]} -- [description] (default: {None})
        outfile {[type]} -- [description] (default: {None})
        newfig {bool} -- [description] (default: {True})
        figsize {[type]} -- [description] (default: {None})
    """

    xmin = sarplat.params['xminSub']  # amin
    xmax = sarplat.params['xmaxSub']  # amax
    ymin = sarplat.params['yminSub']  # rmin
    ymax = sarplat.params['ymaxSub']  # rmax
    SA = sarplat.selection['SubSceneArea']
    SC = sarplat.selection['SubSceneCenter']
    BA = sarplat.selection['SubBeamArea']
    BC = sarplat.selection['SubBeamCenter']
    ta = sarplat.params['taSub']
    SubRnear = sarplat.params['SubRnear']
    SubRfar = sarplat.params['SubRfar']
    SubRbc = sarplat.params['SubRbc']
    SubRsc = sarplat.params['SubRsc']
    tr = sarplat.params['trSub']
    DX = sarplat.params['DX']
    DY = sarplat.params['DY']
    GM = sarplat.params['GeometryMode']
    H = sarplat.sensor['H']
    V = sarplat.sensor['V']
    Ar = sarplat.acquisition['Ar']

    Na, Nr = SI.shape
    nTicks = 10

    if maxp is None:
        maxp = (np.median(SI) + np.max(SI)) / 3.
        # maxp = np.max(SI) * 0.886 * 0.886
    print(maxp, "maxp")
    # print(rmin, rmax, SC, PC, DX, DY)
    # for plt x: horizontal --> range, y: vertical --> azimuth
    if axismod is None:
        axismod = 'Image'

    if axismod is 'Image':
        [amax, rmax] = SI.shape
        extent = [1, rmax, 1, amax]
        xlabelstr = "Range"
        ylabelstr = "Azimuth"
    elif axismod == 'SceneAbsoluteSlantRange':
        if GM == 'BG':
            extent = [SubRnear, SubRfar, BA[2], BA[3]]
        if GM == 'SG':
            extent = [SubRnear, SubRfar, SA[2], SA[3]]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneRelativeSlantRange':
        if GM == 'BG':
            extent = [SubRnear - SubRbc, SubRfar - SubRbc, BA[2], BA[3]]
        if GM == 'SG':
            extent = [SubRnear - SubRsc, SubRfar - SubRsc, SA[2], SA[3]]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneAbsoluteGroundRange':
        if GM == 'BG':
            X = slantr2groundr(C * tr / 2., H, Ar, 0)
            extent = [X[0], X[-1], BA[2], BA[3]]
        if GM == 'SG':
            X = slantr2groundr(C * tr / 2., H, Ar, 0)
            extent = [X[0], X[-1], SA[2], SA[3]]
        xticks = X[::int(len(X) / nTicks)]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneRelativeGroundRange':
        if GM == 'BG':
            X = slantr2groundr(C * tr / 2., H, Ar, BC[0])
            extent = [X[0], X[-1], BA[2], BA[3]]
        if GM == 'SG':
            X = slantr2groundr(C * tr / 2., H, Ar, SC[0])
            extent = [X[0], X[-1], SA[2], SA[3]]
        xticks = X[::int(len(X) / nTicks)]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    else:
        extent = [ta[0] * V, ta[-1] * V, tr[0] * C, tr[-1] * C]
        xlabelstr = 'x'
        ylabelstr = 'y'

    # print(extent)
    extent = np.array(extent)

    if newfig:
        plt.figure(figsize=figsize)
        ax = plt.subplot(111)

    plt.xlabel(xlabelstr)
    plt.ylabel(ylabelstr)

    A = np.absolute(SI)

    plt.title(title)

    ax.imshow(A, extent=extent, vmax=maxp, aspect=aspect, interpolation='none', cmap=cmap)

    if axismod == 'SceneAbsoluteGroundRange' or axismod == 'SceneRelativeGroundRange':
        # plt.xticks(xticks)
        pass
        # ax.xaxis.set_major_locator(FixedLocator(X[::int(len(X) / 10.)]))
    # plt.colorbar()
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)
        print("sar image has been saved to: ", outfile)

    if newfig:
        plt.show()


def show_sarimage(SI, sarplat, axismod=None, title=None, cmap=None, isimgadj=False, aspect=None, outfile=None, newfig=True, figsize=None):
    r"""[summary]

    [description]

    Arguments:
        SI {[type]} -- [description]
        sarplat {[type]} -- [description]

    Keyword Arguments:
        axismod {[type]} -- [description] (default: {None})
        title {[type]} -- [description] (default: {None})
        cmap {[type]} -- [description] (default: {None})
        isimgadj {bool} -- [description] (default: {False})
        aspect {[type]} -- [description] (default: {None})
        outfile {[type]} -- [description] (default: {None})
        newfig {bool} -- [description] (default: {True})
        figsize {[type]} -- [description] (default: {None})
    """

    xmin = sarplat.params['xminSub']  # amin
    xmax = sarplat.params['xmaxSub']  # amax
    ymin = sarplat.params['yminSub']  # rmin
    ymax = sarplat.params['ymaxSub']  # rmax
    SA = sarplat.selection['SubSceneArea']
    SC = sarplat.selection['SubSceneCenter']
    BA = sarplat.selection['SubBeamArea']
    BC = sarplat.selection['SubBeamCenter']
    ta = sarplat.params['taSub']
    SubRnear = sarplat.params['SubRnear']
    SubRfar = sarplat.params['SubRfar']
    SubRbc = sarplat.params['SubRbc']
    SubRsc = sarplat.params['SubRsc']
    tr = sarplat.params['trSub']
    DX = sarplat.params['DX']
    DY = sarplat.params['DY']
    GM = sarplat.params['GeometryMode']
    H = sarplat.sensor['H']
    V = sarplat.sensor['V']
    Ar = sarplat.acquisition['Ar']

    Na, Nr = SI.shape
    nTicks = 10

    # print(rmin, rmax, SC, PC, DX, DY)
    # for plt x: horizontal --> range, y: vertical --> azimuth
    if axismod is None:
        axismod = 'Image'

    if axismod is 'Image':
        [amax, rmax] = SI.shape
        extent = [1, rmax, 1, amax]
        xlabelstr = "Range"
        ylabelstr = "Azimuth"
    elif axismod == 'SceneAbsoluteSlantRange':
        if GM == 'BG':
            extent = [SubRnear, SubRfar, BA[2], BA[3]]
        if GM == 'SG':
            extent = [SubRnear, SubRfar, SA[2], SA[3]]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneRelativeSlantRange':
        if GM == 'BG':
            extent = [SubRnear - SubRbc, SubRfar - SubRbc, BA[2], BA[3]]
        if GM == 'SG':
            extent = [SubRnear - SubRsc, SubRfar - SubRsc, SA[2], SA[3]]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneAbsoluteGroundRange':
        if GM == 'BG':
            X = slantr2groundr(C * tr / 2., H, Ar, 0)
            extent = [X[0], X[-1], BA[2], BA[3]]
        if GM == 'SG':
            X = slantr2groundr(C * tr / 2., H, Ar, 0)
            extent = [X[0], X[-1], SA[2], SA[3]]
        xticks = X[::int(len(X) / nTicks)]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod == 'SceneRelativeGroundRange':
        if GM == 'BG':
            X = slantr2groundr(C * tr / 2., H, Ar, BC[0])
            extent = [X[0], X[-1], BA[2], BA[3]]
        if GM == 'SG':
            X = slantr2groundr(C * tr / 2., H, Ar, SC[0])
            extent = [X[0], X[-1], SA[2], SA[3]]
        xticks = X[::int(len(X) / nTicks)]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    else:
        extent = [ta[0] * V, ta[-1] * V, tr[0] * C, tr[-1] * C]
        xlabelstr = 'x'
        ylabelstr = 'y'

    # print(extent)
    extent = np.array(extent)

    if newfig:
        plt.figure(figsize=figsize)
        ax = plt.subplot(111)

    plt.xlabel(xlabelstr)
    plt.ylabel(ylabelstr)

    SI = np.flipud(SI)

    A = np.absolute(SI)

    plt.title(title)

    if isimgadj:
        A = A / A.max()
        A = 20 * np.log10(A + EPS)
        a = np.abs(A.mean())
        A = (A + a) / a * 255
        A[A < 0] = 0
        A = A.astype('uint8')
        A = np.flipud(A)

    ax.imshow(A, extent=extent, aspect=aspect, interpolation='none', cmap=cmap)

    if axismod == 'SceneAbsoluteGroundRange' or axismod == 'SceneRelativeGroundRange':
        # plt.xticks(xticks)
        pass
        # ax.xaxis.set_major_locator(FixedLocator(X[::int(len(X) / 10.)]))
    # plt.colorbar()
    plt.tight_layout()
    if outfile is not None:
        plt.savefig(outfile)
        print("sar image has been saved to: ", outfile)

    if newfig:
        plt.show()


def show_sarimage3d(SI, sarplat, axismod=None, title=None, cmap=None, isimgadj=False, aspect=None, outfile=None, figsize=None):
    r"""[summary]

    [description]

    Arguments:
        SI {[type]} -- [description]
        sarplat {[type]} -- [description]

    Keyword Arguments:
        axismod {[type]} -- [description] (default: {None})
        title {[type]} -- [description] (default: {None})
        cmap {[type]} -- [description] (default: {None})
        isimgadj {bool} -- [description] (default: {False})
        aspect {[type]} -- [description] (default: {None})
        outfile {[type]} -- [description] (default: {None})
        figsize {[type]} -- [description] (default: {None})
    """

    xmin = sarplat.params['xminSub']  # amin
    xmax = sarplat.params['xmaxSub']  # amax
    ymin = sarplat.params['yminSub']  # rmin
    ymax = sarplat.params['ymaxSub']  # rmax
    Rnear = sarplat.params['Rnear']
    Rfar = sarplat.params['Rfar']
    SC = sarplat.acquisition['SubSceneCenter']
    PC = sarplat.acquisition['SubPlatCenter']
    ta = sarplat.params['taSub']
    tr = sarplat.params['trSub']
    da = sarplat.params['daSub']
    Tsr = sarplat.params['drSub']
    Na = sarplat.params['SubNa']
    Nr = sarplat.params['SubNr']
    Ad = sarplat.acquisition['Ad']
    V = sarplat.sensor['V']
    DX = sarplat.params['SubDX']
    DY = sarplat.params['SubDY']

    # print(rmin, rmax, SC, PC, DX, DY)
    # for plt x: horizontal --> range, y: vertical --> azimuth
    if axismod is None:
        axismod = 'Image'

    if axismod is 'Image':
        [amax, rmax] = SI.shape
        extent = [1, rmax, amax, 1]
        xlabelstr = "Range"
        ylabelstr = "Azimuth"
    elif axismod is 'SceneAbsolute':
        extent = [ymin, ymax, xmax, xmin]
        print(extent)
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
    elif axismod is 'SceneRelative':
        extent = [ymin - SC[1], ymax - SC[1], xmax - SC[0], xmin - SC[0]]
        xlabelstr = "Range (m)"
        ylabelstr = "Azimuth (m)"
        # xlabelstr = "Range"
        # ylabelstr = "Azimuth"
    else:
        extent = [ta[0] * V, ta[-1] * V, tr[0] * C, tr[-1] * C]
        xlabelstr = 'x'
        ylabelstr = 'y'

    # print(extent)
    extent = np.array(extent)
    Z = np.absolute(SI)
    if isimgadj:
        Z = exposure.adjust_log(Z)
    Z = np.flipud(Z)
    # fig = plt.figure(figsize=figsize)
    M, N = np.shape(Z)
    print(M, N)

    X = np.arange(0, N, 1)
    Y = np.arange(0, M, 1)
    X, Y = np.meshgrid(X, Y)
    print(X.shape, Y.shape, Z.shape)

    # mlab.figure(size=(400, 500))
    # mlab.mesh(X, Y, Z)
    # mlab.surf(X, Y, Z)
    # mlab.colorbar()
    # mlab.xlabel(xlabelstr)
    # mlab.ylabel(ylabelstr)
    # mlab.zlabel("Amplitude")
    # mlab.title(title)
    # mlab.show()

    if outfile is not None:
        # mlab.savefig(outfile)
        print("sar image has been saved to: ", outfile)


def imshow(X, cmap=None, norm=None, aspect=None, interpolation=None, alpha=None,
           vmin=None, vmax=None, origin=None, extent=None, shape=None,
           filternorm=1, filterrad=4.0, imlim=None, resample=None, url=None,
           hold=None, data=None, **kwargs):
    """show an image

    This function create an figure and show an image, see ``pyplot.imshow`` for documentation.

    """

    plt.figure()
    plt.imshow(X, cmap=cmap, norm=norm, aspect=aspect, interpolation=interpolation, alpha=alpha,
               vmin=vmin, vmax=vmax, origin=origin, extent=extent, shape=shape,
               filternorm=filternorm, filterrad=filterrad, imlim=imlim, resample=resample, url=url, hold=hold, data=data, **kwargs)
    plt.show()
    return 0
