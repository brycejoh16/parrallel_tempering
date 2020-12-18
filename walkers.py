

import ray
import numpy as np
import energy_modules as em


@ray.remote
class Walker():
    def __init__(self,S:np.ndarray,beta:float,J:float,E0:float):
        '''
        this is the walker class, this will make a Monte Carlo Random Walk.
        :param S: spin states N x N matrix
        :param beta: value of the temperature beta = 1/(k_b * T)
        :param J:  antiferromagnetic type interaction between spins at points,  right now just a constant
        :param E0 : the intial energy given J and the spin states
        '''
        self.beta=[beta]
        self.S=[S]
        self.J=J
        self.N=S.shape[0]
        self.E=[E0]
        self.beta_placeholder=beta


    def walk(self,step:int)->(float,float):
        '''
        a monte carlo walk where steps are accepted based off of the metropolis sampling condition
        :param step : int  , number of steps to take in the walk
        :return: (beta: float,  energy : float)
        '''

        for _ in np.arange(step):
            s = self.S[-1]
            mutate_i = np.random.randint(0, self.N)
            mutate_j = np.random.randint(0, self.N)

            # make a proposed mutation, a single flip
            if s[mutate_i, mutate_j] == -1:
                s_ij = 1
            else:
                s_ij = -1


            # propose a new spin configuration
            proposed_S = s.copy()
            proposed_S[mutate_i, mutate_j] = s_ij

            E_proposed = em.energy(proposed_S.copy(),self.J, self.N)
            # keep accepting mutations based off of metropolis condition. this could be wrong.
            # print(self.beta_placeholder)
            if em.metropolis(self.E[-1], E_proposed,self.beta_placeholder):
                self.E.append(E_proposed)
                self.S.append(proposed_S)
                self.beta.append(self.beta_placeholder)
            else:
                self.E.append(self.E[-1])
                self.S.append(s)
                self.beta.append(self.beta_placeholder)

        return self.beta[-1] , self.E[-1]

    def update_temps(self,new_t:float):
        'this updates the current temperature, to a new temperature'
        self.beta_placeholder=new_t
        # print(self.beta_placeholder)

    def _calculate_energy(self)->float:
        'internal function to calculate energy'
        return em.energy(self.S.copy(), self.J, self.N)
    def return_all_values(self)->(list,list,list):
        '''
        returns all the saved parameters from the walker
        :return: (beta: the temperatures in the run , S: all of the spin states taken in the run, E: all energy values taken)
        '''
        return self.beta,self.S,self.E

def _unit_tests_walker():
    'this is a unit test for the walker class in 2D'
    N=4
    S0 = np.random.randint(0, 2, (N, N))
    S0[S0==0]=-1
    beta=0.3
    J=0.4
    E0=em.energy(S0.copy(),J,N)

    walker=Walker(S0,beta,J,E0)

    (out)=walker.walk(step=5)

if __name__=='__main__':
    _unit_tests_walker()






