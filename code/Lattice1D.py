import numpy as np
import multiprocessing as mp

class Lattice:

    def __init__(self, matrix_size, conc):
        self.matrix_size = matrix_size
        self.spin = np.random.choice([1, -1], p = [conc, 1-conc], size = matrix_size).reshape((matrix_size, 1))
        self.decision_times = []
        self.last_changed = np.zeros((self.matrix_size, 1))
        self.time = 0
        
    def do_change(self, pos, spin_value):
        if(self.spin[pos]==spin_value):
            return False
        self.spin[pos] = spin_value
        self.decision_times.append(int(self.time - self.last_changed[pos]))
        self.last_changed[pos] = self.time
        return True
        
    def snazjd_1d_step(self, media, up=1, down=0):
        changed = False
        N = self.matrix_size
        for spin_update in range(N):
            # select a random site
            i = np.random.choice(np.arange(1, self.matrix_size-2)) 
            old_spins = np.copy(self.spin)
            if self.spin[i]*self.spin[i+1] == 1: # pair agrees
                    self.spin[i-1] = self.spin[i]
                    self.spin[i+2] = self.spin[i+1]
                    # changed = (self.do_change(i-1, self.spin[i]) or self.do_change(i+2, self.spin[i]))

            elif self.spin[i]*self.spin[i+1] == -1: # pair disagrees
                    self.spin[i-1] = np.random.choice([1, -1, self.spin[i+1]], p = [media*up, media*down, 1-media])
                    self.spin[i+2] = np.random.choice([1, -1, self.spin[i]], p = [media*up, media*down, 1-media])
                    # changed = (self.do_change(i-1, next_spin_1) or self.do_change(i+2, next_spin_2))
            changed = self.spin!=old_spins  # positions where change occured
            self.decision_times.append(list(self.time - self.last_changed[changed]))
            self.last_changed[changed] = self.time
            
        
    def magnetization(self):
        return (1/(self.matrix_size))*np.sum(self.spin)

    def staggered_magnetization(self):
        # returns 1 for stalemate
        mask = np.zeros((self.matrix_size, ))
        mask[0::2] = 1
        M_plus = np.mean(self.spin[np.where(mask==1)])
        M_minus = np.mean(self.spin[np.where(mask==0)])
        return abs((M_plus - M_minus))

    # Sweep over lattice until steady state is reached
    def metropolis(self, media = 0, up = 1, down = 0, display = False):
        self.time = 0
        tmax = 500
        while(self.time < tmax):
            
            self.snazjd_1d_step(media)
            m = self.magnetization()
            if(self.staggered_magnetization == 1 or abs(m) == 1):
                break
            self.time = self.time + 1
                
        return m, self.time, self.decision_times
            
    def display(self):
#         fig, ax = plt.subplots(figsize=(3,3))
        plt.matshow(self.spin.reshape(1, self.matrix_size))
#         plt.title("sweep = " + str(sweep_number))
        plt.show()
#         print(self.spin.reshape(1, self.matrix_size))
    
