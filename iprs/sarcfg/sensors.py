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

    'GF3': {
        'Fc': 5.400012e9,  # Hz
        'H': 755000,  # height in m
        'V': 7570.67,  # velocity in m/s
        'Tp': 45.00e-06,  # Range pulse length in seconds
        'Kr': 13.3333e11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1,  # antenna length (range) in m
        'La': 10,  # antenna length (azimuth) in m
        'PRF': 1.413853e+03,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 66.66e+6,
        'Name': 'GF3',
    },
    'Sentinel1': {
        'Fc': 5.400012e9,  # Hz
        'H': 755000,  # height in m
        'V': 7570.67,  # velocity in m/s
        'Tp': 45.00e-06,  # Range pulse length in seconds
        'Kr': 13.3333e11,  # FM ra62e of radar pulse (Hz/s)
        'Lr': 1,  # antenna length (range) in m
        'La': 10,  # antenna length (azimuth) in m
        'PRF': 1.413853e+03,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 300.0e+6,
        'Name': 'Sentinel1',
    },
    'ALOSPALSAR': {
        'Fc': 1.27e9,  # Hz
        'H': 691500.,  # height in m
        'V': 7172.,  # velocity in m/s
        'Tp': 27.0e-6,  # Range pulse length in seconds
        'Kr': -28.e6 / 27.0e-6,  # FM rate of radar pulse (Hz/s)
        'Lr': 2.9,  # antenna length (range) in m
        'La': 8.9,  # antenna length (azimuth) in m
        'PRF': 2155.1724138,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 32.00e+6,
        'Name': 'ALOSPALSAR',
    },
    'ERS': {
        'Fc': 5.3e9,  # Hz
        'H': 791000.,  # height in m
        'V': 7098.,  # velocity in m/s
        'Tp': 3.71e-05,  # Range pulse length in seconds
        'Kr': 15.55e+6 / 3.71e-05,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.,  # antenna length (range) in m
        'La': 10.,  # antenna length (azimuth) in m
        'PRF': 1679.9023438,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 18.9599991e+6,
        'Name': 'ERS',
    },
    'RADARSAT1': {
        'Fc': 5.3e9,  # Hz
        'H': 793000.0,  # height in m
        'V': 7062.0,  # velocity in m/s
        'Tp': 41.750e-06,  # Range pulse length in seconds
        'Kr': -7.2135e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.5,  # antenna length (range) in m
        'La': 15,  # antenna length (azimuth) in m
        'PRF': 1.25698e+03,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 32.317e+6,
        'Name': 'RADARSAT1',
    },
    'RADARSAT2': {
        'Fc': 5.405e9,  # Hz
        'H': 785000.0,  # height in m
        'V': 7126.14,  # velocity in m/s
        'Tp': 37.120e-3,  # Range pulse length in seconds
        'Kr': 4.17788e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.37,  # antenna length (range) in m
        'La': 15,  # antenna length (azimuth) in m
        # 'PRF': 1679.9020,  # Hz
        'PRF': None,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': None,
        'Name': 'RADARSAT2',
    },
    'Air1': {
        'Fc': 5.3e9,  # Hz
        'H': 10000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        # 'Kr': 10e+12,  # FM rate of radar pulse (Hz/s)
        'Kr': 20e+12,  # FM rate of radar pulse (Hz/s)
        # 'Kr': 40e+12,  # FM rate of radar pulse (Hz/s)
        # 'Kr': -20e+12,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        # 'La': 6.0,  # antenna length (azimuth) in m
        'La': 3.0,  # antenna length (azimuth) in m
        # 'La': 1.5,  # antenna length (azimuth) in m
        'PRF': 100.0,  # Hz
        # 'PRF': 200.0,  # Hz
        # 'PRF': 600.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 60.0e6,
        # 'Fs': 100.0e6,
        # 'Fs': 240.3e6,
        'Name': 'Air1',
    },
    'Air2': {
        'Fc': 5.3e9,  # Hz
        'H': 10000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 25e-6,  # Range pulse length in seconds
        'Kr': 40e+12,  # FM rate of radar pulse (Hz/s)
        # 'Kr': 2.5e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 1.0,  # antenna length (azimuth) in m
        'PRF': 200.0,  # Hz
        # 'PRF': 600.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 240.0e6,
        # 'Fs': 100.0e6,
        'Name': 'Air2',
    },
    'Air3': {
        'Fc': 5.3e9,  # Hz
        'H': 10000,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 20e+12,  # FM rate of radar pulse (Hz/s)
        # 'Kr': 2.5e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 12,  # antenna length (range) in m
        'La': 3.0,  # antenna length (azimuth) in m
        'PRF': 100.0,  # Hz
        # 'PRF': 600.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 60.0e6,
        # 'Fs': 100.0e6,
        'Name': 'Air3',
    },
    'DIY1': {
        'Fc': 5.3e9,  # Hz
        'H': 1000.0,  # height in m
        'V': 150.0,  # velocity in m/s
        'Tp': 2.5e-6,  # Range pulse length in seconds
        'Kr': 4.0e+13,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.5,  # antenna length (range) in m
        'La': 15,  # antenna length (azimuth) in m
        'PRF': 600.0,  # Hz
        # 'PRF': 600.0,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 800.0e6,
        # 'Fs': 600e6,
        'Name': 'DIY1',
    },
    # 'DIY1': {
    #     'Fc': 5.3e9,  # Hz
    #     'H': 5000.0,  # height in m
    #     'V': 150.0,  # velocity in m/s
    #     'Tp': 2.5e-6,  # Range pulse length in seconds
    #     'Kr': 40.0e+13,  # FM rate of radar pulse (Hz/s)
    #     'Lr': 1.0,  # antenna length (range) in m
    #     'La': 1.5,  # antenna length (azimuth) in m
    #     'PRF': 150.0,  # Hz
    #     # 'PRF': 600.0,  # Hz
    #     # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
    #     'Fs': 213.0e6,
    #     # 'Fs': 600e6,
    #     'Name': 'DIY1',
    # },
    'SIMSARv1a': {
        'Fc': 5.3e9,  # Hz
        'H': 793000.0,  # height in m
        'V': 7062.0,  # velocity in m/s
        'Tp': 4.1750e-05,  # Range pulse length in seconds
        'Kr': -7.2135e+11,  # FM rate of radar pulse (Hz/s)
        'Lr': 1.5,  # antenna length (range) in m
        'La': 15,  # antenna length (range) in m
        'PRF': 1.25698e+03,  # Hz
        # ADC sampling frequency, can be None: Ts = 1 / (1.2*self._sensor['B'])
        'Fs': 32.317e+6,
        'Name': 'SIMSARv1',
    },

}

