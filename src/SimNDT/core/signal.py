import numpy as	np
from  math import pi, cos, sin
import matplotlib.pyplot as plt

def RaisedCosinePulse(t, Freq, Amplitude):
	"""
	Raised-Cosine Pulse
	
	""" 
	N  = np.size(t,0)
	P  = np.zeros((N,),dtype=np.float32)
	for m in range(0,N):
		if t[m] <= 2.0/Freq:
			P[m] = Amplitude *(1-cos(pi*Freq*t[m]))*cos(2*pi*Freq*t[m])

	return P


def PulseUTsin(t,fc,NT, Amp):
	"""
	Gaussian Pulse

	Code inspired by
	see http://www.k-wave.org/
	"""
	def gaussian_func(x,mean,variance):
		return np.exp(-((x - mean)**2)/(2*variance))


	Ts			 = t[1]-t[0]
	Fs			 = 1.0/Ts
	tone_length	 = ( NT/(fc*1.0) )
	tone_t		 = np.arange(0,tone_length,Ts)
	tone_burst_t = np.sin(2*pi*fc*tone_t)

	x_lim = 3
	window_x = np.arange(-x_lim,x_lim, 2.0*x_lim/(np.size(tone_burst_t)-1) )
	window	 = gaussian_func(window_x,0, 1)

	ind = np.min([ np.size(window_x), np.size(tone_burst_t)])
	tone_burst=np.zeros((ind,))
	tone_burst[0:ind] = window[0:ind]*tone_burst_t[0:ind] 

	y	= np.zeros((np.size(t),))


	#plt.figure()
	#plt.plot(tone_burst)
	#plt.show()
	try:
		y[0:np.size(tone_burst)] = Amp*tone_burst[:]
		return y
	except:
		raise Exception("Signal does not fit in the Configured Time, Increase the Simulation Time to solve this issue")



class Signals():
	
	def __init__(self, Name="RaisedCosine", Amplitud=1, Frequency=1, N_Cycles=1):
		
		self.Name      = Name
		self.Amplitude = Amplitud
		self.Frequency = Frequency
		self.N_Cycles  = N_Cycles
	
	
	def __str__(self):
		return "Signal: "  + unicode(self.Name)

	def __repr__(self):
		return "Signal: " + unicode(self.Name)
		

	def generate(self, t):
		if self.Name == "RaisedCosine":
			return RaisedCosinePulse(t, self.Frequency, self.Amplitude)
		elif self.Name == "GaussianSine":
			return PulseUTsin(t,self.Frequency,self.N_Cycles,self.Amplitude)
		
	def save(self,t):
		self.time_signal  = self.generate(t)
	




