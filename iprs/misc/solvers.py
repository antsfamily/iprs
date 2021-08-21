#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 21:03:52
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
# @note    : This file is developed based on
#            https://github.com/rmiya56/CSToolbox

import numpy as np


class Greedy:
    r"""
    base class of Greedy algorithms
    [args]
        A: measurement matrix (2d ndarray)
        y: measured vector    (1d ndarray)
    [return]
        recovered vector      (1d ndarray)
    """

    def __init__(self, A, y):

        self.A = A
        self.n = A.shape[1]
        self.y = y
        self.e = float("inf")

        # Initialization
        self.z = np.zeros(self.n, dtype=np.complex)
        self.r = self.y

        # Constants about convergence
        self.EPS = 10**-5        # acceptable residual
        # self.ITER_MAX = 1 * 10**5  # max of iterations
        self.ITER_MAX = 1 * 100  # max of iterations

        self.name = "Unknown"
        self.iterations = 0  # iterator var

        # Options
        self.logging = True

    def __iter__(self):
        return self

    # def next(self): # py2
    def __next__(self):  # py3

        # check number of loops
        if self.iterations == self.ITER_MAX:
            if self.logging:
                print("Reach to MAX Iterations")
                print(self.get_result())
            raise StopIteration

        # check convergence by previous iteration
        if self.e < self.EPS:
            if self.logging:
                print("Converged")
                print(self.get_result())
            raise StopIteration

        # iterate
        self.iterations += 1
        self.z = self.iterate()

        # return signal estimated by n-iterations
        self.r = self.y - np.dot(self.A, self.z)
        self.e = np.linalg.norm(self.r) / np.linalg.norm(self.y)
        return self.z

    def get_last(self):

        return [i for i in self][-1]

    def set_epsilon(self, e):
        self.EPS = e

    def set_maxiterations(self, num):
        self.ITER_MAX = num

    def get_status(self):

        status = ""
        status += "iterations:        %d\n" % self.iterations
        status += "residual norm (e): %.2e\n" % self.e
        return status

    def get_result(self):

        result = "------- summary ------\n"
        result += "[ %s ]\n" % self.name
        result += "number of iterations: %d\n" % self.iterations
        result += "specified error:   %.2e\n" % self.EPS
        result += "residual norm (e): %.2e\n" % self.e
        return result

    def activate_logging(self):
        self.logging = True

    def deactivate_logging(self):
        self.logging = False


class OMP(Greedy):
    u"""
    perform OMP
    [args]
        A: measurement matrix (2d ndarray)
        y: measured vector (1d ndarray)
    [return]
        recovered vector (1d ndarray)
    """

    def __init__(self, A, y):

        Greedy.__init__(self, A, y)
        self.name = "OMP"
        self.S = set([])  # support set (indexes)

    def __iter__(self):

        return self

    def iterate(self):

        # project residual vector on measurement matrix,
        # and find the index of the largest entry
        g = np.dot(np.conj(self.A.T), self.r)
        j = np.argmax([np.abs(g[i]) / np.linalg.norm(self.A[:, i])
                       for i in range(self.n)])

        # add the index to the supports set S
        self.S.add(j)

        # make a matrix which of columns have the index in S
        As = self.A[:, sorted(self.S)]

        # to minimum solution of || As z - y ||2 = 0,
        # solve least square
        zs = np.dot(np.linalg.pinv(As), self.y)

        # make approximated signal z,
        # the entries of which are the solutions of
        # the previous least square
        z = np.zeros(self.A.shape[1], dtype=np.complex)
        for j, s in enumerate(sorted(self.S)):
            z[s] = zs[j]

        return z


class CoSaMP(Greedy):
    u"""
    perform CoSaMP
    [args]
        A: measurement matrix (2d ndarray)
        y: measured vector (1d ndarray)
        k: sparsity
    [return]
        recovered vector (1d ndarray)
    """

    def __init__(self, A, y, k):

        Greedy.__init__(self, A, y)
        self.name = "CoSaMP"
        self.S = set([])  # support set (indexes)
        self.k = k

    def __iter__(self):

        return self

    def iterate(self):

        # update support sets
        z = np.dot(np.conj(self.A.T), self.r)
        s = indexThresholding(z, 2 * self.k)
        self.S |= set(s)

        # pick up columns which have the index in S
        As = self.A[:, sorted(self.S)]
        us = np.dot(np.linalg.pinv(As), self.y)  # solve least square
        u = np.zeros(self.A.shape[1], dtype=np.complex)
        for j, s in enumerate(sorted(self.S)):
            u[s] = us[j]

        return hardThresholding(u, self.k)


class IHT(Greedy):
    u"""
    perform IHT
    [args]
        A: measurement matrix (2d ndarray)
        y: measured vector    (1d ndarray)
        k: sparsity
    [return]
        recovered vector      (1d ndarray)
    """

    def __init__(self, A, y, k):

        Greedy.__init__(self, A, y)
        self.name = "IHT"
        self.k = k

    def __iter__(self):

        return self

    def iterate(self):

        p = self.z + np.dot(np.conj(self.A.T),  self.r)
        z = hardThresholding(p, self.k)
        return z


def indexThresholding(z, k):
    u"""
    return k-largetst indexes of vector x,
    which are sorted descending
    z: vector (real or complex)
    k: thresholding bound
    """
    desc_idxes = np.argsort(np.abs(z))[
        ::-1]   # sort indexes in descending order
    return desc_idxes[:k]


def hardThresholding(X, k):

    dim = len(X.shape)

    if dim == 1:
        return _hardThres1D(X, k)

    elif dim == 2:
        return _hardThres2D(X, k)

    else:
        print("support only vector(1d) or matrix(2d)")
        return None


def _hardThres1D(z, k):

    x_ = np.zeros(len(z), dtype=np.complex)
    for s in indexThresholding(z, k):
        x_[s] = z[s]
    return x_


def _hardThres2D(X, k):

    # flatten
    m, n = X.shape
    x = X.flatten()
    # thresholding
    x_ = _hardThres1D(x, k)
    # reshape back
    X_ = x_.reshape(m, n)

    return X_


class HTP(Greedy):
    u"""
    perform HTP
    [args]
        A: measurement matrix (2d ndarray)
        y: measured vector    (1d ndarray)
        k: sparsity
    [return]
        recovered vector      (1d ndarray)
    """

    def __init__(self, A, y, k):

        Greedy.__init__(self, A, y)
        self.name = "HTP"
        self.S = set([])  # support set (indexes)
        self.k = k

    def __iter__(self):

        return self

    def iterate(self):

        # update support sets
        p = self.z + np.dot(np.conj(self.A.T), self.r)
        self.S = set(indexThresholding(p, self.k))

        # make a matrix which of columns have the index in S
        As = self.A[:, sorted(self.S)]

        # to minimum solution of || As z - y ||2 = 0,
        # solve least square
        zs = np.dot(np.linalg.pinv(As), self.y)

        # make approximated signal z,
        # the entries of which are the solutions of
        # the previous least square
        z = np.zeros(self.A.shape[1], dtype=np.complex)
        for j, s in enumerate(sorted(self.S)):
            z[s] = zs[j]

        return z


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from iprs.utils.sensing import gaussian

    m = 10
    n = 20
    s = 2

    A = gaussian(m, n)
    x = np.zeros(n)
    x[3] = -np.sqrt(5)
    x[10] = np.pi
    y = np.dot(A, x)

    iter = OMP(A, y)
    for z in iter:
        plt.clf()
        plt.scatter(np.arange(n), x, s=60, marker='x', c='r')
        plt.stem(z.real)
        # plt.show()
        # print iter.get_status()

    plt.show()
