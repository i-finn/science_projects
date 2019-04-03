These are some scripts for predicting 2D THz spectra in a n-level system using a reduced density matrix formalism. Molecules are treated quantum mechanically and the light fields are treated classically. The time evolution is calculated with a discrete time step solution to the Liouville–von Neumann equation. This whole process is repeated for two pulses with variable time delay between the pulses, generating a 2D time domain reponse. This process is very easy to parallelize, so I assign each core a different set of time delays. The final results are concatenated and plotted with a set of matlab scripts.

I wrote the initial version (shown here) and Dr. Ralph Welsch (now at Center for Free-Electron Laser Science, Hamburg, Germany) added more features and generally improved the code in a later version, which we used for analyzing experimental data in two publications. Please see the first PNAS paper for a detailed description of the code and application. I wrote the matlab data processing scripts with Dr. Marco Allodi (now at University of Chicago).





