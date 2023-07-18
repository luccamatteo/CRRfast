[![](https://img.shields.io/badge/arXiv-2306.08085%20-red.svg)](https://arxiv.org/abs/2306.08085)

# CRRfast, an emulator for the Cosmological Recombination Radiation with effects from inhomogeneous recombination

CRRfast is an emulator designed to quickly and accurately represent the CRR spectrum for a wide range of cosmologies, using the state- of-the-art CosmoSpec code as a reference [Chluba & Ali-Haimoud 2016](https://arxiv.org/abs/1510.03877) (arXiv:1510.03877). This code can be used freely provided you cite the specific release paper ([Lucca et al. 2023](https://arxiv.org/abs/2306.08085)) and CosmoSpec release paper ([Chluba & Ali-Haimoud 2016](https://arxiv.org/abs/1510.03877)).

The folder contains three tables of Taylor coefficeints used to derived the requested CRR spectrum from a reference as well as the python module that performs the calculation. The latter module contains in turn 1) one function that calculates the CRR spectrum depending on the input cosmological parameters and their possible variances with respect to the sky-average and 2) an example of how to use that function to reproduce e.g., Fig. 6 of the release paper.

CRRfast has also been made part of the Boltzmann solver [CLASS](https://github.com/lesgourg/class_public) extending the pre-existing disotrtions.c module.

The development of the code has been supported by the F.R.S.-FNRS, the ERC Consolidator Grant CMBSPEC (No. 725456) and the Royal Society (No. URF/R/191023).
