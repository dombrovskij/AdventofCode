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
        self.pos = {}
        self.vel = {}
        for p, t in zip(['x','y','z'], self.extract_vector(input_position)):
            
            self.pos[p] = t #Position
            self.vel[p] = 0 #Velocity

    def extract_vector(self, input_str):

        '''
        Converts input string format '<x=num1, y=num2, z=num3>' to a numpy array containing [num1, num2, num3]
        '''

        nums = re.search('<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', input_str)
        return np.array([int(nums[1]), int(nums[2]), int(nums[3])])

    def update_vel(self, value, ax):

        self.vel[ax] += value

    def apply_vel(self, ax):

        self.pos[ax] += self.vel[ax]

def apply_gravity(moon1, moon2, ax):

    '''
    Apply gravity that works between two moons.
    '''

    p1 = moon1.pos[ax]
    p2 = moon2.pos[ax]

    if p1 > p2:
        moon1_change = -1
        moon2_change = 1 
    elif p1 < p2:
        moon1_change = 1
        moon2_change = -1
    else:
        moon1_change = 0
        moon2_change = 0

    moon1.update_vel(moon1_change, ax)
    moon2.update_vel(moon2_change, ax)

def find_period(ax, verbose=False):

    '''
    Simulate n_steps timesteps. In each timestep gravity is applied for each moon pair. Subsequently velocity is applied to each moon.
    '''

    #Intiate moon objects
    moons = {}
    for mn, c in zip(moon_names, content):
        moons[mn] = moon(mn, c)

    #All possible pairs
    moon_pairs = list(combinations(moons.keys(), 2))

    ax_vector_cur = [moons[m].pos[ax] for m in moon_names]
    ax_vector_new = []

    count_steps = 0

    while ax_vector_cur != ax_vector_new:
        
        count_steps += 1

        for moon_pair in moon_pairs:

            apply_gravity(moons[moon_pair[0]], moons[moon_pair[1]], ax)

        for p, mn in moons.items():

            mn.apply_vel(ax)
        
        if verbose:
            print('Timestep: {}'.format(n+1))
            print('Moon positions and velocities:')
            for p in moons.keys():
                print(p,' ',moons[p].pos, moons[p].vel)

        ax_vector_new = [moons[m].pos[ax] for m in moon_names]

    print('Start vector ax {}: {}'.format(ax, ax_vector_cur))
    print('Repeated after: {}'.format(count_steps))
    return count_steps+1

period_x = find_period('x')
period_y = find_period('y')
period_z = find_period('z')

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

print('Answer part 2: {}'.format(lcm(period_x, lcm(period_y, period_z))))