__author__ = 'Miguel Molero'


import time, sys
import numpy as np

from PySide.QtCore import *
from SimNDT.gui.Warnings import WarningParms

from SimNDT.engine.efit2d import EFIT2D
from SimNDT.graphics.mplWidget import PlotInline
from SimNDT.core.signal import Signals

class EngineController():

    def __init__(self, simPack, GL= False, IsReceiverPlot = False, statusBarWidget=None, parent= None):

        self.simPack = simPack
        self.GL	= GL
        self.IsReceiverPlot = IsReceiverPlot
        self.statusBarWidget = statusBarWidget
        self.parent = parent

        Platform = self.simPack.Simulation.Platform
        if Platform is not "Serial":
            Platform = "OpenCL"

        self.Platform = Platform



    def run(self):


        self.TimeSteps  = self.simPack.Simulation.TimeSteps
        Name = self.simPack.Inspection.Name

        if Name == "Transmission" or Name == "PulseEcho":
            state = self._run_SingleLaunch()
            return state
        elif Name == "LinearScan":
            state = self._run_LinearScan()
            return state

        elif Name == "Tomography":
            state = self._run_Tomography()
            return state


    def _chooseModel(self):



        self.SimNDT_FD	= EFIT2D(self.simPack, self.Platform)


        try:
            self.SimNDT_FD.setup_CL()

        except Exception as e:
            msgBox = WarningParms("Error!!!!!!!!!!!!!!!!!! %s"% e.message)
            if msgBox.exec_():
                sys.exit()


    def getReceivers(self):
        return self.receiver_signals

    def _run_SingleLaunch(self):
        self.Times = 1.0
        self.n = 0
        self._chooseModel()
        start = time.time()
        state = self._process()
        self.SimNDT_FD.saveOutput()
        print ("Elapsed Time: ",  time.time() -start)
        self.receiver_signals = self.SimNDT_FD.receiver_signals.copy()
        return state

    def _run_LinearScan(self):
        self.Times = np.size(self.simPack.Inspection.ScanVector)
        lscan = np.zeros((int(self.TimeSteps),int(self.Times))).astype(np.float32)

        n=0
        self.n = 0

        self.statusBarWidget.labelInspectionStatusBar.setText("#Inspection: %d - %d "%(n,self.Times))
        self.statusBarWidget.labelInspectionStatusBar.show()
        QCoreApplication.processEvents()

        start = time.time()
        for idx, offset in enumerate(self.simPack.Inspection.ScanVector):
            self.simPack.Transducers[0].CenterOffset = offset
            self.simPack.Inspection.setInspection(	self.simPack.Scenario,
                                                    self.simPack.Transducers[0],
                                                    self.simPack.Simulation)
            self._chooseModel()
            state = self._process(idx)
            self.SimNDT_FD.saveOutput()
            lscan[:,n] = self.SimNDT_FD.receiver_signals.copy()[:,0]
            n+=1

            self.statusBarWidget.labelInspectionStatusBar.setText("#Inspection: %d - %d "%(n,self.Times))
            QCoreApplication.processEvents()
            if state == "Stop":
                break

        print ("Elapsed Time: ",  time.time() -start)

        self.receiver_signals = lscan.copy()
        return state


    def _run_Tomography(self):

        Ntheta = np.size(self.simPack.Inspection.Theta)
        Ntheta1		 = Ntheta-1
        if self.simPack.Inspection.OneProjection:

            self.n = 0
            self.Times = 1.0
            self.receiver_signals = np.zeros((self.TimeSteps, Ntheta1 ), dtype=np.float32 )
            self._chooseModel()
            state = self._process()
            self.receiver_signals[:,:] = self.SimNDT_FD.receiver_signals.copy()[:,:]

        else:
            self.n = 0
            n = 0
            self.Times = Ntheta
            self.statusBarWidget.labelInspectionStatusBar.setText("#Inspection: %d - %d "%(n,self.Times))
            self.statusBarWidget.labelInspectionStatusBar.show()
            QCoreApplication.processEvents()
            self.receiver_signals = np.zeros((int(self.TimeSteps), int(Ntheta1), int(Ntheta)), dtype=np.float32 )

            for idx, theta in enumerate(self.simPack.Inspection.Theta):
                self.simPack.Simulation.rotate_model(theta,self.simPack.Scenario)
                self._chooseModel()
                state = self._process(idx)
                self.receiver_signals[:,:, n] = self.SimNDT_FD.receiver_signals.copy()[:,:]
                n +=1
                self.statusBarWidget.labelInspectionStatusBar.setText("#Inspection: %d - %d "%(n,self.Times))
                QCoreApplication.processEvents()
                if state == "Stop":
                    break

        return state


    def _process(self, idx = None):
        if self.Platform == "OpenCL":
            if self.GL:
                state = self._runGL(idx)
                return state
            else:
                state = self._run(idx)
                return state
        elif self.Platform == "Serial":
            if self.GL:
                state = self._runGLSerial(idx)
                return state
            else:
                state = self._runSerial(idx)
                return state


    def saveOptions(self, step, idx):

        if (self.SimNDT_FD.n % step==0):
            value = (self.n/float(self.TimeSteps*self.Times))*100
            self.statusBarWidget.barStatus.setValue(value)
            self.statusBarWidget.labelStatusBar.setText(" Steps: %d - %d"%(self.SimNDT_FD.n, self.TimeSteps))
            QCoreApplication.processEvents()

        if  self.parent.SimNDT_SnapShots.IsEnable:
            if (self.SimNDT_FD.n % self.parent.SimNDT_SnapShots.Step==0):
                self.save_fig(idx)

        if self.parent.SimNDT_SnapShots.enableFields:
            if (self.SimNDT_FD.n % self.parent.SimNDT_SnapShots.Step==0):
                self.parent.SimNDT_SnapShots.save_fields(self.SimNDT_FD.Vx, self.SimNDT_FD.Vy, self.SimNDT_FD.n)



    def _run(self, idx):
        step  = 50
        while (self.SimNDT_FD.n < self.TimeSteps):

            if self.parent.StopSimulation:
                return "Stop"

            if self.parent.PauseSimulation:
                while True:
                    if self.parent.StopSimulation:
                        return "Stop"
                    if not self.parent.PauseSimulation:
                        break
                    QCoreApplication.processEvents()

            self.SimNDT_FD.run()
            self.SimNDT_FD.n +=1
            self.n +=1

            self.saveOptions(step, idx)





    def _runSerial(self, idx):
        step  = 10
        while (self.SimNDT_FD.n < self.TimeSteps):

            if self.parent.StopSimulation:
                return "Stop"

            if self.parent.PauseSimulation:
                while True:
                    if self.parent.StopSimulation:
                        return "Stop"
                    if not self.parent.PauseSimulation:
                        break
                    QCoreApplication.processEvents()

            self.SimNDT_FD.runSerial()
            self.SimNDT_FD.n +=1
            self.n +=1

            self.saveOptions(step, idx)




    def _runGL(self, idx):

        DB = self.parent.SimNDT_SnapShots.DB
        self.parent.GraphicView.setImage(np.float32(self.SimNDT_FD.SV), DB)
        step  = 50

        if self.IsReceiverPlot:
            SimulationTime = self.parent.SimNDT_Simulation.SimulationTime
            sig = self.SimNDT_FD.receiver_signals
            self.plot = PlotInline()
            self.plot.init(sig, SimulationTime)
            self.plot.show()


        while (self.SimNDT_FD.n < self.TimeSteps):

            if self.parent.StopSimulation:
                return "Stop"

            if self.parent.PauseSimulation:
                while True:
                    if self.parent.StopSimulation:
                        return "Stop"
                    if not self.parent.PauseSimulation:
                        break
                    QCoreApplication.processEvents()

            self.SimNDT_FD.run()
            self.SimNDT_FD.n+=1
            self.n +=1



            if (self.SimNDT_FD.n % step==0):
                self.SimNDT_FD.runGL()
                self.parent.GraphicView.updateWithImage(self.SimNDT_FD.SV, self.SimNDT_FD.n*self.SimNDT_FD.dt*1e6)

                if self.IsReceiverPlot:
                    self.SimNDT_FD.saveOutput()
                    sig = self.SimNDT_FD.receiver_signals[self.SimNDT_FD.n-1,0]
                    self.plot.update(sig)

            elif self.IsReceiverPlot:
                self.SimNDT_FD.saveOutput()
                sig = self.SimNDT_FD.receiver_signals[self.SimNDT_FD.n-1,0]
                self.plot.data.append(sig)


            self.saveOptions(step, idx)



    def _runGLSerial(self, idx):

        DB = self.parent.SimNDT_SnapShots.DB
        self.parent.GraphicView.setImage(np.float32(self.SimNDT_FD.SV), DB)
        step  = 10

        if self.IsReceiverPlot:
            SimulationTime = self.parent.SimNDT_Simulation.SimulationTime
            sig = self.SimNDT_FD.receiver_signals
            self.plot = PlotInline()
            self.plot.init(sig, SimulationTime)
            self.plot.show()

        while (self.SimNDT_FD.n < self.TimeSteps):

            if self.parent.StopSimulation:
                return "Stop"

            if self.parent.PauseSimulation:
                while True:
                    if self.parent.StopSimulation:
                        return "Stop"
                    if not self.parent.PauseSimulation:
                        break
                    QCoreApplication.processEvents()

            self.SimNDT_FD.runSerial()
            self.SimNDT_FD.n+=1
            self.n +=1

            if (self.SimNDT_FD.n % step==0):
                self.SimNDT_FD.runGLSerial()
                self.parent.GraphicView.updateWithImage(self.SimNDT_FD.SV,self.SimNDT_FD.n*self.SimNDT_FD.dt*1e6)

                if self.IsReceiverPlot:
                    sig = self.SimNDT_FD.receiver_signals[self.SimNDT_FD.n-1,0]
                    self.plot.update(sig)


            elif self.IsReceiverPlot:
                sig = self.SimNDT_FD.receiver_signals[self.SimNDT_FD.n-1,0]
                self.plot.data.append(sig)


            self.saveOptions(step, idx)




    def save_fig(self, idx = None):

        if self.Platform == "OpenCL":
            self.SimNDT_FD.runGL()

        elif self.Platform == "Serial":
            self.SimNDT_FD.runGLSerial()


        self.parent.SimNDT_SnapShots.save_fig(self.SimNDT_FD.SV, self.SimNDT_FD.n, idx)













