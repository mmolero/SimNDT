__author__ = 'Miguel Molero'

from SimNDT.graphics.mplWidget import PlotDialog
import numpy as np


class ManagerPlots(object):
    def plotSingleLaunch(self):

        plot = PlotDialog(self)
        sig = self.SimNDT_Receivers.getReceivers()
        Name = self.SimNDT_Inspection.Name

        if Name == "Transmission" or Name == "PulseEcho":
            lenght = np.size(sig)
            self.SimNDT_Simulation.SimulationTime
            time = np.linspace(0, self.SimNDT_Simulation.SimulationTime, lenght) * 1e6

            plot.mpl.ax.plot(time, sig)
            plot.mpl.ax.grid(True, color='gray')
            plot.mpl.ax.set_title("Time Signal", fontsize=10)
            plot.mpl.ax.set_xlabel("Time ($\mu$s)")
            plot.mpl.ax.set_ylabel("Amplitude")
            plot.show()

    def plotLinearScan(self):

        plot = PlotDialog(self)
        sig = self.SimNDT_Receivers.getReceivers()
        Name = self.SimNDT_Inspection.Name

        if Name == "LinearScan":
            lenght, N = np.shape(sig)
            self.SimNDT_Simulation.SimulationTime
            time = self.SimNDT_Simulation.SimulationTime * 1e6

            plot.mpl.ax.imshow(sig, extent=[0, N, time, 0], aspect='auto', interpolation=None)
            plot.mpl.ax.grid(True, color='gray')
            plot.mpl.ax.set_title("Linear Scan", fontsize=10)
            plot.mpl.ax.set_ylabel("Time ($\mu$s)")
            plot.mpl.ax.set_xlabel("# Signals")
            plot.show()

    def plotTomoSignals(self):

        plot = PlotDialog(self)
        sig = self.SimNDT_Receivers.getReceivers()
        t = self.SimNDT_Simulation.t
        Name = self.SimNDT_Inspection.Name
        if Name == "Tomography":

            if self.SimNDT_Inspection.OneProjection:

                M, N = np.shape(sig)
                ind = 0
                delta = 2.0 / float(N)
                ascan = []
                for i in range(0, N):
                    ascan = sig[:, i] / np.max(np.abs(sig))
                    plot.mpl.ax.plot(t * 1e6, ascan + ind)
                    plot.mpl.ax.hold(True)
                    ind += delta
                    plot.mpl.ax.grid(True, color='gray')
                    plot.mpl.ax.set_title("Tomography Signals (One Projection)", fontsize=10)
                    plot.mpl.ax.set_xlabel("Time ($\mu$s)")
                    plot.mpl.ax.set_ylabel("# Signals")
                    plot.mpl.ax.set_yticks([])
                    plot.mpl.ax.tick_params(axis='y', which='both', left='off', right='off')
            else:
                lenght, R, E = np.shape(sig)
                print(lenght, R, E)
                ind = 0
                delta = 2.0 / float(R)
                ascan = []
                for i in range(0, R):
                    ascan = sig[:, i] / np.max(np.abs(sig))
                    plot.mpl.ax.plot(t * 1e6, ascan + ind)
                    plot.mpl.ax.hold(True)
                    ind += delta
                    plot.mpl.ax.grid(True, color='gray')
                    plot.mpl.ax.set_title("Tomography Signals", fontsize=10)
                    plot.mpl.ax.set_xlabel("Time ($\mu$s)")
                    plot.mpl.ax.set_ylabel("# Signals")
                    plot.mpl.ax.set_yticks([])
                    plot.mpl.ax.tick_params(axis='y', which='both', left='off', right='off')

            plot.show()

    def spectraSingleLaunch(self):

        plot = PlotDialog(self)

        sig = self.SimNDT_Receivers.getReceivers()
        Name = self.SimNDT_Inspection.Name

        if Name == "Transmission" or Name == "PulseEcho":
            spectraComplete = np.fft.fft(sig.flatten())
            N2 = np.size(spectraComplete) / 2.0
            spectra = np.abs(spectraComplete[0:N2])
            spectra /= np.max(spectra)
            fs = 1.0 / self.SimNDT_Simulation.dt
            frequency = np.linspace(0, fs / 2.0, N2) * 1e-6

            plot.mpl.ax.plot(frequency, spectra)
            plot.mpl.ax.grid(True, color='gray')
            plot.mpl.ax.set_title("Spectra", fontsize=10)
            plot.mpl.ax.set_ylim([0, 1.2])
            plot.mpl.ax.set_xlim([0, fs * 1e-6 / 4.0])
            plot.mpl.ax.set_xlabel("Frequency (MHz)")
            plot.mpl.ax.set_ylabel("Normalized Magnitude")
            plot.show()
