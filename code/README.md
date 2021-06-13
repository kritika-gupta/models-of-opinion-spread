0. Files in this directory

        - Lattice_1D.py (Class file for one dimensional Lattice object, including methods for Sznajd model simulations)
        - Lattice_2D.py (Class file for two dimensional Lattice object, including methods for Sznajd model simulations)
        - runner_1D.py (Script to set parameters, run 1-D simulations and save output in .csv format)
        - runner_2D.py (Script to set parameters, run 2-D simulations and save output in .csv format)
        
1. General

        1.1 Maximum number of steps (i.e., maximum time for simulation) can be changed by changing variable "tmax" in the Lattice class files for each case. The current value is 500, i.e., the simulations will run for 500*lattice_dimensions times.
        1.2 Number of cores used for simulations are equal to the available cores on the CPU by default. This value can be changed in the runner scripts for each case by changing the variable "num_procs".


2. For 1-D simulation

        2.1 Create folder "./one_dim_outputs/" in current directory to save output csv files.
        2.2 Run "python3 runner_1D.py"
        2.3 Enter "0" for default parameters mentioned in "runner_1D.py" file
        2.4 Enter "1" to specify parameters
        2.5 There is only one method for this model - the default Sznajd model (named as "default")



3. For 2-D simulation

        3.1 Create folder "./two_dim_outputs/" in current directory to save output csv files.
        3.2 Run "python3 runner_2D.py"
        3.3 Enter "0" for default parameters mentioned in "runner_2D.py" file
        3.4 Enter "1" to specify parameters
        3.5 There are 3 possible methods for this model
                - "default" (original model with Stauffer's rules + take media's opinion with probability p)
                - "modified1" (with probably 1-p , take neighbour's neighbour's opinion)
                - "modified2" (with probably 1-p , take neighbour's opinion)


4. Output folder hierarchy

        - x_dim_outputs
                - one folder for each media value
                        - one folder for each campaign split
                                - one folder for each method of simulation the model
                                        - one .csv file for each initial upward spin concentration

5. Plot graphs

        4.1 Run the Jupyter Notebook "plots.ipynb" to run code that generates relevant figures. Minor modifications may be needed to generate different desired figures, rename axes and titles.

