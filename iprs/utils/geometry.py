#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 15:11:16
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$


from __future__ import division, print_function, absolute_import
import numpy as np


def linekb(x, k, b):
    return x * k + b


def isinpolygons(p, pg):
    r"""
    p: point [2,N]
    pg: polygon [2, nP]

    """

    minX = np.min(pg[0])
    maxX = np.max(pg[0])
    minY = np.min(pg[1])
    maxY = np.max(pg[1])
    pass

# int pnpoly(int nvert, float *vertx, float *verty, float testx, float testy)
# {
#   int i, j, c = 0;
#   for (i = 0, j = nvert-1; i < nvert; j = i++) {
#     if ( ((verty[i]>testy) != (verty[j]>testy)) &&
#      (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
#        c = !c;
#   }
#   return c;
# }
# if (p.x < minX || p.x > maxX || p.y < minY || p.y > maxY) {
#     // We're outside the polygon!
# }


def polygon():
    pass
