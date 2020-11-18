import numpy as np
import pandas as pd
from scipy import stats

#========================================== data ============================================
dim = 150
# observational data:
obs_data = pd.read_csv('data/observations.csv',index_col=None); #without pertubtations 
# Simulated data:
dn = pd.read_csv('data/no_p.csv',index_col=None)
dl = pd.read_csv('data/low_p.csv',index_col=None)
dh = pd.read_csv('data/high_p.csv',index_col=None)
# likelihoods pdfs n,l,h per column
Md  = pd.read_csv('data/likelihoods/like_md.csv',index_col=None)
tau = pd.read_csv('data/likelihoods/like_tgas.csv',index_col=None)
com = pd.read_csv('data/likelihoods/like_com.csv',index_col=None)
mtp = pd.read_csv('data/likelihoods/like_Mtp.csv',index_col=None)
mjup= pd.read_csv('data/likelihoods/like_Mjup.csv',index_col=None)
mrock = pd.read_csv('data/likelihoods/like_Mrock.csv',index_col=None)
ngi = pd.read_csv('data/likelihoods/like_ngi.csv',index_col=None)
ntp = pd.read_csv('data/likelihoods/like_ntp.csv',index_col=None)
nplanets = pd.read_csv('data/likelihoods/like_nplanets.csv',index_col=None)

#===================================== likelihoods ==========================================
like_Md  = [Md[str(Md.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_tau = [tau[str(tau.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mtp = [mtp[str(mtp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mrock = [mrock[str(mrock.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_ngi = [ngi[str(ngi.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_ntp = [ntp[str(ntp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]

#======================================= Methods ===========================================
class prior():
    
    def __init__(self, var1, var2, *args):
        self.lenght = 150
        self.org_data = np.array(args)
        self.pdfs = []         
        self.data = np.vstack([var1,var2]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))/np.std(self.data, axis=0) # standarization     
            
    def prior_pdf(self):
        for i in range(len(self.org_data)):
            x = np.linspace(self.data_std[:,i].min(),
                            self.data_std[:,i].max(),
                            self.lenght)
            pdf = stats.norm.pdf(x,loc = self.org_data[i][0], 
                                 scale = self.org_data[i][1])       
            self.pdfs.append(pdf)
            
        if len(self.org_data) == 2:
            M_ones = np.ones([self.lenght, self.lenght]) 
            prior = ((M_ones*self.pdfs[0]).T*self.pdfs[1]).T     
            
            self.pdf_prior = prior
#------ Marginal ------
class Marginal():
    
    def __init__(self, like, prior, *args):
                
        self.like = like; self.prior= prior 
        self.space = [np.linspace(args[i].min(),args[i].max(), 
                                  150) for i in range(len(args))]
    
        self.data = np.vstack([*args]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))/np.std(self.data, axis=0) # standarization
        
        self.diff  = [np.abs(self.data_std[:,i][1]-self.data_std[:,i][0]) for i in range(len(self.data_std[0]))] 
        self.dz = np.abs(self.space[2][1]-self.space[2][0])
        self.z = self.space[2]
        
    def posterior(self):
        post = (self.like.T*self.prior.T).T
        norm = ((post.sum(axis=0)*(self.diff[0])).sum(axis=0)*(self.diff[1])).sum()*(self.diff[2])
        self.post = post/norm
    
    def pdf(self):
        self.posterior()
        M  = (self.post.sum(axis=0)*self.diff[0]).sum(axis=0)*self.diff[1]
        norm = (M*self.dz).sum()
        self.marginal = M/norm

        inte = np.cumsum(self.marginal)*self.dz

        self.z_mean = (self.marginal*self.z*self.dz).sum()
        self.z_std  = ((self.marginal)*((self.z-self.z_mean)**2)*self.dz).sum()**(1/2.)
        
        self.p_25 = self.z[np.argmin((inte-0.25)**2)]
        self.p_50 = self.z[np.argmin((inte-0.50)**2)]
        self.p_75 = self.z[np.argmin((inte-0.75)**2)]

 #-------- plot -------       
