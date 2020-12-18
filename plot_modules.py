import matplotlib.pyplot as plt
import numpy as np
import data_modules as dm
import scipy.stats
# put plot modules right here

def plot_temperature_density(inputs:dict,res:list):
    'this plots the interchanges of temperature for the workers'
        # plotting the temperature for the walkers
    Temp= [r[0] for r in res]
    for temp in Temp:
        plt.plot(np.arange(len(temp)),temp,'--')
    directory=dm.make_directory(inputs)
    plt.title('Temperature changes for walkers')
    plt.xlabel('Monte Carlo Step')
    plt.ylabel('beta')
    plt.savefig(directory+'/walkers_temp.png')
    plt.close()


def plot_temperature_transition(inputs:dict,res:list):
    'this plots the distribution function'
    # these need to be like N x 1 , for both
    Temp= np.concatenate([r[0] for r in res])
    Eng=np.concatenate([r[2] for r in res])

    for temp in np.unique(Temp):
        energies=Eng[Temp==temp]

        hist = np.histogram(energies, bins=100)
        hist_dist = scipy.stats.rv_histogram(hist)

        x=np.arange(-800,20,0.1)
        plt.plot(x,hist_dist.pdf(x),label='beta: %0.2f'%temp)

    directory = dm.make_directory(inputs)
    plt.legend()
    plt.title('Probability of energies for different temperatures [beta : 1/(k_b*T)]')
    plt.xlabel('Energy')
    plt.ylabel('P(E)')
    plt.savefig(directory +'/probability_of_energies.png')
    plt.close()









