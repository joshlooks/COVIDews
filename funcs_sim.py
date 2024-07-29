# function files

import numpy as np 


def gillespieSISExt(initial,
                    beta0,p, gamma, 
                    max_time,burntime):
    np.random.seed()
    T = []
    pop = []
    N = sum(initial)
    pop.append(initial)
    newCase = np.zeros(max_time+burntime+10)
    newCase[0] =0
    T.append(0)
    t = 0
    ind = 0
    state = np.zeros(shape= (2,2))
    rate = np.zeros(2)
    state[:,0] = [-1, 1]
    state[:,1] = [1, -1]
    R1 = beta0*(pop[ind][0])*(pop[ind][1])/N
    R2 = gamma*(pop[ind][1])
    rate[0] = R1
    rate[1] = R2
    while t <max_time+burntime:
        if t<burntime:
            betat = beta0
        else:
            betat = (1-p*(t-burntime))*beta0
        Rtotal = sum(rate)
        if Rtotal >0:
            delta_t= -np.log(np.random.uniform(0,1))/Rtotal

            P = np.random.uniform(0,1)*Rtotal
            t =t+ delta_t
            event = np.min(np.where(P<=np.cumsum(rate)))
            T.append(t)
            if event == 0:
                newCase[int(np.ceil(t))] +=1 
            pop.append(pop[ind]+state[:,event])
            ind=ind+1
            rate[0] = betat*(pop[ind][0])*(pop[ind][1])/N
            rate[1] = gamma*(pop[ind][1])
        else: 
            t = max_time+burntime
            T.append(t)
            pop.append(pop[ind])
    return T, np.array(pop), newCase

def gillespieSISFix(initial, 
                    beta0,p, gamma,
                    max_time,burntime, nu =0):
    np.random.seed()
    T = []
    pop = []
    N = sum(initial)
    pop.append(initial)
    newCase = np.zeros(max_time+burntime+10)
    T.append(0)
    t = 0
    newCase[0] = 0
    ind = 0
    allnewCase = [0]
    state = np.zeros(shape= (2,3))
    rate = np.zeros(3)
    state[:,0] = [-1, 1] # infection
    state[:,1] = [1, -1] #recovery
    state[:,2] = [-1, 1] #external
    R1 = beta0*(pop[ind][0])*(pop[ind][1])/N
    R2 = gamma*(pop[ind][1])
    R3 = nu*pop[ind][0]
    rate[0] = R1
    rate[1] = R2
    rate[2] = R3
    while t <max_time+burntime:
        Rtotal = sum(rate)
        if Rtotal >0:
            delta_t= -np.log(np.random.uniform(0,1))/Rtotal

            P = np.random.uniform(0,1)*Rtotal
            t =t+ delta_t
            event = np.min(np.where(P<=np.cumsum(rate)))
            T.append(t)
            if event == 0:
                newCase[int(np.ceil(t))] +=1
                allnewCase.append(1)
            else:
                allnewCase.append(0)
            pop.append(pop[ind]+state[:,event])
            ind=ind+1
            rate[0] = beta0*(pop[ind][0])*(pop[ind][1])/N
            rate[1] = gamma*(pop[ind][1])
            rate[2] = nu*pop[ind][0]
        else: 
            t = max_time+burntime
            T.append(t)
            pop.append(pop[ind])
            allnewCase.append(0)
    return T, np.array(pop), newCase,allnewCase

def gillespieSISFixCHANGING(initial, beta0,p, gamma, max_time,burntime):
    np.random.seed()
    T = []
    pop = []
    N = sum(initial)
    pop.append(initial)
    newCase = np.zeros(max_time+burntime+10)
    newCase[0] =0
    T.append(0)
    t = 0
    ind = 0
    state = np.zeros(shape= (2,2))
    rate = np.zeros(2)
    state[:,0] = [-1, 1]
    state[:,1] = [1, -1]
    beta0burn = 1
    R1 = beta0burn*(pop[ind][0])*(pop[ind][1])/N
    R2 = gamma*(pop[ind][1])
    rate[0] = R1
    rate[1] = R2

    while t <max_time+burntime:
        if t<burntime:
            betat = beta0burn
        elif t<( burntime + ((1-1.3*gamma)/p)):
            betat = (1-p*(t-burntime))*beta0
        else:
            #print(t)
            betat= 1.3*gamma
        Rtotal = sum(rate)
        if Rtotal >0:
            delta_t= -np.log(np.random.uniform(0,1))/Rtotal

            P = np.random.uniform(0,1)*Rtotal
            t =t+ delta_t
            event = np.min(np.where(P<=np.cumsum(rate)))
            T.append(t)
            if event == 0:
                newCase[int(np.ceil(t))] +=1 
            pop.append(pop[ind]+state[:,event])
            ind=ind+1
            rate[0] = betat*(pop[ind][0])*(pop[ind][1])/N
            rate[1] = gamma*(pop[ind][1])
        else: 
            t = max_time+burntime
            T.append(t)
            pop.append(pop[ind])
    return T, np.array(pop), newCase


def gillespieSteps(gillespieOuput, T, BT):
    t = gillespieOuput[0]
    s = gillespieOuput[1][:,0]
    i = gillespieOuput[1][:,1]
    NC = gillespieOuput[2][:T+BT]
    stept = []
    steps = []
    stepi = []
    stepNc = []
    for ind, x in enumerate(t):
        if ind<len(t)-1:
            steps.append((s[ind], s[ind]))
            stepi.append((i[ind], i[ind]))
            stept.append((t[ind], t[ind+1]))
        else:
            steps.append((s[ind], s[ind]))
            stepi.append((i[ind], i[ind]))
            stept.append((t[ind], t[ind]))
            

    steps = np.array(steps).flatten()
    stepi = np.array(stepi).flatten()
    stept = np.array(stept).flatten()
    return stept, steps, stepi,NC,stepNc
