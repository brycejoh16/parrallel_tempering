import numpy as np
import pickle



def make_directory(inputs:dict):
    title=''
    for key in inputs.keys():
        value=inputs[key]
        title+=str(key)+'_%0.2f_'%value
    return './tempering_results/%s'%title

def initilize_inputs(inputs: dict):
    if 'seed' in inputs.keys():
        np.random.seed(inputs['seed'])
    N = inputs['N']
    if inputs['dim'] == 1:
        S0 = np.random.randint(0, 2, N)
    elif inputs['dim'] == 2:
        S0 = np.random.randint(0, 2, (N, N))
    elif inputs['dim'] == 3:
        S0 = np.random.randint(0, 2, (N, N, N))
    else:
        raise ValueError('invalid dimension')

    S0[S0 == 0] = -1
    step_size=(inputs['beta_max']-inputs['beta_min'])/inputs['num_walkers']
    beta=np.arange(0,inputs['num_walkers']+1,1)*step_size  + inputs['beta_min']

    # save the input parameters for reproducibility
    save_inputs(inputs)

    return S0,N,beta

def save_inputs(inputs:dict):
    directory=make_directory(inputs)
    with open(directory+'/inputs.pkl', 'wb') as handle:
        pickle.dump(inputs, handle, protocol=pickle.HIGHEST_PROTOCOL)