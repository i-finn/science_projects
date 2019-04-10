# Description
I wrote this script for the microwave spectrometer at Caltech. It uses matplotlib embedded in tkinter to generate a simple GUI. Time domain data is read in from a file and the user can select a particular time window. The time domain data is zero padded, apodized, shifted to zero offset, and then the discrete fast Fourier transform (FFT) is calculated and displayed. Units are MHz for frequency and microseconds for time.

In the interface (shown below), the left panel is the FFT, and the right panel is the time domain data. Users input the start and end time for the FFT and the script cuts the time domain data (green trace) and calculates the FFT based on the input sample rate. Some example data for propylene oxide is included (prop_oxide_set1.trc).

# Files

* FFT_windows.py : main script
* prop_oxide_set1.trc : example input from the molecule propylene oxide

# Screenshot

![alt text](https://github.com/iafinn/science_projects/blob/master/FFT_gui/screenshot2.png)



