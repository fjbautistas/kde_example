#==========================================================================================
# This file has methods to plot the marginal distributions, from likelihoods 3d. 
#==========================================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
         r"Total planetary mass $M_{tp}$ [$M_\text{Jup}$]",
         r"Total giant planetary mass $M_{\jupiter}$ [$M_\text{Jup}$]",
         r"Total of rocky planetary mass $M_{r}$ [$M_{\oplus}$]", r"Number of total planets $N_{t}$",
         r"Number of giants planets $N_{\jupiter}$", r"Number of rocky planets $N_{r}$"]

sym   = [r"$p\left(M_d\right)$", r"$p\left(\tau_g\right)$", r"$p\left(r_{\text{cm}}\right)$",
         r"$p\left(M_{tp}\right)$", r"$p\left(M_{\jupiter}\right)$",
         r"$p\left(M_{r}\right)$", r"$p\left(N_{t}\right)$",
         r"$p\left(N_{\jupiter}\right)$",r"$p\left(N_{r}\right)$"]

unities = [r"$M_\odot$", r"y", r"AU", r"$M_\text{Jup}$", r"$M_\text{Jup}$", r"$M_\oplus$"]

titles = ["No perturbations","Low perturbations","High perturbations"]
#======================================= Methods ===========================================
#--------significant figures
from math import log10, floor
def round_sig(x, sig=2):
    r = round(x, sig-int(floor(log10(abs(x))))-1)
    return r

#======================================== plots ============================================
#------------------------------------- For plots -------------------------------------------
'''
def mplot_num(marginal_num, obs, sys, name=names[6:9], sy=sym[6:9], t = titles):
    sf, lw = 2, 2
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]
    fig, ax = plt.subplots(3, 3, sharey=True, figsize=(14.5, 12))
    for m in range(0,3):
        for n in range(0,3): #take care the likelihoods are transponed respect the plot order
            ax[m,n].set_ylim(0,1.05)
            ax[m,n].plot(marginal_num[n][m].z, marginal_num[n][m].marginal/marginal_num[n][m].marginal.max(),
                         label = "PDF: "+sy[m])
            if n == 0 :  
                ax[m,n].set_ylabel(sy[m]);
            #ax[m,n].plot(marginal_num[n][m].z, marginal_num[n][m].inte, label = "acumulative")
            #ax[m,n].axhline(0.25, ls=":"); ax[m,n].axhline(0.5, ls=":"); ax[m,n].axhline(0.75,ls=":")
            if m == 0 :
                ax[m,n].set_title(t[n]); ax[m,n].set_xlim(0,30); 
                ax[m,n].axvline(x = round(marginal_num[n][m].p_25), ls='--', c="C1", lw = 1.5, 
                                label = r"25\% = " + str(round(marginal_num[n][m].p_25)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_50), ls='--', c="C2", lw = 1.5, 
                                label = r"50\% = " + str(round(marginal_num[n][m].p_50)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_75), ls='--', c="C3", lw = 1.5,
                                label = r"75\% = " + str(round(marginal_num[n][m].p_75)))
                ax[m,n].axvline(x = 8, ls='-.',lw = lw,  c="C4",label = r"Solar System = "+str(8))
                ax[m,n].axvline(x = obs[m], ls='-',lw = lw,  c="k",label = r"Observed = "+  str(round(obs[m])))
                
            elif m == 1:
                ax[m,n].set_xlim(0,3)
                ax[m,n].axvline(x = round(marginal_num[n][m].p_75), ls='--', c="C3", lw = 1.5,
                                label = r"75\% = " + str(round(marginal_num[n][m].p_75)))
                ax[m,n].axvline(x = 4, ls='-.', lw = lw, c="C4",
                                label = r"Solar System = "+str(4))
                ax[m,n].axvline(x = obs[m], ls='-', lw = lw, c="k",
                                label = r"observed = "+str(round(obs[m])))
                
            else:
                ax[m,n].set_xlim(0,30)
                ax[m,n].axvline(x = round(marginal_num[n][m].p_25), ls='--', c="C1", lw = 1.5, 
                                label = r"25\% = " + str(round(marginal_num[n][m].p_25)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_50), ls='--', c="C2", lw = 1.5, 
                                label = r"50\% = " + str(round(marginal_num[n][m].p_50)))
                ax[m,n].axvline(x = round(marginal_num[n][m].p_75), ls='--', c="C3", lw = 1.5,
                                label = r"75\% = " + str(round(marginal_num[n][m].p_75)))
                ax[m,n].axvline(x = 4, ls='-.', lw = lw,  c="C4", label = r"Solar System = "+str(4))
                ax[m,n].axvline(x = obs[m], ls='-', lw = lw, c="k",
                                label = r"observed = "+str(round(obs[m])))
                
            ax[m,n].set_xlabel(name[m])
            ax[m,n].legend(handletextpad=.4, labelspacing=.25, loc=0)
            
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/n_planets/"+sys+".pdf")
    plt.show()
'''

def mplot_num2(marginal, obs, sys, name=names[7:9], sy=sym[7:9], t = titles):
    sf = 2; marginal_num = marginal[0][1:3]; lw = 2
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]
    fig, ax = plt.subplots(1, 2, sharey=True, figsize=(9.6, 4.2))
    for n in range(0,2): #take care the likelihoods are transponed respect the plot order
        #xsprint(n)
        #if n == 0 : ax[n].set_xlim(0,6);
        ax[n].set_ylim(0,1.05)
        ax[n].plot(marginal_num[n].z, marginal_num[n].marginal/marginal_num[n].marginal.max(),
                   label = "PDF: "+sy[n])
        ax[n].set_ylabel(sy[n]); 
        
        if n == 0 :
            ax[n].set_xlim(0,3.5);
            
            if  round(marginal_num[n].p_25) == 0 and round(marginal_num[n].p_25) == 0:
                ax[n].axvline(x = round(marginal_num[n].p_75), ls='--', c="C3", lw = 1.5,
                              label = r"75\% = " + str(round(marginal_num[n].p_75)))
                ax[n].axvline(x = 4, ls='-.',lw = lw,  c="C4",label = r"Solar System = "+str(4))
                ax[n].axvline(x = obs[n], ls='-',lw = lw,  c="k",label = r"Observed = "+  str(round(obs[n])))

            elif round(marginal_num[n].p_25) == 0:
                ax[n].axvline(x = round(marginal_num[n].p_50), ls='--', c="C3", lw = 1.5,
                              label = r"50\% = " + str(round(marginal_num[n].p_50)))
                ax[n].axvline(x = round(marginal_num[n].p_75), ls='--', c="C3", lw = 1.5,
                              label = r"75\% = " + str(round(marginal_num[n].p_75)))
                ax[n].axvline(x = 4, ls='-.',lw = lw,  c="C4",label = r"Solar System = "+str(4))
                ax[n].axvline(x = obs[n], ls='-',lw = lw,  c="k",label = r"Observed = "+  str(round(obs[n])))
            
        else:
            ax[n].set_xlim(0,30)
            ax[n].axvline(x = round(marginal_num[n].p_25), ls='--', c="C1", lw = 1.5, 
                            label = r"25\% = " + str(round(marginal_num[n].p_25)))
            ax[n].axvline(x = round(marginal_num[n].p_50), ls='--', c="C2", lw = 1.5, 
                            label = r"50\% = " + str(round(marginal_num[n].p_50)))
            ax[n].axvline(x = round(marginal_num[n].p_75), ls='--', c="C3", lw = 1.5,
                            label = r"75\% = " + str(round(marginal_num[n].p_75)))
            ax[n].axvline(x = 4, ls='-.', lw = lw,  c="C4", label = r"Solar System = "+str(4))
            ax[n].axvline(x = obs[n], ls='-', lw = lw, c="k",
                            label = r"observed = "+str(round(obs[n])))
            
        ax[n].set_xlabel(name[n])
        ax[n].legend(handletextpad=.4, labelspacing=.25, loc=0)
    
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/n_planets/"+sys+"_2.pdf")
    plt.show()
    
'''    
#------------------------------------- Masses ---------------------------------------- 
def mplot_mass(marginal_mass, obs, dobs, sys, name=names[3:6], sy=sym[3:6], unities=unities[3:6], t = titles):
    sf = 3
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]
    fig, ax = plt.subplots(3, 3, sharey=True, figsize=(14.5, 12))
    
    for m in range(0,3):
        for n in range(0,3): #take care the likelihoods are transponed respect the plot order 
            ax[m,n].set_ylim(0,1.05)
            if    m == 0: ax[m,n].set_xlim(0,6);  ax[m,n].set_title(t[n])
            elif  m == 1: ax[m,n].set_xlim(0,6)
            else:         ax[m,n].set_xlim(0,30)
            if    n == 0: ax[m,n].set_ylabel(sy[m])

            line, = ax[m,n].plot(marginal_mass[n][m].z,
                                 marginal_mass[n][m].marginal/marginal_mass[n][m].marginal.max())
            a =ax[m,n].axvline(x = marginal_mass[n][m].p_25,ls='--', c="C1", lw = 1.5)
            b =ax[m,n].axvline(x = marginal_mass[n][m].p_50,ls='--', c="C2", lw = 1.5)
            c =ax[m,n].axvline(x = marginal_mass[n][m].p_75,ls='--', c="C3", lw = 1.5)
            d =ax[m,n].axvline(obs[m], ls='--', c="k", lw = 1.5)
            e =ax[m,n].fill_between(np.array([obs[m]-dobs[m], obs[m]+dobs[m]]), -.5, 1.5, alpha = .2, color ='k')
            
            ax[m,n].set_xlabel(name[m])
            
            if obs[m] != 0:
                ax[m,n].legend([line,a,b,c,(d,e)],
                               ["PDF: "+sy[m],
                                r"25\% = " + str(round_sig(marginal_mass[n][m].p_25, sf))+" "+unities[m],
                                r"50\% = " + str(round_sig(marginal_mass[n][m].p_50, sf))+" "+unities[m],
                                r"75\% = " + str(round_sig(marginal_mass[n][m].p_75, sf))+" "+unities[m],
                                r"Obs = "+"%.3g" % obs[m]+r"$\pm$"+"%.3g" % dobs[m]+" "+unities[m]],
                               handletextpad=.4, labelspacing=.25, loc=0)

            else:
                ax[m,n].legend([line,a,b,c,(d,e)],
                               ["PDF: "+sy[m],
                                r"25\% = " + str(round_sig(marginal_mass[n][m].p_25, sf))+" "+unities[m],
                                r"50\% = " + str(round_sig(marginal_mass[n][m].p_50, sf))+" "+unities[m],
                                r"75\% = " + str(round_sig(marginal_mass[n][m].p_75, sf))+" "+unities[m],
                                r"Obs = No observations"],
                               handletextpad=.4, labelspacing=.25, loc=0)
                    
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/masses/"+sys+".pdf")
    plt.show()


def mplot_mass2(marginal, obs, dobs, sys, name=names[4:6], sy=sym[4:6], unities=unities[4:6]):
    sf = 3; marginal_mass = marginal[0][1:3]
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]
    fig, ax = plt.subplots(1, 2, sharey=True, figsize=(9.6, 4.2))
    for n in range(0,2): #take care the likelihoods are transponed respect the plot order
        #xsprint(n)
        #if n == 0 : ax[n].set_xlim(0,6);
        if n == 0: ax[n].set_xlim(0,6);
        else: ax[n].set_xlim(0,35)

        line, = ax[n].plot(marginal_mass[n].z,
                           marginal_mass[n].marginal/marginal_mass[n].marginal.max())
        a = ax[n].axvline(x = marginal_mass[n].p_25,ls='--', c="C1", lw = 1.5)
        b = ax[n].axvline(x = marginal_mass[n].p_50,ls='--', c="C2", lw = 1.5)
        c = ax[n].axvline(x = marginal_mass[n].p_75,ls='--', c="C3", lw = 1.5)
        d = ax[n].axvline(obs[n], ls='--', c="k", lw = 1.5)
        e  =ax[n].fill_between(np.array([obs[n]-dobs[n], obs[n]+dobs[n]]), -.5, 1.5, alpha = .2, color ='k')

        ax[n].set_xlabel(name[n]);ax[n].set_ylabel(sy[n])
        ax[n].set_ylim(0,1.05)

        if obs[n] != 0:
            ax[n].legend([line,a,b,c,(d,e)],
                           ["PDF: "+sy[n],
                            r"25\% = " + str(round_sig(marginal_mass[n].p_25, sf))+" "+unities[n],
                            r"50\% = " + str(round_sig(marginal_mass[n].p_50, sf))+" "+unities[n],
                            r"75\% = " + str(round_sig(marginal_mass[n].p_75, sf))+" "+unities[n],
                            r"Obs = "+"%.3g" % obs[n]+r"$\pm$"+"%.3g" % dobs[n]+" "+unities[n]],
                           handletextpad=.4, labelspacing=.25, loc=0)

        else:
            ax[n].legend([line,a,b,c,(d,e)],
                           ["PDF: "+sy[n],
                            r"25\% = " + str(round_sig(marginal_mass[n].p_25, sf))+" "+unities[n],
                            r"50\% = " + str(round_sig(marginal_mass[n].p_50, sf))+" "+unities[n],
                            r"75\% = " + str(round_sig(marginal_mass[n].p_75, sf))+" "+unities[n],
                            r"Obs = No observations"],
                           handletextpad=.4, labelspacing=.25, loc=0)
    
    fig.tight_layout()
    plt.subplots_adjust(wspace=.11)
    plt.savefig("images/masses/"+sys+"_2.pdf")
    plt.show()
    
#------------------------------------- Md and Tau ---------------------------------------- 
def mplot_md_tau(marginal_md, marginal_tau, sys, obs, name=names, sy=sym, unities=unities):
    sf= 2
    m = [marginal_md, marginal_tau]
    x = [marginal_md.z, marginal_tau.z]
    y = [marginal_md.marginal/marginal_md.marginal.max(),marginal_tau.marginal/marginal_tau.marginal.max()]
    #z = [np.cumsum(marginal_md.marginal)*marginal_md.dz,np.cumsum(marginal_tau.marginal)*marginal_tau.dz]
    fig, ax = plt.subplots(1, 2, figsize=(10.9,3.9))
    for i in range(0,2):
        ax[i].plot(x[i], y[i], label = "PDF: " + sy[i], lw=2)
        ax[i].yaxis.set_major_locator(plt.MaxNLocator(5))
        #ax[i].plot(x[i], z[i], label = "Acumulative " + sy[i], lw = 2)
        #ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":")
        ax[i].set_xlabel(name[i]); ax[i].set_ylabel(sy[i])
        #ax[i].set_xlim(0,x[i].max()); ax[i].set_ylim(0,1.05)

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
        ax[i].legend(handletextpad=.4, labelspacing=.25, loc=0)
    #fig.text(.49, .95, "System "+sys)
    fig.tight_layout(rect=[-0.02, -0.02, 1, 1])
    plt.savefig("images/md_tau/"+sys+"md.pdf")
    plt.show()

#------------------------------------- COM ------------------------------------------- 
def mplot_com(marginal_com, obs, dobs, sys, name=names[2], sy=sym[2], unities=unities):
    sf = 2
    x = [marginal_com[i].z for i in range(len(marginal_com))]
    y = [marginal_com[i].marginal/marginal_com[i].marginal.max() for i in range(len(marginal_com))]
    #z = [np.cumsum(marginal_com[i].marginal)*marginal_com[i].dz for i in range(len(marginal_com))]

    fig, ax = plt.subplots(1, 3, sharey=True, figsize=(13.9, 4))
    ax[0].set_ylabel(sy)
    for i in range(0,3):
        #ax[i].plot(x[i], z[i], label =  "Acumulative " +sy)
        #ax[i].axhline(0.25, ls=":"); ax[i].axhline(0.5, ls=":"); ax[i].axhline(0.75,ls=":");
        line, = ax[i].plot(x[i], y[i], label = r"PDF "+sy, c="C0", ls = "-")
        ax[i].set_xlim(0,20); ax[i].set_ylim(0,1.05)
        ax[i].set_xlabel(name); 
        ax[i].tick_params(axis='both')
        ax[i].set_title(titles[i])
        
        a0 = ax[i].axvline(x = marginal_com[i].p_25,ls='--', c="C1")
        a1 = ax[i].axvline(x = marginal_com[i].p_50,ls='--', c="C2")
        a2 = ax[i].axvline(x = marginal_com[i].p_75,ls='--', c="C3")
        p1 = ax[i].axvline(x = obs, ls='--', c="k", lw = 1.25)
        p2 = ax[i].fill_between( np.array([obs-dobs, obs+dobs]), -.5, 1.5, alpha = .2, color ='k')

        ax[i].legend([line,a0,a1,a2,(p1,p2)],[r"PDF: " + sy,
                                              r"25\% = "+str(round_sig(marginal_com[i].p_25, sf))+" AU",
                                              r"50\% = "+str(round_sig(marginal_com[i].p_50, sf))+" AU",
                                              r"75\% = "+str(round_sig(marginal_com[i].p_75, sf))+" AU",
                                              r"Obs = "+str(round_sig(obs, sf))+
                                              r"$\pm$"+str(round_sig(dobs, sf))+" AU"],
                     handletextpad=.4, labelspacing=.25, loc=0) 
    
    #plt.subplots_adjust(hspace=-.5)
    fig.tight_layout()
    plt.savefig("images/com/"+sys+".pdf")
    plt.show()
'''
