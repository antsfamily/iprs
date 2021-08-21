#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 22:37:58
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt


X = np.array([[1 + 1j, 2 + 2j], [3+3j, 4 + 4j]])
Y = np.array([[0 + 1j, 2 + 1j], [2+3j, 4 + 3j]])

iprs.ampphaerror(X, Y)


plt.figure
plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Original')
plt.subplot(122)
plt.imshow(imgns, cmap='gray')
plt.title("add wgn with SNR: " + str(SNR) + "dB")
plt.show()
