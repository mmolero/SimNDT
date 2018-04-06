#!/usr/bin/env python
# encoding: utf-8
"""
materialLibrary.py

Created by Miguel Molero on 2013-09-10.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy as np

from collections import OrderedDict


def CC(x):
    rho, VL, VT, = x[1]
    lam = rho * (VL ** 2 - 2 * (VT ** 2))
    mu = rho * (VT ** 2)
    m = list()
    m.append(x[0])
    m.append(np.array((rho, lam, mu, VL, VT)))
    return m


def getMaterialLibrary():
    MaterialList = list()

    MaterialList.append(CC(['air', (1.24, 344, 1e-30)]))
    MaterialList.append(CC(['aggregates', (2600, 5751, 3282)]))
    MaterialList.append(CC(['aluminium', (2720, 6320, 3772)]))
    MaterialList.append(CC(['clay', (2600, 3400, 1600)]))
    MaterialList.append(CC(['cement paste', (2300, 4100, 2296)]))
    MaterialList.append(CC(['concrete', (2500, 4500, 2696)]))
    MaterialList.append(CC(['epoxy', (1210, 2680, 1150)]))
    MaterialList.append(CC(['fat', (920, 1446, 1e-30)]))
    MaterialList.append(CC(['glass', (2510, 5560, 1620)]))
    MaterialList.append(CC(['ice', (920, 3807, 2005)]))
    MaterialList.append(CC(['lead', (11300, 2210, 860)]))
    MaterialList.append(CC(['limestone', (2700, 5440, 3400)]))
    MaterialList.append(CC(['liver', (1060, 1566, 1e-30)]))
    MaterialList.append(CC(['nylon', (1100, 2600, 1300)]))
    MaterialList.append(CC(['perspex', (1179, 2730, 1430)]))
    MaterialList.append(CC(['PZT-5A', (7750, 4350, 2260)]))
    MaterialList.append(CC(['sand', (2670, 5571, 3532)]))
    MaterialList.append(CC(['sandstone', (2300, 2950, 1620)]))
    MaterialList.append(CC(['steel', (7800, 5850, 3220)]))
    MaterialList.append(CC(['water', (1000, 1480, 1e-30)]))

    return OrderedDict(MaterialList)


if __name__ == '__main__':
    print(getMaterialLibrary().keys())
