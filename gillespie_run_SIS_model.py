# gillespie run, SIS no birth, deaths or external

from funcs_sim import gillespieSISExt, gillespieSISFix, gillespieSteps, gillespieSISFixCHANGING
from multiprocessing import Pool
import sys
import numpy as np 
import pandas as pd

# Read command line, and input parameters
pyfile = sys.argv[0]
populationN = int(sys.argv[1])
beta0 = float(sys.argv[2])
gamma = float(sys.argv[3])
simType = sys.argv[4]
realisations = int(sys.argv[5])
print("parameters (beta, gamma): ", beta0, gamma)

# Load other parameters
pRate =1/(500)
changeTime = 500
burnTime = 300
print("Initial conditions:", (gamma/beta0)*populationN, (1-gamma/beta0)*populationN)

def para(gillespie_algorithm):
    gill = gillespie_algorithm(initial = [(gamma/beta0)*populationN,
                                           (1-gamma/beta0)*populationN],
                                beta0=beta0,
                                p=pRate,
                                gamma=gamma,
                                max_time=changeTime,
                                burntime=burnTime)
    
    # make sure output is discrete increases/decreases (not continuous)
    steps = gillespieSteps(gillespieOuput=gill, 
                           T = changeTime, 
                           BT = burnTime)
    
    #linear interpolation
    inter_t = np.arange(0, round(max(steps[0]))+1, 0.1) 
    inter_i = np.interp(inter_t, steps[0],steps[2])
    inter_s = np.interp(inter_t, steps[0], steps[1])
    inter_i = inter_i[:(changeTime+burnTime)*10]
    inter_s = inter_s[:(changeTime+burnTime)*10]
    inter_NC = steps[3]
    return inter_i, inter_s, inter_NC


# embarrasingly parallel
print('parallel inputs:')
if simType == 'Ext':
    print('Extinction run')
    functionInput = gillespieSISExt
elif simType == 'Fix':
    print('Steady state run')
    functionInput = gillespieSISFix
elif simType =='FixChange':
    functionInput = gillespieSISFixCHANGING
else:
    print('incorrect simulation type inputted (argument 4), choose Ext or Fix or FixChange')

print('\n Starting parallel runs')
print('running ', realisations, ' realisations')

runs = [functionInput for i in range(realisations)]
num_threads = 12 # number of threads for parallelisation

with Pool(num_threads) as pool:
    results = pool.map(para, runs)

print('\n simulation runs complete')

print('\n saving...')
gamma_str = str(gamma).replace('.','_')

beta_str = str(beta0).replace('.','_')
np.save(simType+'_SIS_'+str(repeats)+'gamma'+gamma_str+ 'beta'+beta_str+'.npy', results)
