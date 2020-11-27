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

dim = 300
#========================================================== names, variables and unities ======================================================================================
variables = ["md","taugas","com","Mtp","Mjup","Mrock","nplanets","ngi", "npt"]

#Primary transit: Kepler-289, TRAPPIST-1, K2-3, K2-138, TOI-125
#radial velocity: WASP-47, GJ 876 
s= ["Kepler-289", "TRAPPIST-1", "K2-3", "K2-138", "HAT-P-11", "GJ 9827", "WASP-47","HD 38529", "TOI-125", "EPIC 249893012"]

#===================================================================== Methods ================================================================================================
# sitemas is a list sublist of s or the complete list 
#-------- prior ------
def priors(sistemas, data = data, obs_data = obs_data):
    priors = []
    for k in range(len(sistemas)):
        systm = obs_data[obs_data.sys_name == sistemas[k]] 
        print(systm.sys_name)
        prior_sys = []
        for i in range(0,3):
            p = prior([data[i].ms, data[i].metal],
                      [[systm.ms, systm.dms],[systm.metal,systm.dmetal]])
            p.prior_pdf()
            prior_sys.append(p.pdf_prior)
        priors.append(prior_sys)
    return priors

#======================================================================== Marginals ============================================================================================
def predict_md_tau(sistemas, likelihoods, data = data, obs_data = obs_data):
    Marginls = []
    for k in range(len(sistemas)):
        systm = obs_data[obs_data.sys_name == sistemas[k]]
        for m in range(0,3):
            p = prior([data[m].ms, data[m].metal],
                      [[systm.ms, systm.dms],[systm.metal,systm.dmetal]])
            p.prior_pdf()
            for n in range(len(likelihoods)):
                Marg = Marginal(likelihoods[n][m], p.pdf_prior,
                                data[m].ms,data[m].metal, data[m][variables[n]])
                Marg.pdf()
                Marginls.append(Marg)
           # Marg.append(Mar)
        #Marginls.append(Marg)
    return Marginls
    #mplot_md_tau(Marginls[0], Marginls[3], sistemas[0],
    #             [names[0], names[1]], [sym[0],sym[1]], [unities[0], unities[1]])

#likelihoods = [like_md, like_tau, like_com, like_mtp, like_mjup, like_mrock, like_nplanets, like_ngi, like_ntp]

#======================================================================== Marginals ============================================================================================
def predict_com(sistemas, likelihoods):
    p = priors(sistemas)
    Marginls = []
    for j in range(len(p)):
          for m in range(0,3):
              for n in range(len(likelihoods)):
                Ma = Marginal(likelihoods[n][m], p[j][m], data[m].ms,
                              data[m].metal, data[m][variables[n]])
                Ma.pdf()
                Marginls.append(Ma)
           # Marg.append(Mar)
        #Marginls.append(Marg)
    #mplot_md_tau(Marginls[0], Marginls[3], sistemas[0],
    #             [names[0], names[1]], [sym[0],sym[1]], [unities[0], unities[1]])
    return Marginls

#================================================================= Marginals per system =============================================================================================
# likelihoods pdfs n,l,h per column
# ----- md and tau -----  
Md  = pd.read_csv('data/ls_300/like_md.csv',index_col=None);
like_md  = [Md[str(Md.columns[i])].values.reshape(dim,dim,dim)   for i in range(1,4)]
tau = pd.read_csv('data/ls_300/like_tgas.csv',index_col=None);
like_tau = [tau[str(tau.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
l_md_tau = [like_md, like_tau]

# -------- com ----------
com = pd.read_csv('data/ls_300/like_com.csv',index_col=None);
like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]










# ------- com ----------
#com = pd.read_csv('data/ls_300/like_com.csv',index_col=None);
#like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
#mtp = pd.read_csv('data/ls_300/like_Mtp.csv',index_col=None);
#like_mtp = [mtp[str(mtp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)] 
#mjup= pd.read_csv('data/ls_300/like_Mjup.csv',index_col=None);
#like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
#mrock = pd.read_csv('data/ls_300/like_Mrock.csv',index_col=None);
#like_mrock = [mrock[str(mrock.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
#ngi = pd.read_csv('data/ls_300/like_ngi.csv',index_col=None);
#like_ngi = [ngi[str#(ngi.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
#ntp = pd.read_csv('data/ls_300/like_ntp.csv',index_col=None);
#like_ntp = [ntp[str#(ntp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
#nplanets = pd.read_csv('data/ls_300/like_nplanets.csv',index_col=None);
#like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]

#likelihoods = [like_md, like_tau, like_com, like_mtp, like_mjup, like_mrock, like_nplanets, like_ngi, like_ntp]
#========================================================== names, variables and unities ======================================================================================
#Primary transit: Kepler-289, TRAPPIST-1, K2-3, K2-138, TOI-125
#radial velocity: WASP-47, GJ 876 
#========================================================================== Priors ============================================================================================
# sitemas is a list sublist of s or the complete list 
'''
def priors(sistemas, data = data, obs_data =obs_data):
    #-------- prior ------
    priors = []
    for k in range(len(sistemas)):
        systm = obs_data[obs_data.sys_name == sistemas[k]] 
        print(systm.sys_name)
        prior_sys = []
        for i in range(0,3):
            p = prior([data[i].ms, data[i].metal],[[systm.ms, systm.dms],[systm.metal,systm.dmetal]])
            p.prior_pdf()
            prior_sys.append(p.pdf_prior)
        priors.append(prior_sys)

    return priors

#======================================================================== Marginals ============================================================================================
def predict(sistemas, likelihoods = likelihoods):
    p = priors(sistemas)
    marginales = []
    
    for j in range(len(p)):
        print(j)
        for m in range(0,3):
            M=[]
            for n in range(0,9):
                print(n)
                mar = Marginal(likelihoods[n][m], p[j][m], data[m].ms,
                               data[m].metal, data[m][variables[n]])
                mar.pdf()
                M.append(mar)
            marginales.append(M)

    return marginales
    

            #M = []
            #for n, var in enumerate(likelihoods):
            #    m = Marginal(var,)
            #    m.pdf()
            #    M.append(m)



            
    #    M = []
    #    for i in range(0,3):
    #        marginal = Marginal(var[i], priors[0][i], data[i].ms, data[i].metal, data[i].iloc[:,[n]])
    #        marginal.pdf()
    #        M.append(marginal)
    #    marginales.append(M)

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
'''
