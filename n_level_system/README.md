I wrote this script to take an n-level quantum system and numerically calculates its response to an arbitrary classical electric field, given a set of electric dipole coupling strengths between levels. It is a very simple discrete time step solution to the time-dependent Schrodinger equation, and shouldn't be used for long timescales (>20 picoseconds) as the error becomes quite large. It plots the output induced polarization, output electric field, and the Fourier transform of the output E field. This code eventually turned into the RDM code.


![alt text](https://github.com/iafinn/science_projects/blob/master/2_level_system/output.png)
