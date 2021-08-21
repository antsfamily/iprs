#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt

img = scio.loadmat('Image.mat')['img']
X = img.copy()

Nsar = 200
X, ephi = iprs.pgaf_sm(X, Nsar, Nsub=None, windb=25., est='ML', Niter=20, tol=1.e-6, isplot=False)

plt.figure()
plt.subplot(121)
plt.imshow(np.abs(img))
plt.subplot(122)
plt.imshow(np.abs(X))
plt.show()

