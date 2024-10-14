# Studies

QEnergy currently holds 14 studies scripts (in the `studies` folder), corresponding to the figures shown in the article:

* `all_to_all.py`: energy to distribute all-to-all entanglement;
* `bb84_detector.py`: analysis of the impact of different detectors on the BB84 energy consumption;
* `bb84_qber.py`: analysis of the impact of the QBER value on the BB84 energy consumption;
* `bb84_wavelength.py`: analysis of the impact of the wavelength (and detector choice) on the BB84 energy consumption;
* `cka_dist.py`: analysis of the impact of the distance on several Conference Key Agreement protocols;
* `cka.py`: analysis of the impact of the number of parties on several Conference Key Agreement protocols;
* `cv_vs_dv.py`: comparison of DV and CV-QKD energy consumption;
* `cvcka.py`: analysis of the energy consumption of a CV-CKA protocol, in function of the distance and the number of parties;
* `cvqkd.py`: analysis of the energy consumption of the CV-QKD protocol as a function of the distance, for the Gaussian modulated and QPSK modulated case (also nCV-QKD for CKA);
* `energy_efficiency.py`: plot of the energy efficiency metric for DV protocols;
* `measured_values.py`: comparisons of energy consumption between datasheet values and measured values;
* `piecharts.py`: analysis of the repartition of power consumption for several setups;
* `qkd_protocols.py`: analysis of energy consumption for three DV protocols (BB84, E91, MDI);
* `timevspolar.py`: comparison of polarization and time-bin encoding.

The studies can be run individually with their respective python script, or using the Makefile.