import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Methods import *
import matplotlib as mpl
from scipy import stats
import warnings; warnings.simplefilter('ignore')
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']

#=============================== important data =================================
data        = [dn, dl, dh]
likelihoods = [like_Md, like_tau, like_com, like_mtp, like_mjup, 
               like_mrock, like_nplanets, like_ngi, like_ntp]
variables   = ["md","taugas","com","Mtp","Mjup","Mrock","nplanets","ngi","npt"]

#=============================== slect the system ===============================
#Primary transit: Kepler-289, TRAPPIST-1, K2-3, K2-138, TOI-125
#radial velocity: WASP-47, GJ 876 

s= ["Kepler-289",  "TRAPPIST-1", "K2-3", "K2-138", "HAT-P-11",
    "GJ 9827", "WASP-47","HD 38529", "TOI-125", "EPIC 249893012"]

# sisyemas is the above list s, you can change the systems if you want. 
#----- ms and tau -----
def Mar_vars(sistemas):

    for k in range(len(sistemas)):
        systm = obs_data[obs_data.sys_name == sistemas[k]] 
        print(sistemas[k])
        #-------- prior ------
        prior_sys = []
        for i in range(len(data)):
    
            p = prior([data[i]["ms"],data[i]["metal"]],
                      [[systm.ms, systm.dms],
                       [systm.metal,systm.dmetal]])
            p.prior_pdf()
            prior_sys.append(p.pdf_prior)
    
        #-----likelihoods----
        marginals = []
        for n, var in enumerate(likelihoods):
            M = []
            for j in range(len(data)):
                marginal = Marginal(var[j],prior_sys[j],
                                    data[j]["ms"],data[j]["metal"],
                                    data[j][variables[n]])
                marginal.pdf()
                M.append(marginal)

            marginals.append(M)

        #-----plots----
        #mplot_2v(marginals[0][0],marginals[1][0], sistemas[k])
        #mplot_com(marginals[2], systm.com.values[0], sistemas[k])
    return marginals



# run it:
AA = Mar_vars(s)
