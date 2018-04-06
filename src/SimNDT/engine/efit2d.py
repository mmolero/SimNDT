from SimNDT.engine.engineBase import EngineBase

try:
    import SimNDT.engine.efit2dcython as EFIT2DCython
except:
    print("error in importation for Serial EFIT2D")

from SimNDT.core.material import Material
from SimNDT.core.constants import BC

import copy
import numpy as np

global ErrorImportCL

try:
    import pyopencl as cl

    ErrorImportCL = False
except ImportError:
    ErrorImportCL = True

c11 = 4350 * 4350 * 7750
c12 = 4350 * 4350 * 7750 - 2260 * 2260 * 7750
c22 = c11
c44 = 2260 * 2260 * 7750
pzt = Material("pzt", 7750.0, c11, c12, c22, c44)


class EFIT2D(EngineBase):
    def __init__(self, simPack, Platform):
        EngineBase.__init__(self, simPack, Platform)

        self.max_value = 0.0
        self._Receiver = False

    def setup_CL(self):
        if self.Platform == "OpenCL":
            self.initFieldsCL()

    def materialSetup(self):

        Materials = copy.deepcopy(self.simPack.Materials)
        MRI, NRI = np.shape(self.simPack.Simulation.Im)

        # Condicion de vacio si uno de los materiales es aire
        for n in range(len(Materials)):
            if Materials[n].Rho < 2.0:
                Materials[n].Rho = 10e23
                Materials[n].C11 = 1e-20
                Materials[n].C12 = 1e-20
                Materials[n].C22 = 1e-20
                Materials[n].C44 = 1e-20
                Materials[n].Eta_v = 1e-20
                Materials[n].Eta_s = 1e-20
            # verificar que no sea cero exactamente
            if Materials[n].C44 == 0:
                Materials[n].C44 = 1e-30
            if Materials[n].Eta_s == 0:
                Materials[n].Eta_s = 1e-30

        self.Rho = np.zeros((MRI, NRI), dtype=np.float32)
        self.C11 = np.zeros((MRI, NRI), dtype=np.float32)
        self.C12 = np.zeros((MRI, NRI), dtype=np.float32)
        self.C22 = np.zeros((MRI, NRI), dtype=np.float32)
        self.C44 = np.ones((MRI, NRI), dtype=np.float32) * 1e-30
        self.Eta_v = np.zeros((MRI, NRI), dtype=np.float32)
        self.Eta_s = np.zeros((MRI, NRI), dtype=np.float32)

        for n in range(len(Materials)):
            ind = np.nonzero(self.simPack.Simulation.Im == Materials[n].Label)
            self.Rho[ind] = Materials[n].Rho
            self.C11[ind] = Materials[n].C11
            self.C12[ind] = Materials[n].C12
            self.C22[ind] = Materials[n].C22
            self.C44[ind] = Materials[n].C44
            self.Eta_v[ind] = Materials[n].Eta_v
            self.Eta_s[ind] = Materials[n].Eta_s

        # Find the base materials
        for i, item in enumerate(Materials):
            if item.Label == 0:
                base_material = i

        # Set material in boundaries
        ind = np.nonzero(self.simPack.Simulation.Im == 255.0)
        self.Rho[ind] = Materials[base_material].Rho
        self.C11[ind] = Materials[base_material].C11
        self.C12[ind] = Materials[base_material].C12
        self.C22[ind] = Materials[base_material].C22
        self.C44[ind] = Materials[base_material].C44
        self.Eta_v[ind] = Materials[base_material].Eta_v
        self.Eta_s[ind] = Materials[base_material].Eta_s

    def initFields(self):

        MRI, NRI = np.shape(self.simPack.Simulation.Im)
        Signal = self.simPack.Signal
        t = self.simPack.Simulation.t
        self.source = Signal.generate(t)

        self.Vx = np.zeros((MRI, NRI), dtype=np.float32)
        self.Vy = np.zeros((MRI, NRI), dtype=np.float32)
        self.Txx = np.zeros((MRI, NRI), dtype=np.float32)
        self.Txy = np.zeros((MRI, NRI), dtype=np.float32)
        self.Tyy = np.zeros((MRI, NRI), dtype=np.float32)
        self.DVx = np.zeros((MRI, NRI), dtype=np.float32)
        self.DVy = np.zeros((MRI, NRI), dtype=np.float32)
        self.ABS = np.ones((MRI, NRI), dtype=np.float32)
        self.SV = np.zeros((MRI, NRI), dtype=np.float32)

    def staggeredProp(self):

        MRI, NRI = np.shape(self.simPack.Simulation.Im)

        BXtemp = np.zeros((MRI, NRI), dtype=np.float32)
        BYtemp = np.zeros((MRI, NRI), dtype=np.float32)
        self.BX = np.zeros((MRI, NRI), dtype=np.float32)
        self.BY = np.zeros((MRI, NRI), dtype=np.float32)
        self.C44_Eff = np.zeros((MRI, NRI), dtype=np.float32)

        BXtemp[:, :] = 1.0 / self.Rho[:, :]
        BYtemp[:, :] = 1.0 / self.Rho[:, :]

        self.BX[:-2, :] = 0.5 * (BXtemp[1:-1, :] + BXtemp[:-2, :])
        self.BX[-2, :] = np.copy(BXtemp[-2, :])

        self.BY[:, :-2] = 0.5 * (BYtemp[:, 1:-1] + BYtemp[:, :-2])
        self.BY[:, -2] = np.copy(BYtemp[:, -2])

        self.C44_Eff[:-2, :-2] = 4. / (
            (1. / self.C44[:-2, :-2]) + (1. / self.C44[1:-1, :-2]) + (1. / self.C44[:-2, 1:-1]) + (
                1. / self.C44[1:-1, 1:-1]))

        self.Eta_vs = np.zeros((MRI, NRI), dtype=np.float32)
        self.Eta_ss = np.zeros((MRI, NRI), dtype=np.float32)
        self.Eta_vs = self.Eta_v + 2 * self.Eta_s
        self.Eta_ss[:-2, :-2] = 4. / (
            (1. / self.Eta_s[:-2, :-2]) + (1. / self.Eta_s[1:-1, :-2]) + (1. / self.Eta_s[:-2, 1:-1]) + (
                1. / self.Eta_s[1:-1, 1:-1]))

    def applyBoundaries(self):
        Materials = copy.deepcopy(self.simPack.Materials)
        MRI, NRI = np.shape(self.simPack.Simulation.Im)

        APARA = 0.015

        Top = int(self.simPack.Simulation.TapGrid[0])
        Bottom = int(self.simPack.Simulation.TapGrid[1])
        Left = int(self.simPack.Simulation.TapGrid[2])
        Right = int(self.simPack.Simulation.TapGrid[3])

        _Top = Top - np.arange(0, Top)
        _Bottom = np.arange(MRI - Bottom + 1, MRI) - MRI + Bottom - 1
        _Left = Left - np.arange(0, Left)
        _Right = np.arange(NRI - Right + 1, NRI) - NRI + Right - 1

        Boundaries = self.simPack.Boundary
        for boundary in Boundaries:
            if boundary.Name == "Top" and boundary.BC == BC.AirLayer:
                self.BX[0:Top, :] = 0.0
                self.BY[0:Top, :] = 0.0
                self.C11[0:Top, :] = 0.0
                self.C12[0:Top, :] = 0.0
                self.C22[0:Top, :] = 0.0
                self.C44_Eff[0:Top, :] = 0.0
                self.Eta_vs[0:Top, :] = 0.0
                self.Eta_ss[0:Top, :] = 0.0

            if boundary.Name == "Bottom" and boundary.BC == BC.AirLayer:
                self.BX[MRI - Bottom:, :] = 0.0
                self.BY[MRI - Bottom:, :] = 0.0
                self.C11[MRI - Bottom:, :] = 0.0
                self.C12[MRI - Bottom:, :] = 0.0
                self.C22[MRI - Bottom:, :] = 0.0
                self.C44_Eff[MRI - Bottom:, :] = 0.0
                self.Eta_vs[MRI - Bottom:, :] = 0.0
                self.Eta_ss[MRI - Bottom:, :] = 0.0

            if boundary.Name == "Left" and boundary.BC == BC.AirLayer:
                self.BX[:, 0:Left] = 0.0
                self.BY[:, 0:Left] = 0.0
                self.C11[:, 0:Left] = 0.0
                self.C12[:, 0:Left] = 0.0
                self.C22[:, 0:Left] = 0.0
                self.C44_Eff[:, 0:Left] = 0.0
                self.Eta_vs[:, 0:Left] = 0.0
                self.Eta_ss[:, 0:Left] = 0.0
            if boundary.Name == "Right" and boundary.BC == BC.AirLayer:
                self.BX[:, NRI - Right:] = 0.0
                self.BY[:, NRI - Right:] = 0.0
                self.C11[:, NRI - Right:] = 0.0
                self.C12[:, NRI - Right:] = 0.0
                self.C22[:, NRI - Right:] = 0.0
                self.C44_Eff[:, NRI - Right:] = 0.0
                self.Eta_vs[:, NRI - Right:] = 0.0
                self.Eta_ss[:, NRI - Right:] = 0.0

        for j in range(0, NRI):
            self.ABS[0:Top, j] = np.exp(- ((APARA * _Top) ** 2))
            self.ABS[MRI - Bottom + 1:, j] = np.exp(- ((APARA * _Bottom) ** 2))
        for i in range(0, MRI):
            self.ABS[i, 0:Left] = np.exp(- ((APARA * _Left) ** 2))
            self.ABS[i, NRI - Right + 1:] = np.exp(- ((APARA * _Right) ** 2))

    def sourceSetup(self):

        longitudinal = self.simPack.Source.Longitudinal
        shear = self.simPack.Source.Shear

        Pressure = self.simPack.Source.Pressure
        Displacement = self.simPack.Source.Displacement

        if Pressure and not Displacement:
            self.typeSource = 0
        elif not Pressure and Displacement:
            self.typeSource = 1
        elif Pressure and Displacement:
            self.typeSource = 2
        else:
            self.typeSource = 0

        if longitudinal and not shear:
            self.typeWave = np.int32(0)
        elif not longitudinal and shear:
            self.typeWave = np.int32(1)
        elif longitudinal and shear:
            self.typeWave = np.int32(2)
        else:
            self.typeWave = np.int32(0)

        self.Amplitude = self.simPack.Signal.Amplitude
        XL = self.simPack.Inspection.XL
        YL = self.simPack.Inspection.YL
        NX = np.size(XL, 0)

        IsPZT = self.simPack.Transducers[0].PZT

        size1 = int((self.simPack.Simulation.TapGrid[0]))
        size2 = int((self.simPack.Simulation.TapGrid[1]))

        for IT in range(-size1, 0):
            for m in range(0, NX):
                xl = int(XL[m, 0])
                yl = int(YL[m, 0])

                self.BX[xl + IT, yl] = 1.0 / pzt.Rho if IsPZT else 0
                self.BY[xl + IT, yl] = 1.0 / pzt.Rho if IsPZT else 0
                self.C11[xl + IT, yl] = pzt.C11 if IsPZT else 0
                self.C12[xl + IT, yl] = pzt.C12 if IsPZT else 0
                self.C22[xl + IT, yl] = pzt.C22 if IsPZT else 0
                self.C44[xl + IT, yl] = pzt.C44 if IsPZT else 0

        if self.simPack.Inspection.Name == "Transmission":
            for IT in range(1, size2):
                for m in range(0, NX):
                    xl = int(XL[m, 1])
                    yl = int(YL[m, 1])
                    self.BX[xl + IT, yl] = 1.0 / pzt.Rho if IsPZT else 0
                    self.BY[xl + IT, yl] = 1.0 / pzt.Rho if IsPZT else 0
                    self.C11[xl + IT, yl] = pzt.C11 if IsPZT else 0
                    self.C12[xl + IT, yl] = pzt.C12 if IsPZT else 0
                    self.C22[xl + IT, yl] = pzt.C22 if IsPZT else 0
                    self.C44[xl + IT, yl] = pzt.C44 if IsPZT else 0

    def simSetup(self):
        self.MRI, self.NRI = np.shape(self.simPack.Simulation.Im)
        XL = self.simPack.Inspection.XL
        YL = self.simPack.Inspection.YL

        self.NX = np.size(XL, 0)
        self.XL = np.copy(np.int32(XL[:, 0]))
        self.YL = np.copy(np.int32(YL[:, 0]))

        if self.simPack.Transducers[0].Window and not self.simPack.Transducers[0].PointSource:
            self.win = np.float32(1.0 - np.cos(2 * np.pi * np.arange(0, self.NX) / (self.NX + 1)))
        else:
            self.win = np.ones((self.NX,), dtype=np.float32)

    def initFieldsCL(self):

        self.Txx_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.Txx)
        self.Tyy_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.Tyy)
        self.Txy_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.Txy)
        self.Vx_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.Vx)
        self.Vy_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.Vy)

        self.DVx_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.DVx)
        self.DVy_buf = cl.Buffer(self.ctx, self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf=self.DVy)

        self.ABS_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.ABS)
        self.BX_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.BX)
        self.BY_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.BY)
        self.C11_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.C11)
        self.C12_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.C12)
        self.C44_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.C44_Eff)

        self.ETA_vs_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.Eta_vs)
        self.ETA_s_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.Eta_s)
        self.ETA_ss_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.Eta_ss)

        self.XL_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.XL)
        self.YL_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.YL)

        self.WIN_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.win)

        if not self.simPack.Inspection.Name == "Tomography":
            self._Receiver = True
            XL = self.simPack.Inspection.XL
            YL = self.simPack.Inspection.YL
            self.receiver_buf = cl.Buffer(self.ctx, self.mf.WRITE_ONLY | self.mf.COPY_HOST_PTR,
                                          hostbuf=self.receiver_signals)
            self.XXL = np.copy(np.int32(XL[:, 1]))
            self.YYL = np.copy(np.int32(YL[:, 1]))
            self.XXL_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.XXL)
            self.YYL_buf = cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.YYL)

        self.program = cl.Program(self.ctx, self.kernel()).build()

    def receiverSetup(self):
        TimeSteps = int(self.simPack.Simulation.TimeSteps)
        N_IR = np.size(self.simPack.Inspection.IR, 1)
        self.receiver_signals = np.zeros((TimeSteps, N_IR - 1), dtype=np.float32)

    def receivers(self, Var, Var_buf):

        if self._Receiver:
            self.program.Receiver_EFIT2D(self.queue, (self.NX,), None, self.Txx_buf, self.receiver_buf,
                                         np.int32(self.n),
                                         self.XXL_buf, self.YYL_buf).wait()
        else:
            cl.enqueue_copy(self.queue, Var, Var_buf)
            self.receiver_signals[self.n, :] = self.simPack.Inspection.getReceivers(Var)

    def saveOutput(self):
        if self._Receiver:
            cl.enqueue_copy(self.queue, self.receiver_signals, self.receiver_buf).wait()

    def receiversSerial(self, Var):
        self.receiver_signals[self.n, :] = self.simPack.Inspection.getReceivers(Var)

    def run(self):

        y = np.float32(self.source[self.n])
        self.program.Velocity_EFIT2D_Voigt(self.queue, (self.NRI, self.MRI,), None,
                                           self.Txx_buf, self.Txy_buf, self.Tyy_buf,
                                           self.Vx_buf, self.Vy_buf, self.DVx_buf, self.DVy_buf,
                                           self.BX_buf, self.BY_buf, self.ABS_buf, self.ddx).wait()

        if self.typeSource == 1 or self.typeSource == 2:
            self.program.Source_Vel_EFIT2D(self.queue, (self.NX,), None,
                                           self.Vx_buf,
                                           self.Vy_buf,
                                           self.XL_buf,
                                           self.YL_buf,
                                           y, self.typeWave, self.WIN_buf).wait()

        self.program.Stress_EFIT2D_Voigt(self.queue, (self.NRI, self.MRI,), None,
                                         self.Txx_buf, self.Txy_buf, self.Tyy_buf,
                                         self.Vx_buf, self.Vy_buf, self.DVx_buf, self.DVy_buf,
                                         self.C11_buf, self.C12_buf, self.C44_buf, self.ETA_vs_buf,
                                         self.ETA_s_buf, self.ETA_ss_buf, self.ABS_buf).wait()

        if self.typeSource == 0 or self.typeSource == 2:
            self.program.Source_EFIT2D(self.queue, (self.NX,), None,
                                       self.Txx_buf,
                                       self.Tyy_buf,
                                       self.Txy_buf,
                                       self.XL_buf,
                                       self.YL_buf,
                                       y, self.typeWave, self.WIN_buf).wait()

        self.receivers(self.Txx, self.Txx_buf)

    def runGL(self):
        cl.enqueue_copy(self.queue, self.Vx, self.Vx_buf)
        cl.enqueue_copy(self.queue, self.Vy, self.Vy_buf)
        self.SV = np.sqrt(self.Vx ** 2 + self.Vy ** 2)
        value = np.max(np.abs(self.SV))
        self.max_value = self.max_value if self.max_value >= value else value
        self.SV = 20. * np.log10(np.abs(self.SV) / self.max_value + 1e-40)

    def runGLSerial(self, step=50):

        vx = np.copy(self.Vx)
        vy = np.copy(self.Vy)

        self.SV = np.sqrt(vx ** 2 + vy ** 2)
        value = np.max(np.abs(self.SV))
        self.max_value = self.max_value if self.max_value >= value else value
        self.SV = 20. * np.log10(np.abs(self.SV) / self.max_value + 1e-40)

    def runSerial(self):

        y = np.float32(self.source[self.n])

        self.Vx, self.Vy, self.DVx, self.DVy = EFIT2DCython.velocityVoigt(self.Txx, self.Txy, self.Tyy,
                                                                          self.Vx, self.Vy, self.DVx, self.DVy,
                                                                          self.BX, self.BY, self.ABS, self.ddx,
                                                                          self.dt)

        if self.typeSource == 1 or self.typeSource == 2:
            self.Vx, self.Vy = EFIT2DCython.sourceVel(self.Vx, self.Vy, self.XL, self.YL, y, self.typeWave, self.win,
                                                      self.dtdxx)

        self.Txx, self.Tyy, self.Txy = EFIT2DCython.stressVoigt(self.Txx, self.Txy, self.Tyy,
                                                                self.Vx, self.Vy, self.DVx, self.DVy,
                                                                self.C11, self.C12, self.C44_Eff,
                                                                self.Eta_vs, self.Eta_s, self.Eta_ss, self.ABS,
                                                                self.dtx)

        if self.typeSource == 0 or self.typeSource == 2:
            self.Txx, self.Tyy = EFIT2DCython.sourceStress(self.Txx, self.Tyy, self.XL, self.YL, y, self.typeWave,
                                                           self.win, self.dtdxx)

        self.receiversSerial(self.Txx)

    def kernel(self):

        macro = """
					 #define MRI		%s
					 #define NRI		%s
					 #define ind(i, j)	( ( (i)*NRI) + (j) )
					 #define dtx		%gf
					 #define dtdxx		%gf
					 #define Stencil	2
					 #define NX			%s
					 #define dt			%gf



		""" % (str(self.MRI), str(self.NRI), self.dtx, self.dtdxx,
               str(self.NX), self.dt)

        return macro + """


			__kernel void Receiver_EFIT2D(__global float *Buffer, __global float *receiver, const int t,
							              __global const int *XXL, __global const int *YYL){


			  __private float _tmp = 0.0f;


			   for (int i=0; i<get_global_size(0); ++i)
		       {
				 _tmp +=  Buffer[ind(XXL[i],YYL[i])];
			   }
			   receiver[t] = _tmp/(float)get_global_size(0);
            }



			__kernel void Source_Vel_EFIT2D(__global float *Vx, __global float *Vy, 
										__global const int	 *XL, __global const int *YL,  
										  const float source, const int Stype, __global const float *win){

					 uint m =  get_global_id(0);

					 int ix = XL[m];
					 int iy = YL[m];
					 if (Stype ==0){
					  Vx[ind(ix,iy)]   -= (source*dtdxx)*win[m];
					 }
					else if (Stype ==1){
					  Vy[ind(ix,iy)]   -= (source*dtdxx)*win[m];
					 }
					else if (Stype ==2){
					  Vx[ind(ix,iy)]   -= (source*dtdxx)*win[m];
					  Vy[ind(ix,iy)]   -= (source*dtdxx)*win[m];
					 }

			   }



			__kernel void Source_EFIT2D(__global float *Txx, __global float *Tyy, __global float *Txy,
										__global const int	 *XL, __global const int *YL,  
										  const float source, const int Stype,__global const float *win){

					 uint m =  get_global_id(0);

					 int ix = XL[m];
					 int iy = YL[m];
					 if (Stype ==0){
					  Txx[ind(ix,iy)]	-= (source*dtdxx)*win[m];
					  //Txy[ind(ix,iy)]	   = 0;
					 }
					else if (Stype ==1){
					  Tyy[ind(ix,iy)]	-= (source*dtdxx)*win[m];
					  //Txy[ind(ix,iy)]	   = 0;
					 }
					else if (Stype ==2){
					  Txx[ind(ix,iy)]	-= (source*dtdxx)*win[m];
					  Tyy[ind(ix,iy)]	-= (source*dtdxx)*win[m];
					  //Txy[ind(ix,iy)]	   = 0;
					 }

			   }


		  __kernel void Velocity_EFIT2D_Voigt( __global float *Txx, __global float *Txy, __global float *Tyy,
											   __global float *vx,	__global float *vy,
											   __global float *dvx, __global float *dvy,
											   __global const float *BX, __global const float *BY,
											   __global const float *ABS, const float ddx){

					int j = get_global_id(0);
					int i = get_global_id(1);


						  if (i <  MRI-1 && j>0){
								dvx[ind(i,j)]	 = (BX[ind(i,j)]*ddx)*( Txx[ind(i+1,j)] - Txx[ind(i,j)]	  + Txy[ind(i,j)] - Txy[ind(i,j-1)] );
								vx[ind(i,j)]	+= dt*dvx[ind(i,j)];
						  }

						  if (i > 0 &&	j< NRI-1){
								dvy[ind(i,j)]	 = (BY[ind(i,j)]*ddx)*( Txy[ind(i,j)]  - Txy[ind(i-1,j)] + Tyy[ind(i,j+1)] - Tyy[ind(i,j)]		 );
								vy[ind(i,j)]	+= dt*dvy[ind(i,j)];

						  }

						   barrier(CLK_GLOBAL_MEM_FENCE);
							// Apply absorbing boundary conditions
						   vx[ind(i,j)]	  *= ABS[ind(i,j)];
						   vy[ind(i,j)]	  *= ABS[ind(i,j)];


						 }


				__kernel void Stress_EFIT2D_Voigt(__global float *Txx, __global float *Txy, __global float *Tyy,
												  __global float *vx,  __global float *vy,
												  __global float *dvx, __global float *dvy,
												  __global const float *C11,   __global const float *C12, __global const float *C44,
												  __global const float *ETA_VS, __global const float *ETA_S, __global const float *ETA_SS,
												  __global const float *ABS) {


						int j = get_global_id(0);
						int i = get_global_id(1);


						if (i>0 &&	j>0 ){
								Txx[ind(i,j)] += (	( C11[ind(i,j)]* dtx )*(vx[ind(i,j)] - vx[ind(i-1,j)]) +
													( C12[ind(i,j)]* dtx )*(vy[ind(i,j)] - vy[ind(i,j-1)]) +
													( (ETA_VS[ind(i,j)])*dtx) * (dvx[ind(i,j)] - dvx[ind(i-1,j)]) +
													( (ETA_S [ind(i,j)])*dtx) * (dvy[ind(i,j)] - dvy[ind(i,j-1)]) );

								Tyy[ind(i,j)] += (	( C12[ind(i,j)]* dtx )*(vx[ind(i,j)] - vx[ind(i-1,j)]) +
													( C11[ind(i,j)]* dtx )*(vy[ind(i,j)] - vy[ind(i,j-1)]) +
													( (ETA_VS[ind(i,j)])*dtx) *(dvy[ind(i,j)] - dvy[ind(i,j-1)]) +
													( (ETA_S [ind(i,j)])*dtx) * (dvx[ind(i,j)] - dvx[ind(i-1,j)]) );
						 }

						 if (i<MRI-1  && j<NRI-1){
								Txy[ind(i,j)] +=	(  ( C44[ind(i,j)]	   * dtx )*(vx[ind(i,j+1)] - vx[ind(i,j)] + vy[ind(i+1,j)] - vy[ind(i,j)])		+
													   ( ETA_SS[ind(i,j)]  * dtx )*(dvx[ind(i,j+1)] - dvx[ind(i,j)] + dvy[ind(i+1,j)] - dvy[ind(i,j)] ) );
								 }

						  barrier(CLK_GLOBAL_MEM_FENCE);

						  Txx[ind(i,j)] *= ABS[ind(i,j)];
						  Tyy[ind(i,j)] *= ABS[ind(i,j)];
						  Txy[ind(i,j)] *= ABS[ind(i,j)];


				}



		"""
