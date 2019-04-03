

import os
import numpy as np
import sys
import re
import random
import string
from numpy import linalg as LA
import pylab
import math
from numpy import *
from scipy import *
import subprocess
import numpy as np
import subprocess
from math import *
import matplotlib.pyplot as plt
def noise(spectrum):
    spectra_int = []
    spectra_freq = []     
    for i in range(len(spectrum)):                                                  # leave at 0 to include all points in graph
        freq = spectrum[i][0] 
        int = spectrum[i][1] 
        spectra_freq.append(freq)
        spectra_int.append(int)
    return average(spectra_int)*3

    

	
	

def coadd(data_tuple):
	
	#parse each line from the datafile into a tuple of the form (xvals,yvals)
	#store that tuple in a list.
	data = [np.array(fname).T for fname in data_tuple]

	#This is the minimum and maximum from all the datapoints.
	xmin = min(line[0].min() for line in data)
	xmax = max(line[0].max() for line in data)
	p_num = data[0].shape

	#100 points evenly spaced along the x axis
	x_points = np.linspace(xmin,xmax,(p_num[0]+p_num[1]))

	#interpolate your values to the evenly spaced points.
	interpolated = [np.interp(x_points,d[0],d[1]) for d in data]

	#Now do the averaging.
	averages = [np.average(x) for x in zip(*interpolated)]
	final_data = []
	#put the average value along with it's x point into a file.

	for x,avg in zip(x_points,averages):
		final_data.append((x,avg))

	return final_data
	
	
	
	
	
    
    
    
def grapher2(spectrum):
    '''Given an input of a list of frequencies and intensities, plots it on a graph.'''
    spectra_int = []
    spectra_freq = []
    fieldNames = [" "]
    enter_list = []
    #enter_list = multenterbox("Pick a noise floor","Pick a noise floor",fieldNames) # most computers can't graph the half million points, so 
    #floor = float(enter_list[0])                                                    # not counting all points below a certain intensity fixes this
    counter = 0
    skip_num = 1 
    for i in range(len(spectrum)):                                                  # leave at 0 to include all points in graph
        freq = spectrum[i][0] 
        int = spectrum[i][1]
	counter+=1
        if counter==skip_num:
	    counter = 0 
            spectra_freq.append(freq)
            spectra_int.append(int)
    print "Begin Graphing Here"
    plt.scatter(spectra_freq,spectra_int)
    print len(spectra_freq)
    print len(spectra_int)
    plt.ylabel('Intensity')
    plt.xlabel('Frequency')



def grapher(spectrum):
    '''Given an input of a list of frequencies and intensities, plots it on a graph.'''
    spectra_int = []
    spectra_freq = []
    fieldNames = [" "]
    enter_list = []
    #enter_list = multenterbox("Pick a noise floor","Pick a noise floor",fieldNames) # most computers can't graph the half million points, so 
    #floor = float(enter_list[0])                                                    # not counting all points below a certain intensity fixes this
    counter = 0
    skip_num = 1 
    for i in range(len(spectrum)):                                                  # leave at 0 to include all points in graph
        freq = spectrum[i][0] 
        int = spectrum[i][1]
	counter+=1
        if counter==skip_num:
	    counter = 0 
            spectra_freq.append(freq)
            spectra_int.append(int)
    print "Begin Graphing Here"
    plt.plot(spectra_freq,spectra_int)
    
    print len(spectra_freq)
    print len(spectra_int)
    plt.ylabel('Intensity')
    plt.xlabel('Frequency')
    

    

def secondIndex(number, lst):
    '''Returns the second index of a number in a list.'''
    a = lst[:]
    first = a.index(number)
    a[first] = a[first]+1
    if number in a:
        return a.index(number)
    else:
        return 0

def peakpick(input_spectrum, thresh):
    '''This routine takes a spectrum and returns a list of peaks above a certain threshold.'''
    #f = loadtxt(fileopenbox(filetypes = ["*.txt"]))
    spectrum = input_spectrum
    peaks=[]
    for i in range(0, len(spectrum)):
        if (i != 0) and (i != (len(spectrum)-1)):
            if (spectrum[i][1] > thresh) and (spectrum[i][1] > spectrum[(i-1)][1]) and (spectrum[i][1] > spectrum[(i+1)][1]):
                peaks.append((spectrum[i][0], spectrum[i][1]))
    print len(peaks)
    return peaks

def peak_shift(peaks_lower, peaks_upper, MHz):
    '''This routine checks whether the peak was shifted up or down; MHz should be the frequency of the original spectrum .'''
    down_shifted = []
    up_shifted = []
    peaks_to_cut = []
    size = .25                                # size is how much error the program will accept when comparing the two peaks
    for i in range(len(peaks_lower)):
        for j in range(len(peaks_upper)):
            shift_up = peaks_upper[j][0] - 10
            shift_down = peaks_upper[j][0] + 10
            frequency = peaks_lower[i][0]
            if (frequency < shift_up + size) and (frequency > shift_up - size):
                down_shifted.append(peaks_lower[i])
            elif (frequency < shift_down + size) and (frequency > shift_down - size):      
                up_shifted.append(peaks_lower[i])


    ''' This shows that the spectrum taken at 10 hz higher is either shifted up or down.
    If the number shifts up, the mixer subtracts the two, so the peak will be on the lower end.
    If the number shifts down, the mixer adds the two, so the peak will be on the upper end.'''

    real_spectrum = []
    for value in down_shifted:
        real_spectrum.append((MHz - value[0] ,value[1]))
        peaks_to_cut.append(MHz + value[0])
    for value in up_shifted:                                       
        real_spectrum.append((value[0] + MHz,value[1]))
        peaks_to_cut.append(MHz - value[0])
    print len(real_spectrum)
    return real_spectrum,peaks_to_cut
    
def peak_shift2(peaks_lower, peaks_upper, MHz):
    '''This routine checks whether the peak was shifted up or down; MHz should be the frequency of the original spectrum .'''
    down_shifted = []
    up_shifted = []
    peaks_to_cut = []
    size = .25                                # size is how much error the program will accept when comparing the two peaks
    for i in range(len(peaks_lower)):
        for j in range(len(peaks_upper)):
            shift_up = peaks_upper[j][0] + 10
            shift_down = peaks_upper[j][0] - 10
            frequency = peaks_lower[i][0]
            if (frequency < shift_up + size) and (frequency > shift_up - size):
                down_shifted.append(peaks_lower[i])
            elif (frequency < shift_down + size) and (frequency > shift_down - size):      
                up_shifted.append(peaks_lower[i])


    ''' This shows that the spectrum taken at 10 hz higher is either shifted up or down.
    If the number shifts up, the mixer subtracts the two, so the peak will be on the lower end.
    If the number shifts down, the mixer adds the two, so the peak will be on the upper end.'''

    real_spectrum = []
    for value in down_shifted:
        real_spectrum.append((MHz - value[0] ,value[1]))
        peaks_to_cut.append(MHz + value[0])
    for value in up_shifted:                                       
        real_spectrum.append((value[0] + MHz,value[1]))
        peaks_to_cut.append(MHz - value[0])
    print len(real_spectrum)
    return real_spectrum,peaks_to_cut
    
def deconvolve(spectrum, MHz, peak_list_to_cut):
    '''This takes the spectra and deconvolves it using the list of peaks and the frequency of the original spectrum.'''
    peak_list_to_cut.append(MHz+1000.0)
    peak_list_to_cut.append(MHz-1000.0)
    peak_list_to_cut.append(MHz+1500.0)
    peak_list_to_cut.append(MHz-1500.0)
    spectra_frequency = []
    spectra_intensity = []
    peak_frequency = []
    peak_intensity = []
    for i in range(len(spectrum)):
        spectra_frequency.append(spectrum[i][0])
        spectra_intensity.append(spectrum[i][1])
    full_spectrum_freq = []
    full_spectrum_int = []
    for i in range(len(spectra_frequency)):
        full_spectrum_freq.append( MHz - spectra_frequency[i]  )
        full_spectrum_int.append(spectra_intensity[i])
    for i in range(len(spectra_frequency)):
        full_spectrum_freq.append(spectra_frequency[i] + MHz)
        full_spectrum_int.append(spectra_intensity[i])
    
    # This duplicates the spectrum so we can remove the peaks from it
    
    for i in range(len(peak_list_to_cut)):
        freq = peak_list_to_cut[i]
        peak_frequency.append(freq)
        
    cut_width = 0.5
    for i in range(len(peak_frequency)):
        if peak_frequency[i] in full_spectrum_freq:
            a = full_spectrum_freq.index(peak_frequency[i])
            
            for j in range(20):             
                if full_spectrum_freq[a+j]-full_spectrum_freq[a] < cut_width and full_spectrum_freq[a-j]-full_spectrum_freq[a] > -cut_width:
                    full_spectrum_int[a+j] = 0
                    full_spectrum_int[a-j] = 0
            # this removes the peak by setting all the values within the width of the peak to 0
        
    deconvolved_spectrum = []
    for k in range(len(full_spectrum_freq)):
        
        freq = full_spectrum_freq[k]
        int = full_spectrum_int[k]
        deconvolved_spectrum.append((freq, int))
    deconvolved_spectrum.sort()
    return deconvolved_spectrum

	

	
	
   
def file_reader(filename):  
    


    
    file = open(filename)
    spectra_11000 = []
    for line in file:
        frequency = float(line.split()[0])
        
        intensity = float(line.split()[1])
        if frequency<5.0 or frequency>1970:
            intensity=0.0    

        
        spectra_11000.append((frequency,intensity))
    file.close()
    return spectra_11000
    
 
    
def SSB(spectrum, MHz, SB):
    '''This takes the spectra and deconvolves it using the list of peaks and the frequency of the original spectrum.'''
    new_spectrum = []
    if SB == 'USB':
        for i in range(len(spectrum)):
            new_spectrum.append((spectrum[i][0]+MHz,spectrum[i][1]))
    if SB == 'LSB':
        for i in range(len(spectrum)):
            new_spectrum.append((spectrum[i][0]-MHz,spectrum[i][1]))            
        

    return new_spectrum
          
             
                
                   
                      
                         
                            
                               
                                  
                                     
                                        
                                           
                                              
                          
spectra_16010 = file_reader('methdethd16.01ghzaveraged.txt_FFT.txt')
spectra_16000 = file_reader('methdethd16.0ghzaveraged.txt_FFT.txt') 

spectra_11010 = file_reader('methdethd12.01ghzaveraged.txt_FFT.txt')
spectra_11000 = file_reader('methdethd12.0ghzaveraged.txt_FFT.txt')  
spectra_8000 = file_reader('methdethd8.0ghzaveraged.txt_FFT.txt')



#grapher(spectra_10000)




spectra_11010_peaks = peakpick(spectra_11010, noise(spectra_11010))
spectra_11000_peaks = peakpick(spectra_11000, noise(spectra_11000))



spectra_16010_peaks = peakpick(spectra_16010, noise(spectra_16010))
spectra_16000_peaks = peakpick(spectra_16000, noise(spectra_16000))

peak_list_11000,peaks_to_cut_11000 = peak_shift(spectra_11000_peaks,spectra_11010_peaks,12000)

peak_list_11010,peaks_to_cut_11010 = peak_shift2(spectra_11010_peaks,spectra_11000_peaks,12010)

peak_list_16000,peaks_to_cut_16000 = peak_shift(spectra_16000_peaks,spectra_16010_peaks,16000)

peak_list_16010,peaks_to_cut_16010 = peak_shift2(spectra_16010_peaks,spectra_16000_peaks,16010)

#grapher2(peak_list)



deconv_spectrum_11000 = deconvolve(spectra_11000, 12000, peaks_to_cut_11000)

deconv_spectrum_11010 = deconvolve(spectra_11010, 12010, peaks_to_cut_11010)

deconv_spectrum_16000 = deconvolve(spectra_16000, 16000, peaks_to_cut_16000)

deconv_spectrum_16010 = deconvolve(spectra_16010, 16010, peaks_to_cut_16010)

deconv_spectrum_8000 = SSB(spectra_8000, 8000, 'USB')

#grapher(spectra_14000)
#grapher2(peak_list_14000)

#grapher(deconv_spectrum_16000[int(len(deconv_spectrum_16000)/4):])
#grapher(deconv_spectrum_14000[int(len(deconv_spectrum_14000)/8):int(len(deconv_spectrum_14000)*3/4)])
#grapher(deconv_spectrum_11000[int(len(deconv_spectrum_11000)/8):int(len(deconv_spectrum_11000)*7/8)])
#grapher(deconv_spectrum_8000[0:int(len(deconv_spectrum_8000)*3/4)])
#~final_spec = deconv_spectrum_11000+deconv_spectrum_15600

final_spec2 = coadd((deconv_spectrum_11000,deconv_spectrum_11010))

final_spec1 = deconv_spectrum_8000
final_spec3 = coadd((deconv_spectrum_16000,deconv_spectrum_16010))
final_spec = final_spec1+final_spec2+final_spec3

fh = open('coadd_out.txt','w')

file_str = ''
for line in final_spec:
    file_str+= str(line[0]) + ' ' + str(line[1]) + '\n'


fh.write(file_str)
fh.close()