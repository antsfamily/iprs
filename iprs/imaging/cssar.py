#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-13 21:08:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

from __future__ import division, print_function, absolute_import

from ..utils.const import *
from ..misc import visual as vis

from ..dsp import normalsignals as sig
from ..simulation.model import sarmodel
import numpy as np

from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import OrthogonalMatchingPursuit


def cs1d_sar(s, A, D=None, axis=-1, norm=1, factor=0.1, optim='OMP', max_iter=1000, tol=0.0001, gdshape=None, verbose=True):
    r"""Sar imaging based on 1-d Compressive Sensing

    SAR imaging process can be formulated as

    .. math::
       {\bf s} = {\bf A}{\bf g} + {\bf n},

    where, :math:`{\bf s}` is the :math:`m = MN\times 1` recieved SAR raw data vector in phase history domain,
    :math:`\bf g` is the :math:`n = HW \times 1` reflection vector of scene. :math:`\bf A` represents the
    the mapping from scene to SAR raw data. :math:`\bf n` is the noise vector.

    If :math:`\bf g` is not sparse enough, assume that exist a basis :math:`{\bf D} = ({\bf d}_1, {\bf d}_2, \cdots, {\bf d}_n)`
    that satisfies :math:`{\bf g} = {\bf D}{\bf x}` , where, :math:`\bf x` is a :math:`K` sparse :math:`n\times 1` vector, and
    :math:`\bf D` is the so called dictionary matrix of size :math:`n\times n` .

    Our goal is minimize

    .. math::
        \mathop  {\rm min}\limits_{\bf{x}}\|{\bf x}\|_{p}, \ \  s.t. \  {\bf s} = {\bf A}{\bf D}{\bf x} + {\bf n},

    i.e.

    .. math::
        \mathop {\rm min}\limits_{\bf{x}} = \|{\bf s} - {\bf A}{\bf D}{\bf x}\|_2^2 + \lambda \|{\bf x}\|_p,

    where, :math:`\lambda` is the balance factor, and :math:`|\cdot|_p` is the :math:`\cal l_p` norm.

    Let :math:`{\bf \Phi} = {\bf A}{\bf D}` , then we have

    .. math::
        \mathop {\rm min}\limits_{\bf{x}} = \|{\bf s} - {\bf \Phi}{\bf x}\|_2^2 + \lambda \|{\bf x}\|_p.

    Note that, if :math:`{\bf s, \Phi, x} \in {\mathbb C}` , the problem changes to

    .. math::
       {\mathop{\rm Re}\nolimits} ({\bf{s}}) + j{\rm Im}({\bf{s}}) = {\rm Re}({\bf{\Phi x}}) + j{\mathop{\rm Im}\nolimits} ({\bf{\Phi x}})

    so we have:

    .. math::
       \left[ {\begin{array}{*{20}{c}}
       {{\mathop{\rm Re}\nolimits} ({\bf{s}})}\\
       {{\mathop{\rm Im}\nolimits} ({\bf{s}})}
       \end{array}} \right] = \left[ {\begin{array}{*{20}{c}}
       {{\mathop{\rm Re}\nolimits} ({\bf{\Phi}})}&{ - {\mathop{\rm Im}\nolimits} ({\bf{\Phi}})}\\
       {{\rm Im}({\bf{\Phi}})}&{{\mathop{\rm Re}\nolimits} ({\bf{\Phi}})}
       \end{array}} \right]\left[ {\begin{array}{*{20}{c}}
       {{\mathop{\rm Re}\nolimits} ({\bf{x}})}\\
       {{\mathop{\rm Im}\nolimits} ({\bf{x}})}
       \end{array}} \right]

    Parameters
    ----------
    s : {numpy array}
        sar raw data in phase history domain.
    A : {numpy array}
        mapping matrix from scene to sar raw data, see ``iprs.sarmodel``.
    D : {numpy array}, optional
        dictionary (default: {None})
    axis : {number}, optional
        specify which axis is to be compressed: -1 --> both range and azimuth, 0 --> azimuth, 1 --> range (default: {-1})
    norm : {number}, optional
        specify the :math:`\cal l_p` norm, :math:`p=1/2, 1, 2` (default: {1} means :math:`\cal l_1` norm)
    factor : {number}, optional
        the balance factor (default: {0.1})
    optim : {str}, optional
        optimization method: 'OMP' for :math:`\cal l_0` , 'Lasso' for :math:`\cal l_1` , 'Ridge' for :math:`\cal l_2` , (default: {'Lasso'})
    max_iter : {number}, optional
        maximum iterations (default: {1000})
    tol : {number}, optional
        tolerance of error (default: {0.0001})
    gdshape : {list or tuple}, optional
        reshape g to gdshape (default: {None})
    verbose : {bool}, optional
        show more info (default: {False})

    Returns
    -------
    g : complex value numpy array
        Imaging results
    """

    print("================in cs1d_sar================")
    if s is None:
        print("===No raw data!")

    if verbose:
        print("===Type of A, s: ", A.dtype, s.dtype)
    cplxFlag = False
    CPLXDTYPESTR = ['complex128', 'complex64', 'complex']

    if D is not None:
        # =================step1: Sparse Representation===========
        if verbose:
            print("===Sparse Representation: A = AD...")
        A = np.matmul(A, D)
        if verbose:
            print("===Done!...")
    if A.dtype in CPLXDTYPESTR or s.dtype in CPLXDTYPESTR:
        cplxFlag = True
        if verbose:
            print("===Convert complex to real...")
        s = np.concatenate((np.real(s), np.imag(s)), axis=0)
        ReA = np.real(A)
        ImA = np.imag(A)
        A1 = np.concatenate((ReA, -ImA), axis=1)
        A2 = np.concatenate((ImA, ReA), axis=1)
        A = np.concatenate((A1, A2), axis=0)
        if verbose:
            print("===Done!")

    if np.ndim(s) > 1:
        # sshape = s.shape
        s = s.flatten()

    if norm is 2:
        # Reconstruction with L2 (Ridge) penalization
        if optim is 'Ridge':
            if verbose:
                print("===Do Ridge L2...")
            rgr_ridge = Ridge(alpha=factor, max_iter=max_iter, tol=tol)
            rgr_ridge.fit(A, s)
            x = rgr_ridge.coef_
            if verbose:
                print("===Done!")
    # Reconstruction with L1 (Lasso) penalization
    # the best value of alpha was determined using cross validation
    # with LassoCV
    if norm is 1:
        if optim is 'Lasso':
            if verbose:
                print("===Do Lasso L1...")
            rgr_lasso = Lasso(alpha=factor, max_iter=max_iter, tol=tol)
            rgr_lasso.fit(A, s)
            x = rgr_lasso.coef_
            if verbose:
                print("===Done!")
    if norm is 0:
        if optim is 'OMP':
            if verbose:
                print("===Do OMP L0...")
            omp = OrthogonalMatchingPursuit(
                n_nonzero_coefs=None, tol=tol, fit_intercept=True, normalize=True, precompute=False)
            omp.fit(A, s)
            x = omp.coef_
            if verbose:
                print("===Done!")
    if cplxFlag:
        L = np.size(x)
        x = x[:int(L / 2)] + 1j * x[int(L / 2):]
        if verbose:
            print("===size of x: ", L)

    if D is not None:
        g = np.matmul(D, x)
    else:
        g = x
        x = None

    if gdshape is not None:
        g = np.reshape(g, gdshape)
        if verbose:
            print("===shape of g: ", g.shape)
    return g


def cs2d_sar(s, A=None, rsample=(0.5, 0.5), D=None, axis=-1, verbose=True):

    if s is None:
        print("No raw data!")

    # =================step1: Construct Observation Matrix===========
    if verbose:
        print("Construct Observation Matrix ...")

    if A is None:
        pass


def cs_sar_blk():
    r"""

    1. reconstruct range image
    2. split to some parts in range
    3. reconstruct parts
    4. combine to full sized image

    """
    pass
