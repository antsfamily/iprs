#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge


def regular_sar(s, A, norm=1, factor=0.1, optim='Lasso', max_iter=1000, tol=0.0001, shape=None, verbose=True):
    r"""SAR imaging using regularization methods

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
    shape : {list or tuple}, optional
        reshape g to shape (default: {None})
    verbose : {bool}, optional
        show more info (default: {False})

    Returns
    -------
    g : complex value numpy array
        Imaging results
    """

    print("================in regular_sar================")
    if verbose:
        print("===Type of A, s: ", A.dtype, s.dtype)
    cplxFlag = False
    if np.iscomplex(A).any() or np.iscomplex(s).any():
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
            g = rgr_ridge.coef_
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
            g = rgr_lasso.coef_
            if verbose:
                print("===Done!")
    if cplxFlag:
        L = np.size(g)
        g = g[:int(L / 2)] + 1j * g[int(L / 2):]
        if verbose:
            print("===size of g: ", L)

    if shape is not None:
        g = np.reshape(g, shape)
        if verbose:
            print("===shape of g: ", g.shape)

    return g


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from scipy import sparse
    from scipy import ndimage

    def _weights(x, dx=1, orig=0):
        x = np.ravel(x)
        floor_x = np.floor((x - orig) / dx).astype(np.int64)
        alpha = (x - orig - floor_x * dx) / dx
        return np.hstack((floor_x, floor_x + 1)), np.hstack((1 - alpha, alpha))

    def _generate_center_coordinates(l_x):
        X, Y = np.mgrid[:l_x, :l_x].astype(np.float64)
        center = l_x / 2.
        X += 0.5 - center
        Y += 0.5 - center
        return X, Y

    def build_projection_operator(l_x, n_dir):
        """ Compute the tomography design matrix.

        Parameters
        ----------

        l_x : int
            linear size of image array

        n_dir : int
            number of angles at which projections are acquired.

        Returns
        -------
        p : sparse matrix of shape (n_dir l_x, l_x**2)
        """
        X, Y = _generate_center_coordinates(l_x)
        angles = np.linspace(0, np.pi, n_dir, endpoint=False)
        data_inds, weights, camera_inds = [], [], []
        data_unravel_indices = np.arange(l_x ** 2)
        data_unravel_indices = np.hstack((data_unravel_indices,
                                          data_unravel_indices))
        for i, angle in enumerate(angles):
            Xrot = np.cos(angle) * X - np.sin(angle) * Y
            inds, w = _weights(Xrot, dx=1, orig=X.min())
            mask = np.logical_and(inds >= 0, inds < l_x)
            weights += list(w[mask])
            camera_inds += list(inds[mask] + i * l_x)
            data_inds += list(data_unravel_indices[mask])
        proj_operator = sparse.coo_matrix((weights, (camera_inds, data_inds)))
        return proj_operator

    def generate_synthetic_data():
        """ Synthetic binary data """
        rs = np.random.RandomState(0)
        n_pts = 36
        x, y = np.ogrid[0:l, 0:l]
        mask_outer = (x - l / 2.) ** 2 + (y - l / 2.) ** 2 < (l / 2.) ** 2
        mask = np.zeros((l, l))
        points = l * rs.rand(2, n_pts)
        mask[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
        mask = ndimage.gaussian_filter(mask, sigma=l / n_pts)
        res = np.logical_and(mask > mask.mean(), mask_outer)
        return np.logical_xor(res, ndimage.binary_erosion(res))

    # Generate synthetic images, and projections
    l = 128
    proj_operator = build_projection_operator(l, l // 7)
    data = generate_synthetic_data()
    proj = proj_operator * data.ravel()[:, np.newaxis]
    proj += 0.15 * np.random.randn(*proj.shape)

    rec_l2 = regular_sar(s=proj.ravel(), A=proj_operator, norm=2, factor=0.001,
                         optim='Ridge', max_iter=1000, tol=0.001, shape=(l, l), verbose=False)
    rec_l1 = regular_sar(s=proj.ravel(), A=proj_operator, norm=1, factor=0.001,
                         optim='Lasso', max_iter=1000, tol=0.001, shape=(l, l), verbose=False)

    plt.figure(figsize=(8, 3.3))
    plt.subplot(131)
    plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
    plt.axis('off')
    plt.title('original image')
    plt.subplot(132)
    plt.imshow(rec_l2, cmap=plt.cm.gray, interpolation='nearest')
    plt.title('L2 penalization')
    plt.axis('off')
    plt.subplot(133)
    plt.imshow(rec_l1, cmap=plt.cm.gray, interpolation='nearest')
    plt.title('L1 penalization')
    plt.axis('off')

    plt.subplots_adjust(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0,
                        right=1)

    plt.show()
