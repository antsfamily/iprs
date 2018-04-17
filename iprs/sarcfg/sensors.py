#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 22:29:14
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import
import numpy as np

from ..utils.const import *


SENSORS = {
    'Aerial1': {
        'Fc': 4.5e9,  # Hz
        'H': 10000.0,  # height in m
        'V': 200.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 100.0e6,  # band width in Hz
        'La': 2.0,  # antenna length in m
        # 'PRF': 1200.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'Aerial1 SAR',

    },
    'Aerial2': {
        'Fc': 1.5e9,  # Hz
        'H': 500.0,  # height in m
        'V': 50.0,  # velocity in m/s
        'Tp': 2.0e-6,  # Range pulse length in seconds
        'Kr': 1.0e14,  # band width in Hz
        'La': 1.5,  # antenna length in m
        # 'PRF': 500.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'Aerial2 SAR',
    },
    'CSK': {
        'Fc': 9600000000.0,  # Hz
        'H': 625222.52152799,  # height in m
        'V': 7632.8601880878696,  # velocity in m/s
        'Tp': 4e-005,  # Range pulse length in seconds
        'Kr': -1631469726562.5,  # band width in Hz
        'La': 5.6,  # antenna length in m
        'PRF': 3063.72549019608,  # Hz
        # 'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'CSK HImage SAR',
    },
    'TSX': {
        'Fc': 5.331e9,  # Hz
        'H': 785000.0,  # height in m
        'V': 7126.14,  # velocity in m/s
        'Tp': 37.120e-3,  # Range pulse length in seconds
        'Kr': 4.17788e+11,  # band width in Hz
        'La': 10.0,  # antenna length in m
        # 'PRF': 1679.9020,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'Terra-Sar X',
    },
    'DIY': {
        'Fc': 5.3e9,  # Hz
        'H': 1000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 4.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
    'DIY1': {
        'Fc': 5.3e9,  # Hz
        'H': 10000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 4.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
    'DIY2': {
        'Fc': 5.3e9,  # Hz
        'H': 10000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 2.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
    'DIY3': {
        'Fc': 5.3e9,  # Hz
        'H': 10000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 4.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
    'DIY4': {
        'Fc': 5.3e9,  # Hz
        'H': 5000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 4.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
    'DIY5': {
        'Fc': 5.3e9,  # Hz
        'H': 5000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 2.0e+13,  # band width in Hz
        'La': 4.0,  # antenna length in m
        # 'PRF': 94.0,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'DIY SAR',
    },
}


for sensor, value in SENSORS.items():
    SENSORS[sensor]['B'] = SENSORS[sensor]['Tp'] * \
        np.abs(SENSORS[sensor]['Kr'])  # chirp rate in Hz/s
    SENSORS[sensor]['Wl'] = C / SENSORS[sensor]['Fc']  # wave length in m
