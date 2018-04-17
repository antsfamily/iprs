#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-19 00:03:32
# @Author  : Yan Liu & Zhi Liu (zhiliu.mind@gmail.com)
# @Link    : http://iridescent.ink
# @Version : $1.0$

import iprs


def gendata(sarplat, targets):

    Sr, ta, tr = iprs.tgs2rawdata(sarplat, targets, verbose=True)

    # visualize
    iprs.show_amplitude_phase(Sr)

    # do RD imaging
    # img, ta, tr = imcls.RangeDoppler(Sr, sarplat)
    # vis.show_img(img)

    img, ta, tr = iprs.omega_k(Sr, sarplat, verbose=True)

    sardata = iprs.SarData()

    sardata.rawdata = Sr
    sardata.image = img
    sardata.name = " "

    return sardata


if __name__ == '__main__':

    sarplat = iprs.SarPlat()
    # print(SR)
    sarplat.name = 'DIY'
    sarplat.sensor = iprs.SENSORS[sarplat.name]
    sarplat.acquisition = iprs.ACQUISITION['DIY3']
    sarplat.params = None
    sarplat.printsp()

    SC = sarplat.acquisition['SceneCenter']
    Xc = SC[0]
    Yc = SC[1]

    targets = [
        [Xc + 100, Yc + 100, 0, 0, 0, 0, 1],
        [Xc - 150, Yc - 50, 0, 0, 0, 0, 1],
        [Xc, Yc, 0, 0, 0, 0, 1],
        [Xc + 200, Yc, 0, 0, 0, 0, 1],
    ]
    print(targets)

    outfolder = '../data/sar/'

    filename = sarplat.name + '.npy'

    filepath = outfolder + filename

    sardata = gendata(sarplat, targets)

    sardata.store(sarplat, filepath)

    sardata, sarplat = sardata.read(filepath)

    iprs.show_response(sardata['img'])
