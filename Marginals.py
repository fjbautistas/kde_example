import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from files_to_marginals import *
import matplotlib as mpl
from scipy import stats

import warnings; warnings.simplefilter('ignore')
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']

#===================================== important variables ========================================
data        = [dn, dl, dh]
likelihoods = [like_Md, like_tau, like_com, like_mtp, like_mjup, 
               like_mrock, like_nplanets, like_ngi, like_ntp]
variables   = ["md","taugas","com","Mtp","Mjup","Mrock","nplanets","ngi","npt"]
#====================================== define the system  ========================================

systm = obs_data[obs_data.sys_name == "Kepler-289"] 
systm

#-------- prior ------
prior_sys = []
for i in range(len(data)):
    
    p = prior(data[i]["ms"],data[i]["metal"],[systm.ms, systm.dms],[systm.metal,systm.dmetal])
    p.prior_pdf()
    
    prior_sys.append(p.pdf_prior)

#-----likelihoods-----
marginals = []
for n, var in enumerate(likelihoods):
    M = []
    for  i in range(len(data)):
        marginal = Marginal(var[i],prior_sys[i],
                            data[i]["ms"],data[i]["metal"],
                            data[i][variables[n]])
        marginal.pdf()
        M.append(marginal)
        
    marginals.append(M)
#==================================================================================================

