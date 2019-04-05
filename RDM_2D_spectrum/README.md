These are some scripts for predicting 2D THz spectra in a n-level system using a reduced density matrix formalism. Molecules are treated quantum mechanically and the light fields are treated classically. The time evolution is calculated with a discrete time step solution to the Liouville–von Neumann equation. This whole process is repeated for two pulses with variable time delay between the pulses, generating a 2D time domain reponse. This process is very easy to parallelize, so I assign each core a different set of time delays. The final results are concatenated and plotted with a set of matlab scripts. An example output is shown below.

2D_spectrum_generator_v2.py : Takes input parameters, performs main calculation.

Average_Data_wHeader_2D.m : Reads in idividual scans (vectors) and turns them into a matrix. This script was also used for averaging experimental data

FFT_2D_2.m : calculates 2D FFT of the data to get the 2D spectrum.

I wrote the initial version (shown here) and Dr. Ralph Welsch (now at Center for Free-Electron Laser Science, Hamburg, Germany) added more features and generally improved the code in a later version, which we used for analyzing experimental data in two publications. I wrote the matlab data processing scripts with Dr. Marco Allodi (now at University of Chicago). Please see the first PNAS paper for a detailed description of the code and application. It is available from the PNAS website free of charge.

PNAS: Finneran, I. A., Welsch, R., Allodi, M. A., Miller, T. F., & Blake, G. A. (2016). Coherent two-dimensional terahertz-terahertz-Raman spectroscopy. Proceedings of the National Academy of Sciences, 113(25), 6857-6861. [Paper available here](https://doi.org/10.1073/pnas.1605631113)

Followup paper: Finneran, I. A., Welsch, R., Allodi, M. A., Miller III, T. F., & Blake, G. A. (2017). 2D THz-THz-Raman photon-echo spectroscopy of molecular vibrations in liquid bromoform. The Journal of Physical Chemistry Letters, 8(18), 4640-4644. [link to details](https://authors.library.caltech.edu/81443/2/jz7b02106_si_001.pdf)

![alt text](https://github.com/iafinn/science_projects/blob/master/RDM_2D_spectrum/example.png)






