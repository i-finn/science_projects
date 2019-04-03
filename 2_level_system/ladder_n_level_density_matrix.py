from pylab import *
from math import *
from numpy import *
import scipy.signal as signal

f = 2.0#frequency in THz
f0 = 1.0 #frequency in THz


w = f*6.283*10**12 
w0 = f0*6.283*10**12
start = 0.0
stop = 20000*10**-15 # in seconds
step = 0.1e-15
Gaussian_FWHM = 350*10**-15 #in seconds
c = Gaussian_FWHM/2.35482

A = 0.10  #enter electric field in MV/cm
D = 1 #enter transition dipole moment in debye
Amplitude = A*D*3.163029*10**12

t1 = 1500e-15
t2 = 4000e-15
T2 = 5000e-15

freq_axis = [x*(1/step)/(int(stop/step)*10**12) for x in range(int(stop/step))]
def O1(t):
    return -Amplitude*(e**(-((t-t1)**2)/(2*c**2)))*cos(w*t)#-Amplitude*(e**(-((t-t2)**2)/(2*c**2)))*(exp(-1j*w*t))#-Amplitude*(e**(-((t-800e-15)**2)/(2*c**2)))*cos(w*t)
    #return 0.0

Energy_list = [0,2.2*w0,4.0*w0]
#Energy_list = [x*w0 for x in Energy_list]
def ham_builder(dimension,dipole_strength,Energy_list):


    matrix = []
    for x in range(dimension):
        line = [0 for y in range(dimension)]
        line[x]=Energy_list[x]
        matrix.append(line)
        if x==0:
            line[x+1] = dipole_strength
        if x==(dimension-1):
            line[x-1]=conjugate(dipole_strength)
        else:
            line[x-1] =conjugate(dipole_strength)
            line[x+1] = dipole_strength      
    
    a = array(matrix,dtype=complex)
    return a


def T2_matrix(t,T2):
    return array([[1,1/T2,1/T2],[1/T2,1,1/T2],[1/T2,1/T2,1]],dtype=complex)
    #return array([[1,0.9,0.9],[0.9,1,0.9],[0.9,0.9,1]],dtype=complex)
    #return exp(-t/T2)






E_list = []
t=0
rho = array([[0.8,0,0],[0,0.2,0],[0,0,0]],dtype=complex)

dimension=3

dipole = 1

p_list = []
t_list = []
#print psi
pop_list = []
pop_list2 = []
pop_list3 = []
pop_list4 = []
pop_list5 = []
pop_list6 = []
pop_list7 = []
pop_list8 = []
pop_list9 = []
pop_list10 = []

dipole_strength = dipole
matrix = []
for x in range(dimension):
    line = [0 for y in range(dimension)]
    line[x]=0
    matrix.append(line)
    if x==0:
        line[x+1] = dipole_strength
    if x==(dimension-1):
        line[x-1]=dipole_strength
    else:
        line[x-1] =dipole_strength
        line[x+1] = dipole_strength      

dipole_matrix = array(matrix,dtype=complex)
p_list2 = []
phase = -1j
phase_shift_matrix = array([[1,-phase,-phase],[phase,1,-phase],[phase,phase,1]],dtype=complex)



for t in range(int((stop-start)/step)):
    t=t*step
    #print t
    t_list.append(t*10**12)
    dipole_strength = O1(t)
    Ham = ham_builder(dimension,dipole_strength,Energy_list)
    new_rho = (rho - (dot(Ham,rho)-dot(rho,Ham))*step*1j)
    new_rho = new_rho-T2_matrix(t,T2)*rho*step
    rho_shifted = new_rho*phase_shift_matrix
    rho = new_rho
    E = O1(t)/(3.163029e12*D)
    E_list.append(E)
    a = rho[0,0]
    b = rho[1,1]
    
    pop_list.append(a)
    pop_list2.append(b)
    p = trace(dot(dipole_matrix,rho))
    p_list.append(p)
    p_list2.append(0.1*trace(dot(dipole_matrix,rho_shifted))+E)
    #p_list2.append(0.01*p+E)
    #pop_list3.append(psi[2,0]*conjugate(psi[2,0]))
    #pop_list4.append(psi[3,0]*conjugate(psi[3,0]))
    #pop_list5.append(psi[4,0]*conjugate(psi[4,0]))
    #pop_list6.append(psi[5,0]*conjugate(psi[5,0]))
    #pop_list7.append(psi[6,0]*conjugate(psi[6,0]))
    #pop_list8.append(psi[7,0]*conjugate(psi[7,0]))
    #pop_list9.append(psi[8,0]*conjugate(psi[8,0]))
    #pop_list10.append(psi[9,0]*conjugate(psi[9,0]))

#p_list_2 = list(real(signal.hilbert(real(p_list))))

ax1 = subplot(4,1,1)


plot(t_list,E_list)
ylabel("Input E (MV/cm)")
xlabel('Time, ps')
#ax1 = subplot(5,1,1)
#ylabel("Population")
#ax1.plot(t_list,pop_list,label="0")
#ax1.plot(t_list,pop_list2,label="1")
#ax1.plot(t_list,pop_list3,label="2")
#ax1.plot(t_list,pop_list4,label="3")
#ax1.plot(t_list,pop_list5,label="4")
#ax1.plot(t_list,pop_list6,label="5")
#ax1.plot(t_list,pop_list7,label="6")
#ax1.plot(t_list,pop_list8,label="7")
#ax1.plot(t_list,pop_list9,label="8")
#ax1.plot(t_list,pop_list10,label="9")
#ylim([0,1])
subplot(4,1,2)


plot(t_list,p_list)
ylabel("Polarization")
xlabel('Time, ps')


#ax1.legend(loc=0, ncol=3,fontsize=7)


subplot(4,1,3)


plot(t_list,p_list2)
ylabel("Output E (MV/cm)")
xlabel('Time, ps')


#ax1.legend(loc=0, ncol=3,fontsize=7)

subplot(4,1,4)



ylabel("intensity (AU)")
xlabel('f, THz')


ax1.legend(loc=0, ncol=3,fontsize=7)
plot(freq_axis,abs(fft.fft(p_list2))**2/1000)
xlim([0,10])

show()









