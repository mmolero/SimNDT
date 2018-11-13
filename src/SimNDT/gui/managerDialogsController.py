__author__ = 'Miguel Molero'



import os
import copy
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.newScenarioController import NewScenario
from SimNDT.gui.addEllipseController import AddEllipse
from SimNDT.gui.addRectangleController import AddRectangle
from SimNDT.gui.loadScenarioFromImageController import LoadScenarioFromImage
from SimNDT.gui.previewScenarioController import PreviewScenario

from SimNDT.gui.materialSetupController import MaterialSetup
from SimNDT.gui.boundarySetupController import BoundarySetup
from SimNDT.gui.singleLaunchSetupController import SingleLaunchSetup
from SimNDT.gui.linearScanController import LinearScanSetup
from SimNDT.gui.tomographySetupController import TomographySetup

from SimNDT.gui.simulationSetupController import SimulationSetup
from SimNDT.gui.checkSimulationController import CheckSimulation
from SimNDT.gui.runSimulationController import RunSimulation
from SimNDT.gui.engineController import EngineController
from SimNDT.gui.generateVideoController import GenerateVideo

from SimNDT.gui.twoPhaseModelDryCaseController import TwoPhaseModelDryCaseDialog
from SimNDT.gui.threePhaseModelDryCaseController import ThreePhaseModelDryCaseDialog
from SimNDT.gui.twoPhaseModelImmersionCaseController import TwoPhaseModelImmersionCaseDialog
from SimNDT.gui.threePhaseModelImmersionCaseController import ThreePhaseModelImmersionCaseDialog

from SimNDT.core.scenario import Scenario
from SimNDT.core.geometryObjects import Ellipse, Circle, Square, Rectangle
from SimNDT.core.simPack import SimPack
from SimNDT.core.receivers import Receivers

from SimNDT.gui.snapshots import SnapShots
from SimNDT.gui.Warnings import WarningParms, DoneParms
from SimNDT.gui import HelperMethods


from SimNDT.core.concreteModel import TwoPhaseModel


import numpy as np

class ManagerDialogs(object):

    def newGeometryModel(self):

        dialog = NewScenario()

        if self.SimNDT_Scenario is not None:
            dialog.widthLineEdit.setText(str(self.SimNDT_Scenario.Width))
            dialog.heightLineEdit.setText(str(self.SimNDT_Scenario.Height))
            dialog.pixelLineEdit.setText(str(self.SimNDT_Scenario.Pixel_mm))
            dialog.labelSpinBox.setValue(int(self.SimNDT_Scenario.Label))

        if dialog.exec_():
            width = dialog.width
            height = dialog.height
            pixel = dialog.pixel
            label = dialog.label

            self.SimNDT_Scenario = Scenario(width,height,pixel,label)
            self.SimNDT_ObjectList = None
            self.SimNDT_Check = False

            self.dirty = True


            self.updateUI()


    def addEllipse(self):
        dlg = AddEllipse()
        if dlg.exec_():
            centerX, centerY, major, minor, theta, label = dlg.getParms()
            if self.SimNDT_Scenario:
                try:
                    self.SimNDT_Scenario.addEllipse(centerX, centerY, major, minor, theta, label)
                    if major!=minor:
                        obj = Ellipse(centerX, centerY, major, minor, theta, label)
                    else:
                        obj = Circle(centerX,centerY, major, label)

                except Exception as e:
                    msg = WarningParms("Error in the object generation!!!. %s"%e)
                    msg.exec_()
                    return

                if self.SimNDT_ObjectList is None:
                    self.SimNDT_ObjectList = list()
                self.SimNDT_ObjectList.append(obj)


            self.dirty = True
            self.updateUI()


    def addRectangle(self):

        dlg = AddRectangle()
        if dlg.exec_():
            centerX, centerY, width, height, theta, label = dlg.getParms()
            if self.SimNDT_Scenario:

                try:
                    self.SimNDT_Scenario.addRectangle(centerX, centerY, width, height, theta, label)
                    if width!=height:
                        obj = Rectangle(centerX, centerY, width, height, theta, label)
                    else:
                        obj = Square(centerX,centerY, width, theta, label)

                except Exception as e:
                    msg = WarningParms("Error in the object generation!!!")
                    msg.exec_()
                    return

                if self.SimNDT_ObjectList is None:
                    self.SimNDT_ObjectList = list()
                self.SimNDT_ObjectList.append(obj)

            self.dirty = True
            self.updateUI()



    def loadImage(self):

        dlg = LoadScenarioFromImage(self.filename)
        if dlg.exec_():


            M,N    = np.shape(dlg.image_labeled)
            Pixel = float(dlg.Pixel)

            Width  = N/Pixel
            Height = M/Pixel

            if self.SimNDT_Scenario is None:
                self.SimNDT_Scenario = Scenario()
                self.SimNDT_Scenario.setImage(dlg.image_labeled, Width, Height, Pixel, Label=0)
            else:
                self.SimNDT_Scenario.setImage(dlg.image_labeled, Width, Height, Pixel, Label=0)

            self.GraphicView.setupZoom(100)
            self.statusBarWidget.zoomSpinBox.setValue(100)

            self.SimNDT_ObjectList	= None
            self.SimNDT_Boundaries  = None
            self.SimNDT_Check = False

            self.dirty = True
            self.updateUI()


    def previewScenario(self):

        dlg = PreviewScenario(self.SimNDT_Scenario, self)
        dlg.show()


    def rotateScenarioCounterClockwise(self):

        self.SimNDT_Scenario.rotate(direction="clockwise")
        self.dirty = True
        self.SimNDT_Check = False
        self.updateUI()


    def rotateScenarioClockwise(self):
        self.SimNDT_Scenario.rotate(direction="counterclockwise")
        self.dirty = True
        self.SimNDT_Check = False
        self.updateUI()


    def materialSetup(self):

        dlg = MaterialSetup(self.SimNDT_Materials, filename = self.filename)
        if dlg.exec_():
            self.SimNDT_Materials = copy.deepcopy(dlg.SimNDT_Materials)
            self.dirty = True

            self.SimNDT_Check = False
            self.updateUI()


    def boundarySetup(self):

        dlg = BoundarySetup(self.SimNDT_Boundaries)
        if dlg.exec_():
            self.SimNDT_Boundaries = copy.deepcopy(dlg.Boundaries)
            self.SimNDT_Scenario.createBoundaries(self.SimNDT_Boundaries)

            self.dirty = True
            self.SimNDT_Check = False
            self.updateUI()


    def singleLaunchSetup(self):

        dlg = SingleLaunchSetup(self.SimNDT_Scenario, self.SimNDT_Source, self.SimNDT_Inspection, self.SimNDT_Transducers, self.SimNDT_Signal)
        if dlg.exec_():

            self.SimNDT_Source = copy.deepcopy(dlg.Source)
            self.SimNDT_Transducers = copy.deepcopy(dlg.Transducers)
            self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
            self.SimNDT_Signal = copy.deepcopy(dlg.Signal)

            self.SimNDT_Check = False
            self.dirty = True
            self.updateUI()


    def linearScanSetup(self):
        dlg = LinearScanSetup(self.SimNDT_Scenario, self.SimNDT_Source, self.SimNDT_Inspection, self.SimNDT_Transducers, self.SimNDT_Signal)
        if dlg.exec_():

            self.SimNDT_Source = copy.deepcopy(dlg.Source)
            self.SimNDT_Transducers = copy.deepcopy(dlg.Transducers)
            self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
            self.SimNDT_Signal = copy.deepcopy(dlg.Signal)

            self.SimNDT_Check = False
            self.dirty = True
            self.updateUI()


    def tomographySetup(self):
        dlg = TomographySetup(self.SimNDT_Scenario, self.SimNDT_Source, self.SimNDT_Inspection, self.SimNDT_Transducers, self.SimNDT_Signal)
        if dlg.exec_():


            self.SimNDT_Source = copy.deepcopy(dlg.Source)
            self.SimNDT_Transducers = copy.deepcopy(dlg.Transducers)
            self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
            self.SimNDT_Signal = copy.deepcopy(dlg.Signal)

            self.SimNDT_Check = False
            self.dirty = True
            self.updateUI()



    def signalSetup(self):
        pass

    def simulationSetup(self):

        dlg = SimulationSetup(self.SimNDT_Scenario, self.SimNDT_Materials,
                              self.SimNDT_Transducers, self.SimNDT_Signal,
                              self.SimNDT_Simulation)
        if dlg.exec_():

            self.SimNDT_Simulation = copy.deepcopy(dlg.Simulation)
            self.dirty = True
            self.OpenSimFile = False
            self.SimNDT_Check = False
            self.updateUI()


    def checkSimulation(self):

        dlg = CheckSimulation(self.SimNDT_Scenario, self.SimNDT_Materials, self.SimNDT_Boundaries,
                              self.SimNDT_Transducers, self.SimNDT_Inspection, self.SimNDT_Signal, self.SimNDT_Simulation)

        self.SimNDT_Check = False

        if dlg.exec_():
            self.SimNDT_Check = True

        self.SimNDT_Scenario = copy.deepcopy(dlg.Scenario)
        self.SimNDT_Boundaries = copy.deepcopy(dlg.Boundaries)
        self.SimNDT_Inspection = copy.deepcopy(dlg.Inspection)
        self.dirty = True
        self.OpenSimFile = False
        self.updateUI()


    def runSimulation(self):

        dlg = RunSimulation(self.filename, self.SimNDT_Simulation)
        if dlg.exec_():

            DB = dlg.visualizacionRangeSpinBox.value()
            color = dlg.colormapComboBox.currentIndex()
            isView = dlg.viewCheckBox.isChecked()
            isReceiverPlot = dlg.receiverCheckBox.isChecked()
            isEnableFields = dlg.enableSavingFieldsCheckBox.isChecked()


            if isView:
                self.GraphicView.setColormap(color)

            if dlg.basename is not None:
                step = dlg.snapshotStepSpinBox.value()
                self.SimNDT_SnapShots = SnapShots(True, Step=step, Filename = dlg.basename, dB = DB, Color = color, enableFields=isEnableFields)
            else:
                self.SimNDT_SnapShots = SnapShots(dB = DB, enableFields=isEnableFields)


            self.runEngine(isView, isReceiverPlot)



    def runEngine(self, isView=False, isReceiverPlot=False):


        self.dirty = True

        self.menuFile.menuAction().setEnabled(False)
        self.menuConfiguration.menuAction().setEnabled(False)
        self.menuPlotting_Tools.menuAction().setEnabled(False)
        self.menuTools.menuAction().setEnabled(False)
        HelperMethods.setEnabled(self.fileMenuActions, False)
        HelperMethods.setEnabled(self.geometryMenuActions, False)
        HelperMethods.setEnabled(self.inspectionMenuActions, False)
        HelperMethods.setEnabled(self.simulationMenuActions, False)


        self.statusBarWidget.startSimulation(self.SimNDT_Simulation.TimeSteps)

        if isView:
            self.statusBarWidget.viewOn()
        else:
            self.statusBarWidget.updateGeometryFrame()


        simPack = SimPack(self.SimNDT_Scenario, self.SimNDT_Materials, self.SimNDT_Boundaries,
                          self.SimNDT_Inspection, self.SimNDT_Source, self.SimNDT_Transducers, self.SimNDT_Signal,
                          self.SimNDT_Simulation)

        engine = EngineController(simPack, isView, isReceiverPlot, self.statusBarWidget, self)


        state = engine.run()


        self.statusBarWidget.endSimulation()

        self.PauseSimulation = False

        if state == "Stop":
            self.StopSimulation = False
            self.status.showMessage("Stop by User!!!!!", 15000)
            message = WarningParms("Stop by User!!!")
            message.exec_()
        else:
            self.status.showMessage("Done", 15000)
            message = DoneParms()
            message.exec_()



        self.menuFile.menuAction().setEnabled(True)
        self.menuConfiguration.menuAction().setEnabled(True)
        self.menuPlotting_Tools.menuAction().setEnabled(True)
        self.menuTools.menuAction().setEnabled(True)
        HelperMethods.setEnabled(self.fileMenuActions, True)
        HelperMethods.setEnabled(self.geometryMenuActions, True)
        HelperMethods.setEnabled(self.inspectionMenuActions, True)
        HelperMethods.setEnabled(self.simulationMenuActions, True)


        self.setPlotInspectionsMenu()
        self.SimNDT_Receivers = Receivers(self.SimNDT_Inspection.Name)
        self.SimNDT_Receivers.setReceivers(engine)


    def generateVideo(self):

        dlg = GenerateVideo()
        dlg.exec_()


    def twoPhaseModelDryCase(self):

        dlg = TwoPhaseModelDryCaseDialog(None, self.SimNDT_Scenario, self.SimNDT_ConcreteMicrostructure)
        if dlg.exec_():

            self.SimNDT_Scenario.I = dlg.image
            self.SimNDT_Scenario.resetBoundary()
            self.SimNDT_ObjectList = None
            self.SimNDT_Check = False
            self.dirty = True


            self.SimNDT_ConcreteMicrostructure = dlg.concrete2PhaseObject




            self.updateUI()




    def threePhaseModelDryCase(self):

        dlg = ThreePhaseModelDryCaseDialog(None, self.SimNDT_Scenario, self.SimNDT_ConcreteMicrostructure)
        if dlg.exec_():

            self.SimNDT_Scenario.I = dlg.image
            self.SimNDT_Scenario.resetBoundary()
            self.SimNDT_ObjectList = None
            self.SimNDT_Check = False
            self.dirty = True

            self.SimNDT_ConcreteMicrostructure = dlg.concrete3PhaseObject

            self.updateUI()


    def twoPhaseModelImmersionCase(self):

        dlg = TwoPhaseModelImmersionCaseDialog(None, self.SimNDT_Scenario, self.SimNDT_ConcreteMicrostructure)
        if dlg.exec_():

            self.SimNDT_Scenario.I = dlg.image
            self.SimNDT_Scenario.resetBoundary()
            self.SimNDT_ObjectList = None
            self.SimNDT_Check = False
            self.dirty = True

            self.SimNDT_ConcreteMicrostructure = dlg.concrete2PhaseObjectImmersion


            self.updateUI()


    def threePhaseModelImmersionCase(self):

        dlg = ThreePhaseModelImmersionCaseDialog(None, self.SimNDT_Scenario, self.SimNDT_ConcreteMicrostructure)
        if dlg.exec_():

            self.SimNDT_Scenario.I = dlg.image
            self.SimNDT_Scenario.resetBoundary()
            self.SimNDT_ObjectList = None
            self.SimNDT_Check = False
            self.dirty = True

            self.SimNDT_ConcreteMicrostructure = dlg.concrete3PhaseObjectImmersion

            self.updateUI()

