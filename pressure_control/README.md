# Description
I wrote this program to keep a constant pressure in the waveguide microwave spectrometer at New College of Florida. Before implementing this script, we would have to adjust a valve every few minutes. With this script, we could let the instrument run for several hours without intervention. The program reads the pressure from a pressure gauge over serial communication and then adjusts a valve with a hobby servo using an arduino to change the pumpout speed from the gas cell. I used the arduino control software from [here](https://github.com/vdupain/arduino-sketchbook/tree/master/MultipleSerialServoControl)
# Files
* pressure_control.py
# Schematic
![alt text](https://github.com/iafinn/science_projects/blob/master/pressure_control/schematic.png)
