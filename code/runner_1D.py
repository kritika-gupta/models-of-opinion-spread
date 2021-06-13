import numpy as np 
import csv
import time
from Lattice1D import *
import multiprocessing as mp
import json
import os
import sys
import itertools
import shutil

def simulate(params):
    [num_simulations, conc, domains, media_prob, up_prob, down_prob, filename, path] = params

    with open(path+filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(['media','domain','conc','sim','magnetization','relaxation', 'decision'])
        
    for key in list(itertools.product(domains)):
        L = key[0]

        for i in (range(num_simulations)):
            lattice = Lattice(L, conc)
            m, rel_time, dec_times = lattice.metropolis(media = media_prob, up = up_prob, down = down_prob)
            dec_times = [x for sublist in dec_times for x in sublist]
            c = []
            temp = np.unique(dec_times, return_counts=True)
            c.append(list(temp[0]*1.0))
            c.append(list(temp[1]*1.0))    
            with open(path+filename, 'a') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow([media_prob, L, conc, i, m, rel_time, json.dumps(c)])


num_procs = mp.cpu_count()

choice = int(input("Enter 0 to use default parameter values, enter 1 to input the values.\n"))
if(choice==1):
    medias = [float(x) for x in (input("Enter list of media values\n").split())]

    concs_input = tuple(float(x) for x in input("Enter range of initial upward concentrations : start end steps\n").split())
    concs = np.round(np.linspace(concs_input[0], concs_input[1], concs_input[2]), 3)

    num_simulations = int(input("Enter number of simulations\n"))

    ups = [float(x) for x in input("Enter list of ratios of initial upward spins (eg. 1 0.75 0.5)\n").split()]

else:
    medias = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2]
    concs = np.round(np.linspace(0, 1, 25), 3)
    num_simulations = 300
    ups = [1, 0.75, 0.5]

domains = [64]
methods = ['default']

print("domains =", domains)
print("medias =", medias)
print("concentrations =", concs)
print("simulation runs =", num_simulations)
print("upward ratios =", ups)
print("methods =", methods)
print("CPUs available = ", mp.cpu_count())
print("CPUs used = ", num_procs)

output_path = "./one_dim_outputs/"
# make needed folders
for media in medias:
    media_path = output_path + "media"+str(media)+"/"
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

arg_list = [[num_simulations, conc, domains, media, up, 1-up,
            method+"_"+str(num_procs)+"_"+str(conc)+".csv", 
            output_path + "media"+str(media)+"/" + str(up)+"_"+str(1-up)+"/" + method+"/"] 
            for conc in concs for up in ups for method in methods for media in medias]

start = time.time()
pool = mp.Pool(num_procs)
pool.map(simulate, arg_list)
pool.close()
pool.join()
end = time.time()
print("Time taken =", end-start)


    
