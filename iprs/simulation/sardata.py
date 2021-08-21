#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import h5py


class SarData(object):
    r"""SAR data class.
        rawdata
        image
        store
        read

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
        print(file)
        f = h5py.File(file, "w")
        grp = f.create_group("sardata")  # sardata
        grp.create_dataset("name", data=self._name)
        grp.create_dataset("image", data=self._image)
        grp.create_dataset("rawdata", data=self._rawdata)

        grp = f.create_group("sarplat")  # sarplat
        grp.create_dataset("name", data=sarplat.name)

        sensor = sarplat.sensor
        sensor_grp = grp.create_group("sensor")
        for key, value in sensor.items():
            sensor_grp.create_dataset(key, data=value)

        acquis = sarplat.acquisition
        acquis_grp = grp.create_group("acquisition")
        for key, value in acquis.items():
            acquis_grp.create_dataset(key, data=value)

        params = sarplat.params
        params_grp = grp.create_group("params")
        for key, value in params.items():
            params_grp.create_dataset(key, data=value)

        f.close()
        print("sar data has been stored in: ", file)

    def read(self, file):
        r"""Read SAR data file

        Read SAR data file (``.pkl`` or ``.mat``)

        Parameters
        ----------
        file : {str}
            SAR data file path}

        Returns
        -------
        sardata : Instance SarData
            The SAR raw data.

        sarplat : Instance of SarPlat
            The SAR platform for obtain the SAR data.
        """
        f = h5py.File(file, "r")

        ds_sardata = f["sardata"]
        ds_sarpalt = f["sarplat"]

        self._name = ds_sardata['name'].value
        self._image = ds_sardata['image'].value
        self._rawdata = ds_sardata['rawdata'].value

        ds_sarpalt_sensor = ds_sarpalt["sensor"]
        ds_sarpalt_params = ds_sarpalt["params"]
        ds_sarpalt_acquis = ds_sarpalt["acquisition"]
        sensor = dict()
        for key in ds_sarpalt_sensor.keys():
            sensor[key] = ds_sarpalt_sensor[key].value

        params = dict()
        for key in ds_sarpalt_params.keys():
            params[key] = ds_sarpalt_params[key].value

        acquis = dict()
        for key in ds_sarpalt_acquis.keys():
            acquis[key] = ds_sarpalt_acquis[key].value

        sarplat = ds_sarpalt.copy()

        sarplat.sensor = sensor
        sarplat.params = params
        sarplat.acquisition = acquis

        f.close()

        print("read sar data from: ", file)
        return sarplat
