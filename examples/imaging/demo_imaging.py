#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np

imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
imagingMethod = 'ChirpScaling'
# imagingMethod = 'Regualrization'
# imagingMethod = 'CompressiveSensing'

cmap = 'gray'
cmap = 'jet'
# cmap = None
cmap = 'viridis'

sarfile = '../../data/sar/image/sensor=RADARSAT1_acquisition=RADARSAT1_Lotus128_16384Tgs.mat'
# sarfile = '../../data/sar/image/sensor=Air3_acquisition=Air3_Lotus128_16384Tgs.mat'
sarfile = '../../data/sar/point/sensor=RADARSAT1_acquisition=RADARSAT1_point5.mat'
sarfile = '../../data/sar/image/sensor=Air1_acquisition=Air1_Lotus128_81920Tgs.mat'


sardata, sarplat = iprs.sarread(sarfile)

sarplat.printsp()
NstartX = int(sarplat.acquisition['EchoSize'][1] / 2. - sarplat.selection['SubEchoSize'][1] / 2.)
NstartY = int(sarplat.acquisition['EchoSize'][0] / 2. - sarplat.selection['SubEchoSize'][0] / 2.)


print(NstartX, NstartY, "+++++++++++++++++++++++++")

# ===for regularization and cs
optim = 'Lasso'
norm = 1

# optim = 'OMP'
# norm = 0

zpadar = None
zpadar = (256, 256)
H, W = (128, 128)
gdshape = (H, W)

Dict = 'DCT'

if imagingMethod is 'Regualrization' or imagingMethod is 'CompressiveSensing':
    print(imagingMethod)
    A = iprs.sarmodel(sarplat, gdshape=gdshape, mod='2D1')

if imagingMethod is 'CompressiveSensing':
    D = iprs.dctdic((H * W, H * W), axis=-1, isnorm=True)

if type(sardata.rawdata) is not list:
    Srs = list([sardata.rawdata])
    SrIs = list([sardata.image])
else:
    Srs = sardata.rawdata
    SrIs = sardata.image

for Sr, SrI in zip(Srs, SrIs):
    Sr = Sr[:, :, 0] + 1j * Sr[:, :, 1]
    print(np.min(np.abs(Sr)), np.max(np.abs(Sr)))
    print(Sr.shape, SrI.shape)
    # Sr = Sr[NstartY:NstartY + sarplat.selection['SubEchoSize'][0], NstartX:NstartX + sarplat.selection['SubEchoSize'][1]]
    # print(NstartY, NstartY + sarplat.selection['SubEchoSize'][0])
    # print(NstartX, NstartX + sarplat.selection['SubEchoSize'][1])
    print(Sr.shape, SrI.shape)

    # visualize
    iprs.show_amplitude_phase(Sr)
    # iprs.show_image(SrI, cmap=cmap)

    if imagingMethod is 'RangeDoppler':
        # SrIr = iprs.rda(Sr, sarplat, verbose=False)
        SrIr = iprs.rda_adv(Sr, sarplat, zpadar=zpadar, usesrc=True,
                            usedpc=True, rcmc=32, verbose=False)
    if imagingMethod is 'OmegaK':
        SrIr, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)
    if imagingMethod is 'ChirpScaling':
        SrIr = iprs.csa_adv(Sr, sarplat, zpadar=zpadar, usesrc=False,
                            rcmc=32, usedpc=True, verbose=False)
    if imagingMethod is "Regualrization":
        SrIr = iprs.regular_sar(s=Sr, A=A, norm=norm, factor=0.001, optim=optim,
                                max_iter=1000, tol=0.001, gdshape=(H, W), verbose=True)
    if imagingMethod is "CompressiveSensing":
        SrIr = iprs.cs1d_sar(s=Sr, A=A, D=D, axis=-1, norm=norm, factor=0.001,
                             optim=optim, max_iter=1000, tol=0.00001, gdshape=(H, W), verbose=True)
    axismod = 'Image'
    # axismod = 'SceneAbsolute'
    # axismod = 'SceneRelative'
    # axismod = 'ddd'
    Title = 'Reconstructed Image using ' + imagingMethod
    # Title = 'Reconstructed Image using omega-k'

    iprs.show_sarimage(SrIr, sarplat, axismod=axismod, title=Title, cmap=cmap, isimgadj=False,
                       aspect=None)
