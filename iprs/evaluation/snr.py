#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-25 09:53:21
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

from __future__ import division, absolute_import


from iprs.evaluation.error import mse
from iprs.utils.typevalue import peakvalue
import numpy as np

# ========================================================================
# ---this file is for Entropy of the full image (ENT),
#    a measure of image sharpness, the smaller the better
# ---see "Samadi S , M Cetin, Masnadishirazi M A .
#        Sparse representation-based synthetic aperture radar imaging[J].
#        Radar Sonar & Navigation Iet, 2011, 5(2):182-193."
# ========================================================================


def snr():
    pass


def psnr(o, r, Vpeak=None, mode='simple'):
    r"""Peak Signal-to-Noise Ratio

    The Peak Signal-to-Noise Ratio (PSNR) is expressed as

    .. math::
        {\rm PSNR} = 10 \log10(\frac{V_{peak}^2}{\rm MSE})

    For float data, :math:`V_{peak} = 1`;

    For interges, :math:`V_{peak} = 2^{nbits}`,
    e.g. uint8: 255, uint16: 65535 ...


    Parameters
    -----------
    o : array_like
        Reference data array. For image, it's the original image.
    r : array_like
        The data to be compared. For image, it's the reconstructed image.
    Vpeak : float, int or None, optional
        The peak value. If None, computes automaticly.
    mode : str or None, optional
         'simple' or 'rich'. 'simple' (default) --> just return psnr i.e.
         'rich' --> return psnr, mse, Vpeak, imgtype.

    Returns
    -------
    PSNR : float
        Peak Signal to Noise Ratio value.

    """

    if o.dtype != r.dtype:
        print("Warning: o(" + str(o.dtype) + ")and r(" + str(r.dtype) +
              ")have different type! PSNR may not right!")

    if Vpeak is None:
        Vpeak = peakvalue(o)

    MSE = mse(o, r)
    PSNR = 10 * np.log10((Vpeak ** 2) / MSE)
    if mode is None:
        mode = 'simple'
    if mode == 'rich':
        return PSNR, MSE, Vpeak, o.dtype
    else:
        return PSNR


if __name__ == '__main__':
    import iprs

    o = np.array([[251, 200, 210], [220, 5, 6]])
    r = np.array([[0, 200, 210], [220, 5, 6]])
    PSNR, MSE, Vpeak, dtype = iprs.psnr(o, r, Vpeak=None, mode='rich')
    print(PSNR, MSE, Vpeak, dtype)

    o = np.array([[251, 200, 210], [220, 5, 6]]).astype('uint8')
    r = np.array([[0, 200, 210], [220, 5, 6]]).astype('uint8')
    PSNR, MSE, Vpeak, dtype = iprs.psnr(o, r, Vpeak=None, mode='rich')
    print(PSNR, MSE, Vpeak, dtype)

    o = np.array([[251, 200, 210], [220, 5, 6]]).astype('float')
    r = np.array([[0, 200, 210], [220, 5, 6]]).astype('float')
    PSNR, MSE, Vpeak, dtype = iprs.psnr(o, r, Vpeak=None, mode='rich')
    print(PSNR, MSE, Vpeak, dtype)
