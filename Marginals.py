import numpy as np
import pandas as pd
from Methods import prior, Marginal
#from plots import * 
import warnings; warnings.simplefilter('ignore')
#mpl.rcParams['text.usetex'] = True
#mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']

#================================================================= important data =============================================================================================
# observational data:
obs_data = pd.read_csv('data/observations.csv',index_col=None); 
# Simulated data:
dn = pd.read_csv('data/no_p.csv',index_col=None)
dl = pd.read_csv('data/low_p.csv',index_col=None)
dh = pd.read_csv('data/high_p.csv',index_col=None)
data = [dn,dl,dh]

# likelihoods pdfs n,l,h per column
dim = 200
Md  = pd.read_csv('data/likelihoods/like_md.csv',index_col=None);            like_md  = [Md[str(Md.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]   
tau = pd.read_csv('data/likelihoods/like_tgas.csv',index_col=None);          like_tau = [tau[str(tau.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
com = pd.read_csv('data/likelihoods/like_com.csv',index_col=None);           like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
mtp = pd.read_csv('data/likelihoods/like_Mtp.csv',index_col=None);           like_mtp = [mtp[str(mtp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)] 
mjup= pd.read_csv('data/likelihoods/like_Mjup.csv',index_col=None);          like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
mrock = pd.read_csv('data/likelihoods/like_Mrock.csv',index_col=None);       like_mrock = [mrock[str(mrock.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
ngi = pd.read_csv('data/likelihoods/like_ngi.csv',index_col=None);           like_ngi = [ngi[str(ngi.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
ntp = pd.read_csv('data/likelihoods/like_ntp.csv',index_col=None);           like_ntp = [ntp[str(ntp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
nplanets = pd.read_csv('data/likelihoods/like_nplanets.csv',index_col=None); like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]

likelihoods = [like_md, like_tau, like_com, like_mtp, like_mjup, like_mrock, like_nplanets, like_ngi, like_ntp]

#========================================================== names, variables and unities ======================================================================================
names = [r"Mass of Disk $M_d$ [$M_\odot$]", r"Dissipation time $\tau_g$ [y]", r"Center of mass $r_{\text{cm}}$ [AU]", r"Total planetary mass $M_{tp}$ [$M_\odot$]",
         r"Giant planetary mass $M_{\jupiter}$ [$M_\text{jup}$]",r"Rocky planetary mass $M_{r}$ [$M_{\oplus}$]", r"Number of total planets $N_{t}$",
         r"Number of giants $N_{\jupiter}$", r"Number of giants $N_{t}$"]

sym   = [r"$p\left(M_d\right)$", r"$p\left(\tau_g\right)$", r"$p\left(r_\text{cm}\right)$", r"$p\left(M_{tp}\right)$", r"$p\left(M_{\jupiter}\right)$",
         r"$p\left(M_{r}\right)$", r"$p\left(N_{t}\right)$", r"$p\left(N_{\jupiter}\right)$",r"$p\left(N_{\oplus}\right)$"]

unities = [r"$M_\odot$", r"y", r"AU", r"$M_\odot$", r"$M_\text{jup}$", r"$M_{\oplus}$"]

titles = ["No perturbations","Low perturbations","High perturbations"]

#========================================================================== Priors ============================================================================================
#Primary transit: Kepler-289, TRAPPIST-1, K2-3, K2-138, TOI-125
#radial velocity: WASP-47, GJ 876 
s= ["Kepler-289", "TRAPPIST-1", "K2-3", "K2-138", "HAT-P-11", "GJ 9827", "WASP-47","HD 38529", "TOI-125", "EPIC 249893012"]

priors = []
systm = obs_data[obs_data.sys_name == s[0]] 
#-------- prior ------
prior_sys = []
for i in range(0,3):
    p = prior([data[i].ms, data[i].metal],
              [[systm.ms, systm.dms],
               [systm.metal,systm.dmetal]])
    p.prior_pdf()
    prior_sys.append(p.pdf_prior)
priors.append(prior_sys)

#======================================================================== Marginals ============================================================================================

marginales = [] 
for n, var in enumerate(likelihoods):
    M = []
    for i in range(0,3):
        marginal = Marginal(var[i], priors[0][i], data[i].ms, data[i].metal, data[i].iloc[:,[n]])
        marginal.pdf()
        M.append(marginal)
    marginales.append(M)
'''
#marginals.append(M)

        #-----plots----
        #mplot_2v(marginals[0][0],marginals[1][0], sistemas[k])
        #mplot_com(marginals[2], systm.com.values[0], sistemas[k])
        #mplot_Mass([marginals[3], marginals[4], marginals[5]],
        #           systm.Mtp.values[0]*sun_mass,sistemas[k])
    #return marginals

# run it:
#AA = Mar_vars(s)
'''
