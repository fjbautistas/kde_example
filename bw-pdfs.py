#=============================== libraries ==============================
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from scipy.stats import gaussian_kde
import warnings; warnings.simplefilter('ignore')
#============================== Data Variables ==========================
dn=pd.read_csv('data/proc_no_pert.csv',index_col=None); dn["gia"]=dn.ngi>0 #without pertubtations 
dl=pd.read_csv('data/proc_lo_pert.csv',index_col=None); dl["gia"]=dl.ngi>0 #with low pertubtations 
dh=pd.read_csv('data/proc_hi_pert.csv',index_col=None); dh["gia"]=dh.ngi>0 #with high pertubtations
#Terrestrial: t; giant;g
dnt=dn[~dn["gia"]]; dng=dn[dn["gia"]] # without pertubtations 
dlt=dl[~dl["gia"]]; dlg=dl[dl["gia"]] # low pertubtations 
dht=dh[~dh["gia"]]; dhg=dh[dh["gia"]] # high pertubtations 

x_variables = [dng,dlg,dhg,dnt,dlt,dht,dn,dl,dh]

for i, var in enumerate(x_variables):
    var['logeff'] = np.log10(var.massefficiency)
    var['logcom'] = np.log10(var.com)
#================================== Methods ============================

class multidim_bw(object):

    def __init__(self, *args):
        
        dx, length, deciamls = .2, 100, 2       # some constants 
        self.min, self.max = [], []            # it will keep information of min and max values  
        self.var_values = []                   # Their components are objects from class bw_optimal
        self.var_grids  = [] 
        
        for i in range(len(args)):             # It calls the class bw_optimal to standarize data
            variable = args[i].values          # original variable
                                            
            self.x = (variable-variable.mean())/variable.std()  # standarization:
            
            self.x_grid = np.around(np.linspace(self.x.min()-dx,
                                                self.x.max()+dx,
                                                length),deciamls)             
            
            self.var_values.append(self.x)     # std values
            self.var_grids.append(self.x_grid) # lists of x_grids  
            
            self.min.append(self.x.min()); self.max.append(self.x.max()) 
            
        self.n_grid = np.meshgrid(*self.var_grids)
        ll = [self.n_grid[i].ravel() for i in range(len(self.n_grid))]
        self.space  = np.vstack([*ll]).T   # It generates the space for the pdf
        
        self.data   = np.vstack([*self.var_values]).T 
        
    def pdf_ndim(self):
        self.grid = GridSearchCV(KernelDensity(), 
                                 {'bandwidth': np.linspace(0.038, 
                                                           3,
                                                           30)}, cv=20)
        self.grid.fit(self.data)
        
        self.ndim_bw  = self.grid.best_estimator_.bandwidth
        self.ndim_pdf = np.exp(self.grid.best_estimator_.score_samples(self.space).reshape(self.n_grid[0].shape))  #get the pdf
        return self.ndim_pdf 

#================================== example  ============================


ex2 = multidim_bw(dng.logcom, dng.logeff, dng.nplanets)#, dng.metal)
ex2.pdf_ndim()
