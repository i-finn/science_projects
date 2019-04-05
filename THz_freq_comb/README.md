# Description
I wrote these scripts with Dr. Jacob Good and Dr. Brandon Carroll to take data on a THz frequency comb spectrometer. Data taken with these scripts are presented in two publications:

Finneran, I. A., Good, J. T., Holland, D. B., Carroll, P. B., Allodi, M. A., & Blake, G. A. (2015). Decade-spanning high-precision terahertz frequency comb. Physical Review Letters, 114(16), 163902.

Good, J. T., Holland, D. B., Finneran, I. A., Carroll, P. B., Kelley, M. J., & Blake, G. A. (2015). A decade-spanning high-resolution asynchronous optical sampling terahertz time-domain and frequency comb spectrometer. Review of Scientific Instruments, 86(10), 103107.
# Files
* freq_counter.py : used to prepare the spectrometer for data acquisition (lock lasers) and keep track of laser repetition rate, which determines the time axis
* freq_comb_analysis_v3.py : used to analyze data from the instrument, specifically compute spectrum from time domain pulse train
* boxcar_v2.py : moving average for spectra analysis
* sim.py : data acquisition script, also automatically shift comb repetition rate
