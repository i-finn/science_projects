# Description
I wrote this program with Prof. Steve Shipman (New College of Florida) to fit rotational spectra. We never quite finished the program and it still has a few bugs. Nonetheless, it was probably the most useful script in my PhD thesis work as it allowed me to rapidly analyze results from autofit and do the final spectral fits. It uses PyQT4 and matplotlib to generate the GUI. My coworkers and I used it extensively (along with autofit) to analyze data from the Caltech microwave spectrometer. A screenshot is shown below. Here is a walkthrough of typical usage:

* load an experimental spectrum using the file menu
* set the level of the noise in the spectrum and perform a peakfinder (peaks now have dots at the top)
* plug in a set of spectroscopic constants from autofit, then click plot input
* in the top frame you now have a simulated autofit result (black) and experimental (red) spectrum
* adjust the rotational constant sliders to see how the spectrum changes and see how robust the fit actually is
* now start assigning peaks in the spectrum by clicking in the simulated and experimental panels. this can be done with just 3 clicks
* perform nonlinear least square fitting on your assignments. the program automatically updates your predicted spectrum
* when you are satisfied with the fits, grab the SPFIT output files to get the standard errors of the parameters and RMS error of the fit


This program uses SPFIT and SPCAT for prediction of rotational spectra. These programs are quite fast (~20 ms per fit per core on Intel Ivy Bridge CPU) and have become a gold standard in the field. They were written by Dr. Herb Pickett at [JPL](https://spec.jpl.nasa.gov/) and are decribed in this publication:

Pickett, H. M. (1991). The fitting and prediction of vibration-rotation spectra with spin interactions. Journal of Molecular Spectroscopy, 148(2), 371-377.

# Files

* fitting_GUI_v11B.py : main program
* fitting_GUI_B_v11.py : supporting module

# Screenshot


![alt text](https://github.com/iafinn/science_projects/blob/master/rot_spectra_fitting_GUI/screenshot.png)
