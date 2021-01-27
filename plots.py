#==========================================================================================
# This file has methods to plot the marginal distributions, from likelihoods 3d. 
#==========================================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
from Methods import *
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import matplotlib.ticker as mtick

import warnings; warnings.simplefilter('ignore')
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}', r'\usepackage{wasysym}']
plt.style.use('./images/img.mplstyle')

#================================== Names and symbols ======================================
names = [r"Mass of Disk $M_d$ [$M_\odot$]", r"Dissipation time $\tau_g$ [y]",
         r"Center of mass $r_{\text{cm}}$ [AU]",
         r"Total planet mass $M_{tp}$ [$M_\odot$]",
         r"Giant planet mass $M_{\jupiter}$ [$M_\text{jup}$]",
         r"Rocky planet  mass $M_{r}$ [$M_{\oplus}$]", r"Number of total planets $N_{t}$",
         r"Number of giants planets $N_{\jupiter}$", r"Number of rocky planets $N_{\oplus}$"]

sym   = [r"$p\left(M_d\right)$", r"$p\left(\tau_g\right)$", r"$p\left(r_{\text{cm}}\right)$",
         r"$p\left(M_{tp}\right)$", r"$p\left(M_{\jupiter}\right)$",
         r"$p\left(M_{r}\right)$", r"$p\left(N_{t}\right)$",
         r"$p\left(N_{\jupiter}\right)$",r"$p\left(N_{\oplus}\right)$"]

unities = [r"$M_\odot$", r"y", r"AU", r"$M_\odot$", r"$M_\text{jup}$", r"$M_{\oplus}$"]

titles = ["No perturbations","Low perturbations","High perturbations"]
#======================================= Methods ===========================================
#--------significant figures
from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

#======================================== plots ============================================
#------------------------------------- For plots -------------------------------------------
'''
def mplot_num(marginal_num, obs, sys, name=names[6:9], sy=sym[6:9], t = titles):
    sf, lw = 2, 2
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]

    fig, ax = plt.subplots(3, 3, sharey=True, figsize=(14.5, 12))
    for m in range(0,3):
        for n in range(0,3): #take care the likelihoods are transponed respect the plot order 
            ax[m,n].plot(marginal_num[n][m].z, marginal_num[n][m].marginal/marginal_num[n][m].marginal.max(),
                         label = "Probability "+sy[m])
            #ax[m,n].plot(marginal_num[n][m].z, marginal_num[n][m].inte, label = "acumulative")
            #ax[m,n].axhline(0.25, ls=":"); ax[m,n].axhline(0.5, ls=":"); ax[m,n].axhline(0.75,ls=":")
            if m == 2 :  
                ax[m,n].axvline(x = 4, ls='-', lw = lw,  c="C4", label = r"Solar System = "+str(4))

            if m == 0 :
                ax[m,n].set_title(t[n])
                ax[m,n].axvline(x = 8, ls='-',lw = lw,  c="C4",label = r"Solar System = "+str(8))
                ax[m,n].axvline(x = obs, ls='-',lw = lw,  c="k",label = r"observed = "+  str(round(obs)))
                
            if m == 1:
                ax[m,n].axvline(x = 4, ls='-', lw = lw, c="C4",
                                label = r"Solar System = "+str(4))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_75), ls='--', c="C3", lw = 1.5,
                                label = r"75\% = " + str(round(marginal_num[n][m].p_75)))
                ax[m,n].set_xlim(0,3)
                
            else: 
                ax[m,n].axvline(x = round(marginal_num[n][m].p_25), ls='--', c="C1", lw = 1.5, 
                                label = r"25\% = " + str(round(marginal_num[n][m].p_25)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_50), ls='--', c="C2", lw = 1.5, 
                                label = r"50\% = " + str(round(marginal_num[n][m].p_50)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_75), ls='--', c="C3", lw = 1.5,
                                label = r"75\% = " + str(round(marginal_num[n][m].p_75)))
                
            if n == 0 :  
                ax[m,n].set_ylabel(sy[m]);# ax[1,n].set_ylabel(sy[1]); ax[2,n].set_ylabel(sy[2])
                
            ax[m,n].set_xlabel(name[m])
            ax[m,n].legend()
            
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/n_planets/"+sys+".pdf")
    plt.show()


def mplot_mass(marginal_mass, obs, sys, name=names[3:6], sy=sym[3:6], unities=unities[3:6], t = titles):
    sf = 2
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]

    fig, ax = plt.subplots(3, 3, sharey=True, figsize=(14.5, 12))
    for m in range(0,3):
        for n in range(0,3): #take care the likelihoods are transponed respect the plot order 
            ax[m,n].plot(marginal_mass[n][m].z, marginal_mass[n][m].marginal/marginal_mass[n][m].marginal.max(),
                         label = "Probability "+sy[m])
            #ax[m,n].plot(marginal_mass[n][m].z, marginal_mass[n][m].inte, label = "acumulative")
            ax[m,n].axvline(x = marginal_mass[n][m].p_25,ls='--', c="C1", lw = 1.5,
                            label = r"25\% = " + "{:.1e}".format(marginal_mass[n][m].p_25) +" "+ unities[m])
            ax[m,n].axvline(x = marginal_mass[n][m].p_50,ls='--', c="C2", lw = 1.5,
                            label = r"50\% = " + "{:.1e}".format(marginal_mass[n][m].p_50) +" "+ unities[m])
            ax[m,n].axvline(x = marginal_mass[n][m].p_75,ls='--', c="C3", lw = 1.5,
                            label = r"75\% = " + "{:.1e}".format(marginal_mass[n][m].p_75) +" "+ unities[m])
            #ax[m,n].axhline(0.25, ls=":"); ax[m,n].axhline(0.5, ls=":"); ax[m,n].axhline(0.75,ls=":")
            ax[m,n].ticklabel_format(axis="x", style="sci", scilimits=(0,0), useOffset=True, useMathText=True)

            if m == 0 :
                ax[m,n].set_xlim(0,0.0045);
                ax[m,n].set_title(t[n])
                ax[m,n].axvline(x = obs, ls='--', c="k", lw = 1.5,
                                label = r"observed = "+ "{:.1e}".format(obs) +" "+ unities[m])
                
            elif m == 1: ax[m,n].set_xlim(0,1.3);
            else: ax[m,n].set_xlim(0,1000)

            if n == 0 :  
                ax[m,n].set_ylabel(sy[m]);# ax[1,n].set_ylabel(sy[1]); ax[2,n].set_ylabel(sy[2])

            ax[m,n].set_xlabel(name[m])
            ax[m,n].legend()
            
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/masses/"+sys+".pdf")
    plt.show()
            

#------------------------------------- For plots ------------------------------------------- 
def mplot_md_tau(marginal_md, marginal_tau, sys, obs, name=names, sy=sym, unities=unities):
    sf= 2
    m = [marginal_md, marginal_tau]
    x = [marginal_md.z, marginal_tau.z]
    y = [marginal_md.marginal/marginal_md.marginal.max(),marginal_tau.marginal/marginal_tau.marginal.max()]
    #z = [np.cumsum(marginal_md.marginal)*marginal_md.dz,np.cumsum(marginal_tau.marginal)*marginal_tau.dz]
    fig, ax = plt.subplots(1, 2, figsize=(10.9,3.9))
    for i in range(0,2):
        ax[i].plot(x[i], y[i], label = "Probability " + sy[i], lw=2)
        ax[i].yaxis.set_major_locator(plt.MaxNLocator(5))
        #ax[i].plot(x[i], z[i], label = "Acumulative " + sy[i], lw = 2)
        #ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":")
        ax[i].set_xlabel(name[i]); ax[i].set_ylabel(sy[i])
        if i == 0:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",label = r"25\% = "\
                          + str(round_sig(m[i].p_25, sf)) +" "+unities[i])
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",label = r"50\% = "\
                          + str(round_sig(m[i].p_50, sf)) +" "+unities[i])
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",
                          label = r"75\% = " + str(round_sig(m[i].p_75, sf))\
                          +" "+ unities[i])
        if i == 1:
            ax[i].axvline(x = m[i].p_25,ls='--', c="C1",label = r"25\% = "\
                          + "{:.1e}".format(m[i].p_25) +" "+ unities[i])
            ax[i].axvline(x = m[i].p_50,ls='--', c="C2",label = r"50\% = "\
                          + "{:.1e}".format(m[i].p_50)+" "+unities[i])
            ax[i].axvline(x = m[i].p_75,ls='--', c="C3",label = r"75\% = "\
                          + "{:.1e}".format(m[i].p_75) +" "+ unities[i])
            plt.ticklabel_format(axis="x", style="sci", useOffset=False, 
                                 scilimits=(6,6), useMathText=True)
        ax[i].legend()
    #fig.text(.49, .95, "System "+sys)
    fig.tight_layout(rect=[-0.02, -0.02, 1, 1])
    plt.savefig("images/md_tau/"+sys+"md.pdf")
    plt.show()


#------------------------------------- For plots ------------------------------------------- 
'''
def mplot_com(marginal_com, obs, sys, name=names[2], sy=sym[2], unities=unities):
    sf = 2
    x = [marginal_com[i].z for i in range(len(marginal_com))]
    y = [marginal_com[i].marginal/marginal_com[i].marginal.max() for i in range(len(marginal_com))]
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]

    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(13.5, 3.9))
    ax[0].set_ylabel(sy)
    for i in range(0,3):
        #ax[i].plot(x[i], z[i], label =  "Acumulative " +sy)
        #ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":");
        ax[i].plot(x[i], y[i], label = r"Probability "+sy)
        ax[i].set_xlabel(name); 
           
        ax[i].axvline(x = marginal_com[i].p_25,ls='--', c="C1",
                      label = r"25\% = " + str(round_sig(marginal_com[i].p_25, sf)) + " AU")
        ax[i].axvline(x = marginal_com[i].p_50,ls='--', c="C2",
                      label = r"50\% = " + str(round_sig(marginal_com[i].p_50, sf)) + " AU")
        ax[i].axvline(x = marginal_com[i].p_75,ls='--', c="C3",
                      label = r"75\% = " + str(round_sig(marginal_com[i].p_75, sf)) + " AU")
        ax[i].axvline(x = obs, ls='--', c="k",
                      label = r"observed = "+ str(round_sig(obs, sf)) + " AU" )

        ax[i].tick_params(axis='both')
        ax[i].set_title(titles[i])
        ax[i].legend()
    
    #plt.subplots_adjust(hspace=-.5)
    fig.tight_layout()
    plt.savefig("images/com/"+sys+".pdf")
    plt.show()

#------------------------------------- For plots ------------------------------------------- 
