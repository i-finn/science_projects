import numpy as np
import matplotlib.pyplot as plt
from numpy import array
from scipy.fftpack import fft
from math import pi,atan2,log
import scipy.interpolate as inter
import numpy as np
import pylab as plt

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

###############
###############
import os
from os import path
fh = open("raw_peak_data.out")

full_spec = []
for line in fh:
	line.split()
	f = float(line.split()[0])
	
	i = float(line.split()[1])
	full_spec.append((f,i))

f = [x[0] for x in full_spec]
i = [x[1] for x in full_spec]

y = np.array(i)
blank_boxcar = movingaverage(y, 2000)
absorption = [100*(1-(i[x]/blank_boxcar[x]))**2 for x in range(len(blank_boxcar))]

absorption = movingaverage(np.array(absorption), 10)

ax1.plot (f,absorption)
plt.show()
	#ax2.plot(data)
#full_spec.sort()
a = np.dstack((f,absorption))
print a
np.savetxt("test.txt",a[0])
#file = ""
#for x in range(len(full_spec)):
#	file+= str(f[x])+' '+str(absorption[x])+'\n'
#fh = open("spectrum.out","w")
#fh.write(file)
#fh.close()
	
