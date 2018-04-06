__author__ = 'Miguel Molero'

import sys
import numpy as np
import matplotlib.pyplot as plt
from  scipy.misc import imsave
from scipy.io import savemat

from SimNDT.gui.Warnings import WarningParms


class SnapShots:
    def __init__(self, Enable=False, Extension='.png', Step=200, Filename=None, dB=60, Color=0, enableFields=False):

        self.IsEnable = Enable
        self.Extension = Extension
        self.Step = Step
        self.Filename = Filename
        self.DB = dB
        self.Color = Color
        self.enableFields = enableFields

    def save_fields(self, Vx, Vy, n):

        dict = {}
        dict['Vx'] = Vx
        dict['Vy'] = Vy

        FILE = self.Filename + str(int(n / self.Step)) + ".mat"
        savemat(FILE, dict)

    def save_fig(self, SV, n, idx=None):

        SV += self.DB
        ind = np.nonzero(SV < 0)
        SV[ind] = 0
        SV /= np.max(SV)

        if self.Color == 0:
            cmap = plt.get_cmap('jet')
        elif self.Color == 1:
            cmap = plt.get_cmap('gray')

        try:
            _resize = False
            M, N = np.shape(SV)
            if M >= 2000:
                _resize = True
            if N >= 2000:
                _resize = True

            if _resize:
                SVV = SV[::3, ::3]
                rgba_img = cmap(SVV)
            else:
                SVV = SV[::2, ::2]
                rgba_img = cmap(SVV)

            rgb_img = np.delete(rgba_img, 3, 2)

            if idx is not None:
                FILE = self.Filename + "_insp%d_" % idx + str(int(n / self.Step)) + self.Extension
            else:
                FILE = self.Filename + str(int(n / self.Step)) + self.Extension
            imsave(FILE, rgb_img)

        except:
            msgBox = WarningParms("Too larger Snapshots Size!!!!!!!!")
            if msgBox.exec_():
                sys.exit()
