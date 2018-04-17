#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np

from ..utils.const import *
from ..dsp.math import nextpow2


class SarPlat(object):

    """SAR platform class.
        sensor
        params

    """
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError('name must be a string!')
        self._name = value

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, value):
        if not isinstance(value, dict):
            raise ValueError('sensor must be a dict!')
        self._sensor = value

    @property
    def acquisition(self):
        return self._acquisition

    @acquisition.setter
    def acquisition(self, value):
        if not isinstance(value, dict):
            raise ValueError('acquisition must be a dict!')

        Yc = self._sensor['H'] * np.tan(value['Ad'])
        Rc = np.sqrt(self._sensor['H'] ** 2 + Yc ** 2)
        Xc = Rc * np.tan(value['As'])

        value['SceneCenter'] = [Xc, Yc, 0.0]
        if value['SceneArea'] is None:
            value['SceneArea'] = [-128, 128, -256, 256]

        if value['PlatCenter'] is None:
            value['PlatCenter'] = [0.0, 0.0, self._sensor['H']]

        value['PlatCenter'] = np.array(value['PlatCenter'])
        value['SceneCenter'] = np.array(value['SceneCenter'])
        value['SceneArea'] = np.array(value['SceneArea'])
        value['Ls'] = self._sensor['Wl'] * Rc / self._sensor['La']
        value['Rc'] = Rc
        self._acquisition = value

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if not isinstance(self._sensor, dict):
            raise ValueError('sensor must be a dict!')
        if not isinstance(self._acquisition, dict):
            raise ValueError('acquisition must be a dict!')

        H = self._sensor['H']
        V = self._sensor['V']
        La = self._sensor['La']

        Rc = self._acquisition['Rc']
        Ls = self._acquisition['Ls']

        PC = self._acquisition['PlatCenter']
        SC = self._acquisition['SceneCenter']
        SA = self._acquisition['SceneArea']
        As = self._acquisition['As']
        Ad = self._acquisition['Ad']

        Xc = SC[0]
        Yc = SC[1]
        R0 = np.sqrt(np.sum((PC - SC) ** 2))

        S = SA + np.array([Xc, Xc, Yc, Yc])

        if self._sensor['PRF'] is None:
            Tsar = Ls / V
            # Ka = -2.0 * V**2 / self._sensor['Wl'] / Rc
            Ka = -2.0 * V ** 2 / self._sensor['Wl'] / R0
            Ba = np.abs(Ka * Tsar)
            # print(Ka, Ba, "+++=")
            PRF = (1.25 * Ba)
            # PRF = (1.25 * Ba)/2.0
            # PRF = (4.0 * Ba)
        else:
            PRF = self._sensor['PRF']

        PRT = 1.0 / PRF  # azimuth sampling
        da = 1.0 / PRF

        if self._sensor['Fs'] is None:
            # phor = C / (2 * self._sensor['B'])  # range resolution
            Fs = (1.905 * self._sensor['B'])
            # Fs = (1.905 * self._sensor['B'])/2.0
            # Fs = (8.0 * self._sensor['B'])
        else:
            Fs = self._sensor['Fs']

        Ts = 1.0 / Fs  # range sampling
        dr = 1.0 / Fs

        xmin = S[0]
        xmax = S[1]
        ymin = S[2]
        ymax = S[3]

        # amin = -0.5 * Ls + xmin
        # amax = 0.5 * Ls + xmax
        amin = xmin
        amax = xmax
        tamin = amin / V
        tamax = amax / V
        Na = int((tamax - tamin) / da)
        # Na = int(2 ** nextpow2(Na))
        PRT = (tamax - tamin) / Na
        PRF = 1.0 / PRT
        ta = np.linspace(tamin, tamax, Na)
        fa = np.linspace(-0.5 * PRF, 0.5 * PRF, Na)

        Rmin = np.sqrt(H ** 2 + ymin ** 2)
        Rmax = np.sqrt(H ** 2 + ymax ** 2)
        # Rmax = np.sqrt(H ** 2 + ymax ** 2 + (xmax - xmin) ** 2)
        # Rmax = np.sqrt(H ** 2 + ymax ** 2 + (Ls / 2)**2)

        # if "self._sensor['Tp']" is added,
        #  the targets show in diffrent pos in
        # real scence ang reconstructed image
        # trmin = -0.50 * self._sensor['Tp'] + 2.0 * Rmin / C
        # trmax = 0.50 * self._sensor['Tp'] + 2.0 * Rmax / C
        trmin = 2.0 * Rmin / C
        trmax = 2.0 * Rmax / C
        rmin = C * trmin
        rmax = C * trmax
        Nr = int((trmax - trmin) / dr)
        # Nr = int(2 ** nextpow2(Nr))
        Ts = (trmax - trmin) / Nr
        Fs = 1.0 / Ts
        tr = np.linspace(trmin, trmax, Nr)
        fr = np.linspace(-0.5 * Fs, 0.5 * Fs, Nr)
        # print(type(fr))
        self._sensor['PRF'] = PRF
        self._sensor['Fs'] = Fs

        param = dict()
        param['R0'] = R0  # plat center --> scene center
        param['PRT'] = PRT  # azimuth
        param['PRF'] = PRF  # azimuth
        param['Ts'] = Ts  # range
        param['Fs'] = Fs  # range
        param['Na'] = Na  # azimuth
        param['Nr'] = Nr  # range
        param['xmin'] = xmin
        param['xmax'] = xmax
        param['ymin'] = ymin
        param['ymax'] = ymax
        param['Rmin'] = Rmin
        param['Rmax'] = Rmax
        param['amin'] = amin
        param['amax'] = amax
        param['rmin'] = rmin
        param['rmax'] = rmax
        param['tamin'] = tamin
        param['tamax'] = tamax
        param['trmin'] = trmin
        param['trmax'] = trmax
        param['ta'] = ta  # time array in azimuth
        param['fa'] = fa  # freq array in azimuth
        param['tr'] = tr  # time array in range
        param['fr'] = fr  # freq array in range
        param['da'] = da  # resolution in azimuth
        param['dr'] = dr  # resolution in range
        param['Xc'] = Xc  # X center
        param['Yc'] = Yc  # Y center
        param['Rc'] = Rc  # R center
        param['DX'] = C / (2.0 * self._sensor['B'])
        param['DY'] = La / 2.0

        self._params = param

        return self._params

    def printsp(self, verbose=False):
        print("===============SAR platform: ", self._name, "================")
        print("--------------------------sensor-----------------------------")
        for arg, value in self._sensor.items():
            print(arg, value)
        print("-----------------------acquisition---------------------------")
        for arg, value in self._acquisition.items():
            print(arg, value)
        print("--------------------------params-----------------------------")
        if verbose:
            print(self._params)
        else:
            for arg, value in self._params.items():
                if arg == 'ta' or arg == 'tr' or arg == 'fr' or arg == 'fa':
                    print("shape of " + arg + ": ", value.shape)
                else:
                    print(arg, value)
        print("=============================================================")
