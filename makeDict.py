from collections import deque
import wave

def makeDict():
	q = deque()
	get_data = open("sine_data","r")
	data = ' '
	while True:
		data = get_data.readline()
		if data!= '':
			q.append(float(data[:-1]))
		else:
			break
	get_data.close()
	eeg_dict = dict()
	for y in range(0,1024):
		signal = ''
		for i in range(len(q)/512):
			signal += wave.struct.pack('h',(((q[i])*y)/1024)) # transform to binary
		eeg_dict[y] = signal

	get_data = open("sine_data1","r")
	data = ''
	q = deque()
	while True:
		data = get_data.readline()
		if data!= '':
			q.append(float(data[:-1]))
		else:
			break
	get_data.close()
	eeg_dict1 = dict()
	ssignal = ''
	for y in range(0,1024):
		signal = ''
		for i in range(len(q)/512):
			signal += wave.struct.pack('h',(q[i]*y)/(1024)) # transform to binary 
		eeg_dict1[y] = signal
	

	return eeg_dict,eeg_dict1
