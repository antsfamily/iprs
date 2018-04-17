#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 15:44:49
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
from ..utils.const import *


ACQUISITION = {
    'CSK1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, -255, 256], SceneCenter: [Xc, Yc, 0]
        'SceneArea': None,  # SceneArea + [Xc, Xc, Yc, Yc]
        'As': 0.0,  # squint angle
        'Ad': PI / 4.0,  # depression angle
    },
    'CSK2': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': [-256, 256, -512, 512],  # SceneArea + [Xc, Xc, Yc, Yc]
        'As': 0.0,  # squint angle
        'Ad': PI / 4.0,  # depression angle
    },
    'CSK3': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': [-512, 512, -512, 512],  # SceneArea + [Xc, Xc, Yc, Yc]
        'As': 0.0,  # squint angle
        'Ad': PI / 4.0,  # depression angle
    },
    'DIY1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        'SceneArea': [-256, 256, -256, 256],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0 / 4.0,  # squint angle
        'Ad': PI / 4.0,  # depression angle
    },
    'DIY2': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        'SceneArea': [-512, 512, -512, 512],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0 / 4.0,  # squint angle
        'Ad': PI / 4.0,  # depression angle
    },
    'DIY3': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        'SceneArea': [-512, 512, -512, 512],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0 / 4.0,  # squint angle
        'Ad': PI / 6.0,  # depression angle
    },
    'DIY4': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        'SceneArea': [-512, 512, -512, 512],
        # 'SceneArea': [-1024, 1024, -1024, 1024],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0 / 4.0,  # squint angle
        'Ad': PI * 4.0 / 9.0,  # depression angle
    },
    'DIY5': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': [-256, 256, -256, 256],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0 / 3.0,  # squint angle
        'Ad': PI * 4.0 / 9.0,  # depression angle
    },
    'DIY6': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': [-512, 512, -512, 512],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0,  # squint angle
        'Ad': PI * 1.0 / 9.0,  # depression angle
    },
    'DIY7': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': [-512, 512, -512, 512],
        # 'SceneArea': [-127, 128, -255, 256],
        # 'SceneArea': None,
        'As': 0.0,  # squint angle
        'Ad': PI * 51.00005 / 180.0,  # depression angle
    },
}
