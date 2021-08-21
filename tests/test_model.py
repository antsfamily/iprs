#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-26 23:34:49
# @Author  : Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$
import sys
import iprs
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt


sensor_name = 'DIY8'
acquis_name = 'DIY8'

sarplat8 = iprs.SarPlat()
sarplat8.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat8.sensor = iprs.SENSORS[sensor_name]
sarplat8.acquisition = iprs.ACQUISITION[acquis_name]
sarplat8.params = None
sarplat8.printsp()


imgfilepath = '../data/fig/radarsat/Tokyoradarsat004_128.tif'
# imgfilepath = '../data/fig/radarsat/Tokyoradarsat004_256.tif'

imgfilepath = '/mnt/d/ws/dataset/samples5000/000011.png'
# imgfilepath = '/mnt/d/ws/dataset/samples1024/000011.png'

grayimg = iprs.imread(imgfilepath)
[H, W] = grayimg.shape

bgv = 0
Sr08, targets = iprs.img2rawdata(
    sarplat8, grayimg, bg=bgv, noise=None, verbose=True)

print(Sr08.shape)

sensor_name = 'DIY7'
acquis_name = 'DIY7'
sarplat7 = iprs.SarPlat()
sarplat7.name = "sensor=" + sensor_name + "_acquisition=" + acquis_name
sarplat7.sensor = iprs.SENSORS[sensor_name]
sarplat7.acquisition = iprs.ACQUISITION[acquis_name]
sarplat7.params = None
sarplat7.printsp()
Sr7, targets = iprs.img2rawdata(
    sarplat7, grayimg, bg=bgv, noise=None, verbose=True)
# Y --> N Nsa Nsr
Sr07, mask = iprs.sparse_observation(
    np.array([Sr7]), way=0, mode='uniformly', rsample=(0.25, 0.25))
# Y = X

# print(np.sum(Sr-Sr0))

Sr08_img, ta, tr = iprs.range_doppler(Sr08, sarplat8, verbose=False)
Sr07_img, ta, tr = iprs.range_doppler(Sr07[0], sarplat8, verbose=False)
Sr7_img, ta, tr = iprs.range_doppler(Sr7, sarplat7, verbose=False)

# before RD imaging

print(Sr08.shape)
print(Sr07[0].shape)
print(grayimg.shape)
plt.figure()
plt.subplot(221)
plt.imshow(np.abs(Sr08))
plt.title('sim low-resolution')
plt.subplot(222)
plt.imshow(np.abs(Sr07[0]))
plt.title('sample low-resolution')
plt.subplot(223)
plt.imshow(np.abs(Sr7))
plt.title('high-resolution')
plt.subplot(224)
plt.imshow(grayimg)
plt.title('intensity')
plt.show()


# after RD imaging

print(Sr08.shape)
print(Sr07[0].shape)
print(grayimg.shape)
plt.figure()
plt.subplot(221)
plt.imshow(np.abs(Sr08_img))
plt.title('sim low-resolution')
plt.subplot(222)
plt.imshow(np.abs(Sr07_img))
plt.title('sample low-resolution')
plt.subplot(223)
plt.imshow(Sr7_img)
plt.title('intensity')
plt.subplot(224)
plt.imshow(grayimg)
plt.title('intensity')
plt.show()

# Sr = Sr0

# A = iprs.sarmodel(sarplat, mod='vec')

# invA = np.linalg.pinv(A)

# print(A.shape, invA.shape)

fileA = 'sensor' + sensor_name + "acquis" + acquis_name + 'pkl'
# f = open(fileA, 'wb')
# pkl.dump(A, f, 0)
# pkl.dump(invA, f, 0)
# f.close()

f = open(fileA, 'rb')
# for python2
if sys.version_info < (3, 1):
    A = pkl.load(f)
    invA = pkl.load(f)
# for python3
else:
    A = pkl.load(f, encoding='latin1')
    invA = pkl.load(f, encoding='latin1')
f.close()
print(A.shape, invA.shape)

# SNR = 30
# imgns = iprs.imnoise(grayimg, SNR=SNR)

# img = grayimg.flatten()
# print(img.shape)
# Sr = np.matmul(A, img)
# print(Sr.shape)

Sr = Sr.flatten()


rimgpinv = np.matmul(invA, Sr)
print(rimgpinv.shape)
Na = sarplat.params['Na']
Nr = sarplat.params['Nr']

rimgpinv = np.reshape(rimgpinv, (H, W))
print(rimgpinv.shape)

iprs.show_sarimage(rimgpinv, sarplat)


Sr = np.reshape(Sr, (Na, Nr))

iprs.show_amplitude_phase(Sr)

Sr_img, ta, tr = iprs.range_doppler(Sr, sarplat, verbose=False)

# axismod = 'Image'
# axismod = 'SceneAbsolute'
axismod = 'SceneRelative'
title = 'Reconstructed Image using RD'

iprs.show_sarimage(
    Sr_img, sarplat, axismod=axismod, title=title, aspect=None, outfile=None)
