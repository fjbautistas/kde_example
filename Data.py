#=============================== libraries ==============================
import numpy as np
import pandas as pd
import warnings; warnings.simplefilter('ignore')
#============================== Data Variables ==========================

mass = (9.547919)
mass_jup = (1/mass)*(10**4)
mass_earth = 332946

dn=pd.read_csv('data/proc_no_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
dl=pd.read_csv('data/proc_lo_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
dh=pd.read_csv('data/proc_hi_pert.csv',index_col=None)#, usecols = ["ms","md","metal","taugas","com",
                                                      #            "massefficiency","nplanets", "ngi"]); 
#--------total rocky planets -----
dn = dn.assign(npt = dn["nplanets"]-dn["ngi"])
dl = dl.assign(npt = dl["nplanets"]-dl["ngi"])
dh = dh.assign(npt = dh["nplanets"]-dh["ngi"])

#--------- total masss -----------
dn = dn.assign(Mtp = dn["massefficiency"]*dn["md"])
dl = dl.assign(Mtp = dl["massefficiency"]*dl["md"])
dh = dh.assign(Mtp = dh["massefficiency"]*dh["md"])

#------- total giant mass -------
dn = dn.assign(Mjup = ((dn["ngi"]*dn["Mtp"]).divide(dn["nplanets"]))*mass_jup)
dl = dl.assign(Mjup = ((dl["ngi"]*dl["Mtp"]).divide(dl["nplanets"]))*mass_jup)
dh = dh.assign(Mjup = ((dh["ngi"]*dh["Mtp"]).divide(dh["nplanets"]))*mass_jup)

#-------- total rocky mass --------
dn = dn.assign(Mrock = (dn["Mtp"]-(dn["Mjup"]*(mass*10**(-4))))*mass_earth)
dl = dl.assign(Mrock = (dl["Mtp"]-(dl["Mjup"]*(mass*10**(-4))))*mass_earth)
dh = dh.assign(Mrock = (dh["Mtp"]-(dh["Mjup"]*(mass*10**(-4))))*mass_earth)


# reorder
dn = dn[["ms", "metal", "md", "taugas", "com", "Mtp", "Mjup", "Mrock", "nplanets", "ngi", "npt"]]
dl = dl[["ms", "metal", "md", "taugas", "com", "Mtp", "Mjup", "Mrock", "nplanets", "ngi", "npt"]]
dh = dh[["ms", "metal", "md", "taugas", "com", "Mtp", "Mjup", "Mrock", "nplanets", "ngi", "npt"]]


dn.to_csv(r'data/no_p.csv', index = False)
dl.to_csv(r'data/low_p.csv', index = False)
dh.to_csv(r'data/high_p.csv', index = False)
