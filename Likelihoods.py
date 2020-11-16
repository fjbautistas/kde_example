#==================================== libraries =======================================
import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from scipy.stats import gaussian_kde
import warnings; warnings.simplefilter('ignore')

#====================================== Data ===========================================
dn = pd.read_csv("data/no_p.csv", index_col = False)
dl = pd.read_csv("data/low_p.csv", index_col = False)
dh = pd.read_csv("data/high_p.csv", index_col = False)
#================================ likelihood class =====================================
class optimal_pdf(object):

    def __init__(self, *args):
        self.lenght = 150
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

#============================================================================================================    
#================================================ Likelihoods ===============================================
#============================================================================================================    

# md
'''
md_n = optimal_pdf(dn.ms, dn.metal, dn.md); like_md_n = md_n.pdf();
md_l = optimal_pdf(dl.ms, dl.metal, dl.md); like_md_l = md_l.pdf(); 
md_h = optimal_pdf(dh.ms, dh.metal, dh.md); like_md_h = md_h.pdf();

likelihoods_md = pd.DataFrame({'md_n':like_md_n, 'md_l':like_md_l, 'md_h':like_md_h})
likelihoods_md.to_csv("data/like_md.csv")

# com
com_n = optimal_pdf(dn.ms, dn.metal, dn.com); like_com_n = com_n.pdf(); 
com_l = optimal_pdf(dl.ms, dl.metal, dl.com); like_com_l = com_l.pdf(); 
com_h = optimal_pdf(dh.ms, dh.metal, dh.com); like_com_h = com_h.pdf(); 

likelihoods_com = pd.DataFrame({'com_n':like_com_n, 'com_l':like_com_l, 'com_h':like_com_h})
likelihoods_com.to_csv("data/like_com.csv")

# Mtp total mass
Mtp_n = optimal_pdf(dn.ms, dn.metal, dn.Mtp); like_Mtp_n = Mtp_n.pdf(); 
Mtp_l = optimal_pdf(dl.ms, dl.metal, dl.Mtp); like_Mtp_l = Mtp_l.pdf(); 
Mtp_h = optimal_pdf(dh.ms, dh.metal, dh.Mtp); like_Mtp_h = Mtp_h.pdf(); 

likelihoods_Mtp = pd.DataFrame({'Mtp_n':like_Mtp_n, 'Mtp_l':like_Mtp_l, 'Mtp_h':like_Mtp_h})
likelihoods_Mtp.to_csv("data/like_Mtp.csv")

# Mjup total mass
Mjup_n = optimal_pdf(dn.ms, dn.metal, dn.Mjup); like_Mjup_n = Mjup_n.pdf(); 
Mjup_l = optimal_pdf(dl.ms, dl.metal, dl.Mjup); like_Mjup_l = Mjup_l.pdf(); 
Mjup_h = optimal_pdf(dh.ms, dh.metal, dh.Mjup); like_Mjup_h = Mjup_h.pdf();

likelihoods_Mjup = pd.DataFrame({'Mjup_n':like_Mjup_n, 'Mjup_l':like_Mjup_l, 'Mjup_h':like_Mjup_h})
likelihoods_Mjup.to_csv("data/likelihoods/like_Mjup.csv")

# Mrock total mass
Mrock_n = optimal_pdf(dn.ms, dn.metal, dn.Mrock); like_Mrock_n = Mrock_n.pdf(); 
Mrock_l = optimal_pdf(dl.ms, dl.metal, dl.Mrock); like_Mrock_l = Mrock_l.pdf(); 
Mrock_h = optimal_pdf(dh.ms, dh.metal, dh.Mrock); like_Mrock_h = Mrock_h.pdf();

likelihoods_Mrock = pd.DataFrame({'Mrock_n':like_Mrock_n, 'Mrock_l':like_Mrock_l, 'Mrock_h':like_Mrock_h})
likelihoods_Mrock.to_csv("data/likelihoods/like_Mrock.csv")

# Mrock total mass
nplanets_n = optimal_pdf(dn.ms, dn.metal, dn.nplanets); like_nplanets_n = nplanets_n.pdf(); 
nplanets_l = optimal_pdf(dl.ms, dl.metal, dl.nplanets); like_nplanets_l = nplanets_l.pdf(); 
nplanets_h = optimal_pdf(dh.ms, dh.metal, dh.nplanets); like_nplanets_h = nplanets_h.pdf();

likelihoods_nplanets = pd.DataFrame({'nplanets_n':like_nplanets_n, 'nplanets_l':like_nplanets_l, 'nplanets_h':like_nplanets_h})
likelihoods_nplanets.to_csv("data/likelihoods/like_nplanets.csv")

# Njup total mass
ngi_n = optimal_pdf(dn.ms, dn.metal, dn.ngi); like_ngi_n = ngi_n.pdf(); 
ngi_l = optimal_pdf(dl.ms, dl.metal, dl.ngi); like_ngi_l = ngi_l.pdf();
ngi_h = optimal_pdf(dh.ms, dh.metal, dh.ngi); like_ngi_h = ngi_h.pdf();

likelihoods_ngi = pd.DataFrame({'ngi_n':like_ngi_n, 'ngi_l':like_ngi_l, 'ngi_h':like_ngi_h})
likelihoods_ngi.to_csv("data/likelihoods/like_ngi.csv")

# Njup total mass
ntp_n = optimal_pdf(dn.ms, dn.metal, dn.npt); like_ntp_n = ntp_n.pdf(); 
ntp_l = optimal_pdf(dl.ms, dl.metal, dl.npt); like_ntp_l = ntp_l.pdf();
ntp_h = optimal_pdf(dh.ms, dh.metal, dh.npt); like_ntp_h = ntp_h.pdf();

likelihoods_ntp = pd.DataFrame({'ntp_n':like_ntp_n, 'ntp_l':like_ntp_l, 'ntp_h':like_ntp_h})
likelihoods_ntp.to_csv("data/likelihoods/like_ntp.csv")

'''

# tau gass 
tgas_n = optimal_pdf(dn.ms, dn.metal, dn.taugas); like_tgas_n = tgas_n.pdf(); 
tgas_l = optimal_pdf(dl.ms, dl.metal, dl.taugas); like_tgas_l = tgas_l.pdf();
tgas_h = optimal_pdf(dh.ms, dh.metal, dh.taugas); like_tgas_h = tgas_h.pdf();

likelihoods_tgas = pd.DataFrame({'tgas_n':like_tgas_n, 'tgas_l':like_tgas_l, 'tgas_h':like_tgas_h})
likelihoods_tgas.to_csv("data/likelihoods/like_tgas.csv")

