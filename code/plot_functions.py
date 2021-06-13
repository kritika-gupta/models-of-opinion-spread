import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm_notebook
import itertools
from itertools import chain
import csv
import pandas as pd
import ast
import os
import json
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib as mpl
import cycler
import powerlaw
fsize = 14

def plot_magnetization(media_to_dfs, camps, method, path, group = False, groupby_idx = None, save=False):
    
    if(group==False):
        for m in media_to_dfs:
            dfs = media_to_dfs[m]
            plt.figure(figsize=(8,6))
            for i in range(len(dfs)):
                num_sims = (max(dfs[i].sim)+1)
                c_m = dfs[i][['conc','magnetization']].groupby('conc').sum()/num_sims
                plt.plot(c_m, 'o-', label = "m = " + camps[i].split('_')[0])
            plt.title("Sznajd's 2D Model with Media Effect = "+str(m), fontsize = fsize)
            plt.xlabel("initial upward spin concentration", fontsize = fsize)
            plt.ylabel("magnetization", fontsize = fsize)
            plt.legend(loc = 0)
            plt.grid(True)
            if(save):
                plt.savefig(path+method+"media"+str(m)+".png", dpi = 100)
            else:
                plt.show()
        return
    
    if(group==True):
        plt.figure(figsize=(8,6))
        for m in sorted(media_to_dfs, reverse=True):
            dfs = media_to_dfs[m]

            num_sims = (max(dfs[groupby_idx].sim)+1)
            c_m = dfs[groupby_idx][['conc','magnetization']].groupby('conc').sum()/num_sims
            
            
            plt.plot(c_m, 'o-', label = "p = %0.3f"%m)
        plt.title(method, fontsize = fsize)
#             plt.title("Effect of external field", fontsize = fsize)
        plt.xlabel("initial upward spin concentration", fontsize = fsize)
        plt.ylabel("magnetization", fontsize = fsize)
        plt.grid(True)
        plt.legend(loc = 0)
        if(save):
            plt.savefig(path+method+".png", dpi = 100)
        else:
            plt.show()
    return
    
def plot_ss(media_to_dfs, camps, method, path, save=False):
    for media in media_to_dfs:
        dfs = media_to_dfs[media]
        for i in range(len(dfs)):
            plt.figure(figsize = (8, 6))
            conc_grouped = dfs[i].groupby('conc').groups
            concs = sorted(conc_grouped.keys())
            yeslist, nolist, stalematelist, undecidedlist = [], [], [], []
            thresh = 0

            for conc in sorted(conc_grouped):
                m = (dfs[i].iloc[conc_grouped[conc].values])['magnetization']
                yes = (np.sum((m==1) | (abs(1-m) <= thresh)))
                no = (np.sum((m==-1) | (abs(-1-m) <= thresh)))
                stalemate = (np.sum((m==0) | (abs(0-m) <= thresh)))
                undecided = (len(m) - yes - no - stalemate)
                yeslist.append(yes/len(m))
                nolist.append(no/len(m))
                stalematelist.append(stalemate/len(m))
                undecidedlist.append(undecided/len(m))
            plt.title(r"Media Effect $p$= "+str(media), fontsize = fsize)#+" weights = "+camps[i])
#             plt.title("Steady State Distribution", fontsize = fsize)
            plt.plot(concs, yeslist, 'o-', label = 'consensus A')
            plt.plot(concs, nolist, 'o-', label = 'consensus B')
            plt.plot(concs, stalematelist, 'o-', label = 'stalemate')
            plt.plot(concs, undecidedlist, 'o-', label = 'none')
            plt.legend(loc = 0)
            plt.xlabel("initial upward spin concentration "+r"$Cu$", fontsize = fsize)
            plt.ylabel("probability", fontsize = fsize)
            plt.grid(True)
            if(save):
                plt.savefig(path+method+"media"+str(media)+"_"+camps[i]+".png", dpi = 100)
            else:
                plt.show()

            
def load_data(folder_path, method, C, media_list):  
    os.listdir(folder_path)
    media_to_dfs = {}
    for m in media_list:
        dfs = dict.fromkeys(range(C))
        camps = dict.fromkeys(range(C))
        path = folder_path +"media"+str(m)+"/"
        print(path)
        for i, foldername in enumerate(sorted(os.listdir(path))):
            print(i, foldername)
            camps[i] = foldername
            df = pd.DataFrame()
            for filename in os.listdir(path+foldername+"/"+method+"/"):
    #             print(filename)
                if filename.startswith(method) and filename.endswith(".csv"):
                    df_temp = pd.read_csv(path+foldername+"/"+method+"/"+filename)
                    df = pd.concat([df, df_temp], ignore_index=True)
            dfs[i] = df
        media_to_dfs.update({m:dfs})
    return media_to_dfs, camps

# parameter_combination = 'm_0.1d_24_c_0.32653061224489793'
# simulation_number = 'states40'
# states = np.load(folder_path+"media0.1/05_05/default/"+parameter_combination+"/"+simulation_number+".npy")
# print(states.shape)
# sweeps = states.shape[0]
# factor = 1
# L = 24
# kbT = 1
# states = states.reshape(-1, L, L)[:, :, :]
# selection = np.arange(0, states.shape[0], factor)
# states = states[selection]
# print(states.shape)
# np.mean(states[-1])

# M = [np.mean(states[0])]

# def update(i):
#     matrix.set_array(states[i])
#     M.append(np.mean(states[i]))
#     line.set_data(np.arange(0, len(M)), M)
#     sweep_text.set_text("iteration = " + str(i))
#     return matrix, line, sweep_text

# gs=GridSpec(1,2)
# fig = plt.figure(figsize = (15, 6)) 

# ax1 = fig.add_subplot(gs[0, 1])
# matrix = ax1.imshow(states[0])
# sweep_text = ax1.text(0.1, -1, '')

# plt.colorbar(matrix)

# ax2 = fig.add_subplot(gs[0, 0])
# line, = ax2.plot([], [], 'k', lw = 2)
# ax2.set_ylim([-1.1, 1.1])
# ax2.set_xlim([0, len(states)])
# ax2.set_xticklabels((ax2.get_xticks()*factor).astype('int'))
# ax2.set_xlabel("Iteration")
# ax2.set_ylabel("Magnetization")
# ax2.set_title("L = " + str(L))


# ani = animation.FuncAnimation(fig, update, frames = range(0,len(states)))

# ani.save("./images/Animations/"+method+"_"+str(parameter_combination)+"_"+str(simulation_number)+'.gif', writer='imagemagick', fps=4)