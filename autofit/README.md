# Description
## please see [official documentation here](http://faculty.virginia.edu/bpate-lab/autofit/intro.html) and [official repository here](https://github.com/pategroup/bband_scripts/tree/master/autofit)
This was a somewhat longer project that evolved into a collaboration at three institutions (New College, UVa, Caltech). The basic idea is a multicore automated assigner of molecular rotational spectra. The algorithm was proposed and first implemented by the Pate lab at UVa in ptc mathcad. Prof. Steve Shipman and I developed a separate version in python and successfully used it to automatically fit many different spectra. It started as a section of my undergraduate thesis, but we continued to improve the code while I was at Caltech. Nathan Seifert and the Pate lab at UVa put together an excellent set of documentation for the program (linked above), added some extra features, and also benchmarked it on the molecule hexanal. These results are presented in this publication:

Seifert, Nathan A., Ian A. Finneran, Cristobal Perez, Daniel P. Zaleski, Justin L. Neill, Amanda L. Steber, Richard D. Suenram, Alberto Lesarri, Steven T. Shipman, and Brooks H. Pate. "AUTOFIT, an automated fitting tool for broadband rotational spectra, and applications to 1-hexanal." Journal of Molecular Spectroscopy 312 (2015): 13-21.

Autofit uses SPFIT and SPCAT for rotational spectra prediction. These programs are quite fast (~20 ms per fit per core on Intel Ivy Bridge CPU) and have become a gold standard in the field. They were written by Dr. Herb Pickett at [JPL](https://spec.jpl.nasa.gov/) and are decribed in this publication:

Pickett, H. M. (1991). The fitting and prediction of vibration-rotation spectra with spin interactions. Journal of Molecular Spectroscopy, 148(2), 371-377.


# Files

* prog_A_v14b.py : main program

# Program overview


![alt text](https://github.com/iafinn/science_projects/blob/master/autofit/overview.png)

