import numpy as np
import pandas as pd
from Methods import prior, Marginal
from plots import * 
import warnings; warnings.simplefilter('ignore')

#================================================================= important data =============================================================================================
# observational data:
obs_data = pd.read_csv('data/observations.csv',index_col=None); 
# Simulated data:
dn = pd.read_csv('data/no_p.csv',index_col=None)
dl = pd.read_csv('data/low_p.csv',index_col=None)
dh = pd.read_csv('data/high_p.csv',index_col=None)
data = [dn,dl,dh]
# number of data per variable:
dim = 300
#========================================================== names, variables and unities ======================================================================================
variables = ["md","taugas","com","Mtp","Mjup","Mrock","nplanets","ngi", "npt"]
s= ["Kepler-289", "TRAPPIST-1", "K2-3", "K2-138", "HAT-P-11", "GJ 9827", "WASP-47","HD 38529", "TOI-125", "EPIC 249893012"]

#======================================================================== Marginals ============================================================================================
# ----- md and tau -----  
'''
Md  = pd.read_csv('data/ls_300/like_md.csv',index_col=None);
like_md  = [Md[str(Md.columns[i])].values.reshape(dim,dim,dim)   for i in range(1,4)]
tau = pd.read_csv('data/ls_300/like_tgas.csv',index_col=None);
like_tau = [tau[str(tau.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
l_md_tau = [like_md, like_tau]

def predict_md_tau(sistemas, likelihoods, datal = data, obs_data = obs_data):
    Marginls = []
    for k in range(len(sistemas)):
        systm = obs_data[obs_data.sys_name == sistemas[k]]

        for m in range(0,3):
            p = prior([datal[m].ms, datal[m].metal],[systm.ms.values, systm.dms.values,
                                                     systm.metal.values,systm.dmetal.values])
            p.prior_pdf()

            for n in range(len(likelihoods)):
                Marg = Marginal(likelihoods[n][m], p.pdf_prior,
                                data[m].ms,datal[m].metal, datal[m][variables[n]])
                Marg.pdf(); Marginls.append(Marg)
                
    mplot_md_tau(Marginls[0], Marginls[3], sistemas[0], 0)

# -------- com ----------
com = pd.read_csv('data/ls_300/like_com.csv',index_col=None);
like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]

def predict_com(sistemas, likelihoods = like_com, data = data, obs_data = obs_data):
    Marginls = []
    systm = obs_data[obs_data.sys_name == sistemas[0]]
    for m in range(len(likelihoods)):
        p = prior([data[m].ms, data[m].metal],[systm.ms, systm.dms,systm.metal,systm.dmetal])
        p.prior_pdf()
        Marg = Marginal(likelihoods[m], p.pdf_prior, data[m].ms,
                        data[m].metal, data[m]["com"])
        Marg.pdf(); Marginls.append(Marg)
    mplot_com(Marginls, systm.com.values[0], sistemas[0])
'''
# -------- Masses ----------    

mtp = pd.read_csv('data/ls_300/like_Mtp.csv',index_col=None);
like_mtp = [mtp[str(mtp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)] 
mjup= pd.read_csv('data/ls_300/like_Mjup.csv',index_col=None);
like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
mrock = pd.read_csv('data/ls_300/like_Mrock.csv',index_col=None);
like_mrock = [mrock[str(mrock.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_m = [like_mtp, like_mjup, like_mrock]

def predict_mass(sistemas, likelihoods = like_m, data = data, obs_data = obs_data):
    var = ["Mtp","Mjup","Mrock"]
    systm = obs_data[obs_data.sys_name == sistemas[0]]
    Marginls = []
    for i in range(0,3):
        p = prior([data[i].ms, data[i].metal],[systm.ms, systm.dms, systm.metal,systm.dmetal])
        p.prior_pdf()
        m = []
        for j in range(len(likelihoods)):
            Marg = Marginal(likelihoods[j][i], p.pdf_prior, data[i].ms, data[i].metal, data[i][var[j]])
            Marg.pdf();
            m.append(Marg)
        Marginls.append(m)
    mplot_mass(Marginls, systm.Mtp.values[0]*0.000954588, sistemas[0])   
    #return Marginls


# ---- Number of planets ------   
'''
ngi = pd.read_csv('data/ls_300/like_ngi.csv',index_col=None);
like_ngi = [ngi[str(ngi.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
ntp = pd.read_csv('data/ls_300/like_ntp.csv',index_col=None);
like_ntp = [ntp[str(ntp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
nplanets = pd.read_csv('data/ls_300/like_nplanets.csv',index_col=None);
like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_num = [like_nplanets, like_ngi, like_ntp]

def predict_num(sistemas, likelihoods, data = data, obs_data = obs_data):
    var = ["nplanets","ngi","npt"]
    systm = obs_data[obs_data.sys_name == sistemas[0]]
    Marginls = []
    for i in range(0,3):
        p = prior([data[i].ms, data[i].metal],[[systm.ms, systm.dms],[systm.metal,systm.dmetal]])
        p.prior_pdf()
        #Marginls.append(p)
        m = []
        for j in range(len(likelihoods)):
p            Marg = Marginal(likelihoods[j][i], p.pdf_prior, data[i].ms, data[i].metal, data[i][var[j]])
            Marg.pdf(); m.append(Marg)
        Marginls.append(m)
    mplot_num(Marginls, systm.n_planets.values[0], sistemas[0])
    return Marginls
 
'''
