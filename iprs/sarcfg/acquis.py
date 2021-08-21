#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 15:44:49
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
from ..utils.const import *


ACQUISITION = {
    'GF3': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, -255, 256], SceneCenter: [Xc, Yc, 0]
        'SceneArea': None,  # SceneArea + [Xc, Xc, Yc, Yc]
        'EchoSize': [4096, 4096],
        # 'As': 0.0,  # squint angle in earth curve geometry
        'As': 0 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 30.62 * PI / 180.0,  # depression angle
        'Be': 0.2107 * PI / 180.0  # antenna elevation beamwidth
    },
    'Sentinel1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, -255, 256], SceneCenter: [Xc, Yc, 0]
        'SceneArea': None,  # SceneArea + [Xc, Xc, Yc, Yc]
        'EchoSize': [4096, 4096],
        # 'As': 0.0,  # squint angle in earth curve geometry
        'As': 0 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 30.62 * PI / 180.0,  # depression angle
        # 'Be': 3.43 * PI / 180.0  # antenna elevation beamwidth
        'Be': 0.046821 * PI / 180.0  # antenna elevation beamwidth
    },
    'ALOSPALSAR': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, -255, 256], SceneCenter: [Xc, Yc, 0]
        'SceneArea': None,  # SceneArea + [Xc, Xc, Yc, Yc]
        'EchoSize': [35345, 10344],
        'As': 0.0 * PI / 180.,  # squint angle in earth curve geometry
        'Ad': 52.33 * PI / 180.0,  # depression angle
        'Be': 4.108559 * PI / 180.0  # antenna elevation beamwidth
    },
    'ERS': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, -255, 256], SceneCenter: [Xc, Yc, 0]
        'SceneArea': None,  # SceneArea + [Xc, Xc, Yc, Yc]
        'EchoSize': [32768, 5616],
        'As': 0.0,  # squint angle in earth curve geometry
        # 'As': -2.7672 * PI / 180.0,  # squint angle in earth curve geometry
        # 'Ad': 66.0 * PI / 180.0,  # depression angle
        # 'Be': 6.667755 * PI / 180.0  # antenna elevation beamwidth
        'Ad': 63.3 * PI / 180.0,  # depression angle
        'Be': 5.697283 * PI / 180.0  # antenna elevation beamwidth
        # 'Be': None  # antenna elevation beamwidth
        # 'Be': 8.640765 * PI / 180.0  # antenna elevation beamwidth
    },
    'RADARSAT1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        # SceneArea + [Xc, Xc, Yc, Yc]
        # 'SceneArea': [-36025.50318883,  36025.50318883, -54603.5561425,   54603.5561425],
        'SceneArea': None,
        # 'EchoSize': [1536, 2048],
        # 'EchoSize': [1536, 4096],
        'EchoSize': [19438, 9288],
        # 'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'As': -1.53 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 53.285 * PI / 180.0,  # depression angle
        'Be': 3.341740 * PI / 180.0,  # antenna elevation beamwidth , Nsr = 9288
        # 'Be': 2.857291 * PI / 180.0,  # antenna elevation beamwidth , Nsr = 9288
        # 'Be': None,  # antenna elevation beamwidth , Nsr = 2048
    },
    'RADARSAT2': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': [-512, 512, -512, 512],  # SceneArea + [Xc, Xc, Yc, Yc]
        'EchoSize': [256, 256],
        'As': 0.0,  # squint angle in earth curve geometry
        'Ad': PI / 4.0,  # depression angle
        'Be': 0.2725 * PI / 180.0  # antenna elevation beamwidth

    },
    'RS1Min512': {  # a Mini version of RADARSAT1
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': None,
        'EchoSize': [512, 512],
        'As': -1.584 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 53.3 * PI / 180.0,  # depression angle
        'Be': 0.1845 * PI / 180.0  # antenna elevation beamwidth

    },
    'RS1Min256': {  # a Mini version of RADARSAT1
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': None,
        'EchoSize': [256, 256],
        'As': -1.584 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 53.3 * PI / 180.0,  # depression angle
        'Be': 0.0926 * PI / 180.0  # antenna elevation beamwidth

    },
    'RS1Min128': {  # a Mini version of RADARSAT1
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        'SceneArea': None,
        'EchoSize': [128, 128],
        'As': -1.584 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 53.3 * PI / 180.0,  # depression angle
        'Be': 0.046 * PI / 180.0  # antenna elevation beamwidth
    },
    'Air1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': None,
        # 'SceneArea': [-2560, 2560, -187, 187],
        # 'SceneArea': [-32, 32, -32, 32],
        # 'SceneArea': [-255, 256, -255, 256],
        # 'SceneArea': None,
        # 'EchoSize': [1024, 1280],
        # 'EchoSize': [256, 256],
        # 'EchoSize': [512, 512],
        'EchoSize': [256, 320],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.05 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 3.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 8.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 21.9 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 30.0 * PI / 180.0,  # depression angle
        'Be': 1.321600 * PI / 180.0  # antenna elevation beamwidth
        # 'Be': 0.702357 * PI / 180.0  # antenna elevation beamwidth

    },
    'Air2': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': None,
        # 'SceneArea': [-2578.29798384, 2578.49960822, -738.46153846, 738.46153846],
        # 'SceneArea': [-32, 32, -32, 32],
        # 'SceneArea': [-255, 256, -255, 256],
        # 'SceneArea': None,
        'EchoSize': [1024, 1280],
        # 'EchoSize': [1024, 1024],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 3.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 21.9 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 30.0 * PI / 180.0,  # depression angle
        # 'Be': 8.3 * PI / 180.0  # antenna elevation beamwidth
        'Be': 1.322 * PI / 180.0  # antenna elevation beamwidth
        # 'Be': None
    },
    'Air3': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-200, 720, -200, 200],
        # 'SceneArea': None,
        # 'SceneArea': [-2578.29798384, 2578.49960822, -738.46153846, 738.46153846],
        # 'SceneArea': [-32, 32, -32, 32],
        # 'SceneArea': [-255, 256, -255, 256],
        'SceneArea': None,
        'EchoSize': [512, 512],
        # 'EchoSize': [1024, 1024],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 1.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 3.5 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 22.8 * PI / 180.0,  # squint angle in earth curve geometry
        # 'As': 0.005 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 30.0 * PI / 180.0,  # depression angle
        # 'Be': 1.054 * PI / 180.0,  # antenna elevation beamwidth
        # 'Be': 1.045 * PI / 180.0,  # antenna elevation beamwidth
        # 'Be': 1.023 * PI / 180.0,  # antenna elevation beamwidth
        # 'Be': 1.06 * PI / 180.0  # antenna elevation beamwidth
        'Be': 2.114 * PI / 180.0  # antenna elevation beamwidth
        # 'Be': None
    },
    'DIY1': {
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None:default --> [-127, 128, Yc-255, Yc+256]
        # 'SceneArea': [-1024, 1024, -2048, 2048],
        'SceneArea': None,
        # 'SceneArea': [-32, 32, -32, 32],
        # 'SceneArea': [-255, 256, -255, 256],
        # 'SceneArea': None,
        'EchoSize': [128, 256],
        'As': 0.0 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': PI / 4.0,  # depression angle
        'Be': 0.2725 * PI / 180.0  # antenna elevation beamwidth

    },
    'SIMSARv1a': {  # a Mini version of RADARSAT1,
        'PlatCenter': None,  # [x, y, z], None: default --> [0, 0, H]
        # SceneArea:[xmin,xmax,ymin,ymax], unit: m
        # [azimuth min/max range min/max] --> SceneArea + [Xc, Xc, Yc, Yc]
        # None: default --> [-127, 128, Yc-255, Yc+256],
        # SceneArea + [Xc, Xc, Yc, Yc]
        # 'SceneArea': [-121, 121, -90, 90],
        # 'SceneArea': [-242, 242, -180, 180],
        # 'SceneArea': [-484, 484, -360, 360],  # Na-Nr --> 128x128
        # 'SceneArea': [-968, 960, -720, 720],
        # 'SceneArea': [-1926, 1926, -1440, 1440],
        # 'SceneArea': [-3846, 3846, -2878, 2878],  # Na-Nr --> 1024x1024
        'SceneArea': None,
        'EchoSize': [128, 256],
        'As': -1.58 * PI / 180.0,  # squint angle in earth curve geometry
        'Ad': 53.3 * PI / 180.0,  # depression angle
        'Be': 0.2725 * PI / 180.0  # antenna elevation beamwidth

    },
}
