import iprs
import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt


# matfile = '../data/mat/alphasDCT.mat'
# matfile = '/home/liu/Desktop/Data/ws/Matlab/Chapter3/alphasDCTCR4.mat'
matfile = '/home/liu/Desktop/Data/ws/Matlab/Chapter3/alphasNoneCR8.mat'
# matfile = '/home/liu/Desktop/Data/ws/Matlab/Chapter3/alphas.mat'
# matfile = '/home/liu/Desktop/Data/ws/Matlab/Chapter3/alphasMinSAR_NoneCR8.mat'

data = scio.loadmat(matfile, struct_as_record=True)

recs = data['alphas']


datafile = '/mnt/d/DataSets/zhi/SAR/noisy/sensor=DIY4_acquisition=DIY4_center_disc_Scene0.pkl'

sardata, sarplat = iprs.sarread(datafile)

sarplat.printsp

refs = sardata.rawdata

tgregions = [[209, 232, 245, 289]]
# tgregions = [[133, 116, 335, 407]]

# print(recs[0])

for rec, ref in zip(recs, refs):
    # plt.imshow(np.abs(rec))
    # plt.show()
    # TBR = iprs.tbr(rec, ref, TH=None)
    TBR = iprs.tbr2(rec, tgregions=tgregions)
    MSE = iprs.mse(rec, ref)
    print(TBR, MSE)

