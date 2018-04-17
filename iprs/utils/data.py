#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import os
import pickle as pkl
import scipy.io as scio


def sarstore(sardata, sarplat, file):

    ext = os.path.splitext(file)[1]
    if ext == '.pkl':
        f = open(file, 'wb')
        pkl.dump(sardata, f, 0)
        pkl.dump(sarplat, f, 0)
        f.close()
    elif ext == '.mat':
        # scio.savemat(file, {'sardata_name': sardata.name,
        #                     'sardata_rawdata': sardata.rawdata,
        #                     'sardata_image': sardata.image,
        #                     'sarplat_name': sarplat.name,
        #                     'sarplat_sensor': sarplat.sensor,
        #                     'sarplat_acquisition': sarplat.acquisition,
        #                     'sarplat_params': sarplat.params,
        #                     })
        scio.savemat(file, {'sardata_name': sardata.name,
                    'sardata_rawdata': sardata.rawdata,
                    'sardata_image': sardata.image,
                    'sarplat_name': sarplat.name,
                    'sarplat_sensor': sarplat.sensor,
                    'sarplat_acquisition': sarplat.acquisition,
                    'sarplat_params': sarplat.params,
                    })
    print("sar data has been stored in: ", file)
    return 0


def sarread(file):

    filename, EXT = os.path.splitext(file)

    if EXT == '.pkl':
        f = open(file, 'rb')
        sardata = pkl.load(f)
        sarplat = pkl.load(f)
        f.close()
    elif EXT == '.mat':
        data = scio.loadmat(file)
        print("++++++++++++++++++++++++++")
        print(type(data), data)
        print("++++++++++++++++++++++++++")

    print("read sar data from: ", file)
    return sardata, sarplat
