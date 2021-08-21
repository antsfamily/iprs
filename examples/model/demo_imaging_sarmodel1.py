#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 10:14:12
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs
import numpy as np
import matplotlib.pyplot as plt


imagingMethod = 'RangeDoppler'
# imagingMethod = 'OmegaK'
# imagingMethod = 'ChirpScaling'
# imagingMethod = 'Regualrization'
#imagingMethod = 'CompressiveSensing'

cmap = 'gray'
cmap = None
cmap = 'viridis'
isregen = True
# isregen = False


sarfile = '/mnt/d/DataSets/zhi/SAR/MSTAR/'
sarfile = '../data/sar/sensor=DIY4_acquisition=DIY4_640x640_disc_wgnSNR5_2.pkl'
# sarfile = '/mnt/d/DataSets/zhi/SAR/MiniSAR/sensor=DIY4_acquisition=DIY4_gaoxiong001.pkl'
sarfile = '/mnt/d/DataSets/zhi/SAR/misc/MiniSAR128/sensor=DIY8_acquisition=DIY8_MiniSAR_128nScenes100.pkl'
# sarfile = '/mnt/d/DataSets/zhi/SAR/misc/MiniSAR128/sensor=DIY7_acquisition=DIY7_MiniSAR_128nScenes30.pkl'

# sarfile = '/mnt/d/ws/github/sci/radar/iprs/data/sar/MSTAR/sensor=DIY4_acquisition=DIY4_MSTAR_HB06167.pkl'

sarfile = '/mnt/d/DataSets/zhi/SAR/SIMSAR/SIMSAR/data/sensor=DIY7_acquisition=DIY7_SIMSARnScenes512.pkl'
sarfile = '/mnt/d/DataSets/zhi/SAR/SIMSAR/SIMSAR/data/sensor=DIY8_acquisition=DIY8_SIMSARnScenes512.pkl'

sardata, sarplat = iprs.sarread(sarfile)
print(sardata.name)

sarplat.printsp()

sensor_name = 'DIY8'
acquis_name = 'DIY8'


fileA = '../../data/model/' + 'sensor' + \
    sensor_name + "acquis" + acquis_name + '.pkl'


if isregen:
    A = iprs.sarmodel(sarplat, mod='2D1')
    invA = np.linalg.pinv(A)
    AH = A.conj()
    AH = AH.transpose()
    print("A.shape, invA.shape: ", A.shape, invA.shape)

    print("===saving mapping matrix...")
    iprs.save_sarmodel(A=A, invA=invA, AH=AH, datafile=fileA)

# ===load mapping matrix
print("===loading mapping matrix...")

A, invA, AH = iprs.load_sarmodel(fileA, mod='AinvAAH')
print("A.shape, invA.shape: ", A.shape, invA.shape)


# ===========================for imaging tesing

SNR = 30


for s, sI in zip(sardata.rawdata, sardata.image):

    # s = iprs.matnoise(s, SNR=SNR)
    SA = sarplat.acquisition['SceneArea']
    H = SA[1] - SA[0]
    W = SA[3] - SA[2]
    # ---------reconstruct image by g=inv(A)*s
    print("reconstruct image by g=inv(A)*s")

    # invA = np.matmul(np.linalg.inv(np.matmul(AH, A)), AH)
    IpinvASsim = np.matmul(invA, s.flatten())
    IpinvASsim = np.reshape(IpinvASsim, (H, W))
    print("IpinvASsim.shape:", IpinvASsim.shape)

    # ---------reconstruct image by g=A^H*s
    print("reconstruct image by g=A^H*s")
    IAHSsim = np.matmul(AH, s.flatten())
    IAHSsim = np.reshape(IAHSsim, (H, W))
    print("IAHSsim.shape: ", IAHSsim.shape)

    # ----------------reconstruct image by range doppler
    print("===imaging from echo signal simulated")
    RDASsim = iprs.rda_adv(
        s, sarplat, usezpa=True, usesrc=True, usermc=False, verbose=True)

    # ===========================display diff


    plt.figure()
    plt.subplot(221)
    plt.imshow(sI)
    plt.xlabel('Range')
    plt.ylabel('Amplitude')
    plt.title('Intensity')

    plt.subplot(222)
    plt.imshow(np.abs(IpinvASsim))
    plt.xlabel('Range')
    plt.ylabel('Amplitude')
    plt.title('g=A^+s, s:simulated')

    plt.subplot(223)
    plt.imshow(np.abs(IAHSsim))
    plt.xlabel('Range')
    plt.ylabel('Amplitude')
    plt.title('g=A^Hs, s:simulated')

    plt.subplot(224)
    plt.imshow(np.abs(RDASsim))
    plt.xlabel('Range')
    plt.ylabel('Amplitude')
    plt.title('RDA, s:simulated')

    plt.tight_layout()
    plt.show()
