#==========================================================================================
# This file has methods to get and plot the marginal distributions.
#==========================================================================================
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import warnings; warnings.simplefilter('ignore')
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']

#========================================== data ==========================================
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

#===================================== likelihoods ========================================
like_Md  = [Md[str(Md.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_tau = [tau[str(tau.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_com = [com[str(com.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mtp = [mtp[str(mtp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mjup = [mjup[str(mjup.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_mrock = [mrock[str(mrock.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,
                                                                   dim) for i in range(1,4)]
like_ngi = [ngi[str(ngi.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_ntp = [ntp[str(ntp.columns[i])].values.reshape(dim,dim,dim) for i in range(1,4)]
like_nplanets = [nplanets[str(nplanets.columns[i])].values.reshape(dim,dim,
                                                                   dim) for i in range(1,4)]

#======================================= names ===========================================
names = [r"Mass of Disk $M_d$ ($M_\odot$)",
         r"Dissipation time $\tau_g$ (y)",
         r"Center of mass $r_{\text{cm}}$ (AU)",
         r"Total planetary mass $M_{tp}$ ($M_\odot$)",
         r"Gian planetary mass $M_{\jupiter}$ ($M_\text{jup}$)",
         r"Rocky planetary mass $M_{r}$ ($M_{\oplus}$)",
         r"Number of total planets $N_{t}$",
         r"Number of giants $N_{\jupiter}$",
         r"Number of giants $N_{t}$"]

sym   = [r"$p\left(M_d\right)$",
         r"$p\left(\tau_g\right)$",
         r"$p\left(r_\text{cm}\right)$",
         r"$p\left(M_{tp}\right)$",
         r"$p\left(M_{\jupiter}\right)$",
         r"$p\left(M_{r}\right)$",
         r"$p\left(N_{t}\right)$",
         r"$p\left(N_{\jupiter}\right)$",
         r"$p\left(N_{\oplus}\right)$"]    

#======================================= Methods ===========================================
#2d and 3d varbs are a list of variables and args are a lsit of org values [value, error] 
class prior():
    
    def __init__(self, varbs, *args):
        self.lenght = 150
        self.org_data = np.array(args)
        self.pdfs = []         
    
        self.data = np.vstack([*varbs]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))\
            /np.std(self.data, axis=0) # standarization     

            
    def prior_pdf(self):
        for i in range(len(self.org_data[0])):
            x = np.linspace(self.data_std[:,i].min(),
                            self.data_std[:,i].max(),
                            self.lenght)
            pdf = stats.norm.pdf(x,loc = self.org_data[0][i][0], 
                                 scale = self.org_data[0][i][1])       
            self.pdfs.append(pdf)
            
        if len(self.org_data[0]) == 2:
            M_ones = np.ones([self.lenght, self.lenght]) 
            prior = ((M_ones*self.pdfs[0]).T*self.pdfs[1]).T
            self.pdf_prior = prior

        elif len(self.org_data[0]) == 3:
            M_ones = np.ones([self.lenght, self.lenght, self.lenght]) 
            prior = (((M_ones*self.pdfs[0]).T*self.pdfs[1]).T*self.pdfs[2]).T
            self.pdf_prior = prior
            
#------ Marginal ------
class Marginal():
    
    def __init__(self, like, prior, *args):
                
        self.like = like; self.prior= prior 
        self.space = [np.linspace(args[i].min(),args[i].max(),150) for i in range(len(args))]
    
        self.data = np.vstack([*args]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))/np.std(self.data, axis=0)#std
        
        self.diff  = [np.abs(self.data_std[:,i][1]-self.data_std[:,i][0]) for i in range(len(self.data_std[0]))] 
        self.dz = np.abs(self.space[-1][1]-self.space[-1][0])
        self.z = self.space[-1]
        
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

#-------- For plots -------
def mplot_2v(marginal_md, marginal_tau, sys):
    names = [r"Mass of the disk $M_d$ ($M_\odot$)",r"Time of gas dissipation $\tau_g$ (y)"]
    sym   = [r"$p\left(M_d\right)$", r"$p\left(\tau_g\right)$"] 
    size = 15
    m = [marginal_md, marginal_tau]
    x = [marginal_md.space[-1], marginal_tau.space[-1]]
    y = [marginal_md.marginal/marginal_md.marginal.max(),
         marginal_tau.marginal/marginal_tau.marginal.max()]
    #Figure:
    fig, ax = plt.subplots(1,2, figsize=(12,5))
    for i in range(0,2):
        ax[i].plot(x[i], y[i], label = sym[i], lw = 2)
        ax[i].set_xlabel(names[i],fontsize = size)
        ax[i].set_ylabel(sym[i],fontsize = size)
        ax[i].tick_params(axis='both', labelsize=size-2)
        if i == 0:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",
                          label = r"25\% = " + "%.3g"%m[i].p_25)
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",
                          label = r"50\% = " + "%.3g"%m[i].p_50)
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",
                          label = r"75\% = " + "%.3g"%m[i].p_75)
        if i == 1:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",
                          label = r"25\% = " + "{:.2e}".format(m[i].p_25))
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",
                          label = r"50\% = " + "{:.2e}".format(m[i].p_50))
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",
                          label = r"75\% = " + "{:.2e}".format(m[i].p_75))
            plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))

        ax[i].legend(fontsize=size-1)
    
    plt.subplots_adjust(hspace=1.5)
    fig.tight_layout()
    plt.savefig("images/md_tau/"+sys+".pdf")
    plt.show()

#------------------    

def mplot_com(marginal_com, obs, sys):
    names, sym = r"Center of mass $r_\text{cm}$ (AU)", r"$p\left(r_\text{cm}\right)$"
    titles = ["No perturbations","Low perturbations","High perturbations"]
    size = 15

    x = [marginal_com[i].space[-1] for i in range(len(marginal_com))]
    y = [marginal_com[i].marginal/marginal_com[i].marginal.max()
         for i in range(len(marginal_com))]
    
    #Figure:
    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(15,5))

    for i in range(0,3):
        ax[i].plot(x[i], y[i], label = sym, lw = 2)
        ax[i].set_xlabel(names,fontsize = size)
        if i==0:
            ax[i].set_ylabel(sym,fontsize = size)
           
        ax[i].axvline(x = marginal_com[i].p_25,ls='--', c="C1",
                      label = r"25\% = " + "%.3g"%marginal_com[i].p_25)
        ax[i].axvline(x = marginal_com[i].p_50,ls='--', c="C2",
                      label = r"50\% = " + "%.3g"%marginal_com[i].p_50)
        ax[i].axvline(x = marginal_com[i].p_75,ls='--', c="C3",
                      label = r"75\% = " + "%.3g"%marginal_com[i].p_75)

        ax[i].axvline(x = obs, ls='--', c="k",
                      label = r"observed = " + "%.3g"%obs[0])

        ax[i].tick_params(axis='both', labelsize=size-2)
        ax[i].set_title(titles[i], fontsize = size-1)
        ax[i].legend(fontsize=size-1)
    
    plt.subplots_adjust(hspace=-.5)
    fig.tight_layout()
    plt.savefig("images/com/"+sys+".pdf")
    plt.show()

