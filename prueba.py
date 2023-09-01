import numpy as np
import pandas as pd
from Methods import * 
#from Likelihoods import *
import matplotlib.pyplot as plt 

dim = 200
#------data
obs_data = pd.read_csv('data/observations.csv',index_col=None); 
dn = pd.read_csv('data/no_p.csv',index_col=None)
#------system
systm = obs_data[obs_data.sys_name == "Kepler-289"] 
#------ like and prior

mjup= pd.read_csv('data/likelihoods/like_Mjup.csv',index_col=None)
like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]

P = prior([dn.ms, dn.metal],[[systm.ms,systm.dms],[systm.metal,systm.dmetal]])
P.prior_pdf()
#------Marginal
mar = Marginal(like_mjup[2], P.pdf_prior, dn.ms, dn.metal, dn.Mtp)
mar.pdf()

print(mar.p_25,mar.p_50,mar.p_75)

#------plot
plt.step(mar.z, mar.marginal/mar.marginal.max())
plt.plot(mar.z, np.cumsum(mar.marginal)*mar.dz)

if np.argmin((mar.inte-0.25)**2) == 0 or np.argmin((mar.inte-0.325)**2) == 1: 

    plt.axvline(((mar.z[np.argmin((mar.inte-0.3)**2)]-mar.z[np.argmin((mar.inte-0.25)**2)])/2)+mar.z[np.argmin((mar.inte-0.25)**2)],
                ls = "--");
else: 
    plt.axvline(mar.p_25, ls = "--");
#plt.axvline(((mar.z[6]-mar.z[5])/2)+mar.z[5],
#            ls = "--")
plt.axhline(.25, ls = ":"); plt.axhline(.50, ls = ":"); plt.axhline(.75, ls = ":")

plt.axvspan(mar.z[0], mar.z[1], color='y', alpha=0.5, lw=0)
#plt.fill_between(mar.z,.25,0)
plt.xlim(0, 0.004)


#plt.show()

