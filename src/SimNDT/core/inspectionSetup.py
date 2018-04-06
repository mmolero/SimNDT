#!/usr/bin/env python
# encoding: utf-8
"""
inspection.py

Created by Miguel Molero on 2013-09-26.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy as np


def setEmisor(Theta, Size, x2, y2, X0, Y0):
    Ntheta = np.size(Theta, 0)
    NXL = int(2.0 * Size)

    xL = np.zeros((NXL,), dtype=np.float32)
    yL = np.zeros((NXL,), dtype=np.float32)

    for m in range(0, Ntheta):

        if np.abs(np.cos(Theta[m])) < 1e-5:
            yL = np.arange(y2[m] - Size, y2[m] + Size)
            xL[:] = x2[m] * np.ones((NXL,), dtype=np.float32)

        elif np.abs(np.cos(Theta[m])) == 1:
            xL[:] = np.arange(x2[m] - Size, x2[m] + Size)
            yL[:] = y2[m] - ((x2[m] - X0) / (y2[m] - Y0)) * (xL[:] - x2[m])

        else:
            xL[:] = np.linspace(x2[m] - (Size * np.abs(np.cos(Theta[m]))), x2[m] + (Size * np.abs(np.cos(Theta[m]))),
                                num=NXL, endpoint=True)
            yL = y2[m] - ((x2[m] - X0) / (y2[m] - Y0)) * (xL[0:NXL] - x2[m])

        if m == 0:
            XL = np.zeros((np.size(xL, 0), Ntheta), dtype=np.float32)
            YL = np.zeros((np.size(xL, 0), Ntheta), dtype=np.float32)

        XL[:, m] = np.int32((xL[0:np.size(xL, 0)]))
        YL[:, m] = np.int32((yL[0:np.size(xL, 0)]))

    return XL, YL


def centerOffset(XL, YL, Theta, Scenario, transducer, Ratio):
    Ntheta = np.size(Theta, 0)
    if transducer.Location == "Top":
        YL += np.int32(transducer.CenterOffset * Scenario.Pixel_mm * Ratio)
    elif transducer.Location == "Left":
        XL += np.int32(transducer.CenterOffset * Scenario.Pixel_mm * Ratio)

    IR = np.zeros((Ntheta, Ntheta), dtype=np.float32)
    B = range(0, Ntheta)
    IR[:, 0] = np.int32(B[:])

    for i in range(1, Ntheta):
        B = np.roll(B, -1)
        IR[:, i] = np.int32(B)

    return XL, YL, IR


def borderOffset(XL, YL, Scenario, transducer, Ratio):
    if transducer.Location == "Top":
        XL[:, 0] += (np.int32(transducer.BorderOffset * Scenario.Pixel_mm * Ratio))
        XL[:, 1] -= (np.int32(transducer.BorderOffset * Scenario.Pixel_mm * Ratio))
    elif transducer.Location == "Left":
        YL[:, 0] += (np.int32(transducer.BorderOffset * Scenario.Pixel_mm * Ratio))
        YL[:, 1] -= (np.int32(transducer.BorderOffset * Scenario.Pixel_mm * Ratio))

    return XL, YL


def flip(XL):
    return np.fliplr(XL)


def getReceivers(XL, YL, IR, T, Field):
    ReceptorX = (XL)
    ReceptorY = (YL)
    M, N = np.shape(ReceptorX)
    temp = np.zeros((M, N - 1), dtype=np.float32)
    for mm in range(0, M):
        for ir in range(0, N - 1):
            temp[mm, ir] = T[int(ReceptorX[mm, int(IR[0, ir + 1])]), int(ReceptorY[mm, int(IR[0, ir + 1])])]
    if Field:
        return temp.transpose()
    else:
        return np.mean(temp, 0)
