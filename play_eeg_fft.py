from time import sleep, time,ctime
import threading
import serial
import pyaudio
import wave
from Queue import Queue
from makeDictFFT import makeDictFFT
from fft_good_attmpt import PlotSpect,inverse,filter1,filter2
from numpy import resize
import sys

q = Queue(17*256)
chan1 = []
chan2 = []
p = pyaudio.PyAudio()
wf = wave.open("test.wav", 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),              output=True)
eeg_sine,eeg_sine1 = makeDictFFT()


def get_data():
	print "in get_data at", time(), '\n'
	blue = '/dev/ttyUSB0' #will be different in the RPi
	ser = serial.Serial(blue, 57600, timeout = 0)
	if(ser.isOpen() == False):
		ser.open()

		
	pres_packet_loc = 0
	act_amp_chn1 = 0
	act_amp_chn2 = 0
	data1 = []
	time_now = ctime()
	while True:
		now_is = time()
		data = []
		while(len(data) < 17):
			data.append(ser.read(1))
		for x in data:
			if x!= '':
				data1.append(ord(x))
		f = open("EEG at " + time_now,"a")
		for x in range(pres_packet_loc, len(data1)): #alter such that pres_pack_loc moves forward by 17
			if((data1[x]) == 165):
				pres_packet_loc = x
				if(pres_packet_loc + 8 <= len(data1)):
					act_amp_chn1 = ((data1[pres_packet_loc + 4]) << 8)+ (data1[pres_packet_loc + 5])
					act_amp_chn2 = ((data1[pres_packet_loc + 6]) << 8)+ (data1[pres_packet_loc + 7])
					if(act_amp_chn1 < 1024 and act_amp_chn1 > 0 and act_amp_chn2 < 1024 and act_amp_chn2 > 0):
						f.write(str(act_amp_chn1) + " "+ str(act_amp_chn2) + '\n')
						chan1.append(act_amp_chn1)
						chan2.append(act_amp_chn2)
#		print "it took: ", time() - now_is, "to get here \n"
		f.close()
	ser.close()

def filter_it():
	print "in filter_it, at ", time(),'\n'
	
	
#	print len(chan1),len(chan2),"In play it \n"
	r256 = range(0,256)
	t = 0
	
	while True:
		now_is = time()
		if len(chan1) < 256:
			continue
		mean1 = sum(chan1[-256:])/256
		mean2 = sum(chan2[-256:])/256
		print "it took: ", time() - now_is, "to get here after calc means\n"
			
		sum1 = sum((filter2(8.,12.,chan1[-256:])))
		sum2 = sum((filter2(8.,12.,chan2[-256:])))
		
		print "it took: ", time() - now_is, "to get here after filtering\n"
#		print "it took: ", time() - now_is, "to get here after altering the altered channels\n"
#		for x in r256:
#			alt_chan1[x] = alt_chan1[x] + mean1
#			sum1 = sum1 + alt_chan1[x]
#			alt_chan2[x] = alt_chan2[x] + mean2
#			sum2 = sum2 + alt_chan2[x]
		

		to_play1 = int((sum1/256) + mean1)
		to_play2 = int((sum2/256) + mean2)

		print to_play1,to_play2,'\n'
		if t!=0:
			t.join()
		t = threading.Thread(target = play_it, args  = (to_play1,to_play2))
		t.start()
		print "it took: ", time() - now_is, "to get here after new thread stream\n"

	stream.stop_stream()
	stream.close()
	p.terminate()

def play_it(to_play1,to_play2):
#	print "in stream at", time(), "\n"
	now_is = time()
	if(to_play1 < 1024 and to_play1 > 0 and to_play2 < 1024 and to_play2 > 0):
		stream.write(eeg_sine[to_play1] + eeg_sine1[to_play2])
	else:
		stream.write(eeg_sine[512] + eeg_sine1[512])
	print "getting out of stream after: ", time() - now_is, '\n'	

	return


def main():
	
	
	threads = []
	
	t = threading.Thread(target = get_data, args = ())
	threads.append(t)
	t.start()
	t = threading.Thread(target = filter_it, args  = ())
	threads.append(t)
	t.start()

	threads[0].join()

	
	

if __name__ == "__main__":
	main()
