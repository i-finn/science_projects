import u6
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

backing_pressure_setpoint_high = 200.0 #mTorr
backing_pressure_setpoint_low = 1.0 #mTorr

mot_pressure_setpoint_high = 5.0e-8 #Torr
mot_pressure_setpoint_low = 1.0e-11 #Torr

email_list = ["emailaddress@gmail.com"]#enter email addresses to send warning to 

back_flag = 0 #set to 0 to turn on backing emails, set to 2 to turn them off
mot_flag = 2 #set to 0 to turn on mot emails, set to 2 to turn them off

mot_counter = 0
back_counter = 0
fh = open('pressure_data.txt','a+')
fh.write('backing pressure (mTorr) , MOT pressure (Torr) , time , date \n')
fh.close()
def check_pressure():
	fh = open('pressure_data.txt','a+') 
	d = u6.U6()
	AIN_channel = 6 #set MOT AIN channel here
	AIN_voltage = d.getAIN(AIN_channel)
	a = float(int(AIN_voltage))-11.0
	b = (AIN_voltage-float(int(AIN_voltage))+0.1)/0.11
	current_mot_pressure = round(b,3)*10**a     
	e = u6.U6()
	AIN_channel_2 = 10 #set backing AIN channel here
	AIN_voltage = e.getAIN(AIN_channel_2)
	current_backing_pressure = round(10**(float(AIN_voltage)-5.0)*1000.0,1)
	fh.write(str(current_backing_pressure)+" , "+str(current_mot_pressure)+" , "+(time.strftime("%H:%M:%S"))+" , "+(time.strftime("%d/%m/%Y"))+" \n")
	fh.close()
	print("backing pressure: "+str(current_backing_pressure)+" mTorr  "+"MOT pressure: "+str(current_mot_pressure)+" Torr")     
	return current_mot_pressure,current_backing_pressure



def send_backing_email(pressure_value):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("monitoremail@gmail.com", "password")#gmail login info here
	msg = MIMEMultipart()
	msg['Subject'] = "BACKING PRESSURE WARNING!"#email subject
	body = "current backing pressure is "+str(pressure_value)+" mTorr"#email body
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	server.sendmail("monitoremail@gmail.com", email_list, text)#send email

def send_mot_email(pressure_value):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("monitoremail@gmail.com", "password")#gmail login info here
	msg = MIMEMultipart()
	msg['Subject'] = "MOT PRESSURE WARNING!"#email subject
	body = "current MOT pressure is "+str(pressure_value)+" Torr"#email body
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	server.sendmail("monitoremail@gmail.com", email_list, text)#send email


while 1:
	mot_pressure,backing_pressure = check_pressure()
	if backing_pressure>backing_pressure_setpoint_high or backing_pressure<backing_pressure_setpoint_low:
		if back_flag==0:
			send_backing_email(backing_pressure)
			back_flag=1
	if back_flag==1:
		back_counter+=1
		if back_counter==180: #wait 180 * 10 s = 30 min until sending next email
			back_counter=0
			back_flag=0
	if mot_pressure>mot_pressure_setpoint_high or mot_pressure<mot_pressure_setpoint_low:
		if mot_flag==0:
			send_mot_email(mot_pressure)
			mot_flag=1
	if mot_flag==1:
		mot_counter+=1
		if mot_counter==180: #wait 180 * 10 s = 30 min until sending next email
			mot_counter=0
			mot_flag=0



	time.sleep(10.0) #wait 10 seconds