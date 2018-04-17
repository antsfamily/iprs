#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-18 03:46:32
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
import numpy as np

import iprs


r = np.random.randn(128, 256)
r = np.zeros((128, 256), dtype=complex)

print(r, r.shape)

iprs.show_amplitude_phase(r)
