
import keypress
import socket
import time
import mouse
import win32gui, win32api, win32con, ctypes
from time import sleep
import serial
from matplotlib.pyplot import *
import math
from numpy import *




##################################################



total_num = 100  #number of sets
filename = 'ew'
repetition_rate = 400 #Hz
averages = 100000
DR_freq = [ ]


##################################################







def gen_chirp(SR,f_start,f_stop,t_total):

    
    points = int(t_total*SR)
    time = []
    WF = []
    
    
    k = (f_stop-f_start)/t_total
    
    
    
    for x in range(points):
        t = x/SR
        time.append(t)
        WF.append(math.sin(2*math.pi*(f_start*t+(k/2)*t**2))) 
    return time,WF

def gen_sinc(SR,f,width,t_total,amplitude):

    
    points = int(t_total*SR)
    time = []
    WF = []
    
    center = t_total/2
    
    
    
    
    for x in range(points):
        t = x/SR
        time.append(t)
        WF.append(sinc((width)*(t-center))*math.sin(2*math.pi*f*t)*amplitude)
    return time,WF


def std_DR(f_start,f_stop,f_DR,A_DR):
    SR = 10e9

    t_total_chirp = 0.5e-6
    t_total_sinc = 1e-6

    width = 2e6
    time,WF2 = gen_chirp(SR,f_start,f_stop,t_total_chirp)
    time,WF1 = gen_sinc(SR,f_DR,width,t_total_sinc,A_DR)
    
    WF_total = WF2+WF1
    return WF_total














def set_LO(freq):
    #set LO frequency in GHz
    usbport = 'COM13'
    ser = serial.Serial(usbport, 9600, timeout=1)
    
    ser.write('freq %sGHz;pow 11.0dBm;outp on\n\r'%str(freq))
    time.sleep(0.3)
    a = ser.read()
    ser.close()




###################################

def DR_on():
	input_buffer = 2 * 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("131.215.103.230", 4000))
	cmd = "SOURce1:WAVeform \"0_2000MHz_DR_on\"" + "\n"
	s.send(cmd)
	s.close()

def DR_off():
	input_buffer = 2 * 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("131.215.103.230", 4000))
	cmd = "SOURce1:WAVeform \"0_2000MHz_DR_off\"" + "\n"
	s.send(cmd)
	s.close()







#####################################





wait_time = averages/repetition_rate
mouse1 = mouse.Mouse()


def start_acquisition():
    mouse1.invisible_click((1137, 775)) #click single
def save_file(filename):
    time.sleep(1)
    
    keypress.PressKey(0x12) #alt
    keypress.ReleaseKey(0x12)#~alt #click file
    
    keypress.PressKey(0x28)#down
    keypress.ReleaseKey(0x28)
    
    keypress.PressKey(0x28)#down
    keypress.ReleaseKey(0x28)
    
    keypress.PressKey(0x27)#right
    keypress.ReleaseKey(0x27)
    
    keypress.PressKey(0x28)#down
    keypress.ReleaseKey(0x28)
    
    keypress.PressKey(0x0D) #enter
    keypress.ReleaseKey(0x0D)#enter
    
    
    
    
    
    #time.sleep(2)
    
    keypress.Crtla() #select all
    
    time.sleep(0.2)
    
    keypress.type(filename+".txt") #type in filename
    
    time.sleep(0.5)
    
    keypress.PressKey(0x0D) #enter
    keypress.ReleaseKey(0x0D)#enter


def write_WF(freq):
	WF_total = std_DR(0e9,2.0e9,freq,1.0)
	 
	newfile = ''
	newfile+="0,0,0 \n"
	for line in WF_total:
		newfile+=(str(line)+",1,1 \n")
	newfile+="0,0,0\n"

	 
	fh = open("0_2000MHz_DR_on_%s.txt",'w'%str(freq))
	fh.write(newfile)
	fh.close()
	
	
	
	
def load_WF(freq):
	input_buffer = 2 * 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("131.215.103.230", 4000))
	cmd = "IMPORT \"sine1024\",\"sine1024.txt\"" + "\n"
	s.send(cmd)
	s.close()	
	

def run_DR(freq):
	write_WF(freq)
	load_WF(freq)
	
	LO_flag = 0
	for x in range(total_num):

		
		DR_on()
		time.sleep(1)
		start_acquisition()
		time.sleep(wait_time)
		time.sleep(.5)#extra two seconds
		



		newfile = filename+'on'+str(x)
		save_file(newfile)

		
		DR_off()
		time.sleep(1)
		start_acquisition()
		time.sleep(wait_time)
		time.sleep(.5)#extra two seconds
		



		newfile = filename+'off'+str(x)
		save_file(newfile)


for freq in DR_freq:
	run_DR(freq)









#    set_LO((LO_setting+0.01))

#    set_LO(LO_setting)
#    newfile = filename+str((LO_setting))+'GHz'+str(x)
#    time.sleep(1)
#    start_acquisition()
#    time.sleep(wait_time)
#    time.sleep(.5)#extra two seconds
#    newfile = filename+str((LO_setting+0.01))+'GHz'+str(x)
#    save_file(newfile)        
    


