#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-18 20:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import sys
import iprs
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt


# datafile = '/mnt/d/DataSets/zhi/SAR/RadarSat/sensor=DIY4_acquisition=DIY4_IMAGE_HH_SAR001_8bit.pkl'
datafile = '/mnt/d/DataSets/zhi/SAR/misc/MiniSAR128/sensor=DIY7_acquisition=DIY7_MiniSAR_128nScenes10.pkl'

H = 128
W = 128

ITER_MAX = 50

rsample = (0.25, 0.25)

sardata, sarplat = iprs.sarread(datafile)

DCTD = iprs.dctdic((H, W))

print("+++++++++++++++")
# print(DCTD, DCTD.shape)

# col
X = sardata.rawdata

X = np.array(X)
(N, H, W) = X.shape

Nsa = rsample[0] * H
Nsr = rsample[1] * W
m = Nsa * Nsr
n = H * W

print("+++++++++++++++")
A = iprs.gaussian(2 * m, 2 * n)
print("+++++++++++++++")

# fileA = '../data/sensorDIY8acquisDIY8.pkl'

# f = open(fileA, 'rb')
# # for python2
# if sys.version_info < (3, 1):
#     A = pkl.load(f)
#     invA = pkl.load(f)
# # for python3
# else:
#     A = pkl.load(f, encoding='latin1')
#     invA = pkl.load(f, encoding='latin1')
# f.close()
# print(A.shape, invA.shape)

# A1 = np.hstack((A.real, -A.imag))
# A2 = np.hstack((A.imag, A.real))

# A = np.vstack((A1, A2))

# A1 = None
# A2 = None


# A = A / np.linalg.norm(A)


for k in range(1, N):
    print(X[k].shape)
    x = X[k].flatten()
    print(x.shape)
    x = np.hstack((x.real, x.imag))
    print(x.shape, A.shape)
    y = np.matmul(A, x)
    print(y.shape)
    # y = np.hstack((x.real, x.imag))
    iter = iprs.OMP(A, y)
    iter.ITER_MAX = ITER_MAX
    for z in iter:
        R = z.real
        print(R, R.shape, np.sum(R))
    R = R[range(0, n)] + 1j * R[range(n, 2 * n)]
    R = np.reshape(R, (H, W))
    print(R.shape)
    iprs.show_sarimage(np.abs(X[k]), sarplat, cmap='gray')
    iprs.show_sarimage(np.abs(R), sarplat, cmap='gray')


# x = img.flatten()
# m = H * W / 4
# n = H * W

# A = iprs.gaussian(m, n)
# print("+++++++++++++++")
# y = np.dot(A, x)

# print("+++++++++++++++")
# iter = iprs.OMP(A, y)

# plt.figure()
# for z in iter:
#     plt.clf()
#     plt.scatter(np.arange(n), x, s=60, marker='x', c='r')
#     plt.stem(z.real)
#     # plt.show()
#     # print iter.get_status()

# plt.show()


srate_a = 0.5
srate_r = 0.5
datafile = '../data/sar/sensor=DIY4_acquisition=DIY4_point.mat'
datafile = 'D:/DataSets/zhi/sensor=DIY4_acquisition=DIY4_IMAGE_HH_SAR001_8bit.pkl'
sardata, sarplat = iprs.load_data(datafile, way=0, which='all')

sarplat.printsp()

X = sardata.rawdata

XX = iprs.matnoise(X, noise='wgn', SNR=5)

Sr, obmat = iprs.sparse_observation(
    np.array([XX]), way=0, mode='uniformly', rsample=(srate_a, srate_r))

# visualize
iprs.show_amplitude_phase(Sr[0])
# do RD imaging
# Sr_img, ta, tr = iprs.rda(X, sarplat, verbose=False)
Sr_img, ta, tr = iprs.rda(XX, sarplat, verbose=False)
# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)

print(Sr[0].shape, "==============")
sarplat = iprs.process_sarplat(sarplat, rsample=(srate_a, srate_r))
# sarplat.printsp()
Sr_img, ta, tr = iprs.rda(Sr[0], sarplat, verbose=False)

# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD, with arate: ' + \
    str(round(srate_a, 4)) + ", rrate: " + str(round(srate_r, 4))
# title = 'Reconstructed Image using omega-k'
iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None)
