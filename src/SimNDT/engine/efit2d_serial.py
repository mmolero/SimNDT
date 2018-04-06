#!/usr/bin/env python
# encoding: utf-8
"""
efit2d_serial.py

Created by Miguel Molero on 2013-10-08.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy						 as		np
from   scipy.weave   import inline

class EFIT2D_NP:
	
	def __init__(self, MRI, NRI, NX, dt, ddx, dtx, dtdxx):
		
		self.MRI   = MRI
		self.NRI   = NRI
		self.NX    = NX
		self.dt    = dt
		self.dtx   = dtx
		self.ddx   = ddx
		self.dtdxx = dtdxx 
	

	def sourceVel(self, Vx, Vy, XL, YL, source, Stype, win):

	
		if Stype ==0:
			Vx[XL[:],YL[:]]	-= source*self.dtdxx * win[:]
			
		elif Stype ==1:
			Vy[XL[:],YL[:]]	-= source*self.dtdxx * win[:]
			
		elif Stype ==2:
			Vx[XL[:],YL[:]]	-= source* self.dtdxx * win[:]
			Vy[XL[:],YL[:]]	-= source* self.dtdxx * win[:]


		return (Vx, Vy)

	def sourceStress(self, Txx, Tyy, XL, YL, source, Stype, win):

		if Stype ==0:
			Txx[XL[:],YL[:]]	-= source*self.dtdxx * win[:]
			
		elif Stype ==1:
			Tyy[XL[:],YL[:]]	-= source*self.dtdxx * win[:]
			
		elif Stype ==2:
			Txx[XL[:],YL[:]]	-= source* self.dtdxx * win[:]
			Tyy[XL[:],YL[:]]	-= source* self.dtdxx * win[:]


		return (Txx, Tyy)


	def velocityVoigt(self, Txx, Txy, Tyy, vx, vy, d_vx, d_vy, BX, BY, ABS):


		d_vx[:-1,1:]  = ( self.ddx * BX[:-1,1:] )*( Txx[1:,1:] - Txx[:-1,1:] + Txy[:-1,1:]- Txy[:-1,0:-1]);
		vx[:-1,1:]   +=	  self.dt  * d_vx[:-1,1:]
									 							  
		d_vy[1:,:-1] = (  self.ddx * BY[1:,:-1] )*( Txy[1:,:-1]	- Txy[0:-1,:-1] + Tyy[1:,1:] - Tyy[1:,:-1] );
		vy[1:,:-1]   +=    self.dt  * d_vy[1:,:-1]
									  
		vx[:,:]	  *= ABS[:,:]
		vy[:,:]	  *= ABS[:,:]					
						   
		return (vx, vy, d_vx, d_vy)


	def stressVoigt(self,Txx, Txy, Tyy, vx, vy,d_vx, d_vy, C11, C12, C44, ETA_VS, ETA_S, ETA_SS, ABS):
		
		Txx[1:,1:] += ( (self.dtx * C11[1:,1:])    * (vx[1:,1:]   - vx[0:-1,1:])     +
						(self.dtx * C12[1:,1:])    * (vy[1:,1:]   - vy[1:,0:-1])     +
						(self.dtx * ETA_VS[1:,1:]) * (d_vx[1:,1:] - d_vx[0:-1,1:])   +
						(self.dtx * ETA_S[1:,1:] ) * (d_vy[1:,1:] - d_vy[1:,0:-1]) )

		Tyy[1:,1:] += (	(self.dtx * C12[1:,1:] )   * (vx[1:,1:]   - vx[0:-1,1:])     +
					    (self.dtx * C11[1:,1:] )   * (vy[1:,1:]   - vy[1:,0:-1])     +
						(self.dtx * ETA_S[1:,1:])  * (d_vx[1:,1:] - d_vx[0:-1,1:])   +
					  	(self.dtx * ETA_VS[1:,1:]) * (d_vy[1:,1:] - d_vy[1:,0:-1]) ) 
								
		Txy[:-1,:-1] += ( (self.dtx * C44[:-1,:-1])   * (vx[:-1,1:] - vx[:-1,:-1] + vy[1:,:-1] - vy[:-1,:-1] ) + 
						  (self.dtx * ETA_SS[:-1,:-1])* (d_vx[:-1,1:] - d_vx[:-1,:-1] + d_vy[1:,:-1] - d_vy[:-1,:-1])	)
								
		Txx[:,:]	*= ABS[:,:]
		Tyy[:,:]	*= ABS[:,:]
		Txy[:,:]	*= ABS[:,:]
			

		return (Txx, Tyy, Txy)





class EFIT2D_Weave:
	
	def __init__(self, MRI, NRI, NX, dt, ddx, dtx, dtdxx):
		
		self.MRI   = MRI
		self.NRI   = NRI
		self.NX    = NX
		self.dt    = dt
		self.dtx   = dtx
		self.ddx   = ddx
		self.dtdxx = dtdxx 
	

	def sourceVel(self, Vx, Vy, XL, YL, source, Stype, win):

		NX	   = int(self.NX)
		NRI	   = int(self.NRI)
		Stype  = int(Stype)
		DTDXX  = np.float32(self.dtdxx)


		extra_code = """
							#define ind(i,j, N)	 ( ((N)*(i)) + (j) )
		"""

		code = """

				int ix, iy;
				for (int m=0; m<NX; m++)
				{
				   ix = (int)XL[m];
				   iy = (int)YL[m];
				   if (Stype ==0){
					  Vx[ind(ix,iy, NRI)]		-= ((float)source* (float)DTDXX)*win[m];
					}
					else if (Stype ==1){
						  Vy[ind(ix,iy, NRI)]	-= ((float)source* (float)DTDXX)*win[m];
					}
					else if (Stype ==2){
						  Vx[ind(ix,iy, NRI)]	-= ((float)source* (float)DTDXX)*win[m];
						  Vy[ind(ix,iy, NRI)]	-= ((float)source* (float)DTDXX)*win[m];
					 } 
				}
		"""

		variables = ['NRI', 'NX','DTDXX','Vx', 'Vy', 'XL', 'YL','source','Stype','win']
		inline(code, variables,	 support_code = extra_code, compiler='gcc')

		return (Vx, Vy)

	def sourceStress(self, Txx, Tyy, XL, YL, source, Stype, win):

		NX	   = int(self.NX)
		NRI	   = int(self.NRI)
		Stype  = int(Stype)
		dtdxx  = self.dtdxx

		extra_code = """
								#define ind(i,j, N)	 ( ((N)*(i)) + (j) )
		"""

		code = """

					int ix, iy;
					for (int m=0; m<NX; m++)
					{
					   ix = (int)XL[m];
					   iy = (int)YL[m];
					   if (Stype ==0){
						  Txx[ind(ix,iy, NRI)]		 -= ((float)source*(float)dtdxx)*win[m];
						}
						else if (Stype ==1){
							  Tyy[ind(ix,iy, NRI)]	 -= ((float)source*(float)dtdxx)*win[m];
						}
						else if (Stype ==2){
							  Txx[ind(ix,iy, NRI)]	 -= ((float)source*(float)dtdxx)*win[m];
							  Tyy[ind(ix,iy, NRI)]	 -= ((float)source*(float)dtdxx)*win[m];
						 } 
					}
		"""

		variables = ['NRI', 'NX','dtdxx','Txx', 'Tyy', 'XL', 'YL','source','Stype','win']
		inline(code, variables,	 support_code = extra_code, compiler='gcc')

		return (Txx, Tyy)


	def velocityVoigt(self, Txx, Txy, Tyy, vx, vy, d_vx, d_vy, BX, BY, ABS):

		NRI	 = int(self.NRI)
		MRI	 = int(self.MRI)
		DDX	 = np.float32(self.ddx)
		DT	 = np.float32(self.dt)

		extra_code = """

					#define ind(i,j, N)	 ( ((N)*(i)) + (j) )

		"""

		code = """

						for (int i=0; i<MRI; ++i){
							for (int j=0; j<NRI; ++j){

									 if(i<MRI-1 && j>0)
									 {
										d_vx[ind(i,j, NRI)] = ( ((float)DDX) * BX[ind(i,j,NRI)] )*( Txx[ind(i+1,j,NRI)] - Txx[ind(i,j,NRI)]	 + Txy[ind(i,j,NRI)]   - Txy[ind(i,j-1,NRI)] );
										vx[ind(i,j,NRI)]   +=	((float)DT)  * d_vx[ind(i,j, NRI)];
									 }

									 if(j<NRI-1 && i>0)
									  {
										d_vy[ind(i,j,NRI)] = (  (float)DDX *	BY[ind(i,j,NRI)] )*( Txy[ind(i,j,NRI)]	 - Txy[ind(i-1,j,NRI)] + Tyy[ind(i,j+1,NRI)] - Tyy[ind(i,j,NRI)] );
										vy[ind(i,j,NRI)]  +=	(float)DT *d_vy[ind(i,j, NRI)];
									  }
								}
						   }

							for (int i=0; i<MRI; ++i){
								for (int j=0; j<NRI; ++j){

									vx[ind(i,j,NRI)]	  *= ABS[ind(i,j,NRI)];
									vy[ind(i,j,NRI)]	  *= ABS[ind(i,j,NRI)];
								}
							}

		"""

		variables = ['NRI','MRI', 'DDX','DT','Txx', 'Txy', 'Tyy', 'vx', 'vy','d_vx','d_vy','BX', 'BY', 'ABS' ]
		inline(code, variables,	 support_code = extra_code, compiler='gcc')

		return (vx, vy, d_vx, d_vy)


	def stressVoigt(self,Txx, Txy, Tyy, vx, vy,d_vx, d_vy, C11, C12, C44, ETA_VS, ETA_S, ETA_SS, ABS):
		NRI	 = int(self.NRI)
		MRI	 = int(self.MRI)
		DTX	 = np.float32(self.dtx)


		extra_code = """
								#define ind(i,j, N)	 ( ((N)*(i)) + (j) )
		"""

		code = """

						for (int i=0; i<MRI; ++i){
							for (int j=0; j<NRI; ++j){
							  if((i>0 && j>0 )){
									 Txx[ind(i,j, NRI)] += (	( (float)DTX)*( C11[ind(i,j, NRI)] )*(vx[ind(i,j, NRI)] - vx[ind(i-1,j, NRI)]) +
																( (float)DTX)*( C12[ind(i,j, NRI)] )*(vy[ind(i,j, NRI)] - vy[ind(i,j-1, NRI)]) +
																( (float)DTX)*( ETA_VS[ind(i,j, NRI)])*(d_vx[ind(i,j, NRI)] - d_vx[ind(i-1,j, NRI)]) +
																( (float)DTX)*( ETA_S[ind(i,j, NRI)] )*(d_vy[ind(i,j, NRI)] - d_vy[ind(i,j-1, NRI)]) );

									 Tyy[ind(i,j, NRI)] += (	( (float)DTX)*( C12[ind(i,j, NRI)] )*(vx[ind(i,j, NRI)] - vx[ind(i-1,j, NRI)]) +
																( (float)DTX)*( C11[ind(i,j, NRI)] )*(vy[ind(i,j, NRI)] - vy[ind(i,j-1, NRI)]) +
																( (float)DTX)*( ETA_S[ind(i,j, NRI)] )*(d_vx[ind(i,j, NRI)] - d_vx[ind(i-1,j, NRI)])+
																( (float)DTX)*( ETA_VS[ind(i,j, NRI)] )*(d_vy[ind(i,j, NRI)] - d_vy[ind(i,j-1, NRI)]) );
								}								

									 if (i<MRI-1  && j<NRI-1){
										 Txy[ind(i,j, NRI)] += (  ( (float)DTX)*( C44[ind(i,j, NRI)] )*(vx[ind(i,j+1, NRI)] - vx[ind(i,j, NRI)] + vy[ind(i+1,j, NRI)] - vy[ind(i,j, NRI)] ) + 
																  ( (float)DTX)*( ETA_SS[ind(i,j, NRI)] )*(d_vx[ind(i,j+1, NRI)] - d_vx[ind(i,j, NRI)] + d_vy[ind(i+1,j, NRI)] - d_vy[ind(i,j, NRI)] )	);
									  }
							  } 
						  }	   

						 for (int i=0; i<MRI; ++i){
							for (int j=0; j<NRI; ++j){

								Txx[ind(i,j, NRI)]	*= ABS[ind(i,j, NRI)];
								Tyy[ind(i,j, NRI)]	*= ABS[ind(i,j, NRI)];
								Txy[ind(i,j, NRI)]	*= ABS[ind(i,j, NRI)];
							}
						  }
		"""

		variables = ['NRI','MRI', 'DTX','Txx', 'Txy', 'Tyy', 'vx', 'vy','d_vx','d_vy','C11', 'C12', 'C44','ETA_VS', 'ETA_S', 'ETA_SS','ABS' ]
		inline(code, variables,	 support_code = extra_code, compiler='gcc')

		return (Txx, Tyy, Txy)





