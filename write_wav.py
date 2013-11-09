import numpy as N
import wave
import matplotlib.pyplot as plot

class SoundFile:
   def  __init__(self, signal):
       self.file = wave.open('test.wav', 'wb')
       self.signal = signal
       self.sr = 44100

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

# let's prepare signal
duration = 1 # seconds
samplerate = 44100 # Hz
samples = duration*samplerate
frequency = 512 #hz
period = samplerate / float(frequency) # in sample points
omega = N.pi * 2 / period

xaxis = N.arange(int(period),dtype = N.float) * omega
ydata = 16384 * N.sin(xaxis)

signal = N.resize(ydata, (samples,))
xaxis = N.resize(xaxis,(samples,))

#plot.plot(xaxis,signal)
#plot.show()

for x in signal:
	print x


ssignal = ''
for i in range(len(signal)):
   ssignal += wave.struct.pack('h',signal[i]) # transform to binary
#plot.plot(xaxis,signal)
#plot.show()
f = SoundFile(ssignal)
f.write()
