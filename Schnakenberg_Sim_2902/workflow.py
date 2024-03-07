import sim
import vis
import numpy as np
import time


def get_params(filename):
    import ast
    
    folderpath = "Parameters/"
    
    filepath = folderpath + filename + ".txt"

    file_contents = open(filepath, "r").read()

    params = ast.literal_eval(file_contents)
    
    return params


class Simulation:
    """
    Requires the following libraries:
    * sim
    * numpy as np
    * time
    
    """
    

    def __init__(self, filename):
        
        """
        k2 is the birth rate for species A
        k4 is the birth rate for species B
        k3 is the death rate for species A
        k1 is the reaction rate for "2A + B -> 3A" 

        """
        
        self.filename = filename
        self.params = get_params(self.filename)
        
        h = self.params['h']

        self.params['d_A_p'] = self.params['d_A'] * (2*h**2)
        self.params['d_B'] = self.params['d_A'] * self.params['dr']
        self.params['d_B_p'] = self.params['d_B'] * (2*h**2)

        self.params['k2'] = self.params['mu'] / h**3
        self.params['k4'] = self.params['beta'] / h**3
        self.params['k3'] = self.params['alpha']
        self.params['k1'] = self.params['kappa'] * h**6
        
        
    def go(self):
        self.run_movie()
        self.save_movie()
        self.report()

    def run_movie(self):
        arg_dict = {key: self.params[key] for key in 
                    ("N_t", "m", "n", "A_init", "B_init")}
        param_dict = {key: self.params[key] for key in 
                      ("tau", "mu", "beta", "alpha", "kappa", "d_A", "d_B")}
        self.X_A, self.X_B = sim.initialize_movie(**arg_dict)
        
        start_time = time.time()
        for t in np.arange(self.params['N_t'] - 1):
            
            if t % 100_000 == 0:
                print(t)

            self.X_A[t+1], self.X_B[t+1] = sim.calculate_picture(**param_dict, M_A=self.X_A[t], M_B=self.X_B[t])
        
        end_time = time.time()
        self.runtime = end_time - start_time
        
            
    def save_movie(self):
        datapath = "Data/"
        np.save(datapath + self.filename + "-X_A" + ".npy", self.X_A)
        np.save(datapath + self.filename + "-X_B" + ".npy", self.X_B)
    

    def report(self):
        print()
        print('\nFilename:')
        print(self.filename)
        print('\nParams:')
        print(self.params)
        print('\nRuntime:')
        print(self.runtime)


    def visualize(self, every=2_000, window_A=4, max_value_A=1_000, window_B=2, max_value_B=500):
        vis.create_all_gifs(self.X_A, self.filename, kind="X_A", every=every, window=window_A, max_value=max_value_A)
        vis.create_all_gifs(self.X_B, self.filename, kind="X_B", every=every, window=window_B, max_value=max_value_B)

