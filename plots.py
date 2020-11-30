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
         r"Number of giants $N_{\jupiter}$", r"Number of giants $N_{t}$"]

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
def mplot_mass(marginal_mass, obs, sys, name=names[3:6], sy=sym[3:6], unities=unities[3:6], t = titles):
    sf = 2
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]

    fig, ax = plt.subplots(3, 3, sharey=True, figsize=(14.5, 12))
    for m in range(0,3):
        for n in range(0,3): #take care the likelihoods are transponed respect the plot order 
            ax[m,n].plot(marginal_mass[n][m].z, marginal_mass[n][m].marginal/marginal_mass[n][m].marginal.max(),
                         label = "Probability "+sy[m])
            #ax[m,n].plot(marginal_mass[n][m].z, marginal_mass[n][m].inte, label = "acumulative")
            ax[m,n].axvline(x = marginal_mass[n][m].p_25,ls='--', c="C1",
                            label = r"25\% = " + "{:.1e}".format(marginal_mass[n][m].p_25) +" "+ unities[m])
            ax[m,n].axvline(x = marginal_mass[n][m].p_50,ls='--', c="C2",
                            label = r"50\% = " + "{:.1e}".format(marginal_mass[n][m].p_50) +" "+ unities[m])
            ax[m,n].axvline(x = marginal_mass[n][m].p_75,ls='--', c="C3",
                            label = r"75\% = " + "{:.1e}".format(marginal_mass[n][m].p_75) +" "+ unities[m])
            #ax[m,n].axhline(0.25, ls=":"); ax[m,n].axhline(0.5, ls=":"); ax[m,n].axhline(0.75,ls=":")
            ax[m,n].ticklabel_format(axis="x", style="sci", scilimits=(0,0), useOffset=True, useMathText=True)

            if m == 0 :
                ax[m,n].set_xlim(0,0.0045);
                ax[m,n].set_title(t[n])
                ax[m,n].axvline(x = obs, ls='--', c="k",
                                label = r"observed = "+ "{:.1e}".format(obs) +" "+ unities[m])
                
            elif m == 1: ax[m,n].set_xlim(0,1.3);
            else: ax[m,n].set_xlim(0,1000)

            if n == 0 :  
                ax[m,n].set_ylabel(sy[m]);# ax[1,n].set_ylabel(sy[1]); ax[2,n].set_ylabel(sy[2])

            ax[m,n].set_xlabel(name[m])
            ax[m,n].legend()
            
    fig.tight_layout()
    plt.subplots_adjust(wspace=.12)
    plt.savefig("images/masses/"+sys+".pdf")
    plt.show()
            






#maginals_Ms is the list of marginals of Mt, Mjup and Mr
'''
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
            
            ax[1,0].set_ylabel(sym[4],fontsize = size)
            ax[2,0].set_ylabel(sym[5],fontsize = size)
       
    plt.subplots_adjust(hspace=0.288, wspace=0.165)
    fig.tight_layout()
    #plt.savefig("images/masses/"+sys+".pdf")
    plt.show()
'''




