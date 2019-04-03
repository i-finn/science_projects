import serial #import serial library, to talk to SIM mainframe
import time #import time library to define wait times
import numpy as np #import numpy library to define arrays
import mouse #import mouse library, to use mouse clicking routine
step = 100.0 #desired comb step size in Hz
time_sleep = 225 #desired rest time at each step in seconds
mouse1 = mouse.Mouse() #calls the mouse clicker routine in the mouse library
def start_acquisition():
	mouse1.invisible_click((1728,79))
	#single click on start aquisition button in AlazarTech program
	#AlazarTech program must be maximized for click coordinates to work
def save_file():
	#this routine executes a series of clicks to save data files
	mouse1.invisible_click((15,31))
	time.sleep(0.5) #single click file menu
	mouse1.invisible_click((24,79))
	time.sleep(1.0) #single click save as
	mouse1.invisible_click((928,461))
	time.sleep(0.5) #single click to select channel B as the channel to save
	mouse1.invisible_click((1034,763))
	time.sleep(3.0) #single click ok to save in window
	mouse1.invisible_click((1103,571))
	#single click ok to clear save complete message
def move_comb(voltage):
	#this routine sets the output voltage of the PID controller
	#to a the value (voltage) specifed when calling this routine
	ser = serial.Serial(’COM8’, 9600, timeout=3)
	#opens serial port on computer used to talk to SIM mainframe,
	#port:COM8, baud rate: 9600, timeout: 3 ms
	ser.write(’CONN 1,"xyz"\n’)
	#talk to serial port 1 in SIM mainframe: slave slow PID controller,
	#defines escape string as "xyz"
	#when sending commands to the SIM mainframe all strings terminate in \n
	ser.write(’AMAN 0\n’) #set PID controller to manual mode
	ser.write(’MOUT %s\n’%(str(voltage)))
	#set manual voltage to the desired value in Volts
	ser.write(’xyz\n’)
	#send escape string to close serial connection to port 1 in SIM mainframe
	ser.close() #close serial port on control computer
def save_file():
	#this routine executes a series of clicks to save data files
	mouse1.invisible_click((15,31))
	time.sleep(0.5) #single click file menu
	mouse1.invisible_click((24,79))
	time.sleep(1.0) #single click save as
	mouse1.invisible_click((928,461))
	time.sleep(0.5) #single click to select channel B as the channel to save
	mouse1.invisible_click((1034,763))
	time.sleep(3.0) #single click ok to save in window
	mouse1.invisible_click((1103,571))
	#single click ok to clear save complete message
def move_comb(voltage):
	#this routine sets the output voltage of the PID controller
	#to a the value (voltage) specifed when calling this routine
	ser = serial.Serial(’COM8’, 9600, timeout=3)
	#opens serial port on computer used to talk to SIM mainframe,
	#port:COM8, baud rate: 9600, timeout: 3 ms
	ser.write(’CONN 1,"xyz"\n’)
	#talk to serial port 1 in SIM mainframe: slave slow PID controller,
	#defines escape string as "xyz"
	#when sending commands to the SIM mainframe all strings terminate in \n
	ser.write(’AMAN 0\n’) #set PID controller to manual mode
	ser.write(’MOUT %s\n’%(str(voltage)))
	#set manual voltage to the desired value in Volts
	ser.write(’xyz\n’)
	#send escape string to close serial connection to port 1 in SIM mainframe
	ser.close() #close serial port on control computer
converted_step = step/575.0
#conversion factor to convert desired step size in Hz to the required voltage step in V
num_step = int(10.0/converted_step)
#determines the number of steps that will fit into the 10V range of the PID controller
v_list = np.linspace(-5.0,5.0,num_step+1)
#creates a 1D array of volatge steps ascending from -5V to +5V
v_list2 = np.linspace(5.0,-5.0,num_step+1)
#creates a 1D array of volatge steps descending from +5V to -5V
Loops = 1 #control variable to enable repeating voltage steps
while Loops == 1: #run this loop while Loops equals 1
	#change the condition to Loops <= N to run loop N times
	for V in v_list: #for each element V in the 1D array v_list
		move_comb(V) #move to voltage step V
		time.sleep(20) #wait 20 s to let comb equilibrate
		start_acquisition() #begin acquisition of data
		time.sleep(time_sleep) #wait while data is acquired
		save_file() #save data
		#this will run until the voltage has been incremented stepwise up to 5V
	for V in v_list2: #for each element V in the 1D array v_list2
		move_comb(V) #move to voltage step V
		time.sleep(20) #wait 20 s to let comb equilibrate
		start_acquisition() #begin acquisition of data
		time.sleep(time_sleep) #wait while data is acquired
		save_file() #save data
		#this will run until the voltage has been incremented stepwise down to -5V
		#Loops +=1
		#uncomment to increment Loops by 1 and scan voltage up and down once
		#or to scan voltage up and down N times