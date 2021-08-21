#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 19:50:44
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


import numpy as np
import matplotlib.pyplot as plt

import iprs


t = np.linspace(-10, 10, 100, endpoint=True)


s1 = iprs.hs(t)
s2 = iprs.ihs(t)
plt.figure
plt.subplot(121)
plt.plot(t, s1)
plt.title('Heavyside function')
plt.subplot(122)
plt.plot(t, s2)
plt.title('Inverse Heavyside function')
plt.show()


s = iprs.rect(t)
plt.figure
plt.plot(t, s)
plt.title('rect')
plt.show()


s = iprs.chirp(t, 50, 300)
plt.figure
plt.plot(t, s)
plt.title('chirp')
plt.show()


t = np.linspace(0, 20, 1000, endpoint=True)

s1, t1 = iprs.pulse(t, 3, 20, 6)
s2, t2 = iprs.pulse2(3, 20, 1000, 2)

plt.figure
plt.subplot(121)
plt.plot(t1, s1)
plt.title('pulse signal1')
plt.subplot(122)
plt.plot(t2, s2)
plt.title('pulse signal2')
plt.show()
