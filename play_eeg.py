import serial
from time import ctime,sleep,time 
import pyaudio
import wave
from makeDict import makeDict


def main():
	p = pyaudio.PyAudio()
	blue = '/dev/ttyUSB0' #will be different in the RPi
	ser = serial.Serial(blue, 57600, timeout = 0)
	if(ser.isOpen() == False):
		ser.open()

	wf = wave.open("test.wav", 'rb')
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),              output=True)
	eeg_sine,eeg_sine1 = makeDict() 
	pres_packet_loc = 0
	act_amp_chn1 = 0
	act_amp_chn2 = 0
	channel_data = []
	data = []
	data1 = []
	x = 0
	time_now = ctime()

	while True:
		now_is = time()
		data = []
		while(len(data) < 17):
			data.append(ser.read(1))
		print "data getting took: ", (time() - now_is), "\n"
		for x in data:
			if x!= '':
				data1.append(ord(x))

		print "data changing took: ", (time() - now_is), "\n"
		f = open("EEG at " + time_now,"a")
		for x in range(pres_packet_loc, len(data1)): #alter such that pres_pack_loc moves forward by 17
			if((data1[x]) == 165):
				pres_packet_loc = x
				if(pres_packet_loc + 8 <= len(data1)):
					act_amp_chn1 = ((data1[pres_packet_loc + 4]) << 8)+ (data1[pres_packet_loc + 5])
					act_amp_chn2 = ((data1[pres_packet_loc + 6]) << 8)+ (data1[pres_packet_loc + 7])
	#				x = x + 16
					print str(act_amp_chn1) , str(act_amp_chn2), str(pres_packet_loc), str(len(data1))
					if(act_amp_chn1 < 1024 and act_amp_chn1 > 0 and act_amp_chn2 < 1024 and act_amp_chn2 > 0):
						f.write(str(act_amp_chn1) + " "+ str(act_amp_chn2) + '\n')
						print "coming till here took: ", (time() - now_is), "\n"
						stream.write(eeg_sine[act_amp_chn1] + eeg_sine1[act_amp_chn2])
					#	stream1.write(eeg_sine1[act_amp_chn2])
		 				print "this took: ", (time() - now_is), "\n"
		f.close()
						
	f.close()
	ser.close()
	stream.stop_stream()
	stream.close()
	stream1.stop_stream()
	stream1.close()
	p.terminate()

if __name__ == "__main__":
	main()

