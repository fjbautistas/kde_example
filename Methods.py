#==========================================================================================
# This file has methods to get the marginal distributions.
#==========================================================================================
import numpy as np
import pandas as pd
from scipy import stats, interpolate
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import warnings; warnings.simplefilter('ignore')



#=================================== Likelihoods ==========================================
def interpol(percnt, x1, x2, y1, y2):
    return y1+(((percnt-x1)/(x2-x1))*(y2-y1))

# args are a lsit of simulated data per colums dn.ms, dn,metal, dn.ngi ....
class optimal_pdf(object):

    def __init__(self, *args):
        self.lenght = 300
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
        self.lenght = 300
        self.org_data = np.array(*args)
        
        self.data = np.vstack([*varbs]).T
        self.data_std = (self.data-np.mean(self.data, axis=0))\
            /np.std(self.data, axis=0) # standarization     

        mu1 = (self.org_data[0] - np.mean(self.data, axis=0)[0])/np.std(self.data, axis=0)[0]
        sigma1 = self.org_data[1]/np.std(self.data, axis = 0)[0]
        mu2 = (self.org_data[2] - np.mean(self.data, axis=0)[1])/np.std(self.data, axis=0)[1]
        sigma2 = self.org_data[3]/np.std(self.data, axis = 0)[1]

        self.mu = [mu1[0],mu2[0]]
        self.sigma = [sigma1[0],sigma2[0]]
        
    def prior_pdf(self):
        self.pdfs = []         
        for i in range(len(self.data[0])):
            x = np.linspace(self.data_std[:,i].min(),
                            self.data_std[:,i].max(),
                            self.lenght)
                       
            pdf = stats.norm.pdf(x,loc = self.mu[i], scale = self.sigma[i])
            
            self.pdfs.append(pdf)

        if len(self.org_data) == 4:
            M_ones = np.ones([self.lenght, self.lenght]) 
            prior = ((M_ones*self.pdfs[0]).T*self.pdfs[1]).T
            self.pdf_prior = prior

        elif len(self.org_data[0]) == 6:
            M_ones = np.ones([self.lenght, self.lenght, self.lenght]) 
            prior = (((M_ones*self.pdfs[0]).T*self.pdfs[1]).T*self.pdfs[2]).T
            self.pdf_prior = prior

#========================================= Marginal =======================================
# args are the same variables from likelihood var1, var2, var3 (to analyze) 
class Marginal():
    
    def __init__(self, like, prior, *args):
        self.lenght = 300     
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

        #percentage: It is necessary to interpolate:

        f = interpolate.interp1d(self.inte, self.z)
        
        self.p_25 = f(0.25).tolist()
        self.p_50 = f(0.50).tolist()
        self.p_75 = f(0.75).tolist()

        #----25:
        #p25_1 = np.argmin((self.inte-0.25)**2); p25_2 = np.argmax((self.inte-0.25)**2)
        #if p25_1 > p25_2:
        #    self.p_25 = interpol(.25, self.inte[p25_1-1], self.inte[p25_1],
        #                            self.z[p25_1-1], self.z[p25_1])
        #else:
        #    self.p_25 = interpol(.25, self.inte[p25_1], self.inte[p25_1+1],
        #                             self.z[p25_1], self.z[p25_1+1])
        #----50:
        #p50_1 = np.argmin((self.inte-0.50)**2); p50_2 = np.argmax((self.inte-0.50)**2)
        #if p50_1 > p50_2:
        #    self.p_50 = interpol(.50, self.inte[p50_1-1], self.inte[p50_1],
        #                            self.z[p50_1-1], self.z[p50_1])
        #else:
        #    self.p_50 = interpol(.50, self.inte[p50_1], self.inte[p50_1+1],
        #                             self.z[p50_1], self.z[p50_1+1])
        #----75:
        #p75_1 = np.argmin((self.inte-0.75)**2); p75_2 = np.argmax((self.inte-0.75)**2)
        #if p25_1 > p25_2:
        #     self.p_75 = interpol(.75, self.inte[p75_1-1], self.inte[p75_1],
        #                             self.z[p75_1-1], self.z[p75_1])
        #else:
        #    self.p_75 = interpol(.75, self.inte[p75_1], self.inte[p75_1+1],
        #                             self.z[p75_1], self.z[p75_1+1])

        #self.p_25 = self.z[np.argmin((self.inte-0.25)**2)]
        #self.p_50 = self.z[np.argmin((self.inte-0.50)**2)]
        #self.p_75 = self.z[np.argmin((self.inte-0.75)**2)]



