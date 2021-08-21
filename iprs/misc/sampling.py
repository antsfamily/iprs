#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
#

import numpy as np
from PIL import Image


def dnsampling(X, ratio, axis=-1, mod='uniform', method='throwaway'):

    nDims = np.ndim(X)
    if type(axis) is int:
        if type(ratio) is not float:
            raise ValueError('Downsampling ratio should be a number!')
        else:
            if axis == -1:
                axis = list(range(0, nDims))
                ratio = [ratio] * nDims
            else:
                axis = [axis]
                ratio = [ratio]
    elif type(axis) is list or tuple:
        if len(axis) != len(ratio):
            raise ValueError('You should specify the DS ratio for each axis!')
    else:
        raise TypeError('Wrong type of axis!')

    if mod in ['uniform', 'UNIFORM', 'Uniform']:
        index = [slice(None)] * nDims
        for a, r in zip(axis, ratio):
            d = np.size(X, a)
            da = int(round(1. / r))
            index[a] = slice(0, d, da)
        index = tuple(index)

        if method in ['throwaway', 'THROWAWAY', 'Throwaway', 'ThrowAway']:
            return X[index]
        elif method in ['fillzeros', 'FILLZEROS', 'Fillzeros', 'FillZeros']:
            Y = np.zeros(X.shape, dtype=X.dtype)
            Y[index] = X[index]
            return Y
    else:
        pass

        return None


def upsampling(X, shape, axis=-1, method='Lanczos'):

    # Na, Nr = X.shape
    # Y = np.zeros(shape, dtype=X.dtype)
    # for a in range(Na):
    #     Y[a, :] = np.interp(range(shape[1]), range(Nr), X[a, :])
    # for r in range(Nr):
    #     Y[:, a] = np.interp(range(shape[0]), range(Na), X[:, r])

    # return Y

    print(shape, X.shape)
    imgXr = Image.fromarray(X[:, :, 0])
    # imgXr = imgXr.resize((shape[1], shape[0]), Image.LANCZOS)
    # imgXr = imgXr.resize((shape[1], shape[0]), Image.BILINEAR)
    imgXr = imgXr.resize((shape[1], shape[0]), Image.NEAREST)
    # imgXr = imgXr.resize((shape[1], shape[0]), Image.ANTIALIAS)
    imgXi = Image.fromarray(X[:, :, 1])
    # imgXi = imgXi.resize((shape[1], shape[0]), Image.LANCZOS)
    # imgXi = imgXi.resize((shape[1], shape[0]), Image.BILINEAR)
    imgXi = imgXi.resize((shape[1], shape[0]), Image.NEAREST)
    # imgXi = imgXi.resize((shape[1], shape[0]), Image.ANTIALIAS)
    return np.transpose(np.array([np.array(imgXr), np.array(imgXi)]), (1, 2, 0))


if __name__ == '__main__':

    Na, Nr, Nc = (9, 12, 2)
    x = np.random.randint(0, 1000, Na * Nr * Nc).reshape(Na, Nr, Nc)

    print(x[:, :, 0], 'x')
    print(x[:, :, 1], 'x')

    y = dnsampling(x, ratio=(0.2, 0.5), axis=(0, 1), mod='uniform', method='throwaway')
    print(y[:, :, 0], 'throwaway')
    print(y[:, :, 1], 'throwaway')

    y = dnsampling(x, ratio=(0.2, 0.5), axis=(0, 1), mod='uniform', method='fillzeros')
    print(y[:, :, 0], 'fillzeros')
    print(y[:, :, 1], 'fillzeros')
