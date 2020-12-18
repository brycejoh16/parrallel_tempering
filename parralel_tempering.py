
import numpy as np
# iniultt J values to random values that can be guassian distributed.
import os
import ray
from walkers import Walker
import energy_modules as em
import data_modules as dm
import plot_modules as pm
import time
def driver(inputs:dict):
    # first initilize the parralel library to use
    if ray.is_initialized():
        ray.shutdown()
    ray.init()

    # make the directory to save data
    directory = dm.make_directory(inputs)
    os.system('mkdir %s'%directory)
    # initilize the inputs to parralel tempering
    S0, N, Beta = dm.initilize_inputs(inputs)
    # initlize all the walkers

    E0= em.energy(S0.copy(),inputs['J'],inputs['N'])

    walkers=[Walker.remote(S0,beta,inputs['J'],E0) for beta in Beta]


    # for each loop of parrelel tempering
    T=[]
    for j in np.arange(inputs['num_loops']):
        # walk the walkers
        start=time.time()
        out=ray.get([w.walk.remote(inputs['num_steps']) for w in walkers])
        T.append(time.time()-start)
        # out = (temperature,  energy)


        # just pick one temperature to look for a switch .
        o2s=np.random.randint(0,len(walkers))


        # then decide if to should switch up or down
        if o2s==0 :
            # if we are the first temperature , have to go up
            ud=1
        elif o2s==len(walkers)-1:
            # if we are the last have to go down
            ud=len(walkers)-2
        else:
            # if we are in a middle temperature can pick randomly up or down
            ud=np.random.choice([-1,1]) + o2s

        # if metropolis indicates we should switch temperatures, then switch.
        if em.metropolis_temperature(*out[o2s],*out[ud]):
            # swap the temperatures of the two workers
            ray.get(walkers[o2s].update_temps.remote(out[ud][0]))
            ray.get(walkers[ud].update_temps.remote(out[o2s][0]))
        else:
            pass

        # output indicator
        if j % inputs['loop2save']==0:
            print('loop :%i,Average TIME per walk: %0.2f'%(j,np.mean(T)))


    # get the results from all the walkers
    res=ray.get([w.return_all_values.remote() for w in walkers])

    # analyzing the results based off pdf values
    pm.plot_temperature_density(inputs,res)
    pm.plot_temperature_transition(inputs,res)


    # shutdown the parralel service
    ray.shutdown()

    return


if __name__=='__main__':
    # right now just doing a constant value of J. that will have to change later for obvious reasons
    # have flag for random or gaussian distributed for J ...
    inputs={'beta_max': 1.3,
            'beta_min': 0.3,
            'num_walkers': 8, # make the number of
            'J': 0.4,
            'N':20,
            'seed': 3329239, # for reproducibility
            'dim': 2,
            'num_steps': 100,
            'num_loops': 1000,
            'loop2save': 100,
    }
    driver(inputs)