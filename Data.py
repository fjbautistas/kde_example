#=============================== libraries ==============================
import numpy as np
import pandas as pd
import warnings; warnings.simplefilter('ignore')
#============================== Data Variables ==========================

mass     = (9.547919)
mass_jup = (1/mass)*(10**4)
m_jup    = 317.8 # terrestrial masses.
mass_earth = 332946

dn=pd.read_csv('data/proc_no_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
dl=pd.read_csv('data/proc_lo_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
dh=pd.read_csv('data/proc_hi_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
#--------total number of rocky planets -----
dn = dn.assign(n_r = dn["nplanets"]-dn["ngi"])
dl = dl.assign(n_r = dl["nplanets"]-dl["ngi"])
dh = dh.assign(n_r = dh["nplanets"]-dh["ngi"])

#--------total planet masss (Mjup)-----------
dn = dn.assign(M_tp = dn["massbudget"]*(1/m_jup))
dl = dl.assign(M_tp = dl["massbudget"]*(1/m_jup))
dh = dh.assign(M_tp = dh["massbudget"]*(1/m_jup))

#-------- total giant mass (Mjup ) ----------
dn = dn.assign(M_gi = (dn["massbudget"]-dn["mtr"])*(1/m_jup))
dl = dl.assign(M_gi = (dn["massbudget"]-dn["mtr"])*(1/m_jup))
dh = dh.assign(M_gi = (dn["massbudget"]-dn["mtr"])*(1/m_jup))

#-------- total rocky mass --------
dn = dn.assign(M_rock = dn["mtr"])
dl = dl.assign(M_rock = dl["mtr"])
dh = dh.assign(M_rock = dh["mtr"])

# reorder
dn = dn[["ms", "metal", "md", "taugas", "com", "M_tp", "M_gi", "M_rock", "nplanets", "ngi", "n_r"]]
dl = dl[["ms", "metal", "md", "taugas", "com", "M_tp", "M_gi", "M_rock", "nplanets", "ngi", "n_r"]]
dh = dh[["ms", "metal", "md", "taugas", "com", "M_tp", "M_gi", "M_rock", "nplanets", "ngi", "n_r"]]


dn.to_csv(r'data/no_p.csv', index = False)
dl.to_csv(r'data/low_p.csv', index = False)
dh.to_csv(r'data/high_p.csv', index = False)
