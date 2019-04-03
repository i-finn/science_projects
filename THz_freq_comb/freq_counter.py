import math #import math library to use math.floor()
import serial #import serial library to talk to SIM mainframe
import mouse #import mouse to use mouseclicker
import visa #import pyVisa to communicate with GPIB devices
# Agilent frequency synthesizer and frequency counter
import time #import time library to add wait times
def read_master_freq():
	#when called this routine querries the frequency counter
	#and returns the value of the master rep rate as an int
	rm = visa.ResourceManager()
	rm.list_resources()
	inst = rm.open_resource('GPIB0::3::INSTR')
	#these three lines of code list the avaliable GPIB devices
	#connected to the computer and then opens a connection with
	#the device on GPIB channel 3, the frequency counter
	inst.write("FU1") #sends a command to read the frequency
	#from channel A on the frequency counter
	data = inst.visalib.read(inst.session, 17)
	#stores the data from the frequency counter as a string
	#reads 17 characters in the format "FREQ 79980883"
	a = str(data[0]) #failsafe to read only one line of FREQ data
	x = a.find("F") #finds the beginning of the string
	masterfreq = float(a[x+4:x+14])*10**7 #discard the "FREQ"
	masterfreq = int(math.floor(masterfreq)) #convert to int
	return masterfreq #returns the freq reading as an int
def setfreqsynth(targetfreq):
	#when called this routine sets the frequency of the synth
	#to the desired value given by targetfreq
	freq = targetfreq
	freq = freq*12 #calculates the 12th harmonic of the input
	#since the RF lock circuit operates at the 12th harmonic
	rm = visa.ResourceManager()
	rm.list_resources()
	synth = rm.open_resource('GPIB0::21::INSTR')
	#opens a connection on GPIB channel 21, the Agilent synth
	Command = 'FREQ '+str(freq)+" Hz\n"
	#builds a string with the appropriate syntax for the synth
	synth.write(Command)
	#sends the command string to the synth to go to the desired frequency
	print Command #prints the command in the command prompt
def lock_comb():
	#when called this routine sets the PID controller to PID control
	ser = serial.Serial('COM8', 9600, timeout=3)
	#open serial connection on port COM8, the SIM mainframe
	ser.write('CONN 1,"xyz"\n')
	#open connection to port 1 in the mainframe, the PID controller
	ser.write('AMAN 1\n') #set PID controller to PID control
	ser.write('xyz\n') #send the escape string to terminate connection
	ser.close() #close the serial connection
def move_comb(voltage):
	#when called this routine switches the PID controller to manual control and
	#sets the manual voltage on the PID controller to the desired value (voltage)
	ser = serial.Serial('COM8', 9600, timeout=3)
	#open serial connection on port COM8, the SIM mainframe
	ser.write('CONN 1,"xyz"\n')
	#open connection to port 1 in the mainframe, the PID controller
	ser.write('AMAN 0\n') #set PID controller to manual control
	ser.write('MOUT %s\n'%(str(voltage)))
	#move manual voltage to (voltage)
	ser.write('xyz\n') #send the escape string to terminate connection
	ser.close() #close the serial connection
def read_voltage():
	#when called this routine querries the PID controller
	#and returns the current control voltage
	ser = serial.Serial('COM8', 9600, timeout=6)
	#open serial connection on port COM8, the SIM mainframe
	ser.write('CONN 1,"xyz"\n')
	#open connection to port 1 in the mainframe, the PID controller
	ser.write('OMON?\n') #query PID controller output voltage
	volt = ser.read(7) #read 7 bytes of the returned serial stream
	ser.write('xyz\n') #send the escape string to terminate connection
	ser.close() #close the serial connection
	return volt #return the current voltage value
def start_acquisition():
	#this routine clicks the acquire data button to start a scan
	mouse1 = mouse.Mouse() #defines the mouseclicker routine
	mouse1.invisible_click((1728,79))
	#single clicks the start button
def save_file():
	#this routine saves the data file once the scan is complete
	mouse1 = mouse.Mouse() #defines the mouseclicker routine
	mouse1.invisible_click((15,31)) #clicks the file menu
	time.sleep(0.5) #wait for menu to open
	mouse1.invisible_click((24,79)) #clicks save as
	time.sleep(1.0) #waits for the dialog box to open
	mouse1.invisible_click((928,461)) #sets save to channel B
	time.sleep(0.5) #waits for channel to update
	mouse1.invisible_click((1034,763)) #clicks the save button
	time.sleep(3.0) #waits for file to save
	mouse1.invisible_click((1103,571)) #clicks the ok button
	#to clear the save complete dialogue box
def freq_lock():
	#this routine reads the current frequency of the master laser
	#from the frequency counter and rounds the frequency to the
	#nearest multiple of the desired freqeuency step
	#it then sets the synth to the 12th harmonic of the target freq
	#and applies the appropriate voltage step to the PID controller
	#to adjust the master freq to the target freq, a multiple of
	#the deisred freq step, and then engages PID control to lock
	#the master laser repetition rate to the desired frequency
	freq_step = 100 #desired frequency step in Hz
	freqtovolt = -0.002 #+0.100V = -50 Hz conversion factor
	masterfreq = read_master_freq()
	#reads in the master freq from the frequency counter
	current_volt = float(read_voltage())
	#reads in the current voltage of the PID controller
	round = masterfreq % freq_step
	#rounds to the nearest multiple of the freq step size
	if round <= freq_step/2: #if closer to the next lowest freq
		rounddown = round #round down by the remainder
		targetfreq = masterfreq - rounddown #to get the target freq
		targetvolt = current_volt - float(rounddown)*freqtovolt
		#then calculates the appropriate voltage adjustment
	else: #otherwise freq is closer to the next highest freq
		roundup = freq_step - round #round up by freq_step-remainder
		targetfreq = masterfreq + roundup #to get the target freq
		targetvolt = current_volt + float(roundup)*freqtovolt
		#then calculates the appropriate voltage adjustment
	print targetfreq #prints the calculated target frequency
	setfreqsynth(targetfreq) #sets the synth to the target freq
	move_comb(targetvolt) #adjusts the PID controller voltage
	time.sleep(2.0) #let masterfreq equilibrate before engaging PID
	lock_comb() #engage PID control
	return targetfreq #returns the target frequency
def freq_step_up():
	#this routine steps the voltage of the PID controller
	#up by the desired step amount and then locks the
	#master laser repetition rate to the new frequency
	freq_step = 100 #desired frequency step in Hz
	freqtovolt = -0.002 #+0.100V = -50 Hz conversion factor
	volt_step = freqtovolt*float(freq_step)
	#calculates the size of the appropriate voltage step
	current_volt = float(read_voltage())
	#reads the current voltage of the PID controller
	move_volt = current_volt + volt_step
	#calculates the target voltage based on the current voltage
	move_comb(move_volt)
	#applies the voltage step to the PID controller
	masterfreq = freq_lock()
	#engage PID control of the master laser rep rate
	return masterfreq #returns the new master laser rep rate
def freq_step_down():
	#this routine steps the voltage of the PID controller
	#down by the desired step amount and then locks the
	#master laser repetition rate to the new frequency
	freq_step = 100 #desired frequency step in Hz
	freqtovolt = -0.002 #+0.100V = -50 Hz conversion factor
	volt_step = freqtovolt*float(freq_step)
	#calculates the size of the appropriate voltage step
	current_volt = float(read_voltage())
	#reads the current voltage of the PID controller
	move_volt = current_volt - volt_step
	#calculates the target voltage based on the current voltage
	move_comb(move_volt)
	#applies the voltage step to the PID controller
	masterfreq = freq_lock()
	#engage PID control of the master laser rep rate
	return masterfreq #returns the new master laser rep rate
def take_data():
	#this routine initiates data acquisition, waits for the scan
	#to complete and then saves the data
	scan_time = 230 #scan time in seconds
	start_acquisition() #begin scan
	time.sleep(scan_time) #wait for data
	save_file() #save file
def scan_comb():
	#this routine first locks the master laser repetition rate
	#then scans the master laser rep rate up and back down through
	#a series of defined frequency steps, saving data at each step
	masterfreq = freq_lock() #lock the master laser rep rate
	equilibrate_time = 10.0
	#time to wait for the master laser rep rate to stabilize
	time.sleep(equilibrate_time)
	upper_lim_freq = 79984300
	#upper frequency limit, highest value possible: 79984300
	lower_lim_freq = 79977200
	#lower frequency limit, lowest value possilbe: 79977200
	scan = 1 #a loop parameter used to turn infinite scanning on
	while scan == 1: #while the scan parameter is true, step freq
		while masterfreq < upper_lim_freq:
			#while the master frequency is below the upper limit
			masterfreq = freq_step_up()
			#step the master rep rate up by the step size
			print masterfreq #print the new frequency
			time.sleep(equilibrate_time)
			#wait for master rep rate to stabilize
			take_data() #acquire and save data
		while masterfreq > lower_lim_freq:
			#while the master frequency is above the lower limit
			masterfreq = freq_step_down()
			#step the master rep rate down by the step size
			print masterfreq #print the new frequency
			time.sleep(equilibrate_time)
			#wait for master rep rate to stabilize
			take_data() #acquire and save data
scan_comb() #runs the scan comb routine when freq_counter.py is called