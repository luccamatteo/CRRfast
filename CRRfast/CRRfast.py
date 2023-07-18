#!/usr/bin/env python
from numpy import *
import numpy as np
import matplotlib.pyplot as plt

# CRRfast, a Python emulator to calculate the CRR spectrum as explained in Lucca et al. 2023 (arXiv:2306.08085).
# The Taylor coefficient tables underlaying the code have been derived using the more refined CosmoSpec code,
# Chluba & Ali-Haimoud 2016 (arXiv:1510.03877). By any use of CRRfast, please cite both references.

# Funtion to read table_Taylor_coeff tables and compute CRR spectrum for given choice of parameters
# Input:   array of values of the cosmological paramters {omega_b, Yp, T0, omega_cdm, N_eff} ('cosmo_param_vals')
# Input:   array of values of the corresponding inhomogeneous fluctuations sigma_p ('inhom_param_vals')
# Output:  nu, reference and total DI_CRR
def run_Taylor_exp(cosmo_param_vals, inhom_param_vals):
  # Set fiducial and read correct Taylor_exp table (depending on the pivot value of omega_cdm)
  param_vals_ref = np.array([0.02242, 0.2437, 2.7255, 0.11933, 2.99])
  if(cosmo_param_vals[3]<(param_vals_ref[3]+0.2177712)/2.):
    array=loadtxt('table_Taylor_coeff_1.dat')
  elif(cosmo_param_vals[3]>(0.3266568+0.2177712)/2.):
    param_vals_ref[3]=0.3266568
    array=loadtxt('table_Taylor_coeff_3.dat')
  else:
    param_vals_ref[3]=0.2177712
    array=loadtxt('table_Taylor_coeff_2.dat')
  array=array.T
  nu=array[0]
  DI_CRR_ref=array[1]
  DDI_CRR=[array[i+2] for i in range(0,len(param_vals_ref))]
  DDDI_CRR=np.zeros((len(nu), len(param_vals_ref), len(param_vals_ref)))
  for i in range(0,len(param_vals_ref)):
    for j in range(0,len(param_vals_ref)):
      DDDI_CRR[:,i,j]=array[2+len(param_vals_ref)+len(param_vals_ref)*i+j]

  # Compute sky-averaged spectrum
  Dp_cosmo = np.array(cosmo_param_vals)-np.array(param_vals_ref)
  DI_CRR_Taylor_O1 = np.zeros((len(nu)))
  DI_CRR_Taylor_O2 = np.zeros((len(nu)))
  for k in range(0, len(nu)):
    for i in range(0, len(param_vals_ref)):
      DI_CRR_Taylor_O1[k] += DDI_CRR[i][k]*Dp_cosmo[i]
      for j in range(0, len(param_vals_ref)):
        DI_CRR_Taylor_O2[k] += DDDI_CRR[k,i,j]*Dp_cosmo[i]*Dp_cosmo[j]/2.
  DI_CRR = DI_CRR_ref+DI_CRR_Taylor_O1+DI_CRR_Taylor_O2

  # Compute inhomogeneous corrections
  Dp_inhom = inhom_param_vals*param_vals_ref
  DI_CRR_Taylor_O2_inhom = np.zeros((len(nu)))
  for k in range(0, len(nu)):
    for j in range(0, len(param_vals_ref)):
        DI_CRR_Taylor_O2_inhom[k] += DDDI_CRR[k,j,j]*Dp_inhom[j]**2./2.
  DI_CRR += DI_CRR_Taylor_O2_inhom

  return nu, DI_CRR_ref, DI_CRR

# Example to reproduce Fig. 6 of Lucca et al. 2023 (arXiv:2306.08085)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.ylabel(r'$\langle \Delta I_{\rm CRR} \rangle$ [Jy/sr]', fontsize=15)
plt.xlabel(r'$\nu$ [GHz]',fontsize=15)
plt.xlim(1.e0, 3.e3)
plt.ylim(3.e-2, 1.2e0)
plt.subplots_adjust(left=0.15,right=0.95,top=0.93,bottom=0.15)

cosmo_param_vals = np.array([0.02242, 0.2437, 2.7255, 0.11933, 2.99])
inhom_param_vals = np.array([0., 0., 0., 0., 0.])
nu, DI_CRR_ref, DI_CRR = run_Taylor_exp(cosmo_param_vals, inhom_param_vals)
plt.loglog(nu, DI_CRR*1.e26, '-', color='k', label=r'$\sigma_{\omega_b} = 0$')
cosmo_param_vals = np.array([0.02242, 0.2437, 2.7255, 0.11933, 2.99])
inhom_param_vals = np.array([0.75, 0., 0., 0., 0.])
nu, DI_CRR_ref, DI_CRR = run_Taylor_exp(cosmo_param_vals, inhom_param_vals)
plt.loglog(nu, DI_CRR*1.e26, '-', color='orange', label=r'$\sigma_{\omega_b} = 0.75$')
plt.show()

