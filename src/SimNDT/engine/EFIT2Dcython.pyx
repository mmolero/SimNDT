cimport cython
cimport numpy as np


@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
def sourceVel(np.float32_t[:,:] Vx,  np.float32_t[:,:] Vy, 
              np.int32_t[:] XL, 
			  np.int32_t[:] YL, 
			  double source, int Stype, win, double dtdxx):

	cdef unsigned int i
	cdef int ii, jj
	cdef int N = XL.shape[0]

	if Stype == 0:
		for i in range(N):		
			ii = XL[i]
			jj = YL[i]
			Vx[ii, jj]	-= source*dtdxx * win[i]
		
	elif Stype ==1:
		for i in range(N):
			ii = XL[i]
			jj = YL[i]
			Vy[ii,jj]	-= source*dtdxx * win[i]
		
	elif Stype ==2:
		for i in range(N):
			ii = XL[i]
			jj = YL[i]
			Vx[ii,jj]	-= source* dtdxx * win[i]
			Vy[ii,jj]	-= source* dtdxx * win[i]


	return (Vx, Vy)
	

@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
def sourceStress(np.float32_t[:,:] Txx,  np.float32_t[:,:] Tyy, 
                 np.int32_t[:] XL, np.int32_t[:] YL, 
				 double source, int Stype, win,  double dtdxx):

	cdef int N = XL.shape[0]
	cdef unsigned int i
	cdef int ii, jj

	if Stype ==0:
		for i in range(0, N):
			Txx[XL[i],YL[i]]	-= source*dtdxx * win[i]
		
	elif Stype ==1:
		for i in range(0, N):
			Tyy[XL[i],YL[i]]	-= source*dtdxx * win[i]
		
	elif Stype ==2:
		for i in range(0, N):
			Txx[XL[i],YL[i]]	-= source* dtdxx * win[i]
			Tyy[XL[i],YL[i]]	-= source* dtdxx * win[i]


	return (Txx, Tyy)


@cython.boundscheck(False)
@cython.wraparound(False)
def velocityVoigt(np.float32_t[:,:] Txx, np.float32_t[:,:] Txy, np.float32_t[:,:] Tyy, 
                  np.float32_t[:,:] vx, np.float32_t[:,:] vy,  np.float32_t[:,:] d_vx, np.float32_t[:,:] d_vy, 
				  np.float32_t[:,:] BX, np.float32_t[:,:] BY, np.float32_t[:,:] ABS, double  ddx, double  dt):


	cdef int M = Txx.shape[0]
	cdef int N = Txx.shape[1]
	cdef int i
	cdef int j
   
  
	for i in range(0,M-1):
		for j in range(1,N):
			d_vx[i,j]	 = (BX[i,j] * ddx) * ( Txx[i+1,j] - Txx[i,j] + Txy[i,j] - Txy[i,j-1] )
			vx[i,j]	    += dt * d_vx[i,j]

											
	for i in range(1,M): 	
		for j in range(0, N-1):
			d_vy[i,j]	 = (BY[i,j] * ddx) * ( Txy[i,j]  - Txy[i-1,j] + Tyy[i,j+1] - Tyy[i,j] )
			vy[i,j]	    +=  dt * d_vy[i,j]

	for i in range(0,M):
		for j in range(0,N):	  
			vx[i,j]	  *= ABS[i,j]
			vy[i,j]	  *= ABS[i,j]	

			
					   
	return (vx, vy, d_vx, d_vy)
	

@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
def stressVoigt(np.float32_t[:,:] Txx, np.float32_t[:,:] Txy, np.float32_t[:,:] Tyy, 
                np.float32_t[:,:] vx, np.float32_t[:,:] vy, np.float32_t[:,:] d_vx, np.float32_t[:,:] d_vy, 
				np.float32_t[:,:] C11, np.float32_t[:,:] C12, np.float32_t[:,:] C44, 
				np.float32_t[:,:] ETA_VS, np.float32_t[:,:] ETA_S, np.float32_t[:,:] ETA_SS, 
				np.float32_t[:,:] ABS, double dtx):
	
	
	cdef int M = Txx.shape[0]
	cdef int N = Txx.shape[1]
	cdef int i
	cdef int j
	
	for i in range(1,M):
		for j in range(1,N):
			Txx[i,j] += (	( C11[i,j] * dtx )*(vx[i,j] - vx[i-1,j]) +
							( C12[i,j] * dtx )*(vy[i,j] - vy[i,j-1]) +
							( (ETA_VS[i,j]) * dtx) * (d_vx[i,j] - d_vx[i-1,j]) +
							( (ETA_S [i,j]) * dtx) * (d_vy[i,j] - d_vy[i,j-1]) )
							
			Tyy[i,j] += (	( C12[i,j]* dtx )*(vx[i,j] - vx[i-1,j]) +
						( C11[i,j]* dtx )*(vy[i,j] - vy[i,j-1]) +
						( (ETA_VS[i,j])*dtx) *(d_vy[i,j] - d_vy[i,j-1]) +
						( (ETA_S [i,j])*dtx) * (d_vx[i,j] - d_vx[i-1,j]) )
					
	for i in range(0, M-1):
		for j in range(0, N-1):
			Txy[i,j] +=	(  ( C44[i,j] * dtx )*(vx[i,j+1] - vx[i,j] + vy[i+1,j] - vy[i,j])	+
						   ( ETA_SS[i,j]  * dtx )*(d_vx[i,j+1] - d_vx[i,j] + d_vy[i+1,j] - d_vy[i,j] ) )
							 
	for i in range(0,M):
		for j in range(0,N):
			Txx[i,j] *= ABS[i,j];
			Tyy[i,j] *= ABS[i,j];
			Txy[i,j] *= ABS[i,j];
		

	return (Txx, Tyy, Txy)
   

 