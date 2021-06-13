import numpy as np 
import csv
import time
from Lattice2D import * 
import multiprocessing as mp
import json
import os
import sys
import itertools
import shutil

def simulate(params):
    [num_simulations, conc, domains, media_prob, up_prob, down_prob, method, filename, path] = params
    # method_path = method + "/"

    with open(path+filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['media','domain','conc','sim','magnetization','relaxation', 'decision'])
        
    for key in list(itertools.product(domains)):
        L = key[0]
        # conc = key[1]
        
        # folder to save states for this combination
        # parameter_path = method_path+"m_"+str(media_prob)+"d_"+str(L)+"_c_"+str(conc)+"/"
        # os.mkdir(parameter_path)

        for i in (range(num_simulations)):
            lattice = Lattice(L, conc)
            m, rel_time, dec_times, states = lattice.metropolis(media = media_prob, up = up_prob, down = down_prob, method = method)
            dec_times = [x for sublist in dec_times for x in sublist]
            c = []
            temp = np.unique(dec_times, return_counts=True)
            c.append(list(temp[0]*1.0))
            c.append(list(temp[1]*1.0))    
            with open(path+filename, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([media_prob, L, conc, i, m, rel_time, json.dumps(c)])
            # if(i%10==0):
                # np.save(parameter_path+"states"+str(i), np.array(states))

num_procs = mp.cpu_count()
choice = int(input("Enter 0 to use default parameter values, enter 1 to input the values.\n"))
if(choice==1):
    medias = [float(x) for x in (input("Enter list of media values\n").split())]

    concs_input = tuple(float(x) for x in input("Enter range of initial upward concentrations : start end steps\n").split())
    concs = np.round(np.linspace(concs_input[0], concs_input[1], concs_input[2]), 3)

    domains = [24]

    num_simulations = int(input("Enter number of simulations\n"))

    ups = [float(x) for x in input("Enter list of ratios of initial upward spins (eg. 1 0.75 0.5)\n").split()]

    method_list = ['default', 'modified1', 'modified2']
    methods = [method_list[int(x)] for x in input("Enter list of method codes (default(0), modified1(1), modified2(2))\n").split()]

else:
    medias = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2]
    concs = np.round(np.linspace(0, 1, 25), 3)
    domains = [24]
    num_simulations = 3
    ups = [1, 0.75, 0.5]
    methods = ['default', 'modified1', 'modified2']


print("domains =", domains)
print("medias =", medias)
print("concentrations =", concs)
print("simulation runs =", num_simulations)
print("upward ratios =", ups)
print("methods =", methods)
print("CPUs available = ", mp.cpu_count())
print("CPUs used = ", num_procs)

# make needed folders
for media in medias:
    media_path = "./two_dim_outputs/media"+str(media)+"/"
    if(os.path.exists(media_path)):
        shutil.rmtree(media_path)
    os.mkdir(media_path)

    for up in ups:
        down = 1-up
        camps_path = media_path + str(up)+"_"+str(down)+"/"
        os.mkdir(camps_path)
        for method in methods:     
            method_path = camps_path + method+"/"
            os.mkdir(method_path)

arg_list = [[num_simulations, conc, domains, media, up, 1-up, method, 
            method+"_"+str(num_procs)+"_"+str(conc)+".csv", 
            "./two_dim_outputs/media"+str(media)+"/" + str(up)+"_"+str(1-up)+"/" + method+"/"] 
            for conc in concs for method in methods for up in ups for media in medias]

pool = mp.Pool(num_procs)
start = time.time()
pool.map(simulate, arg_list)
pool.close()
pool.join()
end = time.time()
print("Time taken = ", end-start)
    
