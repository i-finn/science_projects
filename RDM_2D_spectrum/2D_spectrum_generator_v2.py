import sys
from multiprocessing import Process
#from pylab import *
from math import *
from numpy import *
import csv

from math import *
from numpy import *



def O1(t,Amplitude1,Amplitude2,Amplitude3,c,w,t1,t2,t3):
    t1 = -t1
    t2 = -t2
    t3 = -t3
    return Amplitude1*(e**(-((t-t1)**2)/(2*c**2)))*cos(w*(t-t1))+Amplitude2*(e**(-((t-t2)**2)/(2*c**2)))*cos(w*(t-t2))+Amplitude3*(e**(-((t-t3)**2)/(2*c**2)))*cos(w*(t-t3))
    #return 0.0
def T2_matrix(t,T2_a,T2_b):
        return array([[1,1/T2_a,1/T2_b],[1/T2_a,1,1/T2_a],[1/T2_b,1/T2_a,1]],dtype=complex)
        #return array([[1,1,1/T2_b],[1,1,1],[1/T2_b,1,1]],dtype=complex)
        #return array([[1,0.9,0.9],[0.9,1,0.9],[0.9,0.9,1]],dtype=complex)
        #return exp(-t/T2)

def ham_builder(dimension,dipole_strength,Energy_list):


    matrix = [[Energy_list[0],dipole_strength,dipole_strength],[conjugate(dipole_strength),Energy_list[1],dipole_strength],[conjugate(dipole_strength),conjugate(dipole_strength),Energy_list[2]]]
    """
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
    """
    a = array(matrix,dtype=complex)
 
    return a

def polarization(t1_list,t2,t3,A1,A2,A3):
    for t1 in t1_list:
        
        f = 3.0#frequency in THz
        f0 = 1.0 #frequency in THz
        
        
        w = f*6.283*10**12 
        w0 = f0*6.283*10**12
        start = -1000*10**-15
        stop = 4000*10**-15 # in seconds
        step = 1.0e-15
        Gaussian_FWHM = 400*10**-15 #in seconds
        c = Gaussian_FWHM/2.35482
        
        A = 0.3  #enter electric field in MV/cm
        D = 0.1 #enter transition dipole moment in debye
        Amplitude1 = A*D*3.163029*10**12*A1
        Amplitude2 = A*D*3.163029*10**12*A2
        Amplitude3 = 0
        #Amplitude3 = A*D*3.163029*10**12*A3
        #t1 = 1500e-15
        #t2 = 4000e-15
        #t3 = 5000e-15
        T2_a = 1700e-15
        T2_b = 1700e-15
        freq_axis = [x*(1/step)/(int(stop/step)*10**12) for x in range(int(stop/step))]
    
        
        Energy_list = [0,2.7*w0,6.6*w0]
        #Energy_list = [x*w0 for x in Energy_list]
        E_list = []
        t=0
        rho = array([[exp(0/6.2),0,0],[0,exp(-2.7/6.2),0],[0,0,exp(-6.56/6.2)]],dtype=complex)
        rhoA = rho
        rhoB = rho
        old_rho = rho
        old_rhoA = rho
        old_rhoB = rho
		
		
		
		
		
		
		
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
        
        
        
        counter =0 
        for t in range(int((stop-start)/step)):
            t=t*step+start
            
            #print t
            #t_list.append(t*10**12)
            
            ###AB
            dipole_strength = O1(t,Amplitude1,Amplitude2,Amplitude3,c,w,t1,t2,t3)
            Ham = ham_builder(dimension,dipole_strength,Energy_list)
            new_rho = (old_rho - (dot(Ham,rho)-dot(rho,Ham))*step*2j)
            new_rho = new_rho-T2_matrix(t,T2_a,T2_b)*rho*step*2
            rho_shifted = new_rho*phase_shift_matrix
            old_rho = rho
            rho = new_rho
            ###
            
            ###A
            dipole_strength = O1(t,Amplitude1,0,0,c,w,t1,t2,t3)
            Ham = ham_builder(dimension,dipole_strength,Energy_list)
            new_rhoA = (old_rhoA - (dot(Ham,rhoA)-dot(rhoA,Ham))*step*2j)
            new_rhoA = new_rhoA-T2_matrix(t,T2_a,T2_b)*rhoA*step*2
            rho_shiftedA = new_rhoA*phase_shift_matrix
            old_rhoA = rhoA
            rhoA = new_rhoA             
            ###
            
            ###B
            dipole_strength = O1(t,0,Amplitude2,Amplitude3,c,w,t1,t2,t3)
            Ham = ham_builder(dimension,dipole_strength,Energy_list)
            new_rhoB = (old_rhoB - (dot(Ham,rhoB)-dot(rhoB,Ham))*step*2j)
            new_rhoB = new_rhoB-T2_matrix(t,T2_a,T2_b)*rhoB*step*2
            rho_shiftedB = new_rhoB*phase_shift_matrix
            old_rhoB = rhoB
            rhoB = new_rhoB  
            ###
            
            
            #E = O1(t,Amplitude1,Amplitude2,Amplitude3,c,w,t1,t2,t3)/(3.163029e12*D)
            #E_list.append(E)
            #a = rho[0,0]
            #b = rho[1,1]
            
            #pop_list.append(a)
            #pop_list2.append(b)
            #p = trace(dot(dipole_matrix,rho))
            #p_list.append(p)
            #p_list2.append(0.1*trace(dot(dipole_matrix,rho_shifted))+E)
            if counter%10==0:
				p_list2.append([t*10**12,real(0.1*trace(dot(dipole_matrix,rho_shifted))-0.1*trace(dot(dipole_matrix,rho_shiftedA))-0.1*trace(dot(dipole_matrix,rho_shiftedB)))])
            #counter+=1
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
        

        
        myfile = open('test__%.6f_t1_01'%(t1*10**12), 'w')
        wr = csv.writer(myfile,delimiter=' ')
        wr.writerow(['Pointsperps',int(1/(step*10**12)),'window(ps)',int((stop-start)*10**12-1)])
        wr.writerows(p_list2)    
        myfile.close()
        
    
    #return(t_list,p_list2)

if __name__ == '__main__':
    processors = 6
    start = -1500*10**-15
    stop =  1500*10**-15 # in seconds
    step =  50e-15

    t2 = 0
    t3 = 11000e-15
    
    A1 = 1.0
    A2 = 1.0
    A3 = 1.0
    t_list = [t*step+start for t in range(int((stop-start)/step)+1)]
    t_list_parts = []
    for num in range(processors):
        processors = float(processors)
        num = float(num)
        x = int((num)*(len(t_list)/processors))
        y = int(len(t_list)*((num+1)/processors))
        t_list_parts.append(t_list[x:y])
    
    
    processors = int(processors)
    
    for num in range(processors):
        vars()["p%s"%str(num)] = Process(target=polarization, args=(t_list_parts[num],t2,t3,A1,A2,A3))
    
    for num in range(processors):
        vars()["p%s"%str(num)].start()
    for num in range(processors):
        vars()["p%s"%str(num)].join()            
                
                            
    











