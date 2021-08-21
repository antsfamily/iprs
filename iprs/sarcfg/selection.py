#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 15:44:49
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
from ..utils.const import *


SELECTION = {
    'ROI1': {
        'SubSceneArea': None,  # SceneArea
        # 'SubSceneArea': [-255, 256, -255, 256],
        'SubEchoSize': None,  # EchoSize
        # 'SubEchoSize': [128, 256],
    },
    'ROI2': {
        # 'SubSceneArea': None,  # SceneArea
        'SubSceneArea': [0.5, 0.5, 0.5, 0.5],  # SceneArea/2.0
        # 'SubEchoSize': None,  # EchoSize
        'SubEchoSize': [0.5, 0.5],  # EchoSize / 2.0
    },
    'ROI3': {
        # 'SubSceneArea': None,  # SceneArea
        'SubSceneArea': [-128, 128, -128, 128],
        'SubEchoSize': None,  # Auto Compute
    },
    'ROI4': {
        # 'SubSceneArea': None,  # SceneArea
        'SubSceneArea': None,  # Auto Compute
        'SubEchoSize': [128, 128],
    },
}
