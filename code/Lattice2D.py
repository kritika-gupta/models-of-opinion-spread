import numpy as np
from itertools import chain

class Lattice:

    def __init__(self, N, conc):
        self.matrix_size = N
        self.spin = np.random.choice([1, -1], p = [conc, 1-conc], size = (N, N))
        self.decision_times = []
        self.last_changed = np.zeros((N, N))
        self.time = 0
        self.vert = lambda x,y : [((x,y),(x%N, (y-1)%N)), ((x,y),(x%N, (y+2)%N))]
        self.hori = lambda x,y : [((x,y),((x-1)%N, y%N)), ((x,y),((x+2)%N, y%N))]
        
        
    def stauffer_2d_step(self, media, up, down):
        states = [np.copy(self.spin)]
        N = self.matrix_size
        for spin_update in range(self.matrix_size*self.matrix_size):
            
            # select random site 
            x = np.random.choice(np.arange(0, self.matrix_size-1))
            y = np.random.choice(np.arange(0, self.matrix_size-1))

            rows = np.arange(x-1, x+3)%self.matrix_size
            cols = np.arange(y-1, y+3)%self.matrix_size
            M = self.spin[np.ix_(rows, cols)] # mini matrix of 4x4
            array_list = [M[1, :], M[2, :], M[:, 1], M[:, 2]]
            old_spins = np.copy(self.spin)

            small_m = M[np.ix_([1, 2], [1, 2])] # mini matrix of 2x2
            if(small_m[0,0]==small_m[0,1]==small_m[1,0]==small_m[1,1]):
                for array in array_list:
                    assert(len(array)==4)
                    array[0] = array[1]
                    array[3] = array[1]
                       
            # effect of media on neighboring 8 positions
            else:
                for array in array_list:
                    assert(len(array)==4)
                    array[0] = np.random.choice([1, -1, array[0]], p = [media*up, media*down, 1-media])
                    array[3] = np.random.choice([1, -1, array[3]], p = [media*up, media*down, 1-media])

            self.spin[np.ix_(rows, cols)] = M
            changed = self.spin != old_spins
            self.decision_times.append(list(self.time - self.last_changed[changed]))
            self.last_changed[changed] = self.time
            self.time = self.time + 1
        return changed, states
        
            
    def stauffer_2d_step_modified(self, method_version, media, up, down):
        N = self.matrix_size
        # states = [np.copy(self.spin)]
        for spin_update in range(self.matrix_size*self.matrix_size):            
            # select random site 
            x = np.random.choice(np.arange(0, self.matrix_size-1))
            y = np.random.choice(np.arange(0, self.matrix_size-1))

            rows = np.arange(x-1, x+3)%self.matrix_size
            cols = np.arange(y-1, y+3)%self.matrix_size
            M = self.spin[np.ix_(rows, cols)]
            array_list = [M[1, :], M[2, :], M[:, 1], M[:, 2]]
            old_spins = np.copy(self.spin)

            small_m = M[np.ix_([1, 2], [1, 2])]
            if(small_m[0,0]==small_m[0,1]==small_m[1,0]==small_m[1,1]):
                for array in array_list:
                    assert(len(array)==4)
                    array[0] = array[1]
                    array[3] = array[1]  

            else:
                for array in array_list:
                    assert(len(array)==4)
                    if(method_version==0):
                        # modified : take neighbor's neighbor's position
                        array[0] = np.random.choice([1, -1, array[2]], p = [media*up, media*down, 1-media])
                        array[3] = np.random.choice([1, -1, array[1]], p = [media*up, media*down, 1-media])
                    else:
                        # modified : take neighbor's position
                        array[0] = np.random.choice([1, -1, array[1]], p = [media*up, media*down, 1-media])
                        array[3] = np.random.choice([1, -1, array[2]], p = [media*up, media*down, 1-media])

            self.spin[np.ix_(rows, cols)] = M
            changed = self.spin != old_spins
            self.decision_times.append(list(self.time - self.last_changed[changed]))
            self.last_changed[changed] = self.time
            self.time = self.time + 1
        return changed

    # Sweep over lattice until steady state is reached
    def metropolis(self, media = 0, up = 1, down = 0, method = "default", display = False):
        
        self.time = 0
        tmax = 500
        epsilon = 0.001
        # time_of_last_change = 0
        threshold = self.matrix_size
        total = self.matrix_size*self.matrix_size
        states = [np.copy(self.spin)]

        while(self.time < tmax*total):

            if(method == "default"):
                changed = self.stauffer_2d_step(media, up, down)
            elif(method == "modified1"):
                 changed = self.stauffer_2d_step_modified(0, media, up, down) 
            elif(method == "modified2"):
                 changed = self.stauffer_2d_step_modified(1, media, up, down) 
            m = self.magnetization()
            staggered_m =  self.staggered_magnetization()
            states.append(np.copy(self.spin))

            # steady state consensus --> exit
            if(abs(m) == 1 or 1-abs(m) <= epsilon):
                break
            # steady state stalemate
            elif(staggered_m == 1):
                break

        return m, self.time, self.decision_times, states
            
    def magnetization(self):
        return np.mean(self.spin)

    def staggered_magnetization(self):
        # returns 1 for stalemate
        mask = np.zeros((self.matrix_size, self.matrix_size))
        mask[0::2, 0::2] = 1
        mask[1::2, 1::2] = 1
        M_plus = np.mean(self.spin[np.where(mask==1)])
        M_minus = np.mean(self.spin[np.where(mask==0)])
        return abs(0.5*(M_plus - M_minus))


                
    def display(self):
        fig, ax = plt.subplots(figsize=(3,3))
        img = ax.imshow(self.spin, cmap='Greys')
        plt.colorbar(img)
        plt.show()
    
