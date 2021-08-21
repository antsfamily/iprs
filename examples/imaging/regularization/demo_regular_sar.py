#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-12 11:06:13
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt


sensor_name = 'DIY8'
acquis_name = 'DIY8'

# sensor_name = 'DIY7'
# acquis_name = 'DIY9'

sarplat = iprs.SarPlat()
sarplat.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat.sensor = iprs.SENSORS[sensor_name]
sarplat.acquisition = iprs.ACQUISITION[acquis_name]
sarplat.selection = None
sarplat.params = None
sarplat.select()
sarplat.printsp()

Na = sarplat.params['Na']
Nr = sarplat.params['Nr']

# isregen = False
isregen = True

cmap = 'gray'
cmap = None
cmap = 'jet'


imgfilepath = '../../../data/img/points32.png'
# imgfilepath = '../../../data/img/pointsx32.png'
# imgfilepath = '../../../data/img/Lotus32.png'
# imgfilepath = '../../../data/img/ship32.png'
# imgfilepath = '../../../data/img/points128.png'
imgfilepath = '../../../data/img/pointsx128.png'
# imgfilepath = '../../../data/img/Lotus128.png'
# imgfilepath = '../../../data/img/ship128.png'

imgRGB = iprs.imread(imgfilepath)

grayimg = imgRGB[:, :, 0]
print("grayimg.shape: ", grayimg.shape)
[H, W] = grayimg.shape
SNR = 30
imgns = iprs.imnoise(grayimg, SNR=SNR)
img = iprs.scale(imgns, [0.0, 255.0], [0.0, 1.0])
print("img.shape: ", img.shape)

# gdshape = (H * 2, W * 2)
gdshape = (H, W)

bgv = 0
Ssim, targets = iprs.img2rawdata(
    sarplat, img, bg=bgv, noise=None, TH=0.0, gdshape=gdshape, verbose=True)

plt.figure()
plt.subplot(131)
plt.imshow(img)
plt.subplot(132)
plt.imshow(np.abs(Ssim))
plt.subplot(133)
plt.imshow(np.angle(Ssim))
plt.show()
# iprs.show_amplitude_phase(Ssim)

print(Ssim.shape)

fileA = '../../../data/model/' + 'sensor' + \
    sensor_name + "acquis" + acquis_name + '.pkl'


if isregen:
    A = iprs.sarmodel(sarplat, mod='2D1', gdshape=gdshape)
    invA = np.linalg.pinv(A)

    print("A.shape, invA.shape: ", A.shape, invA.shape)

    print("===saving mapping matrix...")
    iprs.save_sarmodel(A=A, invA=invA, datafile=fileA)

# ===load mapping matrix
print("===loading mapping matrix...")

A, invA = iprs.load_sarmodel(fileA, mod='AinvA')
print("A.shape, invA.shape: ", A.shape, invA.shape)


# ---------gen echo by s=Ag
Smodel, img = iprs.sarmodel_genecho(A, img, mod='2D1', gdshape=gdshape)
print("Smodel.shape", Smodel.shape)
Smodel = np.reshape(Smodel, (Na, Nr))

# ===========================for imaging tesing
# ---------reconstruct image by regularization l2
print("reconstruct image by regularization l2")

Il2_Ssim = iprs.regular_sar(s=Ssim, A=A, norm=2, factor=0.01, optim='Ridge',
                            max_iter=1000, tol=0.0001, shape=gdshape, verbose=True)

Il2_Smodel = iprs.regular_sar(s=Smodel, A=A, norm=2, factor=0.01, optim='Ridge',
                              max_iter=1000, tol=0.0001, shape=gdshape, verbose=True)

# ---------reconstruct image by regularization l1
print("reconstruct image by regularization l1")

Il1_Ssim = iprs.regular_sar(s=Ssim, A=A, norm=1, factor=0.01, optim='Lasso',
                            max_iter=1000, tol=0.0001, shape=gdshape, verbose=True)

Il1_Smodel = iprs.regular_sar(s=Smodel, A=A, norm=1, factor=0.01, optim='Lasso',
                              max_iter=1000, tol=0.0001, shape=gdshape, verbose=True)

# ----------------reconstruct image by range doppler
print("reconstruct image by RDA(simulated)")
RDASsim = iprs.rda_adv(
    Ssim, sarplat, usezpa=True, usesrc=True, usermc=False, verbose=True)

print("reconstruct image by RDA(model)")
RDASmodel = iprs.rda_adv(
    Smodel, sarplat, usezpa=True, usesrc=False, usermc=False, verbose=True)

# ===========================display diff

print("error: ||Smodel-Ssim||", np.linalg.norm(Smodel - Ssim, ord=2))
print("error: ||RDASmodel-RDASsim||",
      np.linalg.norm(RDASmodel - RDASsim, ord=2))


plt.figure()
plt.subplot(321)
plt.imshow(np.abs(Il2_Ssim), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('Regularization(l2), s:simulated')

plt.subplot(322)
plt.imshow(np.abs(Il2_Smodel), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('Regularization(l2), s=Ag')

plt.subplot(323)
plt.imshow(np.abs(Il1_Ssim), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('Regularization(l1), s=simulated')

plt.subplot(324)
plt.imshow(np.abs(Il1_Smodel), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('Regularization(l1), s=Ag')

plt.subplot(325)
plt.imshow(np.abs(RDASsim), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('RDA, s:simulated')

plt.subplot(326)
plt.imshow(np.abs(RDASmodel), cmap=cmap)
plt.xlabel('Range')
plt.ylabel('Amplitude')
plt.title('RDA, s=Ag')
plt.tight_layout()
plt.show()
