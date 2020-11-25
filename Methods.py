#==========================================================================================
# This file has methods to get the marginal distributions.
#==========================================================================================
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import warnings; warnings.simplefilter('ignore')

#=================================== Likelihoods ==========================================
# args are a lsit of simulated data per colums dn.ms, dn,metal, dn.ngi ....
class optimal_pdf(object):

    def __init__(self, *args):
        self.lenght = 200
        self.dim  = len(args)
        self.data = np.vstack([*args]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))/np.std(self.data, axis=0) # standarization
        
    def grids(self): 
        self.real_interval, self.std_interval = [], []
        
        for i in range(self.dim):
            self.real_interval.append(np.linspace(self.data[:,i].min(),
                                                  self.data[:,i].max(),
                                                  self.lenght))
            self.std_interval.append(np.linspace(self.data_std[:,i].min(),
                                                 self.data_std[:,i].max(),
                                                 self.lenght))
        
        self.real_grid = np.meshgrid(*self.real_interval)        # PROBLEM MEMORY FOR 5D,6D... nD.
        self.std_grid  = np.meshgrid(*self.std_interval)         # PROBLEM MEMORY FOR 5D,6D... nD.
        # std
        std = [self.std_grid[i].ravel() for i in range(len(self.std_grid))];
        self.space_std = np.vstack([*std]).T
        # real
        real = [self.real_grid[i].ravel() for i in range(len(self.real_grid))];
        self.space_real = np.vstack([*real]).T
        
    def bw(self):
        lenght, cv = 50, 10  
        dmin = np.abs(np.diff(self.data_std, axis=0))[np.abs(np.diff(self.data_std, axis=0))>0].min()
        # Search vector
        V_search = {'bandwidth':np.linspace(dmin, 3*self.data_std.std(), lenght)}
        # GridSearchCV
        self.grid_std = GridSearchCV(KernelDensity(), V_search, cv = cv).fit(self.data_std)
        self.bw_std  = self.grid_std.best_estimator_.bandwidth
    
    def pdf(self):
        self.bw(); self.grids() # initialize the above method
        self.scores, kde_i = [], []
    
        self.pdf_std = np.exp(self.grid_std.best_estimator_.score_samples(self.space_std).reshape(self.std_grid[0].shape))        
        return self.pdf_std.ravel()

#=====================================  Priors  ===========================================  
#2d and 3d varbs are a list of variables and args are a lsit of org values [value, error] 
class prior():
    
    def __init__(self, varbs, *args):
        self.lenght = 200
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

#========================================= Marginal =======================================
# args are the same variables from likelihood var1, var2, var3 (to analyze) 
class Marginal():
    
    def __init__(self, like, prior, *args):
        self.lenght = 200     
        self.like = like; self.prior= prior 
        self.space = [np.linspace(args[i].min(),args[i].max(),
                                  self.lenght) for i in range(len(args))]
    
        self.data = np.vstack([*args]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))/np.std(self.data, axis=0)#std
        
        self.diff  = [np.abs(self.data_std[:,i][1]-self.data_std[:,i][0]) for i in range(len(self.data_std[0]))]
        self.z = self.space[-1]
        self.dz = np.abs(self.z[1]-self.z[2])
        
    def posterior(self):
        post = (self.like.T*self.prior.T).T
        norm = ((post.sum(axis=0)*(self.diff[0])).sum(axis=0)*(self.diff[1])).sum()*(self.diff[2])
        self.post = post/norm
    
    def pdf(self):
        self.posterior()
        M  = (self.post.sum(axis=0)*self.diff[0]).sum(axis=0)*self.diff[1]
        norm = (M*self.dz).sum()
        self.marginal = M/norm

        self.inte = np.cumsum(self.marginal)*self.dz

        self.z_mean = (self.marginal*self.z*self.dz).sum()
        self.z_std  = ((self.marginal)*((self.z-self.z_mean)**2)*self.dz).sum()**(1/2.)

        #percentage:
        #if np.argmin((self.inte-0.25)**2) == 0 or 
        
        self.p_25 = self.z[np.argmin((self.inte-0.25)**2)]
        self.p_50 = self.z[np.argmin((self.inte-0.50)**2)]
        self.p_75 = self.z[np.argmin((self.inte-0.75)**2)]



