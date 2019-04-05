# Description
I wrote this script with Daniel Guth and Jerry Feng at Caltech for the microwave spectrometer. We used it for several years to deconvolve spectra from the instrument. It takes in two spectra with different local oscillator settings as inputs. It compares peaks in the two spectra and determines if they are in the lower sideband or upper sideband. Then it outputs a deconvolved spectrum by folding the input spectrum over both sides of the local oscillator and cutting out peaks that are in the wrong sideband. It is not a very elegant solution, but it works if the spectra are fairly sparse --- which was the case for nearly all of the data sets taken on this instrument. 
# Files
* Spectra_Deconvolution.py : main script for deconvolution
