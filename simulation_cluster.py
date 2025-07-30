import sys
import numpy as np
import os
from scipy.interpolate import interp1d

def gillespie_seir(N, beta_func, delta, gamma, mu, initial_infected, initial_exposed, max_time):
    # Initial conditions
    S = N - initial_infected - initial_exposed
    E = initial_exposed
    I = initial_infected
    R = 0
    
    # Arrays to store results
    times = np.zeros(300000)
    susceptible = np.zeros(300000)
    susceptible[0] = S
    exposed = np.zeros(300000)
    exposed[0] = E
    infected = np.zeros(300000)
    infected[0] = I
    recovered = np.zeros(300000)
    recovered[0] = R
    
    t = 0
    ind = 0
    beta = beta_func(t)
    while t < max_time:
        # Calculate rates (transmission, symptom onset, recovery, birth and deaths)
        beta = beta_func(t)
        lambda_SE = beta * S * I / N
        lambda_EI = delta * E
        lambda_IR = gamma * I
        lambda_birth = mu * N
        lambda_death_S = mu * S
        lambda_death_E = mu * E
        lambda_death_I = mu * I
        lambda_death_R = mu * R
        total_rate = (lambda_SE + lambda_EI + lambda_IR + lambda_birth +
                      lambda_death_S + lambda_death_E + lambda_death_I + lambda_death_R)
        
        if total_rate == 0:
            break
        
        # Calculate time step
        dt = np.random.exponential(1 / total_rate)
        t += dt
        ind += 1
        # Determine which event occurs
        rand = np.random.rand() * total_rate
        
        # Work out which event had happened
        if rand < lambda_SE:
            S -= 1
            E += 1
        elif rand < lambda_SE + lambda_EI:
            E -= 1
            I += 1
        elif rand < lambda_SE + lambda_EI + lambda_IR:
            I -= 1
            R += 1
        elif rand < lambda_SE + lambda_EI + lambda_IR + lambda_birth:
            S += 1
        else:
            rand_death = rand - (lambda_SE + lambda_EI + lambda_IR + lambda_birth)
            if rand_death < lambda_death_S:
                S -= 1
            elif rand_death < lambda_death_S + lambda_death_E:
                E -= 1
            elif rand_death < lambda_death_S + lambda_death_E + lambda_death_I:
                I -= 1
            else:
                R -= 1
        
        # Append results
        times[ind] = t
        susceptible[ind] = S
        exposed[ind] = E
        infected[ind] = I
        recovered[ind] = R
    
    return times[:ind+1], susceptible[:ind+1], exposed[:ind+1], infected[:ind+1], recovered[:ind+1]

identity = sys.argv[2]
num = int(sys.argv[1])
script_dir = os.path.dirname(__file__)

# Constant Parameters
N = 1e5  # Total population
delta = 1/5 # Symptom onset rate (1/delta is the infectious)
gamma = 1/10  # Recovery rate (1/gamma is the infectious period)
R_0 = 4 # Basic reproduction number estimated for alpha variant
mu = 0.00003424657  # Birth and death rate
initial_infected = 10
initial_exposed = 0
max_time = 200
beta_0 = 0.40020550287655116

# Transmission functions
betat = lambda x: 0.4002
p = (beta_0-0.05)/100
tau = 30
def beta_increasing_t(t):
    betat = 0.05+p*(t-tau) if t > tau else 0.05
    if betat >= beta_0:
        return beta_0
    else:
        return betat
def beta_decreasing_t(t):
    betat = beta_0-p*(t-tau) if t > tau else beta_0
    if betat <= 0.05:
        return 0.05
    else:
        return betat
def beta_step_t(t):
    return beta_0 if t<tau else 0.05

# Setup sims and output files
if identity == 'constant':
    results_dir = os.path.join(script_dir,'constant')
    beta_t = betat
    def sim():
        return gillespie_seir(N, betat, delta, gamma, mu, initial_infected, initial_exposed, max_time)
elif identity == 'increasing':
    results_dir = os.path.join(script_dir,'increasing')
    beta_t = beta_increasing_t
    def sim():
        return gillespie_seir(N, beta_increasing_t, delta, gamma, mu, initial_infected, initial_exposed, max_time)
elif identity == 'decreasing':
    results_dir = os.path.join(script_dir,'decreasing')
    beta_t = beta_decreasing_t
    def sim():
        return gillespie_seir(N, beta_decreasing_t, delta, gamma, mu, initial_infected, initial_exposed, max_time)
else:
    results_dir = os.path.join(script_dir,'step')
    beta_t = beta_step_t
    def sim():
        return gillespie_seir(N, beta_step_t, delta, gamma, mu, initial_infected, initial_exposed, max_time)

# Run number of sims
days = np.arange(0,201,1)
times = np.arange(0,200.1,0.1)
num_sims = 100
Is = np.zeros((num_sims,len(days)))
Rs = np.zeros((num_sims,len(times)))
for i in range(100):
    res = sim()
    Is[i,:] = interp1d(res[0],res[3],kind='previous',fill_value='extrapolate')(days)/N
    Rs[i,:]= np.interp(times,res[0],res[1])/N * delta/((delta+mu)*(gamma+mu)) * np.array([beta_t(t) for t in times])
i = np.random.randint(100)
fpath_I = os.path.join(results_dir,f'I_{num}_{i}.npy')
fpath_R = os.path.join(results_dir,f'R_{num}_{i}.npy')
np.save(fpath_I,Is)
np.save(fpath_R,Rs)
