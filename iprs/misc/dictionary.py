#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 20:59:03
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import numpy as np
from scipy.fftpack import dct, idct
from iprs.utils.const import *


def dctdic(dictshape, axis=-1, isnorm=False, verbose=True):
    r"""generates DCT dictionary

    Generates M-by-N DCT dictionary

    Arguments
    ---------------------
    dictshape { `list` or `tuple` }
        shape of DCT dict [M, N]

    Keyword Arguments
    ---------------------
    axis { `number` }
        Axis along which the dct is computed.
        If -1 then the transform is multidimensional(default=-1) (default: {-1})

    isnorm { `bool` }
        normalization (default: {False})

    verbose { `bool` }
        display log info (default: {True})

    Returns
    ---------------------
    D : `ndarray`
        DCT dictionary
    """

    print("================in dctdic================")
    (M, N) = dictshape
    if verbose:
        print("===Construct DCT dictionary...")
        print("---DCT dictionary shape: ", dictshape)

    DCTD = np.zeros((M, N))
    DCTD[:, 0] = 1.0 / np.sqrt(M)
    for k in range(1, N):
        idx = np.linspace(0, M, M)
        v = np.cos(idx * PI * k / N)
        # print(k, v)
        v = v - np.mean(v)
        norm = np.linalg.norm(v)
        # print(norm)
        if isnorm:
            if norm > 0:
                DCTD[:, k] = v / norm
    if verbose:
        print("===Done!")

    return DCTD


def dwtdic(dictshape, axis=-1):
    r"""generates DWT dictionary

    Generates M-by-N DWT dictionary

    Arguments
    -----------------------
    dictshape { `list` or `tuple` }
        shape of DWT dict [M, N]

    Keyword Arguments
    -----------------------
    axis { `number` }
        Axis along which the dct is computed.
        If -1 then the transform is multidimensional(default=-1) (default: {-1})

    isnorm { `bool` }
        normalization (default: {False})

    verbose { `bool` }
        display log info (default: {True})

    Returns
    ------------
    D : `ndarray`
        DWT dictionary
    """
    (M, N) = dictshape
    DWTD = np.zeros((M, N))
    print(M, N)
    DWTD[:, 0] = 1.0 / np.sqrt(M)
    for k in range(1, N):
        v = np.cos(np.array(range(M)) * PI * k / N)
        # print(k, v)
        v = v - np.mean(v)
        norm = np.linalg.norm(v)
        # print(norm)
        if norm > 0:
            DWTD[:, k] = v / norm

    return DWTD

# function [D] = OrthogonalDWT(nb)
# % =========================================================================
# % DESCRIPTION:
# % Get a orthogonal DWT dictionary for sparsifying the spectra of HSI. Only
# % when nb is the multiple of 4 (e.g. nb = 128), a dictionary of [nb,nb] can
# % be generated, and thus HSI X can be sparsely represented  as X = D * Y,
# % where Y is the sparse represnetation.
# % -------------------------------------------------------------------------
# % INPUT ARGUMENTS:
# % nb                    dimension of spectrum
# % -------------------------------------------------------------------------
# % OUTPUT ARGUMENTS:
# % D                     orthogonal DWT dictionary of size [nb,np]
# % -------------------------------------------------------------------------
# %
# WaveletName = 'db1';
# X = eye(nb,nb);
# [xm,xn] = size(X);
# DecLevel = max(floor(log2(xm)) - 1,1);
# [C0, S0] = wavedec(X(:,1), DecLevel, WaveletName);
# [mc,nc] = size(C0);
# D = zeros(mc,xn);
# D(:,1) = C0;
# L = S0;
# for i = 2 : xn
#     C0 = wavedec(X(:,i), DecLevel, WaveletName);
#     D(:,i) = C0;
# end
# D = D';
# end


if __name__ == '__main__':

    D = dctdic((256, 256))
    print(D)
