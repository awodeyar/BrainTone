from numpy import sin, linspace, pi,fft
from matplotlib.pylab import plot, show, title, xlabel, ylabel, subplot,clf,ylim
from scipy import arange,signal
from scipy.signal import butter, lfilter
from scipy.signal import fir_filter_design as ffd
from scipy.signal import filter_design as ifd
from scipy.signal import firwin, remez, kaiser_atten, kaiser_beta


def PlotSpect(y,Fs):
	n = len(y)
	k = arange(n)
	T = n/Fs
	frq = k/T
	frq = frq[range(n/2)]
	Y = fft.fft(y) / n
	Y = Y[range(n/2)]
	clf()
	ylim([0,20])
	plot(frq,abs(Y),'b') #plotting the spectrum
	show()
#	set_autoscaley_on(False)
	
 	xlabel('Freq (Hz)')
 	ylabel('|Y(freq)|')

def inverse(y,frq1,frq2,Fs):
	n = len(y)
	k = arange(n)
	T = n/Fs
	frq = k/T
	frq = frq[range(n/2)]
	Y = fft.fft(y) / n
	for x in abs(Y):
		print x
	Y1 = Y[range(frq1,frq2)]
#	Y2 = Y[range(-frq2,-frq1)]
#	Y = Y1 + Y2
#	for i in range(len(Y)):
#		if i>(40*95):Y[i] = 0
	y = abs(fft.ifft(Y))
	return y

def filter1(y,Fs):
#	n = len(y)
#	k = arange(n)
#	T = n/Fs
#	frq = k/T
#	frq = frq[range(n/2)]
	fs = Fs
	fso2 = fs/2
#	N,wn = buttord(ws=[5./fso2,40./fso2], wp=[4./fso2,41./fso2],gpass=0.1, gstop=30.0)
	B, A = butter(1, 40 / fso2, btype='low') # 1st order Butterworth low-pass
	filtered_signal = lfilter(B, A, y)
#	Y = fft.fft(filtered_signal)
#	Y = Y[range(n/2)]
	clf()
#	plot(frq,abs(Y),'b') #plotting the spectrum
#	show()
 #	xlabel('Freq (Hz)')
 #	ylabel('|Y(freq)|')

	return filtered_signal

def filter2(band_start,band_end,y):
	# setup some of the required parameters
	Fs = 256           # sample-rate defined in the question, down-sampled

	# remez (fir) design arguements
	Fpass1 = band_end      # passband edge
	Fstop1 = band_end + 1.     # stopband edge
	Fpass2 = band_start
	Fstop2 = band_start -1.
#	Wp = Fpass/(Fs)    # pass normalized frequency
#	Ws = Fstop/(Fs)    # stop normalized frequency

	# iirdesign agruements
	Wip = [(Fpass2)/(Fs/2),(Fpass1)/(Fs/2)]		#[8./(128),14./(128)]
	Wis = [(Fstop2)/(Fs/2),(Fstop2)/(Fs/2)]		#[7./128,15./128]
	Rp = 1             # passband ripple
	As = 42            # stopband attenuation

	# The iirdesign takes passband, stopband, passband ripple, 
	# and stop attenuation.
	bc, ac = ifd.iirdesign(Wip, Wis, Rp, As, ftype='ellip')  
#	bb, ab = ifd.iirdesign(Wip, Wis, Rp, As, ftype='cheby2') 
	return lfilter(bc,ac,y)
