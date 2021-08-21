#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-25 09:53:21
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


import numpy as np

# ========================================================================
# ---this file is for Entropy of the full image (ENT),
#    a measure of image sharpness, the smaller the better
# ---see "Samadi S , M Cetin, Masnadishirazi M A .
#        Sparse representation-based synthetic aperture radar imaging[J].
#        Radar Sonar & Navigation Iet, 2011, 5(2):182-193."
# ========================================================================


def ent(rec, L=None, isshow=False):
    r"""Entropy of the full image (ENT)

    .. math::
        {\rm ENT} = -\sum_{i=0}^L p(i){\rm log}_2 p(i)

    where :math:`L` is the number of levels in the histogram,
    :math:`p(i)` denotes the normalised frequency of occurrence of each gray level

    Parameters
    ----------
    rec : ndarray
        reconstructed, if complex, abs(rec) is used.
    L : number, optional
        gray levels (default: {None=256})
    isshow : {bool}, optional
        show histogram (default: {False})

    Returns
    -------
    ENT : float
        Entropy of the full image (ENT)
    """

    rec = np.abs(rec)
    rec = rec.flatten()
    freq, _ = np.histogram(rec, bins=L, normed=True)
    ENT = -np.sum(freq * np.log2(freq))

    if isshow:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.hist(rec, bins=L, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.xlabel("levels")
        plt.ylabel("frequency")
        plt.title("frequency~levels")
        plt.show()

    return ENT


if __name__ == '__main__':

    A = np.array([[1, 1, 2, 2, 3, 3, 4, 4], [1, 2, 3, 1, 1, 1, 3, 3]])
    # A = np.array([1, 1, 2, 2, 3, 3, 4, 4, 1, 2, 3, 1, 1, 1, 3, 3])
    freq, levels = np.histogram(A, bins=4)
    freq, levels = np.histogram(A, bins=4, normed=True)
    print(A)
    print(freq, levels)

    ENT = ent(A, L=levels, isshow=True)
    print(ENT)
