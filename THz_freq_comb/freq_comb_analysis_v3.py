import numpy as np
import matplotlib.pyplot as plt
from numpy import array
from scipy.fftpack import fft
from math import pi,atan2,log
import scipy.interpolate as inter
import numpy as np
import pylab as plt

###############
###############
import os
from os import path




Main_frequency = 79980833



files = filter(path.isfile, os.listdir("."))





files_2 = []
for file in files:
    if file[-4:]==".txt":
        files_2.append((file,Main_frequency))

comb_list = files_2

            
#comb_list = [('981560Hz_1000avg_1.1.B.txt',79979480)]  
"""
comb_list = [('H2O_120mTorr_979480Hz_B.txt','Blank_11mTorr_979480Hz_B.txt',79979480),\
			('H2O_120mTorr_979960Hz_B.txt','Blank_11mTorr_979960Hz_B.txt',79979960),\
			('Blank_11mTorr_980050Hz_1.1.B.txt','Blank_11mTorr_980050Hz_1.1.B.txt',79980050),\
			('H2O_120mTorr_980170Hz_B.txt','Blank_11mTorr_980170Hz_B.txt',79980170),\
			('Blank_11mTorr_980250Hz_1.1.B.txt','Blank_11mTorr_980250Hz_1.1.B.txt',79980250),\
			('Blank_11mTorr_980360Hz_1.1.B.txt','Blank_11mTorr_980360Hz_1.1.B.txt',79980360),\
			('Blank_11mTorr_979770Hz_1.1.B.txt','Blank_11mTorr_979770Hz_1.1.B.txt',79979770),\
			('Blank_11mTorr_979780Hz_1.1.B.txt','Blank_11mTorr_979780Hz_1.1.B.txt',79979780),\
			('H2O_120mTorr_979830Hz_1.1.B.txt','Blank_11mTorr_979830Hz_1.1.B.txt',79979830),\
			('Blank_11mTorr_979880Hz_1.1.B.txt','Blank_11mTorr_979880Hz_1.1.B.txt',79979880),\
			('Blank_11mTorr_979890Hz_1.1.B.txt','Blank_11mTorr_979890Hz_1.1.B.txt',79979890),\
			('H2O_120mTorr_979170Hz_B.txt','Blank_11mTorr_979170Hz_B.txt',79979170),\
			('H2O_120mTorr_979040Hz_1.1.B.txt','Blank_11mTorr_979040Hz_1.1.B.txt',79979040),\
			('H2O_120mTorr_978190Hz_1.1.B.txt','Blank_11mTorr_978190Hz_1.1.B.txt',79978190),\
			('H2O_120mTorr_980790Hz_1.1.B.txt','Blank_11mTorr_980790Hz_1.1.B.txt',79980790),\
			('H2O_120mTorr_981550Hz_1.1.B.txt','Blank_10mTorr_981550Hz_1.1.B.txt',79981550),\
			('H2O_120mTorr_978780Hz_B.txt','Blank_11mTorr_978780Hz_B.txt',79978780)]
"""
#comb_list = [('H2O_120mTorr_979960Hz_B.txt','Blank_11mTorr_979960Hz_B.txt',79979960),\
#			('H2O_120mTorr_980170Hz_B.txt','Blank_11mTorr_980170Hz_B.txt',79980170)]

			#('H2O_120mTorr_982170Hz_1.1.B.txt','Blank_11mTorr_982170Hz_1.1.B.txt',79982170)]
			
			 
		
			


thresh = 0.25
scale_factor = -100
plot_time_figure = 0

plot_freq_figure = 1

###############
###############















#def peakpicker(spectrum,inten,thresh_l,thresh_h):#Code taken from Cristobal's peak-picking script; assumes spectrum is in increasing frequency order
#	peaks=[]
#	peaks2 = []
#	i_list = []
#	for i in range(len(spectrum)):
#		if inten[i] > thresh_l and inten[i] < thresh_h and inten[i] > inten[(i-1)] and inten[i] > inten[(i+1)]:
#			peaks.append(spectrum[i])
#			peaks2.append(inten[i])
#			i_list.append(i)
#			
#	return peaks,peaks2,i_list
def peakpicker(spectrum,inten,thresh_l,thresh_h):#Code taken from Cristobal's peak-picking script; assumes spectrum is in increasing frequency order
	peaks=[]
	peaks2 = []
	i_list = []
	delta_i_list = []
	for i in range(len(spectrum)):
		if inten[i] > thresh_l and inten[i] < thresh_h and inten[i] > inten[(i-1)] and inten[i] > inten[(i+1)]:
			peaks.append(spectrum[i])
			peaks2.append(inten[i])
			i_list.append(i)
			if len(i_list)>1:
				
				if abs(peaks[-2]-peaks[-1])<8.1e-5:
					
					delta_i_list.append(abs(i_list[-2]-i_list[-1]))
		if len(i_list)>1:		
			
			if abs(spectrum[i_list[-1]]-spectrum[i])>10.0e-5:
				#print abs(spectrum[i_list[-1]]-spectrum[i]),spectrum[i]
				
				
				 
				average = sum(delta_i_list)/len(delta_i_list)
				new_value = i_list[-1]+average+1
				#print spectrum[new_value]-spectrum[i_list[-1]]
				i_list.append(new_value)
				
	return peaks,peaks2,i_list
	


def fft_data(filename,Master_rep_rate):

	

	oscilliscope_sample_rate = 40e6

	

	##############
	###############
	offset = 400.0
	sample_rate = oscilliscope_sample_rate*(1/offset)*Master_rep_rate
	sample_rate = sample_rate/1e12
	#print sample_rate

	fh = open(filename)

	data = []


	for line in fh:
		data.append(float(line))



	E_field = data
	
	time_values = []




	for time in range(0,len(E_field)):
	   time_value = (time/sample_rate)*1e6
	   time_values.append(time_value) 




	cut_E_field_new = [float(a)*float(b) for a,b in zip(list(np.kaiser(len(E_field),8)),E_field)]#<<<<<<<<<<<<<<<<<<<<<<<<<<<<

	num = len(cut_E_field_new)

	noct=int(log(num)/log(2))

	num_fft=2**23
	df = 1/(float(num_fft)*(1/sample_rate))
	

	fft_length = float(sample_rate)
	freq_list = []

	for f in range(0,int(fft_length/df)):
	   freq_list.append(f*df)


        
	Fourier_transform =abs(np.fft.fft(array(cut_E_field_new),2**23))
	
	f_lower_bound = .15
	f_upper_bound = 3
	length_freq_list = len(freq_list)
	freq_list = freq_list[0:length_freq_list/2]
	Fourier_transform = Fourier_transform[0:length_freq_list/2]


	freq_list = freq_list[int(f_lower_bound/df):int(f_upper_bound/df)]
	Fourier_transform = Fourier_transform[int(f_lower_bound/df):int(f_upper_bound/df)]
	#print len(freq_list),len(Fourier_transform)
	
	#print len(E_field)
	
	return freq_list,Fourier_transform,data

fh = open("acetonitrile.cat")
x = []
ymin = []
ymax = []

for line in fh:
	line = line.split()
	x.append(float(line[0])/1e6)
	ymin.append(0)
	ymax.append(10**(float(line[1]))*scale_factor)

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
plt.xlabel('Frequency (THz)')
plt.ylabel('% Power Change')
plt.vlines(x, ymin, ymax, colors=u'k', linestyles=u'solid')


if plot_time_figure==1:
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1, 1, 1)

if plot_freq_figure==1:
	fig3 = plt.figure()
	ax3 = fig3.add_subplot(1, 1, 1)
	plt.xlabel('Frequency (THz)')
	plt.ylabel('Magnitude')
	plt.vlines(x, ymin, ymax, colors=u'k', linestyles=u'solid')
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

full_spec = []

comb_list_length = len(comb_list)
counter = 1
for sample_file,rate in comb_list:	
    blank_file = sample_file
    freq_b,inten_b,data_b = fft_data(blank_file,rate)
    peak1_b,peak2_b,i_list = peakpicker(freq_b,inten_b,thresh,1000)
	#if plot_freq_figure==1:
		#ax3.plot(freq_b,inten_b,'k')
		#ax3.scatter(peak1_b,peak2_b)
    if plot_time_figure==1:
        ax1.scatter(peak1_b,peak2_b)
    freq_s =  freq_b
    inten_s = inten_b
    data_s = data_b
    peak1_s = [freq_s[x] for x in i_list ]
    peak2_s = [inten_s[x] for x in i_list ]
    if plot_freq_figure==1:
		test=1
		ax3.plot(freq_s,inten_s,'r')	
		#ax3.scatter(peak1_s,peak2_s)
    if plot_time_figure==1:
        ax1.scatter(peak1_s,peak2_s)
	
    absorption = [inten_s[x] for x in i_list]
    
    
    #ax1.scatter(peak1_s,absorption)
    x = np.array(peak1_s)
    y = np.array(absorption)
    blank_boxcar = movingaverage(y, 200)
    #ax1.plot(peak1_s,blank_boxcar,'r-')
   
    
    #absorption = [100*(1-(absorption[x]/blank_boxcar[x]))**2 for x in range(len(blank_boxcar))]
    spectrum = [(peak1_s[x],absorption[x]) for x in range(len(absorption))]
    full_spec+=spectrum
    print str(counter)+" of "+str(comb_list_length)+" combs done"
    counter+=1    
full_spec.sort()


file = ""
for line in full_spec:
	file+= str(line[0])+' '+str(line[1])+'\n'
fh = open("raw_peak_data.out","w")
fh.write(file)
fh.close()


	














