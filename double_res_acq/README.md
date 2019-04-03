I wrote this script to take automated double resonance spectra on the microwave spectrometer at Caltech. My coworkers and I used it for several years to take data on a variety of projects. Here is an overview of the code:

1) User inputs a list of double resonance frequencies, chirped pulse parameters, and local oscillator frequencies.


For each set of double resonance frequencies the program performs the following steps:


1) A waveform is created that consists of a linearly chirped pulse and single tone sinc pulse. A separate waveform (the control) is created with a only the chirped pulse.

2) The waveform is uploaded to a Tektronix 10 GS/s arbitrary waveform generator via ethernet over the local area network. The waveform generator is initialized to prepare for triggered operation.

3) The frequency on the microwave synthesizer (local oscillator) is set to the correct value over serial communication

4) The digitizer on the computer is started via a mouse click (unfortunately there wasn't a good API for the digitizer at the time so we just used automated mouse clicking). When the acquisition is finished, a filename is automatically typed in and the time domain data is saved.

5) The above steps are repeated for the waveform that only has the chirped pulse.


Altogether, this program allows the user to determine which peaks in a spectrum are connected to which other peaks. This helps considerably in spectral assignment.
