#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-23 07:01:55
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import os
import iprs
import h5py
import sys
import pickle as pkl
import scipy.io as scio
import numpy as np
import logging


def sarstore(sardata, sarplat, file):
    r"""Read SAR file

    Store SAR data and platform to a file (``.pkl`` or ``.mat``)

    Parameters
    ----------
    sardata : SarData
        The SAR raw data.

    sarplat : SarPlat
        The SAR platform for obtain the SAR data.

    Returns
    -------
    file : {string}
        The file path for storing SAR data and platform
    """

    logging.info("---Store SAR data...")

    if np.iscomplex(sardata.rawdata).any():
        sardata.rawdata = np.array(
            [np.real(sardata.rawdata), np.imag(sardata.rawdata)]).transpose(1, 2, 0)

    folder, filename = os.path.split(file)
    _, ext = os.path.splitext(filename)
    if os.path.exists(folder) is False:
        os.makedirs(folder)

    if ext == '.pkl':
        f = open(file, 'wb')
        pkl.dump(sardata, f, 0)
        pkl.dump(sarplat, f, 0)
        f.close()
    elif ext == '.mat':
        # f = h5py.File(file, "w")
        # grp = f.create_group("sardata")  # sardata
        # grp.create_dataset("name", data=sardata.name)
        # grp.create_dataset("image", data=sardata.image)
        # grp.create_dataset("rawdata", data=sardata.rawdata)

        # grp = f.create_group("sarplat")  # sarplat
        # grp.create_dataset("name", data=sarplat.name)

        # sensor = sarplat.sensor
        # sensor_grp = grp.create_group("sensor")
        # for key, value in sensor.items():
        #     sensor_grp.create_dataset(key, data=value)

        # acquis = sarplat.acquisition
        # acquis_grp = grp.create_group("acquisition")
        # for key, value in acquis.items():
        #     acquis_grp.create_dataset(key, data=value)

        # params = sarplat.params
        # params_grp = grp.create_group("params")
        # for key, value in params.items():
        #     params_grp.create_dataset(key, data=value)

        # f.close()

        # ==================================================

        sardatadict = {}
        sarplatdict = {}
        sardatadict['name'] = sardata.name
        sardatadict['rawdata'] = sardata.rawdata
        sardatadict['image'] = sardata.image
        sardatadict['description'] = sardata.description
        sarplatdict['name'] = sarplat.name
        sarplatdict['sensor'] = sarplat.sensor
        sarplatdict['acquisition'] = sarplat.acquisition
        sarplatdict['params'] = sarplat.params
        sarplatdict['selection'] = sarplat.selection
        scio.savemat(file, {'sardata': sardatadict, 'sarplat': sarplatdict})

    logging.info("~~~SAR data has been stored in: %s" % file)
    logging.info("---Done!")

    return 0


def sarread(file):
    r"""Read SAR file

    Read SAR file (``.pkl`` or ``.mat``) and returns SAR data and platform

    Parameters
    ----------
    file : {string}
        SAR data (contains platform) file path.

    Returns
    -------
    sardata : Instance SarData
        The SAR raw data.

    sarplat : Instance of SarPlat
        The SAR platform for obtain the SAR data.
    """

    logging.info("---Read SAR data...")

    filename, EXT = os.path.splitext(file)

    if EXT == '.pkl':
        f = open(file, 'rb')
        # for python2
        if sys.version_info < (3, 1):
            sardata = pkl.load(f)
            sarplat = pkl.load(f)
        # for python3
        else:
            sardata = pkl.load(f, encoding='latin1')
            sarplat = pkl.load(f, encoding='latin1')
        f.close()
    elif EXT == '.mat':
        data = scio.loadmat(file, struct_as_record=True)
        sardata = iprs.SarData()
        sarplat = iprs.SarPlat()

        temp = data['sardata']
        sardata.name = str(temp['name'][0][0][0])
        sardata.image = temp['image'][0][0]
        sardata.rawdata = temp['rawdata'][0][0]
        sardata.description = temp['description'][0][0]

        if 'sarplat' in data.keys():
            temp = data['sarplat']
            sarplat.name = str(temp['name'][0][0][0])
            sensor = temp['sensor'][0][0][0][0]
            acquis = temp['acquisition'][0][0][0][0]
            params = temp['params'][0][0][0][0]
            selection = temp['selection'][0][0][0][0]

            sensordict = {}
            sensordict['Fc'] = sensor['Fc'][0][0]
            sensordict['H'] = sensor['H'][0][0]
            sensordict['V'] = sensor['V'][0][0]
            sensordict['Tp'] = sensor['Tp'][0][0]
            sensordict['Kr'] = sensor['Kr'][0][0]
            sensordict['Lr'] = sensor['Lr'][0][0]
            sensordict['La'] = sensor['La'][0][0]
            sensordict['PRF'] = sensor['PRF'][0][0]
            sensordict['Fs'] = sensor['Fs'][0][0]
            sensordict['Name'] = str(sensor['Name'][0])
            sensordict['B'] = sensor['B'][0][0]
            sensordict['Wl'] = sensor['Wl'][0][0]
            sensordict['Rs'] = sensor['Rs'][0][0]
            sensordict['To'] = sensor['To'][0][0]
            sensordict['Ws'] = sensor['Ws'][0][0]
            sensordict['Vs'] = sensor['Vs'][0][0]
            sensordict['Vr'] = sensor['Vr'][0][0]
            sensordict['Vg'] = sensor['Vg'][0][0]
            sarplat.sensor = sensordict
            # print(sensordict)

            acqdict = {}
            acqdict['PlatCenter'] = acquis['PlatCenter'][0]
            acqdict['SceneCenter'] = acquis['SceneCenter'][0]
            acqdict['BeamCenter'] = acquis['BeamCenter'][0]
            acqdict['SceneArea'] = acquis['SceneArea'][0]
            acqdict['BeamArea'] = acquis['BeamArea'][0]
            acqdict['EchoSize'] = acquis['EchoSize'][0]
            acqdict['As'] = acquis['As'][0][0]
            acqdict['Ar'] = acquis['Ar'][0][0]
            acqdict['Ad'] = acquis['Ad'][0][0]
            acqdict['Be'] = acquis['Be'][0][0]
            acqdict['Ai'] = acquis['Ai'][0][0]
            acqdict['Rbc'] = acquis['Rbc'][0][0]
            acqdict['Rb0'] = acquis['Rb0'][0][0]
            acqdict['Rsc'] = acquis['Rsc'][0][0]
            acqdict['Rs0'] = acquis['Rs0'][0][0]

            # print(acquis['SceneArea'], acquis['PlatCenter'], acquis['EchoSize'])
            sarplat.acquisition = acqdict

            # sarplat.params = None
            pardict = {}
            pardict['GeometryMode'] = str(params['GeometryMode'][0])  # geometry mode: beam/scene
            pardict['Rb0'] = params['Rb0'][0][0]  # beam center min distance
            pardict['Rbc'] = params['Rbc'][0][0]  # beam center distance
            pardict['Rs0'] = params['Rs0'][0][0]  # scene center min distance
            pardict['Rsc'] = params['Rsc'][0][0]  # scene center distance
            pardict['Tp'] = params['Tp'][0][0]  # Pulse repetition period
            pardict['PRT'] = params['PRT'][0][0]  # azimuth
            pardict['PRF'] = params['PRF'][0][0]  # azimuth
            pardict['Fsa'] = params['Fsa'][0][0]  # azimuth, Fsa = PRF
            pardict['Fs'] = params['Fs'][0][0]  # range
            pardict['Fsr'] = params['Fsr'][0][0]  # range, Fsr = Fs
            pardict['Na'] = params['Na'][0][0]  # azimuth
            pardict['Nr'] = params['Nr'][0][0]  # range
            pardict['Ka'] = params['Ka'][0][0]  # azimuth
            pardict['Kr'] = params['Kr'][0][0]  # range
            pardict['xmin'] = params['xmin'][0][0]
            pardict['xmax'] = params['xmax'][0][0]
            pardict['ymin'] = params['ymin'][0][0]
            pardict['ymax'] = params['ymax'][0][0]
            pardict['Rnear'] = params['Rnear'][0][0]
            pardict['Rfar'] = params['Rfar'][0][0]
            pardict['tnear'] = params['tnear'][0][0]
            pardict['tfar'] = params['tfar'][0][0]
            pardict['tstart'] = params['tstart'][0][0]
            pardict['tend'] = params['tend'][0][0]
            pardict['ta'] = params['ta'][0]  # time array in azimuth
            pardict['fa'] = params['fa'][0]  # freq array in azimuth
            pardict['tr'] = params['tr'][0]  # time array in range
            pardict['fr'] = params['fr'][0]  # freq array in range
            pardict['Tsa'] = params['Tsa'][0][0]  # resolution in azimuth
            pardict['Tsr'] = params['Tsr'][0][0]  # resolution in range
            pardict['Xc'] = params['Xc'][0][0]  # X center
            pardict['Yc'] = params['Yc'][0][0]  # Y center
            pardict['DA'] = params['DA'][0][0]
            pardict['DR'] = params['DR'][0][0]
            pardict['DY'] = params['DY'][0][0]
            pardict['DX'] = params['DX'][0][0]
            pardict['FPa'] = params['FPa'][0][0]
            pardict['FPr'] = params['FPr'][0][0]
            pardict['BWa'] = params['BWa'][0][0]
            pardict['Ta'] = params['Ta'][0][0]
            pardict['Tr'] = params['Tr'][0][0]
            pardict['t0'] = params['t0'][0][0]
            pardict['tac'] = params['tac'][0][0]
            pardict['fadc'] = params['fadc'][0][0]
            pardict['Bdop'] = params['Bdop'][0][0]
            pardict['Nsar'] = params['Nsar'][0][0]
            pardict['Tsar'] = params['Tsar'][0][0]
            pardict['Lsar'] = params['Lsar'][0][0]

            pardict['Ad'] = params['Ad'][0][0]  # depression angle
            pardict['As'] = params['As'][0][0]  # squint angle
            pardict['Ar'] = params['Ar'][0][0]  # squint angle
            pardict['Be'] = params['Be'][0][0]  # antenna elevation beamwidth
            pardict['Ai'] = params['Ai'][0][0]  # incidence angle

            pardict['taSub'] = params['taSub'][0]
            pardict['faSub'] = params['faSub'][0]
            pardict['trSub'] = params['trSub'][0]
            pardict['frSub'] = params['frSub'][0]
            pardict['SubNa'] = params['SubNa'][0][0]
            pardict['SubNr'] = params['SubNr'][0][0]
            pardict['SubTa'] = params['SubTa'][0][0]
            pardict['SubTr'] = params['SubTr'][0][0]
            pardict['tnearSub'] = params['tnearSub'][0][0]
            pardict['tfarSub'] = params['tfarSub'][0][0]
            pardict['tstartSub'] = params['tstartSub'][0][0]
            pardict['tendSub'] = params['tendSub'][0][0]
            pardict['SubRnear'] = params['SubRnear'][0][0]
            pardict['SubRfar'] = params['SubRfar'][0][0]
            pardict['SubSceneArea'] = params['SubSceneArea'][0]
            pardict['SubBeamArea'] = params['SubBeamArea'][0]
            pardict['SubSceneCenter'] = params['SubSceneCenter'][0]
            pardict['SubBeamCenter'] = params['SubBeamCenter'][0]
            pardict['SubEchoAnchor'] = params['SubEchoAnchor'][0]
            pardict['SubEchoSize'] = params['SubEchoSize'][0]
            pardict['SubFPa'] = params['SubFPa'][0][0]
            pardict['SubFPr'] = params['SubFPr'][0][0]
            pardict['SubRsc'] = params['SubRsc'][0][0]
            pardict['SubRs0'] = params['SubRs0'][0][0]
            pardict['SubRbc'] = params['SubRbc'][0][0]
            pardict['SubRb0'] = params['SubRb0'][0][0]
            pardict['xminSub'] = params['xminSub'][0][0]
            pardict['xmaxSub'] = params['xmaxSub'][0][0]
            pardict['yminSub'] = params['yminSub'][0][0]
            pardict['ymaxSub'] = params['ymaxSub'][0][0]
            pardict['SubBe'] = params['SubBe'][0][0]
            pardict['SubAd'] = params['SubAd'][0][0]
            pardict['SubKa'] = params['SubKa'][0][0]
            pardict['SubBa'] = params['SubBa'][0][0]

            sarplat.params = pardict

            seldict = {}
            seldict['taSub'] = selection['taSub'][0]
            seldict['faSub'] = selection['faSub'][0]
            seldict['trSub'] = selection['trSub'][0]
            seldict['frSub'] = selection['frSub'][0]
            seldict['SubNa'] = selection['SubNa'][0][0]
            seldict['SubNr'] = selection['SubNr'][0][0]
            seldict['SubTa'] = selection['SubTa'][0][0]
            seldict['SubTr'] = selection['SubTr'][0][0]
            seldict['tnearSub'] = selection['tnearSub'][0][0]
            seldict['tfarSub'] = selection['tfarSub'][0][0]
            seldict['tstartSub'] = selection['tstartSub'][0][0]
            seldict['tendSub'] = selection['tendSub'][0][0]
            seldict['SubRnear'] = selection['SubRnear'][0][0]
            seldict['SubRfar'] = selection['SubRfar'][0][0]
            seldict['SubSceneArea'] = selection['SubSceneArea'][0]
            seldict['SubBeamArea'] = selection['SubBeamArea'][0]
            seldict['SubSceneCenter'] = selection['SubSceneCenter'][0]
            seldict['SubBeamCenter'] = selection['SubBeamCenter'][0]
            seldict['SubEchoAnchor'] = selection['SubEchoAnchor'][0]
            seldict['SubEchoSize'] = selection['SubEchoSize'][0]
            seldict['SubFPa'] = selection['SubFPa'][0][0]
            seldict['SubFPr'] = selection['SubFPr'][0][0]
            seldict['SubRsc'] = selection['SubRsc'][0][0]
            seldict['SubRs0'] = selection['SubRs0'][0][0]
            seldict['SubRbc'] = selection['SubRbc'][0][0]
            seldict['SubRb0'] = selection['SubRb0'][0][0]
            seldict['xminSub'] = selection['xminSub'][0][0]
            seldict['xmaxSub'] = selection['xmaxSub'][0][0]
            seldict['yminSub'] = selection['yminSub'][0][0]
            seldict['ymaxSub'] = selection['ymaxSub'][0][0]
            seldict['SubBe'] = selection['SubBe'][0][0]
            seldict['SubAd'] = selection['SubAd'][0][0]
            seldict['SubKa'] = selection['SubKa'][0][0]
            seldict['SubBa'] = selection['SubBa'][0][0]
            sarplat.selection = seldict
        else:
            sarplat = None

    elif EXT == '.hdf5':
        f = h5py.File(file, "r")
        sardata = iprs.SarData()
        sarplat = iprs.SarPlat()

        ds_sardata = f["sardata"]
        ds_sarpalt = f["sarplat"]

        sardata.name = ds_sardata['name'].value
        sardata.image = ds_sardata['image'].value
        sardata.rawdata = ds_sardata['rawdata'].value

        ds_sarpalt_sensor = ds_sarpalt["sensor"]
        ds_sarpalt_params = ds_sarpalt["params"]
        ds_sarpalt_acquis = ds_sarpalt["acquisition"]
        ds_sarpalt_select = ds_sarpalt["selection"]
        sensor = dict()
        for key in ds_sarpalt_sensor.keys():
            sensor[key] = ds_sarpalt_sensor[key].value

        params = dict()
        for key in ds_sarpalt_params.keys():
            params[key] = ds_sarpalt_params[key].value

        acquis = dict()
        for key in ds_sarpalt_acquis.keys():
            acquis[key] = ds_sarpalt_acquis[key].value

        selection = dict()
        for key in ds_sarpalt_select.keys():
            selection[key] = ds_sarpalt_select[key].value

        sarplat.name = ds_sarpalt['name'].value
        sarplat.sensor = sensor
        sarplat.params = params
        sarplat.acquisition = acquis
        sarplat.selection = selection

        f.close()

    else:
        raise(TypeError("Not supported! Only support: (pkl, mat, hdf5)!"))
    logging.info("~~~SAR data has been read from: %s" % file)
    logging.info("---Done!")

    return sardata, sarplat


def load_data(datafile, way=0, which='all', normlize=False):
    r"""load SAR data from file

    load SAR data from file

    Parameters
    ----------
    datafile : {string}
        SAR data file path
    way : {number}, optional
            if way is 1:  # [N Na Nr]
        return X, I, sarplat

        if way is 2: [2 N Na Nr]
            return X, sarplat

        if way is 3: [N 2 Na Nr]
            return X, sarplat
        if way is 4: [N Na Nr 2]

        (the default is 0, which [default_description])
    which : {str}, optional
        'rawdata', 'image', 'all' --> rawdata and image
        (the default is 'all', which load rawdata and image)
    normlize : {bool}, optional
        Is normalize data (the default is False, which does not normalize data.)

    Returns
    -------
    X: numpy array
        SAR raw data
    sarplat: SarPlat object
        SAR platform for obtaining data
    I: numpy array
        Intesity image of the data.
    XmaxValue: complex number
        Maximum value in X

    """

    sardata, sarplat = iprs.sarread(datafile)

    if way is 0:
        return sardata, sarplat

    X = np.array(sardata.rawdata)  # [N Na Nr] complex
    I = np.array(sardata.image)

    XmaxValue = np.max(np.abs(X.flatten()))
    if normlize:
        X = X / XmaxValue

    if np.ndim(X) is 2:
        X = np.array([X])
        I = np.array([I])
    print(datafile, way, X.shape)
    N, Na, Nr = X.shape
    if way is 1:  # [N Na Nr]
        return X, I, sarplat

    if way is 2:  # [2 N Na Nr]
        X = np.array([X.real, X.imag])  # [2 N Na Nr]
        return X, sarplat

    if way is 3:  # [N 2 Na Nr]
        X = np.array([X.real, X.imag])  # [2 N Na Nr]
        X = np.swapaxes(X, 0, 1)  # [N 2 Na Nr]
        return X, sarplat
    if way is 4:  # [N Na Nr 2]
        X = np.array([X.real, X.imag])  # [2 N Na Nr]
        X = X.transpose(1, 2, 3, 0)  # [N Na Nr 2]

        return X, sarplat, I, XmaxValue
    # if way is 5:


def format_data(X, modefrom='chnl_last', modeto='chnl_first'):
    """format data

    Format data to chanel first or chanel last.

    Parameters
    ----------
    X : {numpy array}
        data to be formated
    modefrom : {str}, optional
        chnl_last  --> chanel last; chnl_first  --> chanel first
        (the default is 'chnl_last', which chanel first)
    modeto : {str}, optional
        chnl_last  --> chanel last; chnl_first  --> chanel first
        (the default is 'chnl_last', which chanel first)

    Returns
    -------
    X : numpy array
        Formated data

    Raises
    ------
    TypeError
        X should be a 3 or 4 dimention array!
    ValueError
        Unknown mode of modefrom or modeto
    """

    if modefrom == modeto:
        return X
    if np.ndim(X) is 4:
        s = 1
        m = 2
        e = 3
    elif np.ndim(X) is 3:
        s = 0
        m = 1
        e = 2
    else:
        raise TypeError("X should be a 3 or 4 dimention array!")
    if modefrom is 'chnl_last':
        if modeto is 'chnl_first':
            X = np.swapaxes(X, s, e)  # N H W C --> N C W H
            X = np.swapaxes(X, m, e)  # N C W H --> N C H W
        else:
            raise ValueError("Unknown mode of: ", modeto)
    elif modefrom is 'chnl_first':
        if modeto is 'chnl_last':
            X = np.swapaxes(X, s, e)  # N C H W --> N W H C
            X = np.swapaxes(X, s, m)  # N W H C --> N H W C
    return X
