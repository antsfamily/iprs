#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 20:17:32
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $Id$

import iprs
import numpy as np
import matplotlib.pyplot as plt


imgfile = '/home/liu/Desktop/Data/ws/dataset/fig/Tokyoradarsat001_8bit_256.tif'

img = iprs.imread(imgfile)

(H, W) = img.shape

DCTD = iprs.dctdic((H, W))

print("+++++++++++++++")
# print(DCTD, DCTD.shape)

X = img

# ===============================col
# m = H / 4
# n = H

# A = iprs.gaussian(m, n)
# print("+++++++++++++++")
# Y = np.dot(A, X)

# print("+++++++++++++++")

# R = np.zeros((H, W))
# for i in range(W):
#     y = Y[:, i]
#     iter = iprs.OMP(A, y)

#     # plt.figure()
#     for z in iter:
#         R[:, i] = z.real

# iprs.show_image(np.abs(R), cmap='gray')

# two===============================
x = X.flatten()
m = H * W / 16
n = H * W

A = iprs.gaussian(m, n)
print("+++++++++++++++")
y = np.dot(A, x)

print("+++++++++++++++")
iter = iprs.OMP(A, y)

for z in iter:
    R = z.real
    print(R.shape, np.sum(R))

R = np.reshape(R, (H, W))
iprs.show_image(np.abs(R), cmap='gray')
#     plt.clf()
#     plt.scatter(np.arange(n), x, s=60, marker='x', c='r')
#     plt.stem(z.real)
#     # plt.show()
#     # print iter.get_status()

# plt.show()
