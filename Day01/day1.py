import numpy as np 

with open('input.txt') as f:
    content = f.readlines()

module_masses = [float(x.strip()) for x in content] 

def mass_to_fuel(mass):
    return int((mass/3.)) - 2

module_fuel = list(map(mass_to_fuel, module_masses))
print('Total fuel required for modules (answer part 1): {}'.format(np.sum(module_fuel)))

def fuel_req(fuel):
    
    #Calculates additional fuel needed for input fuel
    
    mtfs = []

    while fuel > 0:

        new_fuel = mass_to_fuel(fuel)
        mtfs.append(new_fuel)
        fuel = new_fuel
    
    return np.sum(mtfs)

additional_fuel = list(map(fuel_req, module_fuel))
print('Total fuel required for modules and fuel (answer part 2): {}'.format(np.sum(module_fuel) + np.sum(additional_fuel)))