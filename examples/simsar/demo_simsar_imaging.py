#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs

imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
# imagingMethod = 'ChirpScaling'
# imagingMethod = 'Regualrization'
# imagingMethod = 'CompressiveSensing'

cmap = 'gray'
cmap = None
cmap = 'viridis'

sarfile = '/mnt/d/DataSets/zhi/SAR/SIMSAR/SIMSARv1/sensor=SIMSARv1a_acquisition=SIMSARv1a_000007.pkl'

sardata, sarplat = iprs.sarread(sarfile)
print(sardata.name)

sarplat.printsp()


# ===for regularization and cs
optim = 'Lasso'
norm = 1

# optim = 'OMP'
# norm = 0

H, W = (128, 128)

Dict = 'DCT'

if imagingMethod is 'Regualrization' or imagingMethod is 'CompressiveSensing':
    print(imagingMethod)
    A = iprs.sarmodel(sarplat, mod='2D1')

if imagingMethod is 'CompressiveSensing':
    D = iprs.dctdic((H * W, H * W), axis=-1, isnorm=True)

if type(sardata.rawdata) is not list:
    Srs = list([sardata.rawdata])
    SrIs = list([sardata.image])
else:
    Srs = sardata.rawdata
    SrIs = sardata.image


for Sr, SrI in zip(Srs, SrIs):
    print(Sr.shape, SrI.shape)
    # visualize
    iprs.show_amplitude_phase(Sr)
    iprs.show_image(SrI, cmap=cmap)

    if imagingMethod is 'RangeDoppler':
        # do RD imaging
        # SrIr, ta, tr = iprs.rda(Sr, sarplat, verbose=False)
        SrIr = iprs.rda_adv(
            Sr, sarplat, usezpa=False, usesrc=False, usermc=False, verbose=True)
            # Sr, sarplat, usezpa=True, usesrc=True, usermc=True, verbose=True)
    if imagingMethod is 'OmegaK':
        SrIr, ta, tr = iprs.omega_k(Sr, sarplat, verbose=False)
    if imagingMethod is 'ChirpScaling':
        SrIr = iprs.chirp_scaling(Sr, sarplat, verbose=False)
    if imagingMethod is "Regualrization":
        SrIr = iprs.regular_sar(s=Sr, A=A, norm=norm, factor=0.001, optim=optim,
                                max_iter=1000, tol=0.001, gdshape=(H, W), verbose=True)
    if imagingMethod is "CompressiveSensing":
        SrIr = iprs.cs1d_sar(s=Sr, A=A, D=D, axis=-1, norm=norm, factor=0.001,
                             optim=optim, max_iter=1000, tol=0.00001, gdshape=(H, W), verbose=True)
    # axismod = 'Image'
    # axismod = 'SceneAbsolute'
    axismod = 'SceneRelative'
    # axismod = 'ddd'
    Title = 'Reconstructed Image using ' + imagingMethod
    # Title = 'Reconstructed Image using omega-k'

    iprs.show_sarimage(
        SrIr, sarplat, axismod=axismod, title=Title, cmap=cmap, isimgadj=False,
        aspect=None)
