import sys, os, datetime
import numpy as np
from scipy.io import savemat, loadmat

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_mainwindow import Ui_MainWindow

from SimNDT.gui import HelperMethods
from SimNDT.gui import managerFile

from SimNDT.gui.managerDialogsController import ManagerDialogs
from SimNDT.gui.managerPlotsController import ManagerPlots
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.checkOpenCL import isOpenCL

from SimNDT.gui.statusBarWidget import StatusBarWidget
from SimNDT.gui.treeWidget import TreeWidget
from SimNDT.gui.helpForm import HelpForm

from SimNDT.graphics.graphicView import GraphicView

from SimNDT.core.scenario import Scenario
from SimNDT.core.material import Material
from SimNDT.core.boundary import Boundary
from SimNDT.core.geometryObjects import Ellipse, Circle, Inclusions, Rectangle, Square
from SimNDT.core.geometryObjects import Concrete2Phase, Concrete2PhaseImmersion, Concrete3Phase, Concrete3PhaseImmersion
from SimNDT.core.inspectionMethods import Source, LinearScan, Transmission, PulseEcho, Tomography
from SimNDT.core.signal import Signals
from SimNDT.core.receivers import Receivers
from SimNDT.core.transducer import Transducer
from SimNDT.core.simulation import Simulation

YEAR = 2080
MONTH = 12


class Info:
    def __init__(self):
        self.version = "0.52"
        self.date = "13-11-2018"


info = Info()

class MainWindow(QMainWindow, Ui_MainWindow, ManagerDialogs, ManagerPlots):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init()

        self.createMenus()
        self.createToolBar()
        self.setupGraphicView()
        self.setupStatusBar()
        self.tree()
        self.setupConnections()
        self.initSettings()

        isOpenCL(self.statusBarWidget.openclIcon, self.statusBarWidget.openclLabel)
        self.OnLicence()

        self.updateFileMenu()

        self.OpenSimFile = False
        QTimer.singleShot(0, self.loadInitialFile)

        if self.filename is None:
            self.initSim()

    def OnLicence(self):
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        if year >= YEAR and month >= MONTH:
            dial = WarningParms('Get the new version!!!!, please contact to: miguel.molero@gmail.com')
            if dial.exec_():
                self.close()
                sys.exit()

    def createObjects(self):

        self.SimNDT_Scenario = None
        self.SimNDT_ObjectList = None
        self.SimNDT_Materials = None
        self.SimNDT_Boundaries = None
        self.SimNDT_Transducers = None
        self.SimNDT_Inspection = None
        self.SimNDT_Source = None
        self.SimNDT_Signal = None
        self.SimNDT_Simulation = None
        self.SimNDT_Receivers = None
        self.SimNDT_SnapShots = None

        self.SimNDT_ConcreteMicrostructure = None

    def setupConnections(self):
        self.actionNew_Geometry_Model.triggered.connect(self.newGeometryModel)
        self.actionPreview_Labeled_Scenario.triggered.connect(self.previewScenario)
        self.actionAdd_Ellipse.triggered.connect(self.addEllipse)
        self.actionAdd_Rectangle.triggered.connect(self.addRectangle)
        self.actionLoad_Scenario_From_Image.triggered.connect(self.loadImage)
        self.actionRotate_The_Scenario_90_Clockwise.triggered.connect(self.rotateScenarioClockwise)
        self.actionRotate_The_Scenario_90_Counter_Clockwise.triggered.connect(self.rotateScenarioCounterClockwise)

        self.actionTwo_Phase_Model_Dry_Case.triggered.connect(self.twoPhaseModelDryCase)
        self.actionThree_Phase_Model_Dry_Case.triggered.connect(self.threePhaseModelDryCase)
        self.actionTwo_Phase_Model_Immersion_Case.triggered.connect(self.twoPhaseModelImmersionCase)
        self.actionThree_Phase_Model_Immersion_Case.triggered.connect(self.threePhaseModelImmersionCase)

        self.actionMaterials_Setup.triggered.connect(self.materialSetup)
        self.actionBoundaty_Conditions_Setup.triggered.connect(self.boundarySetup)
        self.actionSingle_Launch_Inspection.triggered.connect(self.singleLaunchSetup)
        self.actionLinear_Scan_Inspections.triggered.connect(self.linearScanSetup)
        self.actionTomography_Inspections.triggered.connect(self.tomographySetup)
        self.actionSignal.triggered.connect(self.signalSetup)
        self.actionSimulation_Setup.triggered.connect(self.simulationSetup)
        self.actionCheck_Simulation_Setup.triggered.connect(self.checkSimulation)
        self.actionRun_Simulation.triggered.connect(self.runSimulation)

        self.actionPlot_Receiver_Signals_SingleLaunch.triggered.connect(self.plotSingleLaunch)
        self.actionPlot_Receiver_Signals_Spectra.triggered.connect(self.spectraSingleLaunch)
        self.actionPlot_Receivers_Signals_LinearScan.triggered.connect(self.plotLinearScan)
        self.actionPlot_Receivers_Signals_Tomography.triggered.connect(self.plotTomoSignals)

        self.actionCreate_Video_from_Images.triggered.connect(self.generateVideo)

        self.GraphicView.refreshZoom.zoomed.connect(self.statusBarWidget.zoomSpinBox.setValue)

    def init(self):

        self.SimNDT_Info = Info()
        self.SimNDT_Check = False

        self.dirty = False
        self.reset = False
        self.filename = None
        self.recentFiles = []

        self.StopSimulation = False
        self.PauseSimulation = False

        self.setGeometry(100, 100, 900, 600)
        self.setMinimumSize(400, 400)

        self.setWindowTitle('SimNDT v' + self.SimNDT_Info.version)
        self.setWindowFlags(self.windowFlags())

    def setTitle(self, fname):
        title = os.path.basename(fname)
        self.setWindowTitle('SimNDT v' + self.SimNDT_Info.version + ': ' + title)

    def loadInitialFile(self):
        settings = QSettings()
        fname = settings.value("LastFile")
        if fname and QFile.exists(fname):
            self.loadFile(fname)

    def createMenus(self):

        newFileAction = HelperMethods.createAction(self, "&New Simulation", self.fileNew,
                                                   QKeySequence.New, "document-new.png", self.tr("New Simulation File"))
        fileOpenAction = HelperMethods.createAction(self, "&Open existing Simulation", self.fileOpen,
                                                    QKeySequence.Open, 'document-open.png',
                                                    self.tr("Open an existing Simulation"))
        fileSaveAction = HelperMethods.createAction(self, "&Save Simulation", self.fileSave,
                                                    QKeySequence.Save, "document-save.png",
                                                    self.tr("Save the current Simulation"))
        fileSaveAsAction = HelperMethods.createAction(self, "Save &As", self.fileSaveAs,
                                                      QKeySequence.SaveAs, icon="document-save-as.png",
                                                      tip=self.tr("Save Simulation File As"))

        fileOpenAction.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        # fileSaveAction.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))


        fileExportMatlabAction = HelperMethods.createAction(self, "Export in .mat File", self.exportMatlab,
                                                            "Ctrl+E", icon="exportMatlab.png",
                                                            tip=self.tr("Export in .mat File"))

        fileResetAction = HelperMethods.createAction(self, "Reset Settings", self.resetSettings, icon="reset.png")

        fileQuitAction = HelperMethods.createAction(self, "&Quit", self.close,
                                                    "Ctrl+Q", "close", self.tr("Close the application"))

        self.fileMenuActions = (newFileAction, fileOpenAction,
                                fileSaveAction, fileSaveAsAction, fileExportMatlabAction, None, fileResetAction,
                                fileQuitAction)

        HelperMethods.setEnabled(self.fileMenuActions[2:5], False)
        self.connect(self.menuFile, SIGNAL("aboutToShow()"), self.updateFileMenu)

        self.geometryMenuActions = (
        self.actionNew_Geometry_Model, None, self.actionAdd_Ellipse, self.actionAdd_Rectangle,
        self.actionLoad_Scenario_From_Image, None, self.actionPreview_Labeled_Scenario,
        self.actionRotate_The_Scenario_90_Clockwise, self.actionRotate_The_Scenario_90_Counter_Clockwise)

        HelperMethods.setEnabled(self.menuNew_Simulation_Scenario, False)
        HelperMethods.setEnabled(self.geometryMenuActions, False)

        self.configurationMenuActions = (self.actionMaterials_Setup, self.actionBoundaty_Conditions_Setup)
        HelperMethods.setEnabled(self.configurationMenuActions, False)

        self.inspectionMenuActions = (
        self.actionSingle_Launch_Inspection, self.actionLinear_Scan_Inspections, self.actionTomography_Inspections)
        inspectionGroup = QActionGroup(self)
        HelperMethods.addActions(inspectionGroup, self.inspectionMenuActions)

        HelperMethods.setEnabled(self.menuInspection_Setup, False)
        HelperMethods.setEnabled(self.actionSimulation_Setup, False)
        HelperMethods.setEnabled(self.actionCheck_Simulation_Setup, False)
        HelperMethods.setEnabled(self.actionRun_Simulation, False)

        self.actionSignal = HelperMethods.createAction(self, "&Signal Setup", self.signalSetup,
                                                       "Ctrl+Shift+p", "signal.png", self.tr("Signal Setup"))

        self.simulationMenuActions = (self.actionNew_Geometry_Model, self.actionMaterials_Setup,
                                      self.actionBoundaty_Conditions_Setup, self.actionSingle_Launch_Inspection,
                                      self.actionLinear_Scan_Inspections, self.actionTomography_Inspections,
                                      self.actionSimulation_Setup, self.actionCheck_Simulation_Setup,
                                      self.actionRun_Simulation)

        self.menuPlotting_Tools.menuAction().setVisible(False)

        # self.menuAdd_Microstructure.menuAction().setVisible(False)
        # self.menuTools.menuAction().setVisible(False)


        helpAboutAction = HelperMethods.createAction(self, "&About SimNDT", self.helpAbout)
        helpHelpAction = HelperMethods.createAction(self, self.tr("&Help"), self.helpHelp, QKeySequence.HelpContents)

        helpMenu = self.menubar.addMenu(self.tr("&Help"))
        HelperMethods.addActions(helpMenu, (helpAboutAction, helpHelpAction))

    def updateFileMenu(self):

        self.menuFile.clear()
        HelperMethods.addActions(self.menuFile, self.fileMenuActions[0:-2])
        current = self.filename if self.filename is not None else None
        recentFiles = []

        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.menuFile.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon(":/logo_SimNDT.png"), "&%d %s" % (
                    i + 1, QFileInfo(fname).fileName()), self)
                action.setData(fname)
                self.connect(action, SIGNAL("triggered()"),
                             self.loadFile)
                self.menuFile.addAction(action)

        self.menuFile.addSeparator()
        self.menuFile.addAction(self.fileMenuActions[-2])
        self.menuFile.addAction(self.fileMenuActions[-1])

    def okToContinue(self):

        if self.dirty:
            reply = QMessageBox.question(self,
                                         "SimNDT - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()
        return True

    def loadFile(self, fname=None):

        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return

        if fname:
            self.filename = None
            self.addRecentFile(fname)
            self.filename = fname
            self.dirty = False
            HelperMethods.setEnabled(self.fileMenuActions[2:4], True)
            self.setTitle(fname)
            self.openSim()

    def addRecentFile(self, fname):

        if fname is None:
            return
        if not self.recentFiles.count(fname):
            self.recentFiles.insert(0, fname)
            while len(self.recentFiles) > 9:
                self.recentFiles.pop()

    def createToolBar(self):

        self.fileToolBar = self.addToolBar("File Tools")
        self.fileToolBar.setObjectName("FileToolBar")
        HelperMethods.addActions(self.fileToolBar, self.fileMenuActions[:-2])

    def simulationToolBar(self, numWidgets):

        if not hasattr(self, 'SimToolBar'):
            self.SimToolBar = QToolBar(self.tr("Simulation Tools"))
            self.SimToolBar.setObjectName("SimToolBar")
            self.SimToolBar.setAllowedAreas(
                Qt.TopToolBarArea | Qt.BottomToolBarArea | Qt.LeftToolBarArea | Qt.RightToolBarArea)

        self.SimToolBar.clear()
        HelperMethods.addActions(self.SimToolBar, self.simulationMenuActions[0:numWidgets])
        self.addToolBar(Qt.TopToolBarArea, self.SimToolBar)

    def geometryToolBar(self, reset=False, LoadImage=False):
        if not hasattr(self, 'GeometryToolBar'):
            self.GeometryToolBar = QToolBar(self.tr("Geometry Tools"))
            self.GeometryToolBar.setObjectName("GeometryToolBar")
            self.GeometryToolBar.setAllowedAreas(
                Qt.TopToolBarArea | Qt.BottomToolBarArea | Qt.LeftToolBarArea | Qt.RightToolBarArea)

        self.GeometryToolBar.clear()
        if LoadImage:
            HelperMethods.addActions(self.GeometryToolBar, self.geometryMenuActions[4])
            self.addToolBar(Qt.RightToolBarArea, self.GeometryToolBar)
            return

        if reset:
            return
        else:
            HelperMethods.addActions(self.GeometryToolBar, self.geometryMenuActions[2:])
            # self.addToolBarBreak(Qt.TopToolBarArea)
            self.addToolBar(Qt.RightToolBarArea, self.GeometryToolBar)

    def setupGraphicView(self):

        self.GraphicView = GraphicView(self)
        self.setCentralWidget(self.GraphicView)

    def setupStatusBar(self):

        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)

        self.statusBarWidget = StatusBarWidget()
        self.connect(self.statusBarWidget.zoomSpinBox, SIGNAL("valueChanged(int)"), self.GraphicView,
                     SLOT("setZoom(int)"))

        self.status.insertPermanentWidget(0, self.statusBarWidget.statusFrame)
        self.status.showMessage("Ready", 15000)

        self.connect(self.statusBarWidget.StopStatusBar, SIGNAL("clicked()"), self.stopFunc)
        self.connect(self.statusBarWidget.StartPauseStatusBar, SIGNAL("clicked()"), self.startPauseFunc)

        self.StopSimulation = False
        self.PauseSimulation = False

    def tree(self):

        self.treeWidget = TreeWidget()
        self.treeDockWidget = QDockWidget(self.tr("Simulation Parameters"))
        self.treeDockWidget.setObjectName("treeDockWidget")
        self.treeDockWidget.setWidget(self.treeWidget)
        self.treeDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.treeWidget.deleteDone.sig.connect(self.updateUI)

    def initSettings(self):

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles")
        size = settings.value("MainWindow/Size", QSize(900, 600))
        position = settings.value("MainWindow/Position", QPoint(50, 50))
        self.restoreState(settings.value("MainWindow/State"))
        zoom = float(settings.value("Graphics/Zoom", 100.0))

        if self.recentFiles is None:
            self.recentFiles = []

        self.resize(size)
        self.move(position)

        # self.GraphicView.setupZoom(zoom)
        self.statusBarWidget.zoomSpinBox.setValue(zoom)

    def resetSettings(self):

        settings = QSettings()
        settings.clear()
        self.reset = True
        self.close()

    def fileNew(self):

        if not self.okToContinue():
            return

        fname = managerFile.fileNew(self.filename)

        if fname:
            HelperMethods.setEnabled(self.fileMenuActions[2:4], True)
            self.filename = fname
            self.dirty = True
            self.setTitle(fname)
            self.newSim()

    def fileOpen(self):

        if not self.okToContinue():
            return

        fname = managerFile.fileOpen(self.filename)
        if fname:
            self.loadFile(fname)

    def fileSave(self):

        if self.filename is None:
            self.fileSaveAs()
        else:
            self.dirty = False
            self.saveSim()

    def fileSaveAs(self):

        fname = managerFile.fileSaveAs(self.filename)

        if fname:
            if "." not in fname:
                fname += ".sim"

            self.addRecentFile(fname)
            self.filename = fname
            self.setTitle(self.filename)
            self.saveSim()

    def exportMatlab(self):

        fname = managerFile.exportMatlab(self.filename)

        if fname:
            if "." not in fname:
                fname += ".mat"

            self.exportSimulation(fname)

    def initSim(self):

        self.createObjects()
        self.treeWidget.clear()

        self.statusBarWidget.zoomSpinBox.setVisible(False)
        self.GraphicView.clearUpdate()
        self.removeDockWidget(self.treeDockWidget)

    def newSim(self):

        self.initSim()

        self.simulationToolBar(1)
        self.geometryToolBar(reset=True)

        HelperMethods.setEnabled(self.menuNew_Simulation_Scenario, True)
        HelperMethods.setEnabled(self.geometryMenuActions[0], True)
        HelperMethods.setEnabled(self.geometryMenuActions[4], True)

        # Show loadImage in Geometric Toolbar
        self.geometryToolBar(LoadImage=True)
        self.updateUI()

    def openSim(self):
        data2load = {}
        data2load = loadmat(self.filename, squeeze_me=True, struct_as_record=False)

        self.OpenSimFile = True
        if "Info" in data2load:
            self.SimNDT_Info = HelperMethods.mat2Obj(data2load["Info"], Info())

        if "Scenario" in data2load:
            Width = getattr(data2load["Scenario"], 'Width')
            Height = getattr(data2load["Scenario"], 'Height')
            Pixel_mm = getattr(data2load["Scenario"], 'Pixel_mm')
            Label = getattr(data2load["Scenario"], 'Label')
            self.SimNDT_Scenario = Scenario(Width=Width, Height=Height, Pixel_mm=Pixel_mm, Label=Label)
            self.SimNDT_Scenario = HelperMethods.mat2Obj(data2load["Scenario"], self.SimNDT_Scenario)

        self.SimNDT_Materials = HelperMethods.loadDataFromList(data2load, 'Materials', Material())
        self.SimNDT_Boundaries = HelperMethods.loadDataFromList(data2load, "Boundaries", Boundary())
        self.SimNDT_Transducers = HelperMethods.loadDataFromList(data2load, "Transducers", Transducer())

        geoLabels = ["ellipse", "circle", "square", "rectangle"]
        geoObjects = [Ellipse(), Circle(), Square(), Rectangle()]
        self.SimNDT_ObjectList = HelperMethods.loadDataFromListWithLabels(data2load, 'GeometricObjects', geoLabels,
                                                                          geoObjects)

        ConcreteLabels = ["Concrete2Phase", "Concrete2PhaseImmersion", "Concrete3Phase", "Concrete3PhaseImmersion"]
        ConcreteObjects = [Concrete2Phase(), Concrete2PhaseImmersion(), Concrete3Phase(), Concrete3PhaseImmersion()]

        if "ConcreteMicrostructure" in data2load:
            self.SimNDT_ConcreteMicrostructure = HelperMethods.loadDataWithLabels(data2load, 'ConcreteMicrostructure',
                                                                                  ConcreteLabels, ConcreteObjects)

        if "Inspection" in data2load:
            inspLabels = ['Transmission', 'PulseEcho', 'LinearScan', 'Tomography']
            inspObjects = [Transmission(), PulseEcho(), LinearScan(), Tomography()]
            self.SimNDT_Inspection = HelperMethods.loadDataWithLabels(data2load, "Inspection", inspLabels, inspObjects)

        if "Source" in data2load:
            self.SimNDT_Source = HelperMethods.mat2Obj(data2load["Source"], Source())

        if "Signal" in data2load:
            self.SimNDT_Signal = HelperMethods.mat2Obj(data2load["Signal"], Signals())

        if "Simulation" in data2load:
            self.SimNDT_Simulation = HelperMethods.mat2Obj(data2load["Simulation"], Simulation())

        if "Receivers" in data2load:
            self.SimNDT_Receivers = HelperMethods.mat2Obj(data2load["Receivers"], Receivers())

            self.setPlotInspectionsMenu()

        self.updateUI()

    def saveSim(self):
        self._saveSimulation(self.filename)

    def exportSimulation(self, filename):
        self._saveSimulation(filename)

    def _saveSimulation(self, filename):

        data2save = {}

        if self.SimNDT_Info is not None:
            data2save['Info'] = self.SimNDT_Info

        if self.SimNDT_Scenario is not None:
            data2save['Scenario'] = self.SimNDT_Scenario

        if self.SimNDT_ObjectList is not None:
            data2save["GeometricObjects"] = self.SimNDT_ObjectList

        if self.SimNDT_ConcreteMicrostructure is not None:
            data2save["ConcreteMicrostructure"] = self.SimNDT_ConcreteMicrostructure

        if self.SimNDT_Materials is not None:
            data2save["Materials"] = self.SimNDT_Materials

        if self.SimNDT_Boundaries is not None:
            data2save["Boundaries"] = self.SimNDT_Boundaries

        if self.SimNDT_Transducers is not None:
            data2save["Transducers"] = self.SimNDT_Transducers

        if self.SimNDT_Inspection is not None:
            data2save["Inspection"] = self.SimNDT_Inspection

        if self.SimNDT_Source is not None:
            data2save["Source"] = self.SimNDT_Source

        if self.SimNDT_Signal is not None:
            data2save["Signal"] = self.SimNDT_Signal

        if self.SimNDT_Simulation is not None:
            data2save["Simulation"] = self.SimNDT_Simulation

        if self.SimNDT_Receivers is not None:
            data2save["Receivers"] = self.SimNDT_Receivers

        savemat(filename, data2save, appendmat=False)
        self.dirty = False

    def stopFunc(self):
        self.StopSimulation = True

    def startPauseFunc(self):
        self.PauseSimulation = not self.PauseSimulation
        if self.PauseSimulation:
            self.statusBarWidget.StartPauseStatusBar.setIcon(QIcon(":/play.png"))
        else:
            self.statusBarWidget.StartPauseStatusBar.setIcon(QIcon(":/pause.png"))

    def helpAbout(self):

        QMessageBox.about(self, "About SimNDT",
                          """ <b> SimNDT </b> v{0}, date: {1}
                              <p> Copyright &#169; 2014 M.Molero </p>
                              <p> Ultrasonic Simulation Software
                              <p> info:
                              <p> miguel.molero@gmail.com
                              <p> https://sites.google.com/site/miguelmolero/
                              <p>
                              <p> if you use SimNDT Software in your research, we would appreciate the citation of the following article:
                              <p> M.Molero, U. Iturraran-Viveros, S. Sofia, M.G. Hernandez,
                              <p> Optimized OpenCL implementation of the Elastodynamic Finite Integration Technique for viscoelastic media,
                              <p> Computer Physics Communications Volume 185, Issue 10, October 2014, Pages 2683-2696
                          """.format(info.version, info.date))

    def helpHelp(self):

        dlg = HelpForm("index.html", self)
        dlg.show()

    def closeEvent(self, event):

        if self.reset:
            return

        if self.okToContinue():
            settings = QSettings()
            filename = self.filename if self.filename is not None else None
            settings.setValue("LastFile", filename)
            recentFiles = self.recentFiles if self.recentFiles else None
            settings.setValue("RecentFiles", recentFiles)
            settings.setValue("MainWindow/Size", self.size())
            settings.setValue("MainWindow/Position", self.pos())
            settings.setValue("MainWindow/State", self.saveState())
            settings.setValue("Graphics/Zoom", self.GraphicView.getZoom())

        else:
            event.ignore()

    def setPlotInspectionsMenu(self):

        HelperMethods.setEnabled(self.actionPlot_Receiver_Signals_SingleLaunch, False)
        HelperMethods.setEnabled(self.actionPlot_Receiver_Signals_Spectra, False)

        HelperMethods.setEnabled(self.actionPlot_Receivers_Signals_LinearScan, False)
        HelperMethods.setEnabled(self.actionPlot_Receivers_Signals_Tomography, False)

        Name = self.SimNDT_Inspection.Name
        if Name == "Transmission" or Name == "PulseEcho":
            self.menuPlotting_Tools.menuAction().setVisible(True)
            HelperMethods.setEnabled(self.actionPlot_Receiver_Signals_SingleLaunch, True)
        elif Name == "LinearScan":
            self.menuPlotting_Tools.menuAction().setVisible(True)
            HelperMethods.setEnabled(self.actionPlot_Receivers_Signals_LinearScan, True)
        elif Name == 'Tomography':
            self.menuPlotting_Tools.menuAction().setVisible(True)
            HelperMethods.setEnabled(self.actionPlot_Receivers_Signals_Tomography, True)

    def updateUI(self):

        if self.SimNDT_Scenario is not None:
            try:
                self.GraphicView.imshow(self.SimNDT_Scenario.I)
            except Exception as e:
                msgBox = WarningParms("Unable to display GRAPHICS!!!. Incompatible Graphic Card, %s" % e)
                if msgBox.exec_():
                    sys.exit()

            HelperMethods.setEnabled(self.menuNew_Simulation_Scenario, True)
            HelperMethods.setEnabled(self.fileMenuActions[2:5], True)
            HelperMethods.setEnabled(self.geometryMenuActions[0:], True)
            HelperMethods.setEnabled(self.configurationMenuActions[0], True)

            self.addDockWidget(Qt.LeftDockWidgetArea, self.treeDockWidget)
            self.treeDockWidget.show()

            self.geometryToolBar()
            self.simulationToolBar(2)
            self.statusBarWidget.zoomSpinBox.setVisible(True)

        if self.SimNDT_Materials is not None:
            HelperMethods.setEnabled(self.configurationMenuActions[1], True)
            self.simulationToolBar(3)

        if self.SimNDT_Boundaries is not None:

            aa = np.size(self.SimNDT_Scenario.Iabs)
            if np.size(self.SimNDT_Scenario.Iabs) == 1:
                self.GraphicView.imshow(self.SimNDT_Scenario.I)
            else:
                self.GraphicView.imshow(self.SimNDT_Scenario.Iabs)
            HelperMethods.setEnabled(self.menuInspection_Setup, True)
            HelperMethods.setEnabled(self.inspectionMenuActions[:], True)
            self.simulationToolBar(6)

        if self.SimNDT_Inspection is not None:
            HelperMethods.setEnabled(self.simulationMenuActions[6], True)
            self.simulationToolBar(7)

        if self.SimNDT_Simulation is not None:
            HelperMethods.setEnabled(self.simulationMenuActions[7], True)
            self.simulationToolBar(8)

        if self.SimNDT_Check:
            HelperMethods.setEnabled(self.actionRun_Simulation, True)
            if not self.OpenSimFile:
                self.simulationToolBar(9)

        self.treeWidget.update(self.SimNDT_Scenario,
                               self.SimNDT_ObjectList,
                               self.SimNDT_Materials,
                               self.SimNDT_Boundaries,
                               self.SimNDT_Inspection,
                               self.SimNDT_Source,
                               self.SimNDT_Transducers,
                               self.SimNDT_Signal,
                               self.SimNDT_Simulation)
