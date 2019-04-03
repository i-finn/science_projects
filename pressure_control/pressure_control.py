import serial
import time
usbport1 = 'COM4'
ser2 = serial.Serial(usbport1, 9600, timeout=1, stopbits=1)
usbport2 = 'COM3'
ser1 = serial.Serial(usbport2, 9600, timeout=1)
def move(servo, angle):
	'''Moves the specified servo to the supplied angle.
	Arguments:
	servo
	the servo number to command, an integer from 1-4
	angle
	the desired servo angle, an integer from 0 to 180
	(e.g.) >>> servo.move(2, 90)
	... # "move servo #2 to 90 degrees"'''
	if (0 <= angle <= 180):
	ser1.write(chr(255))
	ser1.write(chr(servo))
	ser1.write(chr(angle))
	else:
	print "Servo angle must be an integer between 0 and
	180.\n"
ser2.write("p")#this retrieves the pressure from the pressure gauge
x = float(ser2.readline()[0:5])#this selects gauge 1
pressure = x
last_p = pressure
y = 90
move(1,y)
time.sleep(2)
counter = 0
marker = ""
100
while 1:
	counter +=1
	if counter ==180:
		fh = open("pressure_data.txt","a")
		data = str(x)+"\n"
		fh.write(data)
		fh.close
		counter =0
	ser2.write("p")
	x = float(ser2.readline()[0:5])#this selects gauge 1
	print x
	if x>last_p:
		marker = "up"
	if x<last_p:
		marker = "down"
	if abs(pressure-x)<0.1:
		marker = "stable"
	if x<(pressure-0.1) and marker != "up":
		y+=1
		if y>155:
			y=155
		move(1,y)
		time.sleep(.3)
	if x>(pressure+0.1) and marker !="down":
		y+=-1
		if y<20:
			y=20
		move(1,y)
		time.sleep(.3)
	time.sleep(.3)
	last_p = x