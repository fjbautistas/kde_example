#==========================================================================================
# This file has methods to plot the marginal distributions, from likelihoods 3d. 
#==========================================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
from Mthods import *
import warnings; warnings.simplefilter('ignore')
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']

#========================================== data ==========================================
dim = 150
# observational data:
obs_data = pd.read_csv('data/observations.csv',index_col=None); 
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
names = [r"Mass of Disk $M_d$ [$M_\odot$]",
         r"Dissipation time $\tau_g$ [y]",
         r"Center of mass $r_{\text{cm}}$ [AU]",
         r"Total planetary mass $M_{tp}$ [$M_\odot$]",
         r"Giant planetary mass $M_{\jupiter}$ [$M_\text{jup}$]",
         r"Rocky planetary mass $M_{r}$ [$M_{\oplus}$]",
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

unities = [r"$M_\odot$", r"y", r"AU", r"$M_\odot$", r"$M_\text{jup}$", r"$M_{\oplus}$"]

titles = ["No perturbations","Low perturbations","High perturbations"]

#======================================= Methods ===========================================
#--------significant figures
from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

#======================================== plots ============================================
#-------- For plots -------
def mplot_2v(marginal_md, marginal_tau, sys):
    name = [names[0], names[1]]
    sy   = [sym[0], sym[1]] 
    size, sf  = 15, 2
    m = [marginal_md, marginal_tau]
    x = [marginal_md.space[-1], marginal_tau.space[-1]]
    y = [marginal_md.marginal/marginal_md.marginal.max(),
         marginal_tau.marginal/marginal_tau.marginal.max()]
    z = [np.cumsum(marginal_md.marginal)*marginal_md.dz,
         np.cumsum(marginal_tau.marginal)*marginal_tau.dz]

    #Figure:
    fig, ax = plt.subplots(1,2, figsize=(12,5))
    for i in range(0,2):
        ax[i].plot(x[i], y[i], label = "Probability " + sy[i], lw = 2)
        ax[i].plot(x[i], z[i], label = "Acumulative " + sy[i], lw = 2)
        ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":");
        ax[i].set_xlabel(name[i],fontsize = size)
        ax[i].set_ylabel(sy[i],fontsize = size)
        ax[i].tick_params(axis='both', labelsize=size-2)
        if i == 0:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",
                          label = r"25\% = " + str(round_sig(m[i].p_25, sf)) + r' $M_\odot$')
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",
                          label = r"50\% = " + str(round_sig(m[i].p_50, sf)) + r' $M_\odot$')
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",
                          label = r"75\% = " + str(round_sig(m[i].p_75, sf)) + r' $M_\odot$')
        if i == 1:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",
                          label = r"25\% = " + "{:.1e}".format(m[i].p_25) + " y")
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",
                          label = r"50\% = " + "{:.1e}".format(m[i].p_50) + " y")
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",
                          label = r"75\% = " + "{:.1e}".format(m[i].p_75) + " y")
            plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)

        ax[i].legend(fontsize=size-1)
    
    plt.subplots_adjust(hspace=1.5)
    fig.tight_layout()
    plt.savefig("images/md_tau/"+sys+".pdf")
    #plt.show()

#------------------    
def mplot_com(marginal_com, obs, sys):
    name, sy = names[2], sym[2]
    size, sf = 15, 2

    x = [marginal_com[i].space[-1] for i in range(len(marginal_com))]
    y = [marginal_com[i].marginal/marginal_com[i].marginal.max()
         for i in range(len(marginal_com))]
    z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]
    #Figure:
    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(15,5))

    for i in range(0,3):
        ax[i].plot(x[i], z[i], label =  "Acumulative " +sy, lw = 2)
        ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":");
        ax[i].plot(x[i], y[i], label =  "Probability " +sy, lw = 2)
        ax[i].set_xlabel(name,fontsize = size)
        if i==0:
            ax[i].set_ylabel(sy,fontsize = size)
           
        ax[i].axvline(x = marginal_com[i].p_25,ls='--', c="C1",
                      label = r"25\% = " + str(round_sig(marginal_com[i].p_25, sf)) + " AU")
        ax[i].axvline(x = marginal_com[i].p_50,ls='--', c="C2",
                      label = r"50\% = " + str(round_sig(marginal_com[i].p_50, sf)) + " AU" )
        ax[i].axvline(x = marginal_com[i].p_75,ls='--', c="C3",
                      label = r"75\% = " + str(round_sig(marginal_com[i].p_75, sf)) + " AU")

        ax[i].axvline(x = obs, ls='--', c="k",
                      label = r"observed = " + str(round_sig(obs, sf)) + " AU" )

        ax[i].tick_params(axis='both', labelsize=size-2)
        ax[i].set_title(titles[i], fontsize = size-1)
        ax[i].legend(fontsize=size-1)
    
    plt.subplots_adjust(hspace=-.5)
    fig.tight_layout()
    plt.savefig("images/com/"+sys+".pdf")
    #plt.show()

#---------------------
#maginals_Ms is the list of marginals of Mt, Mjup and Mr
def mplot_Mass(marginal_Ms, obs, sys):
    name, sy = [names[3], names[4], names[5]], [sym[3], sym[4], sym[5]]
    size, sf  = 15, 3

    x, y, z = [], [], []
    
    for j in range(len(marginal_Ms)):
        x.append([marginal_Ms[j][i].space[2] for i in range(len(marginal_Ms[j]))])
        y.append([marginal_Ms[j][i].marginal/marginal_Ms[j][i].marginal.max() for i in range(len(marginal_Ms[j]))])
        z.append([np.cumsum(marginal_Ms[j][i].marginal)*marginal_Ms[j][i].dz for i in range(len(marginal_Ms[j]))])
        
    #Figure:
    fig, ax = plt.subplots(3, 3, sharey='row', figsize=(15,10))
    mins, maxs = [0,0,0], [0.003,1.1,800]
    
    for k in range(0,3):
        print(name[k])
        for m in range(0,3):
            ax[k,m].set_xlim(mins[k],maxs[k])
            ax[k,m].plot(x[k][m],y[k][m], label="Probability " + sym[3+k])
            ax[k,m].set_xlabel(names[k+3], fontsize = size)
            ax[k,m].tick_params(axis='both', labelsize=size-2)
            ax[k,m].plot(x[k][m],z[k][m])
            ax[k,m].axhline(0.25, ls=":")
            ax[k,m].axhline(0.5, ls=":")
            ax[k,m].axhline(0.75, ls=":")
            '''
            if k==0:
                ax[k,m].axvline(marginal_Ms[k][m].p_50,ls='--', c="C2",
                            label = r"50\% = " + "{:.2e}".format(marginal_Ms[k][m].p_50)+" "+unities[3+k])
                ax[k,m].axvline(marginal_Ms[k][m].p_75,ls='--', c="C3",
                            label = r"75\% = " + "{:.2e}".format(marginal_Ms[k][m].p_75)+" "+unities[3+k])
                ax[k,m].ticklabel_format(axis="x", style="sci", scilimits=(0,0))
                ax[k,m].set_title(titles[m], fontsize = size-1)
                ax[k,0].set_ylabel(sym[3+k],fontsize = size)
                ax[k,m].axvline(x = obs, ls='--', c="k",
                                label = r"observed = " + "{:.2e}".format(obs)+" "+unities[3+k])
                ax[k,m].legend(fontsize=size-1)
                
            elif k == 2:
                ax[k,m].axvline(marginal_Ms[k][m].p_25, ls='--', c="C1",
                                label = r"25\% = " + str(round_sig(marginal_Ms[k][m].p_25, sf))+" "+unities[3+k])
                ax[k,m].axvline(marginal_Ms[k][m].p_50,ls='--', c="C2",
                                label = r"50\% = " + str(round_sig(marginal_Ms[k][m].p_50, sf))+" "+unities[3+k])
                ax[k,m].axvline(marginal_Ms[k][m].p_75,ls='--', c="C3",
                                label = r"75\% = " + str(round_sig(marginal_Ms[k][m].p_75, sf))+" "+unities[3+k])
                ax[k,m].legend(fontsize=size-1)

            else:
                ax[k,m].axvline(marginal_Ms[k][m].p_50,ls='--', c="C2",
                                label = r"50\% = " + str(round_sig(marginal_Ms[k][m].p_50, sf))+" "+unities[3+k])
                ax[k,m].axvline(marginal_Ms[k][m].p_75,ls='--', c="C3",
                                label = r"75\% = " + str(round_sig(marginal_Ms[k][m].p_75, sf))+" "+unities[3+k])
                ax[k,m].legend(fontsize=size-1)
            '''    
            ax[1,0].set_ylabel(sym[4],fontsize = size)
            ax[2,0].set_ylabel(sym[5],fontsize = size)
       
    plt.subplots_adjust(hspace=0.288, wspace=0.165)
    fig.tight_layout()
    #plt.savefig("images/masses/"+sys+".pdf")
    plt.show()





