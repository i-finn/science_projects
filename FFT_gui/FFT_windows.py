from Tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from easygui import *
from numpy import *
from numpy import array
from scipy.fftpack import fft
from math import pi,atan2,log

# plotting function: clear current, plot & redraw
counter =0
def plot(x, y):
    global counter
    global plot_handle

    plt.figure(1)
    
    plt.clf()
    
    plt.plot(x,y)
        # just plt.draw() won't do it here, strangely

    plt.gcf().canvas.draw()
    
def plot2(x, y,x2,y2):
    plt.figure(2)
    plt.clf()
    plt.plot(x,y)
    #plt.ylim([0,1])
    plt.plot(x2,y2)
    # just plt.draw() won't do it here, strangely
    plt.gcf().canvas.draw()

# just to see the plot change
plotShift = 0
"""
def main():

    global E_field
    global cut_E_field


    #global plotShift

    ##x = np.arange(0.0,3.0,0.01)
    #y = np.sin(2*np.pi*x + plotShift)
    #plot(x, y)

    #plotShift += 1
"""
def main2():
    global E_field
    global time_values
    global cut_E_field
    global sample_rate
    global filename
    sample_rate = float(app_entry5.get())*1e9
    fh = open(filename)
    E_field = []
    time_values = []
    for line in fh:
       E_value = float(line.split()[1])#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<set col here
       
       E_field.append(E_value)
    fh.close()
    for time in range(0,len(E_field)):
       time_value = (time/sample_rate)*1e6
       time_values.append(time_value) 



    lower_bound = float(app_entry.get())
    upper_bound = float(app_entry2.get())

    f_lower_bound = float(app_entry3.get())*1e6
    f_upper_bound = float(app_entry4.get())*1e6

    
    cut_E_field = E_field[int(lower_bound*sample_rate*1e-6):int(upper_bound*sample_rate*1e-6)]
    average = sum(cut_E_field)/len(cut_E_field)
    cut_E_field = [asd-average for asd in cut_E_field]
                   
    cut_time_values = time_values[int(lower_bound*sample_rate*1e-6):int(upper_bound*sample_rate*1e-6)]
    plot2(time_values,E_field,cut_time_values,cut_E_field)

    zero_padding = list(zeros(len(cut_E_field)))
    cut_E_field_new = [float(a)*float(b) for a,b in zip(list(kaiser(len(cut_E_field),6)),cut_E_field)]#<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    cut_E_field_new=cut_E_field_new+zero_padding+zero_padding+zero_padding+zero_padding+zero_padding+zero_padding+zero_padding+zero_padding+zero_padding#<<<<<<<<<<<<<<<<<<<<<<
    num = len(cut_E_field_new)

    noct=int(log(num)/log(2))

    num_fft=2**noct
    df = 1/(float(num_fft)*(1/sample_rate))
    cut_E_field_new=cut_E_field_new[0:num_fft]

    fft_length = float(sample_rate)
    freq_list = []

    for f in range(0,int(fft_length/df)):
       freq_list.append(f*df/1e6)

    


    Fourier_transform =abs(fft(cut_E_field_new))
    length_freq_list = len(freq_list)
    freq_list = freq_list[0:length_freq_list/2]
    Fourier_transform = Fourier_transform[0:length_freq_list/2]

    
    freq_list = freq_list[int(f_lower_bound/df):int(f_upper_bound/df)]
    Fourier_transform = Fourier_transform[int(f_lower_bound/df):int(f_upper_bound/df)]
    print len(freq_list),len(Fourier_transform)
    plot(freq_list,Fourier_transform)


    #x = np.arange(0.0,3.0,0.01)
    #y = np.sin(2*np.pi*x + plotShift)
    #plot2(x, y)
    
    #plotShift += 1

def file1():
    #f = tk_FileDialog.askopenfilename(parent=localRoot)
    global E_field
    global time_values
    global sample_rate
    global filename
    filename =fileopenbox(msg="Choose your Spectrum")
    
# GUI
root = Tk()
counter =0

#draw_button = Button(root, text="Update FFT", command = main)
draw_button2 = Button(root, text="UPDATE", command = main2)
draw_button3 = Button(root, text="FID Filename", command = file1)
app_entry = Entry(root)
label = Label(root,text="Lower t (us)")
label2 = Label(root,text="Upper t (us)")
label3 = Label(root,text="Lower f (MHz)")
label4 = Label(root,text="Upper f (MHz)")
label5 = Label(root,text="Sample Rate(Gs/s)")
app_entry2 = Entry(root)
app_entry3 = Entry(root)
app_entry4 = Entry(root)
app_entry5 = Entry(root)
app_entry.insert(0,"0.0")
app_entry2.insert(0,"10.0")
app_entry3.insert(0,"1.0")
app_entry4.insert(0,"2500")
app_entry5.insert(0,"5")

#draw_button.grid(row=1, column=0)
draw_button2.grid(row=2, column=1)
draw_button3.grid(row=3, column=1)
app_entry.grid(row=5, column=1)
app_entry2.grid(row=6, column=1)
app_entry3.grid(row=7, column=1)
app_entry4.grid(row=8, column=1)
app_entry5.grid(row=9, column=1)
label.grid(row=5, column=0)
label2.grid(row=6, column=0)
label3.grid(row=7, column=0)
label4.grid(row=8, column=0)
label5.grid(row=9, column=0)

# init figure
fig = plt.figure(1)
canvas = FigureCanvasTkAgg(fig, master=root)
toolbar = NavigationToolbar2TkAgg(canvas, root)
canvas.get_tk_widget().grid(row=0,column=2)
toolbar.grid(row=1,column=2)
fig2 = plt.figure(2)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
toolbar2 = NavigationToolbar2TkAgg(canvas2, root)
canvas2.get_tk_widget().grid(row=0,column=3,columnspan=10)
toolbar2.grid(row=1,column=3)
root.mainloop()
