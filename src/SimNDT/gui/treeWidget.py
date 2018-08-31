__author__ = 'Miguel Molero'

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.constants import *
import numpy as np

from SimNDT.core.constants import *
from SimNDT.gui import HelperMethods


class MySignal(QObject):
    sig = Signal()


class TreeWidget(QTreeWidget):
    def __init__(self, parent=None):

        super(TreeWidget, self).__init__(parent)

        self.setGeometry(QRect(0, 0, 350, 840))
        self.setHeaderLabels(["", ""])
        self.setMaximumWidth(450)
        self.setMinimumWidth(150)
        # self.setRootIsDecorated(True)
        self.setAlternatingRowColors(True)
        self.setColumnCount(2)
        self.header().resizeSection(0, 200)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.actionDeleteObject = HelperMethods.createAction(self, "Delete Selected Object", self.deleteObject,
                                                             icon="delete.png")

        self.deleteDone = MySignal()

    def deleteObject(self):

        print("delete", self.index)
        print
        self.SimNDT_ObjectList.pop(self.index)
        self.SimNDT_Scenario.resetImage()
        for obj in self.SimNDT_ObjectList:
            self.SimNDT_Scenario.addObject(obj)

        if len(self.SimNDT_ObjectList) == 0:
            self.SimNDT_ObjectList = None

        self.deleteDone.sig.emit()

    def showContextMenu(self, pos):
        item = self.itemAt(pos)
        menu = QMenu()
        it = QTreeWidgetItem.UserType + 1
        if item.type() == it:
            HelperMethods.addActions(menu, self.actionDeleteObject)
            self.index = item.parent().indexOfChild(item)

        menu.exec_(self.mapToGlobal(pos))

    def update(self, SimNDT_Scenario,
               SimNDT_ObjectList,
               SimNDT_Materials,
               SimNDT_Boundaries,
               SimNDT_Inspection,
               SimNDT_Source,
               SimNDT_Transducers,
               SimNDT_Signal,
               SimNDT_Simulation):

        self.clear()
        # Scenario


        if SimNDT_Scenario:
            self.SimNDT_Scenario = SimNDT_Scenario

            scenario_tree = QTreeWidgetItem(self)
            scenario_tree.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)

            scenario_tree.setText(0, "Scenario")
            scenario_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_1, QFont.Bold))
            scenario_tree.setIcon(0, QIcon(":/newImage.png"))

            # Dimensions
            dimensions_tree = QTreeWidgetItem(scenario_tree)
            dimensions_tree.setText(0, "Dimensions")
            dimensions_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))

            scenario_labels = ("Width", "Height", "Pixel/mm", "Label", "Geometric Model Size")
            modelSize = "%d x %d" % (SimNDT_Scenario.M, SimNDT_Scenario.N)
            print
            "SIZE Scenario", SimNDT_Scenario.I.shape
            scenario_values = (SimNDT_Scenario.Width, SimNDT_Scenario.Height,
                               SimNDT_Scenario.Pixel_mm, SimNDT_Scenario.Label, modelSize)
            self.populateTree(dimensions_tree, scenario_labels, scenario_values)

            labels_tree = QTreeWidgetItem(scenario_tree)
            numLabels = np.size(np.unique(SimNDT_Scenario.I))
            labels_tree.setText(0, "Labels in Scenario")
            labels_labels = ("Total Number", "Labels")
            labels_values = (numLabels, str(np.unique(SimNDT_Scenario.I)))
            labels_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            self.populateTree(labels_tree, labels_labels, labels_values)

            self.expandItem(scenario_tree)

        # Objects
        if SimNDT_ObjectList:

            ItemType1 = QTreeWidgetItem.UserType + 1
            self.SimNDT_ObjectList = SimNDT_ObjectList

            objects_tree = QTreeWidgetItem(scenario_tree)
            objects_tree.setText(0, "Objects")
            objects_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            for item in SimNDT_ObjectList:
                objects_parent = QTreeWidgetItem(objects_tree, ItemType1)
                objects_parent.setText(0, item.Name)
                if item.Name == "ellipse":
                    objects_labels = ("Center X", "Center Y", "Semi-Major", "Semi-Minor", "Angle", "Label")
                    objects_values = (item.x0, item.y0, item.a, item.b, item.theta, item.Label)
                if item.Name == "circle":
                    objects_labels = ("Center X", "Center Y", "Radius", "Label")
                    objects_values = (item.x0, item.y0, item.r, item.Label)
                if item.Name == 'rectangle':
                    objects_labels = ("Center X", "Center Y", "Width", "Height", "Label")
                    objects_values = (item.x0, item.y0, item.W, item.H, item.Label)
                if item.Name == 'square':
                    objects_labels = ("Center X", "Center Y", "Side", "Label")
                    objects_values = (item.x0, item.y0, item.L, item.Label)

                self.populateTree(objects_parent, objects_labels, objects_values)
            self.expandItem(objects_tree)

        # Materials
        if SimNDT_Materials is not None:
            material_tree = QTreeWidgetItem(self)
            material_tree.setText(0, "Materials")
            material_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_1, QFont.Bold))
            material_tree.setIcon(0, QIcon(":/material.png"))

            materials_label = (RHO, "VL", "VT", "Label")

            for item in SimNDT_Materials:
                materials_parent = QTreeWidgetItem(material_tree)
                materials_parent.setText(0, item.Name)
                materials_parent.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))

                materials_values = ("%0.2f" % (item.Rho), "%0.2f" % (item.VL), "%0.2f" % (item.VT), item.Label)
                self.populateTree(materials_parent, materials_label, materials_values)

            self.expandItem(material_tree)

        # Boundaries
        if SimNDT_Boundaries is not None:
            boundaries_tree = QTreeWidgetItem(self)
            boundaries_tree.setText(0, "Boundaries")
            boundaries_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_1, QFont.Bold))
            boundaries_tree.setIcon(0, QIcon(":/boundary.png"))

            for item in SimNDT_Boundaries:
                boundaries_parent = QTreeWidgetItem(boundaries_tree)
                boundaries_parent.setText(0, item.Name)
                boundaries_parent.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))

                boundaries_label = ("Layer", "Size")
                size = item.Size if item.BC == BC.AbsorbingLayer else None
                boundaries_values = (BC.keys[item.BC], size)
                self.populateTree(boundaries_parent, boundaries_label, boundaries_values)
            self.expandItem(boundaries_tree)

        # Inspections
        if SimNDT_Inspection is not None:

            if SimNDT_Inspection.Name == "LinearScan":
                method = SimNDT_Inspection
                Name = SimNDT_Inspection.Name + ": " + SimNDT_Inspection.Method


            else:
                method = SimNDT_Inspection
                Name = method.Name

            source = SimNDT_Source

            inspection_tree = QTreeWidgetItem(self)
            inspection_tree.setText(0, "Inspection Method")
            inspection_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_1, QFont.Bold))

            if SimNDT_Inspection.Name == "LinearScan":
                inspection_tree.setIcon(0, QIcon(":/linearScan.png"))
            elif SimNDT_Inspection.Name == "Tomography":
                inspection_tree.setIcon(0, QIcon(":/tomoSetup.png"))
            else:
                inspection_tree.setIcon(0, QIcon(":/singleLaunch.png"))

            inspection_parent = QTreeWidgetItem(inspection_tree)

            inspection_parent.setText(0, Name)
            inspection_parent.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            inspection_label = ("Longitudinal Source", "Shear Source")
            inspection_values = (bool(source.Longitudinal), bool(source.Shear))
            self.populateTree(inspection_parent, inspection_label, inspection_values)

            transductor_tree = QTreeWidgetItem(inspection_parent)
            transductor_tree.setText(0, "Emisor Transducer")
            transductor_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            if method.Name == "Tomography":

                transductor_label = ("Size", "Point Source", "Windowed Source")
                transductor_values = (SimNDT_Transducers[0].Size,
                                      bool(SimNDT_Transducers[0].PointSource),
                                      bool(SimNDT_Transducers[0].Window))
            else:
                transductor_label = ("Size", "Center Offset", "Border Offset", "Point Source", "Windowed Source")
                transductor_values = (SimNDT_Transducers[0].Size,
                                      SimNDT_Transducers[0].CenterOffset,
                                      SimNDT_Transducers[0].BorderOffset,
                                      bool(SimNDT_Transducers[0].PointSource),
                                      bool(SimNDT_Transducers[0].Window))
            self.populateTree(transductor_tree, transductor_label, transductor_values)

            signal_tree = QTreeWidgetItem(inspection_parent)
            signal_tree.setText(0, "Signal")
            signal_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            signal_tree.setIcon(0, QIcon(":/signal.png"))

            if SimNDT_Signal.Name == "GaussianSine":
                signal_label = ("Type", "Amplitude", "Frequency (MHz)", "# Cycles")
                signal_values = (SimNDT_Signal.Name, SimNDT_Signal.Amplitude,
                                 SimNDT_Signal.Frequency * 1e-6, SimNDT_Signal.N_Cycles)
            else:
                signal_label = ("Type", "Amplitude", "Frequency (MHz)", "# Cycles")
                signal_values = (SimNDT_Signal.Name, SimNDT_Signal.Amplitude,
                                 SimNDT_Signal.Frequency * 1e-6)

            self.populateTree(signal_tree, signal_label, signal_values)

            self.expandItem(signal_tree)
            self.expandItem(inspection_tree)
            self.expandItem(inspection_parent)

        # Simulation
        if SimNDT_Simulation is not None:
            simulation_tree = QTreeWidgetItem(self)
            simulation_tree.setText(0, "Simulation Parameters")
            simulation_tree.setFont(0, QFont(FONT_NAME, FONT_SIZE_1, QFont.Bold))
            simulation_tree.setIcon(0, QIcon(":/simModel.png"))

            simulation_label = ("Time Scale", "Max. Frequency (MHz)", "Points/Cycle",
                                "Simulation Time", "Device", "OpenCL",
                                "dx (mm)", "dt (%ss)" % MU, "Numerical Model Size")

            freq = SimNDT_Simulation.MaxFreq * 1e-6
            dx = "%.4f" % (SimNDT_Simulation.dx * 1e3)
            dt = "%.4f" % (SimNDT_Simulation.dt * 1e6)
            simTime = SimNDT_Simulation.SimulationTime * 1e6
            modelSize = "%d x %d" % (SimNDT_Simulation.MRI, SimNDT_Simulation.NRI)

            Platform = False if SimNDT_Simulation.Platform == "Serial" else True

            simulation_values = (SimNDT_Simulation.TimeScale, freq,
                                 SimNDT_Simulation.PointCycle, simTime,
                                 SimNDT_Simulation.Device, Platform,
                                 dx, dt, modelSize)

            self.populateTree(simulation_tree, simulation_label, simulation_values)

            self.expandItem(simulation_tree)

    def populateTree(self, parent, labels, values):

        for i, j in zip(labels, values):
            if j is None:
                continue
            item = QTreeWidgetItem(parent)
            item.setText(0, i)
            item.setFont(0, QFont(FONT_NAME, FONT_SIZE_2, QFont.Normal))
            if isinstance(j, bool):
                if j is True:
                    item.setText(1, MARK)
                else:
                    item.setText(1, CROSS)
            else:
                item.setText(1, str(j))

            item.setFont(1, QFont(FONT_NAME, FONT_SIZE_3, QFont.Normal))

        self.expandItem(parent)
