import numpy as np 
import re
from itertools import combinations

#Read input
with open('Day12/input.txt') as f:
    content = [x.strip() for x in f.readlines()]  

moon_names = ['Io', 'Europa', 'Ganymede', 'Callisto']

class moon:
    
    '''
    This object is a moon with a name, position and velocity.
    '''

    def __init__(self, name, input_position):

        self.name = name
        self.pos = self.extract_vector(input_position) #Position
        self.vel = np.array([0,0,0]) #Velocity

    def extract_vector(self, input_str):

        '''
        Converts input string format '<x=num1, y=num2, z=num3>' to a numpy array containing [num1, num2, num3]
        '''

        nums = re.search('<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', input_str)
        return np.array([int(nums[1]), int(nums[2]), int(nums[3])])

    def update_vel(self, input_vector):

        self.vel += np.array(input_vector)

    def apply_vel(self):

        self.pos += self.vel

    def total_energy(self):

        pot_energy = np.sum(np.abs(self.pos))
        kin_energy = np.sum(np.abs(self.vel))

        return pot_energy*kin_energy



def apply_gravity(moon1, moon2):

    '''
    Apply gravity that works between two moons.
    '''

    moon1_change = []
    moon2_change = []

    #For (x1, x2), (y1, y2), (z1, z2) move coordinates closer together.

    for p1, p2 in zip(moon1.pos, moon2.pos):

        if p1 > p2:
            moon1_change.append(-1)
            moon2_change.append(1)
        elif p1 < p2:
            moon1_change.append(1)
            moon2_change.append(-1)
        else:
            moon1_change.append(0)
            moon2_change.append(0)

    moon1.update_vel(moon1_change)
    moon2.update_vel(moon2_change)

    return None
    



def simulate(n_steps, verbose=False):

    '''
    Simulate n_steps timesteps. In each timestep gravity is applied for each moon pair. Subsequently velocity is applied to each moon.
    '''

    #Intiate moon objects
    moons = {}
    for mn, c in zip(moon_names, content):
        moons[mn] = moon(mn, c)

    #All possible pairs
    moon_pairs = list(combinations(moons.keys(), 2))

    for n in range(n_steps):

        for moon_pair in moon_pairs:

            apply_gravity(moons[moon_pair[0]], moons[moon_pair[1]])

        for p, mn in moons.items():

            mn.apply_vel()
        
        if verbose:
            print('Timestep: {}'.format(n+1))
            print('Moon positions and velocities:')
            for p in moons.keys():
                print(p,' ',moons[p].pos, moons[p].vel)

    total_energy_system = 0
    for p, mn in moons.items():

        total_energy_system += mn.total_energy()

    return total_energy_system

print('Total energy after 10 steps: {}'.format(simulate(10, verbose=True)))
print('Total energy after 1000 steps: {}'.format(simulate(1000)))