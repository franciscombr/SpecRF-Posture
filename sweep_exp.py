from fieldfox_interface.FieldFox import FieldFox
from horn_sweep_actuation.python_client.StepperClient import StepperClient
import numpy as np
import pandas as pd
import time

import fieldfox_interface.dataprocessing as dataprocessing

my_ffox = FieldFox()
my_ffox.connect_to_vna('USB0::0x2A8D::0x5C18::MY57271394::0::INSTR')
my_ffox.set_vna_to_network_analyzer_mode()
my_ffox.set_vna_measurement_averages(1)

my_stepper = StepperClient('/dev/ttyUSB0',115200)
freqs = my_ffox.get_vna_sweep_range()

#angles = [26.57, 27.9 , 29.36, 30.96, 32.74, 34.7 , 36.87, 39.29, 41.99, 45. , 51.34, 57.53, 63.43, 68.96, 74.05, 78.69, 82.87, 86.63, 90. , 93.01]
angles = [ 0., 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 11., 13., 15., 17., 19., 21., 24., 27., 31., 34., 38.,  41., 45., 48., 51.]
angles = np.array(angles)
angles *=1.8
my_stepper.set_pos(0)
input("Set horn to left position. Press Enter to continue...")
pose = input("Pose: ")
test_scenario = "dataset"
n_sweeps = int(input("Number of sweeps: "))
running_start = int(input("Intermediate starting iteration: "))
for n in range(running_start,n_sweeps):  
    my_stepper.set_pos(0)
    meas = []
    for angle in angles:
        if not my_stepper.set_pos(angle):
            break
        meas.append(np.reshape(my_ffox.take_raw_measurement(),(-1,2)))
        time.sleep(1)

    file_dir = f"../data/{test_scenario}/{pose}_{n}.csv"
    dataprocessing.raw_meas_to_csv(meas,freqs,angles,file_dir)

    #acrescentar flag para pause a cada 10 sweep
    
    if n>0 and n%30==0 and n!=n_sweeps-1:
        input("Pause for subject rest. Press enter to continue...")

