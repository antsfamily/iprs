#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 21:14:04
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import random
from .data import format_data


def sparse_observation(X, way=0, mode='uniformly', rsample=(0.5, 0.5)):
    r"""
    X: numpy array: N-Na-Nr or N-Na-Nr-Nc
    """
    # np.random.seed(2018)

    Y = np.array(X.copy())

    if np.ndim(Y) is 3:
        N, Na, Nr = Y.shape
    elif np.ndim(Y) is 4:
        N, Na, Nr, Nc = Y.shape

    obmat, _, _, nNas, nNrs, _, _ = gen_sample_mask(
        (Na, Nr), mode=mode, rsample=rsample)

    if way is 0:  # [N Nsa Nsr] complex
        if np.ndim(Y) is 3:
            YYY = np.zeros((N, nNas, nNrs), dtype=Y.dtype)
        elif np.ndim(Y) is 4:
            YYY = np.zeros((N, nNas, nNrs, Nc), dtype=Y.dtype)

        for n in range(len(Y)):
            YY = Y[n]
            # print(YY.shape)
            YY = YY[obmat > 0]
            # print(YY.shape, (nNas, nNrs))
            YYY[n] = np.reshape(YY, (nNas, nNrs))
        return YYY, obmat

    if way is 1:  # [N Na Nr] complex
        for n in range(len(Y)):
            Y[n] = np.multiply(Y[n], obmat)
        return Y, obmat

    if way is 2:  # [2 N Na Nr]
        for n in range(len(Y[0])):
            Y[0][n] = np.multiply(Y[0][n], obmat)
            Y[1][n] = np.multiply(Y[1][n], obmat)
        return Y, obmat

    if way is 3:  # [N 2 Na Nr]
        for n in range(len(Y)):
            Y[n][0] = np.multiply(Y[n][0], obmat)
            Y[n][1] = np.multiply(Y[n][1], obmat)
        return Y
    if way is 4:  # [N Na Nr 2]
        Y = format_data(Y, modefrom='chnl_last', modeto='chnl_first')
        for n in range(len(Y)):
            Y[n][0] = np.multiply(Y[n][0], obmat)
            Y[n][1] = np.multiply(Y[n][1], obmat)
        Y = format_data(Y, modefrom='chnl_first', modeto='chnl_last')

        return Y, obmat
    # if way is 5:


def gen_sample_mask(maskshape, mode='uniformly', rsample=(0.5, 0.5)):
    """[summary]

    [description]

    Arguments:
        maskshape {[type]} -- [description]

    Keyword Arguments:
        mode {str} -- [description] (default: {'uniformly'})
        rsample {tuple} -- [description] (default: {(0.5, 0.5)})
    """
    (Na, Nr) = maskshape
    obmat1 = np.zeros((Na, Nr))
    obmat2 = np.zeros((Na, Nr))

    nNas = int(Na * rsample[0])
    nNrs = int(Nr * rsample[1])

    if mode is 'uniformly':
        dNas = int(1.0 / rsample[0])
        dNrs = int(1.0 / rsample[1])

        idxNas = range(0, Na, dNas)
        idxNrs = range(0, Nr, dNrs)

    elif mode is 'randomly':
        idxNas = random.sample(range(Na), nNas)
        idxNrs = random.sample(range(Nr), nNrs)
    elif mode is None:
        return
    else:
        raise ValueError("Not Support!")

    # print(len(idxNas), len(idxNrs))
    # print(idxNas[0:10], idxNrs[0:10])

    obmat1[idxNas, :] = 1
    obmat2[:, idxNrs] = 1

    obmat = obmat1 * obmat2
    return obmat, obmat1, obmat2, nNas, nNrs, idxNas, idxNrs


def process_sarplat(sarplat, rsample=None):
    """

    only support uniform sampling

    Arguments:
        sarplat {[type]} -- [description]

    Keyword Arguments:
        rsample {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """

    if rsample is None:
        return
    sarplat0 = iprs.SarPlat()
    sarplat0.name = sarplat.name
    sarplat0.sensor = sarplat.sensor
    sarplat0.acquisition = sarplat.acquisition
    sarplat0.params = sarplat.params

    sarplat0 = sarplat
    Fs = sarplat.sensor['Fs']
    sarplat0.sensor['Fs'] = Fs * rsample[1]
    PRF = sarplat.sensor['PRF']
    sarplat0.sensor['PRF'] = PRF * rsample[0]
    fr = sarplat.params['fr']
    tr = sarplat.params['tr']
    fa = sarplat.params['fa']
    ta = sarplat.params['ta']
    Nr = sarplat.params['Nr']
    Na = sarplat.params['Na']
    dNas = int(1.0 / rsample[0])
    dNrs = int(1.0 / rsample[1])
    idxNas = range(0, Na, dNas)
    idxNrs = range(0, Nr, dNrs)

    sarplat0.params['fr'] = fr[idxNrs]
    sarplat0.params['tr'] = tr[idxNrs]
    sarplat0.params['fa'] = fa[idxNas]
    sarplat0.params['ta'] = ta[idxNas]
    sarplat0.params['Nr'] = len(idxNrs)
    sarplat0.params['Na'] = len(idxNas)

    # print(len(fr[idxNas]))
    # print(len(fr[idxNas]))
    # print(sarplat0.params['Na'])
    # print(sarplat0.params['Nr'])

    return sarplat0
