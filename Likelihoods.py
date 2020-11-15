#=============================== libraries ==============================
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from scipy.stats import gaussian_kde
import warnings; warnings.simplefilter('ignore')
#============================== Data Variables ==========================

mass = (9.547919)
mass_jup = (1/mass)*(10**4)
mass_earth = 332946

dn=pd.read_csv('data/proc_no_pert.csv',index_col=None, usecols = ["ms","md","metal","taugas","com",
                                                                  "massefficiency","nplanets", "ngi"]); 
dl=pd.read_csv('data/proc_lo_pert.csv',index_col=None, usecols = ["ms","md","metal","taugas","com",
                                                                  "massefficiency","nplanets", "ngi"]); 
dh=pd.read_csv('data/proc_hi_pert.csv',index_col=None, usecols = ["ms","md","metal","taugas","com",
                                                                  "massefficiency","nplanets", "ngi"]); 

#------- total mass no perturbations-------
dn = dn.assign(Mtp = dn["massefficiency"]*dn["md"])
#------- total mass -------

dn = dn.assign(Mjup = ((dn["ngi"]*dn["Mtp"]).divide(dn["nplanets"]))*mass_jup)

dn = dn.assign(Mrock = (dn["Mtp"]-(dn["Mjup"]*(mass*10**(-4))))*mass_earth)




dl = dn.assign(Mtp = dl["massefficiency"]*dl["md"])
dh = dn.assign(Mtp = dh["massefficiency"]*dh["md"])
