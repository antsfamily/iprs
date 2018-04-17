#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import h5py
import iprs


class SarData(object):
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
    def rawdata(self):
        return self._rawdata

    @rawdata.setter
    def rawdata(self, value):
        self._rawdata = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    def store(self, sarplat, file):
        sen = sarplat.sensor
        print(sarplat.sensor, type(sen))
        f = h5py.File(file, "w")
        grp_sar = f.create_group("SAR")
        grp_sar.create_dataset("sardata.name", data=self._name)
        grp_sar.create_dataset("sardata.rawdata", data=self._rawdata)
        grp_sar.create_dataset("sardata.image", data=self._image)
        grp_sar.create_dataset("sarplat.name", data=sarplat.name)
        grp_sar.create_dataset("sensor", data=sen)
        grp_sar.create_dataset("acquisition", data=sarplat.acquisition)
        grp_sar.create_dataset("params", data=sarplat.params)
        f.close()
        print("sar data has been stored in: ", file)

    def read(self, file):
        sarplat = iprs.SarPlat()
        f = h5py.File(file, "r")
        grp_sar = f['SAR']
        self._name = grp_sar['sardata.name']
        self._rawdata = grp_sar['sardata.rawdata']
        self._image = grp_sar['sardata.image']
        sarplat.name = grp_sar['sarplat.name']
        sarplat.sensor = grp_sar['sarplat.sensor']
        sarplat.acquisition = grp_sar['sarplat.acquisition']
        sarplat.params = grp_sar['sarplat.params']

        print("read sar data from: ", file)
        return sarplat
