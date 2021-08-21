#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-23 21:14:04
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
import matplotlib.pyplot as plt


# ========================================================================
# ---this file is for Target-to-Background Ratio (TBR)
# ---see "Samadi S , M Cetin, Masnadishirazi M A .
#        Sparse representation-based synthetic aperture radar imaging[J].
#        Radar Sonar & Navigation Iet, 2011, 5(2):182-193.""
# ========================================================================


def tbr1(rec, ref, TH=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        {\rm{TBR}} = 20{\rm{lo}}{{\rm{g}}_{10}}\left( {\frac{{{\rm{ma}}{{\rm{x}}_{i \in \mathbb{T}}}(|{{\bf{I}}_i}|)}}{{(1/{N_\mathbb{B}}){\Sigma _{j \in \mathbb{B}}}|{{\bf{I}}_j}|}}} \right)

    Parameters
    ----------
    rec : {numpy ndarray}
        reconstructed, if complex, abs(rec) is used
    ref : {numpy ndarray}
        reference, if complex, abs(ref) is used
    TH : {float}, optional
        for getting Target regions, tg>TH, bg<TH (the default is None, which rec will be scaled by it's maximum value)
    isshow : {bool}, optional
        show target seprated by TH in both reconstructed and reference (the default is False)

    Returns
    -------
    TBR : float
        Target-to-Background Ratio (TBR).
    """

    ABS_REC = np.abs(rec)
    ABS_REF = np.abs(ref)

    if TH is None:
        ABS_REF = ABS_REF / np.max(ABS_REF)
        TH = 0.5

    # mask of BG
    BGM = np.zeros(ABS_REF.shape)
    BGM[ABS_REF < TH] = 1

    # mask of TG
    TGM = 1 - BGM

    # pixel number of bgs
    NB = np.sum(BGM)

    R = np.max(ABS_REC * TGM) / (((1 / NB) * np.sum(ABS_REC * BGM)) + 1e-13)

    TBR = 20 * np.log10(R)

    if isshow:
        plt.figure
        plt.subplot(121)
        plt.imshow(ABS_REF * TGM)
        plt.subplot(122)
        plt.imshow(ABS_REC * TGM)
        plt.show()

    return TBR


def tbr2(rec, tgregions=None, isshow=False):
    r"""Target-to-Background Ratio (TBR)

    .. math::
        {\rm{TBR}} = 20{\rm{lo}}{{\rm{g}}_{10}}\left( {\frac{{{\rm{ma}}{{\rm{x}}_{i \in \mathbb{T}}}(|{{\bf{I}}_i}|)}}{{(1/{N_\mathbb{B}}){\Sigma _{j \in \mathbb{B}}}|{{\bf{I}}_j}|}}} \right)

    Parameters
    ----------
    rec : {numpy ndarray}
        reconstructed, if complex, abs(rec) is used
    tgregions : {lists}, optional
        target regions:[[TG1],[TG2], ..., [TGn]], [TGk] = [lefttop, rightbottom]] (default: {None}
    isshow : {bool}, optional
        show target mask given by tgregions and selected target regions in reference] (default: {False}

    Returns
    -------
    TBR : float
        Target-to-Background Ratio (TBR)

    Raises
    ------
    TypeError
        tgregions mast be given
    """

    ABS_REC = np.abs(rec)

    if tgregions is None:
        raise TypeError("Please give the region of target!")

    # mask of TG
    TGM = np.zeros(ABS_REC.shape)
    # print(TGM, ABS_REC.shape)

    for tgregion in tgregions:
        TGM[tgregion[0]:tgregion[2], tgregion[1]:tgregion[3]] = 1

    # mask of BG
    BGM = 1 - TGM

    # pixel number of bgs
    NB = np.sum(BGM)

    R = np.max(ABS_REC * TGM) / (((1 / NB) * np.sum(ABS_REC * BGM)) + 1e-13)

    TBR = 20 * np.log10(R)

    if isshow:
        plt.figure
        plt.subplot(121)
        plt.imshow(TGM)
        plt.subplot(122)
        plt.imshow(ABS_REC * TGM)
        plt.show()

    return TBR


if __name__ == '__main__':

    rec = np.zeros((6, 6))
    ref = np.zeros((6, 6))

    # rec[1:4, 1:5] = 10
    # rec[0:6, 0:6] = 10
    # rec[1:5, 1:5] = 10
    # rec[2:3, 2:3] = 10
    rec[2:4, 2:4] = 10
    # rec[2:5, 2:5] = 100
    # rec[2:5, 2:5] = 10
    ref[2:5, 2:5] = 10

    print(rec)
    print("---------")
    print(ref)

    TBR = tbr1(rec, ref)

    print("TBR", TBR)
