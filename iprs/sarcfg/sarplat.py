#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-15 15:52:43
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
from __future__ import division, print_function, absolute_import

import numpy as np

import logging
from iprs.utils.const import *
from iprs.sharing.range_azimuth_beamwidth_footprint import azimuth_beamwidth, compute_range_beamwidth, cr_footprint, ar_footprint

AirboneSatelliteHeightBoundary = 60e3  # 60 km


class SarPlat(object):
    r"""SAR platform class.
        sensor
        acquisition
        params
    """

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        logging.info("---Check and set SAR platform name...")

        if not isinstance(value, str):
            raise ValueError('name must be a string!')
        self._name = value
        logging.info("---Done!")

    @property
    def sensor(self):
        return self._sensor

    @sensor.setter
    def sensor(self, value):
        logging.info("---Check and set SAR sensor parameters...")

        if not isinstance(value, dict):
            raise ValueError('sensor must be a dict!')
        self._sensor = value

        self._sensor['B'] = self._sensor['Tp'] * np.abs(self._sensor['Kr'])  # chirp rate in Hz/s
        self._sensor['Wl'] = C / self._sensor['Fc']  # wave length in m

        Re = Rep
        Rs = self._sensor['H'] + Re
        # Rs = self._sensor['H'] + Ree
        self._sensor['Rs'] = Rs
        if value['H'] < AirboneSatelliteHeightBoundary:
            logging.info("---Airbone.")
            self._sensor['Vs'] = self._sensor['V']
            self._sensor['Vr'] = self._sensor['V']
            self._sensor['Vg'] = self._sensor['V']
            self._sensor['To'] = -1
            self._sensor['Ws'] = -1
        else:
            logging.info("---Satellite.")
            # Earth Bending Geometry (Vg < Vr < Vs, Vr = \sqrt{Vg*Vs})
            self._sensor['To'] = 2 * PI * np.sqrt((Rs)**3 / Ge)
            self._sensor['Ws'] = 2 * PI / self._sensor['To']
            self._sensor['Vs'] = Rs * self._sensor['Ws']
            self._sensor['Vr'] = self._sensor['V']
            # Equivalent velocity (Linear geometry)
            self._sensor['Vg'] = self._sensor['Vr']**2 / self._sensor['Vs']  # ground velocity
        Vr = self._sensor['Vs'] * np.sqrt(Re / Rs)
        logging.info("---Computed equivalent velocity is " + str(Vr) +
                     ", setted equivalent velocity is " + str(self._sensor['Vr']) + ".")
        logging.info("---Done!")

    @property
    def acquisition(self):
        return self._acquisition

    @acquisition.setter
    def acquisition(self, value):
        logging.info("---Check and set acquisition parameters...")

        if not isinstance(value, dict):
            raise ValueError('acquisition must be a dict!')

        H = self._sensor['H']
        V = self._sensor['V']
        Vr = self._sensor['Vr']
        Vs = self._sensor['Vs']
        PRF = self._sensor['PRF']
        Fsr = self._sensor['Fs']
        Tp = self._sensor['Tp']
        Rs = self._sensor['Rs']

        As = value['As']
        Ad = value['Ad']
        Be = value['Be']
        SA = value['SceneArea']
        PC = value['PlatCenter']
        ES = value['EchoSize']

        # As: squint angle in earth curve geometry, Ar: squint angle in line geometry
        Ar = (Vs / Vr) * As

        if PC is None:
            PC = [0.0, 0.0, self._sensor['H']]

        if value['EchoSize'] is None:
            logging.error("~~~EchoSize should be specified!")

        SAV = [0, 0, 0, 0]
        BAV = [0, 0, 0, 0]
        if SA is None:
            SA = [None, None, None, None]

        if Be is None:
            Nr = ES[1]
            Be = compute_range_beamwidth(Nr, Fsr, H, Ad, Tp)

        # if Be is None and (SA[1] is None or SA[0] is None):
        #     logging.error(
        #         r"~~~The antenna elevation beamwidth Be or scene area must be specified!")
        #     raise ValueError(
        #         "The antenna elevation beamwidth Be or scene area must be specified!")

        if (Ad - Be / 2.0) <= 0 or (Ad + Be / 2.0) >= np.pi / 2.0:
            logging.error(r"~~~The antenna elevation beamwidth Be is too large!")

        # print(Ad * 180 / PI, Be * 180 / PI, "[[[[")
        Rnear = H / (np.sin(Ad + Be / 2.0) + EPS)
        Rfar = H / (np.sin(Ad - Be / 2.0) + EPS)
        FPr = np.sqrt(Rfar**2 + Rnear**2 - 2. * Rnear * Rfar * np.cos(Be) + EPS)

        Rsc = 0.5 * np.sqrt(2. * Rfar**2 + 2. * Rnear**2 - FPr**2 + EPS)
        Rs0 = Rsc * np.cos(Ar)

        Ysc = Rsc * np.sin(Ar)
        Xsc = np.sqrt(np.abs(Rs0**2 - H**2))
        SC = [Xsc, Ysc, 0.0]

        Rbc = H / (np.sin(Ad) + EPS)
        Rb0 = Rbc * np.cos(Ar)

        Ybc = Rbc * np.sin(Ar)
        Xbc = np.sqrt(np.abs(Rb0**2 - H**2))
        BC = [Xbc, Ybc, 0.0]

        if (SA[0] is None) or (SA[1] is None):
            Ynear = Rnear * np.sin(Ar)
            Yfar = Rfar * np.sin(Ar)
            Xnear = np.sqrt((Rnear ** 2 - H**2) - Ynear ** 2 + EPS)
            Xfar = np.sqrt((Rfar ** 2 - H**2) - Yfar ** 2 + EPS)
            SAV[0] = Xnear - Xsc
            SAV[1] = Xfar - Xsc
        else:
            SAV[0] = SA[0]
            SAV[1] = SA[1]

        if (SA[2] is None) or (SA[3] is None):
            Na, Nr = ES
            Ta = Na / PRF
            SAV[2] = -Ta * V / 2.0
            SAV[3] = Ta * V / 2.0
        else:
            SAV[2] = SA[2]
            SAV[3] = SA[3]

        Na, Nr = ES
        Ta = Na / PRF
        FPr0 = H / np.tan(Ad + Be / 2.) - H / np.tan(Ad)
        FPr1 = H / np.tan(Ad - Be / 2.) - H / np.tan(Ad)
        BAV = (FPr0, FPr1, -Ta * V / 2.0, Ta * V / 2.0)

        if H < AirboneSatelliteHeightBoundary:
            logging.info("---Airbone.")
            Ai = PI / 2. - Ad
        else:
            Ao = np.arccos((Rs**2 + Rea**2 - Rbc**2) / (2. * Rs * Rea))
            Ai = (PI / 2. - Ad) + Ao
            logging.info("---Satellite.")
        logging.info('---Done!')

        value['PlatCenter'] = np.array(PC)
        value['SceneCenter'] = np.array(SC)
        value['BeamCenter'] = np.array(BC)
        value['SceneArea'] = np.array(SAV)
        value['BeamArea'] = np.array(BAV)
        value['Rbc'] = Rbc
        value['Rb0'] = Rb0
        value['Rsc'] = Rsc
        value['Rs0'] = Rs0
        value['Rnear'] = Rnear
        value['Rfar'] = Rfar
        value['Be'] = Be
        value['Ar'] = Ar
        value['Ai'] = Ai

        self._acquisition = value

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):

        logging.info("---Check and set algorithm parameters...")

        if value is not None:
            if not isinstance(value, dict):
                raise ValueError('params must be a dict!')
            if hasattr(self, '_params'):
                for k, v in value.items():
                    self._params[k] = v
            else:
                self._params = value

            return self._params

        GM = self._params['GeometryMode']
        if not isinstance(self._sensor, dict):
            raise ValueError('sensor must be a dict!')
        if not isinstance(self._acquisition, dict):
            raise ValueError('acquisition must be a dict!')

        H = self._sensor['H']
        V = self._sensor['V']
        Vr = self._sensor['Vr']
        Vg = self._sensor['Vg']
        Vs = self._sensor['Vs']
        La = self._sensor['La']
        Fsa = self._sensor['PRF']  # sampling rate in Azimuth dimension
        Fsr = self._sensor['Fs']  # sampling rate in range dimension
        Tp = self._sensor['Tp']  # Pulse repetition period
        Fc = self._sensor['Fc']
        Wl = self._sensor['Wl']
        Kr = self._sensor['Kr']
        La = self._sensor['La']

        Rbc = self._acquisition['Rbc']
        Rb0 = self._acquisition['Rb0']
        Rsc = self._acquisition['Rsc']
        Rs0 = self._acquisition['Rs0']
        Rbc = self._acquisition['Rbc']
        Rsc = self._acquisition['Rsc']
        Rnear = self._acquisition['Rnear']
        Rfar = self._acquisition['Rfar']

        PC = self._acquisition['PlatCenter']
        SC = self._acquisition['SceneCenter']
        BC = self._acquisition['BeamCenter']
        SA = self._acquisition['SceneArea']
        BA = self._acquisition['BeamArea']
        ES = self._acquisition['EchoSize']
        As = self._acquisition['As']
        Ar = self._acquisition['Ar']
        Ad = self._acquisition['Ad']
        Be = self._acquisition['Be']
        Ai = self._acquisition['Ai']

        if GM == 'BG':
            Xc = BC[0]
            Yc = BC[1]
            t0 = 2 * Rbc / C
            R0 = Rb0
        if GM == 'SG':
            t0 = 2 * Rsc / C
            Xc = SC[0]
            Yc = SC[1]
            R0 = Rs0

        Lsar = self._sensor['Wl'] * Rnear / La  # Rb0, Rbc, R?
        # Ka = (2.0 * Vr**2) / (Wl * Rs0)
        Ka = (-2.0 * Vr**2 * np.cos(Ar)**3) / (Wl * Rnear)
        Tsar = Lsar / Vr
        Ba = np.abs(Ka * Tsar)

        if self._sensor['PRF'] is None:
            PRF = (1.25 * Ba)
        else:
            PRF = self._sensor['PRF']

        Fsa = PRF
        if Fsa / Ba < 1.1 or Fsa / Ba > 2.0:
            logging.warning(
                "~~~Sampling rate should be in range [1.1, 2.0]*Ba, \r\n   Fsa %f Ba %f!" % (Fsa, Ba))

        PRT = 1.0 / PRF  # azimuth sampling
        Tsa = 1.0 / PRF

        if self._sensor['Fs'] is None:
            Fs = (1.905 * self._sensor['B'])
        else:
            Fs = self._sensor['Fs']

        Fsr = Fs
        Tsr = 1.0 / Fsr

        Na, Nr = ES

        Ta = Na * 1.0 / Fsa
        ta = np.linspace(-Ta / 2.0, Ta / 2.0, Na)
        fa = np.linspace(-Fsa / 2.0, Fsa / 2.0, Na)

        tnear = Rnear / C
        tfar = Rfar / C
        tstart = 2.0 * tnear
        # tend = 2.0 * tfar + Tp
        tend = 2.0 * tfar

        Tr = tend - tstart
        if abs(Nr - Tr * Fsr) > 1:
            Be = compute_range_beamwidth(Nr, Fsr, H, Ad, Tp)
            print(Tr, Nr, Fsr, Be*180/PI)
            logging.error("~~~Nr should be Tr×Fsr= % f×% f= % f\r\n\
                          or Fsr should be Nr÷Tr= % f\\% f= % f\r\n\
                          or Be should be Be= % f degree!" %
                          (Tr, Fsr, Tr * Fsr, Nr, Tr, Nr / Tr, Be * 180. / PI))
            raise ValueError("Nr ≠ Tr × Fsr! %f ≠ %f × %f = %f" %
                             (Nr, Tr, Fsr, Tr * Fsr))

        tr = np.linspace(tstart, tend, Nr)
        # tr = np.linspace(-Tr / 2.0, Tr / 2.0, Nr) + t0
        fr = np.linspace(-Fsr / 2.0, Fsr / 2.0, Nr)

        # tac = -Yc / Vg
        # tac = -R0 * np.tan(As) / Vg
        tac = -R0 * np.tan(Ar) / Vr

        # both are ok, equal
        fadc = 2.0 * Vr * np.sin(Ar) / Wl
        # fadc = 2.0 * Vs * np.sin(As) / Wl

        Bdop = 0.886 * (2 * Vs * np.cos(As) / La)

        xmin, xmax, ymin, ymax = SA + [Xc, Xc, Yc, Yc]

        if 1.0 / Fsa - Tp < Tr:
            logging.info(
                "r~~~Sampling rate should be lower to avoid range ambiguity \r\n   \
                (1.0 ÷ Fsa - Tp = 1.0 ÷ %f - %f > Tr = %f" % (Fsa, Tp, Tr))

        self._sensor['PRF'] = PRF
        self._sensor['Fs'] = Fs

        FPa = cr_footprint(Wl, H, La, Ad)
        # FPr = ar_footprint(Wl, H, Lr, Ad)
        FPr = SA[1] - SA[0]
        BWa = azimuth_beamwidth(Wl, La)

        PRFmin = 2.0 * V / H
        PRFmax = C / (2.0 * FPa * np.sin(Ad))

        if Lsar > FPa:
            logging.warning(
                r"~~~The synthetic aperture length Lsar=%s is large than \r\n   \
                the cross range footprint size Rcr=%s which maks a point outside the beam footprint." % (Lsar, FPa))
        if PRF < PRFmin or PRF > PRFmax:
            logging.warning(r"~~~To avoid grating lobe issues, PRF=%s should in [%s, %s]."
                            % (PRF, PRFmin, PRFmax))
        param = dict()
        param['GeometryMode'] = GM  # geometry mode: beam/scene
        param['Rb0'] = Rb0  # beam center distance
        param['Rbc'] = Rbc  # beam center distance
        param['Tp'] = Tp  # Pulse repetition period
        param['PRT'] = PRT  # azimuth
        param['PRF'] = PRF  # azimuth
        param['Fsa'] = Fsa  # azimuth, Fsa = PRF
        param['Fs'] = Fs  # range
        param['Fsr'] = Fsr  # range, Fsr = Fs
        param['Na'] = Na  # azimuth
        param['Nr'] = Nr  # range
        param['Ka'] = Ka  # azimuth
        param['Kr'] = Kr  # range
        param['xmin'] = xmin
        param['xmax'] = xmax
        param['ymin'] = ymin
        param['ymax'] = ymax
        param['Rnear'] = Rnear
        param['Rfar'] = Rfar
        param['tnear'] = tnear
        param['tfar'] = tfar
        param['ta'] = ta  # time array in azimuth
        param['fa'] = fa  # freq array in azimuth
        param['tr'] = tr  # time array in range
        param['fr'] = fr  # freq array in range
        param['Tsa'] = Tsa  # azimuth sampling period
        param['Tsr'] = Tsr  # range sampling period
        param['Xc'] = Xc  # X scene center
        param['Yc'] = Yc  # Y scene center
        param['Rsc'] = Rsc  # R scene center
        param['Rs0'] = Rs0  # R min scene center
        param['Ad'] = Ad  # depression angle
        param['As'] = As  # squint angle
        param['Ar'] = Ar  # squint angle
        param['Be'] = Be  # antenna elevation beamwidth
        param['Ai'] = Ai  # incidence angle
        param['DA'] = La / 2.0  # low squint SAR
        # slant range resolution
        param['DR'] = C / (2.0 * self._sensor['B'])
        # ground range resolution
        param['DY'] = param['DA']  # low squint SAR
        param['DX'] = param['DR'] / (np.sin(param['Ai']) + EPS)
        param['FPa'] = FPa
        param['FPr'] = FPr
        param['BWa'] = BWa
        param['Tr'] = Tr  # range sampling times
        param['Ta'] = Ta  # azimuth sampling times
        param['t0'] = t0
        param['tac'] = tac
        param['fadc'] = fadc
        param['Bdop'] = Bdop
        param['Lsar'] = Lsar
        param['Tsar'] = Tsar
        param['Nsar'] = int(Tsar * Fsa)
        param['tstart'] = tstart
        param['tend'] = tend
        self._params = param
        logging.info('---Done!')

        return self._params

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value):
        logging.info("---Check and set sub area selection...")
        SA = self._acquisition['SceneArea']
        SC = self._acquisition['SceneCenter']
        BC = self._acquisition['BeamCenter']
        ES = self._acquisition['EchoSize']
        Ad = self._acquisition['Ad']
        As = self._acquisition['As']
        Ar = self._acquisition['Ar']
        Fsr = self._params['Fsr']
        Fsa = self._params['Fsa']
        Tsa = self._params['Tsa']
        Tsr = self._params['Tsr']
        Na = self._params['Na']
        Nr = self._params['Nr']
        Rnear = self._params['Rnear']
        Rfar = self._params['Rfar']
        FPr = self._params['FPr']
        H = self._sensor['H']
        Vr = self._sensor['Vr']
        Tp = self._sensor['Tp']
        Wl = self._sensor['Wl']
        La = self._sensor['La']
        GM = self._params['GeometryMode']
        Lsar = self._params['Lsar']

        if value is None:
            SubSA = SA
            SubES = ES
            SubEA = [0, 0]
        else:
            SubSA = value['SubSceneArea']
            SubES = value['SubEchoSize']
            SubEA = value['SubEchoAnchor']

        SubNa, SubNr = SubES
        # SubRnear = SubEA[1] * ((Rfar - Rnear) / float(Nr)) + Rnear
        # SubRfar = (SubEA[1] + SubNr) * ((Rfar - Rnear) / float(Nr)) + Rnear
        SubRnear = iprs.min_slant_range(Fsr, SubEA[1], Rnear)
        SubRfar = iprs.min_slant_range(Fsr, SubEA[1] + SubES[1], Rnear)

        Anear, Afar = (np.arccos(H / SubRnear), np.arccos(H / SubRfar))
        SubFPr = float(SubNr * FPr) / Nr
        SubBe = np.arccos((SubRnear**2 + SubRfar**2 - SubFPr**2) / (2. * SubRnear * SubRfar))
        SubAd = PI / 2. - Anear - SubBe / 2.
        # SubBe = compute_range_beamwidth(SubNr, Fsr, H, SubAd, Tp)

        SubTa = SubNa * Tsa
        taSub = np.linspace(-SubTa / 2.0, SubTa / 2.0, SubNa)
        faSub = np.linspace(-Fsa / 2.0, Fsa / 2.0, SubNa)

        SubRsc = 0.5 * np.sqrt(2. * SubRfar**2 + 2. * SubRnear**2 - SubFPr**2 + EPS)
        SubRs0 = SubRsc * np.cos(Ar)

        SubYsc = SubRsc * np.sin(Ar)
        SubXsc = np.sqrt(np.abs(SubRs0**2 - H**2))
        SubSC = [SubXsc, SubYsc, 0.0]

        SubRbc = H / (np.sin(Ad) + EPS)
        SubRb0 = SubRbc * np.cos(Ar)

        SubYbc = SubRbc * np.sin(Ar)
        SubXbc = np.sqrt(np.abs(SubRb0**2 - H**2))
        SubBC = [SubXbc, SubYbc, 0.0]

        SubYnear = SubRnear * np.sin(Ar)
        SubYfar = SubRfar * np.sin(Ar)
        SubXnear = np.sqrt((SubRnear ** 2 - H**2) - SubYnear ** 2 + EPS)
        SubXfar = np.sqrt((SubRfar ** 2 - H**2) - SubYfar ** 2 + EPS)
        SubSA = [SubXnear - SubXsc, SubXfar - SubXsc, -SubTa * Vr / 2.0, SubTa * Vr / 2.0]

        SubFPr0 = H / np.tan(Ad + SubBe / 2.) - H / np.tan(Ad)
        SubFPr1 = H / np.tan(Ad - SubBe / 2.) - H / np.tan(Ad)
        SubBA = [SubFPr0, SubFPr1, -SubTa * Vr / 2.0, SubTa * Vr / 2.0]

        tnearSub = SubRnear / C
        tfarSub = SubRfar / C
        tstartSub = 2.0 * tnearSub
        tendSub = 2.0 * tfarSub
        # tendSub = 2.0 * tfarSub + Tp

        SubTr = tendSub - tstartSub

        if GM == 'BG':
            Xc = SubBC[0]
            Yc = SubBC[1]
            SubR0 = SubRb0
            t0Sub = 2 * SubRbc / C
            trSub = np.linspace(tstartSub, tendSub, SubNr)
            # trSub = np.linspace(-SubTr / 2.0, SubTr / 2.0, SubNr) + t0Sub
            xminSub, xmaxSub, yminSub, ymaxSub = np.array(SubBA) + np.array([Xc, Xc, Yc, Yc])
        if GM == 'SG':
            Xc = SubSC[0]
            Yc = SubSC[1]
            SubR0 = SubRs0
            t0Sub = 2 * SubRsc / C
            trSub = np.linspace(tstartSub, tendSub, SubNr)
            # trSub = np.linspace(-SubTr / 2.0, SubTr / 2.0, SubNr) + t0Sub
            xminSub, xmaxSub, yminSub, ymaxSub = np.array(SubSA) + np.array([Xc, Xc, Yc, Yc])

        frSub = np.linspace(-Fsr / 2.0, Fsr / 2.0, SubNr)

        SubKa = (-2.0 * Vr**2 * np.cos(Ar)**3) / (Wl * SubRnear)
        SubLsar = Wl * SubRnear / La

        SubTsar = SubLsar / Vr
        SubBa = np.abs(SubKa * SubTsar)

        SubFPa = self._params['FPa']
        SubFPr = SubSA[1] - SubSA[0]

        self._selection = dict()
        self._selection['taSub'] = taSub
        self._selection['faSub'] = faSub
        self._selection['trSub'] = trSub
        self._selection['frSub'] = frSub
        self._selection['SubNa'] = SubNa
        self._selection['SubNr'] = SubNr
        self._selection['SubTa'] = SubTa
        self._selection['SubTr'] = SubTr
        self._selection['tnearSub'] = tnearSub
        self._selection['tfarSub'] = tfarSub
        self._selection['tstartSub'] = tstartSub
        self._selection['tendSub'] = tendSub
        self._selection['SubRnear'] = SubRnear
        self._selection['SubRfar'] = SubRfar
        self._selection['SubSceneArea'] = SubSA
        self._selection['SubBeamArea'] = SubBA
        self._selection['SubSceneCenter'] = SubSC
        self._selection['SubBeamCenter'] = SubBC
        self._selection['SubEchoAnchor'] = SubEA
        self._selection['SubEchoSize'] = SubES
        self._selection['SubFPa'] = SubFPa
        self._selection['SubFPr'] = SubFPr
        self._selection['SubRsc'] = SubRsc
        self._selection['SubRs0'] = SubRs0
        self._selection['SubRbc'] = SubRbc
        self._selection['SubRb0'] = SubRb0
        self._selection['xminSub'] = xminSub
        self._selection['xmaxSub'] = xmaxSub
        self._selection['yminSub'] = yminSub
        self._selection['ymaxSub'] = ymaxSub
        self._selection['SubBe'] = SubBe
        self._selection['SubAd'] = SubAd
        self._selection['SubKa'] = SubKa
        self._selection['SubBa'] = SubBa
        self._selection['SubTsar'] = SubTsar
        self._selection['SubLsar'] = SubLsar

        self._params['taSub'] = taSub
        self._params['faSub'] = faSub
        self._params['trSub'] = trSub
        self._params['frSub'] = frSub
        self._params['SubNa'] = SubNa
        self._params['SubNr'] = SubNr
        self._params['SubTa'] = SubTa
        self._params['SubTr'] = SubTr
        self._params['tnearSub'] = tnearSub
        self._params['tfarSub'] = tfarSub
        self._params['tstartSub'] = tstartSub
        self._params['tendSub'] = tendSub
        self._params['SubRnear'] = SubRnear
        self._params['SubRfar'] = SubRfar
        self._params['SubSceneArea'] = SubSA
        self._params['SubBeamArea'] = SubBA
        self._params['SubSceneCenter'] = SubSC
        self._params['SubBeamCenter'] = SubBC
        self._params['SubEchoAnchor'] = SubEA
        self._params['SubEchoSize'] = SubES
        self._params['SubFPa'] = SubFPa
        self._params['SubFPr'] = SubFPr
        self._params['SubRsc'] = SubRsc
        self._params['SubRs0'] = SubRs0
        self._params['SubRbc'] = SubRbc
        self._params['SubRb0'] = SubRb0
        self._params['xminSub'] = xminSub
        self._params['xmaxSub'] = xmaxSub
        self._params['yminSub'] = yminSub
        self._params['ymaxSub'] = ymaxSub
        self._params['SubBe'] = SubBe
        self._params['SubAd'] = SubAd
        self._params['SubKa'] = SubKa
        self._params['SubBa'] = SubBa
        self._params['SubTsar'] = SubTsar
        self._params['SubLsar'] = SubLsar
        logging.info('---Done!')

    def printsp(self, verbose=False):
        print("===============SAR platform: ", self._name, "================")
        print("--------------------------sensor-----------------------------")
        for key in sorted(self._sensor):
            print(key, self._sensor[key])

        print("-----------------------acquisition---------------------------")
        for key in sorted(self._acquisition):
            print(key, self._acquisition[key])

        print("--------------------------params-----------------------------")
        if verbose:
            print(self._params)
        else:
            for key in sorted(self._params):
                value = self._params[key]
                if type(value) in [list, tuple, np.ndarray] and len(value) > 10:
                    print("shape of " + key + ": ", value.shape)
                else:
                    print(key, self._params[key])

        print("-------------------------selection---------------------------")
        for key in sorted(self._selection):
            value = self._selection[key]
            if type(value) in [list, tuple, np.ndarray] and len(value) > 10:
                print("shape of " + key + ": ", value.shape)
            else:
                print(key, self._selection[key])
        print("=============================================================")

