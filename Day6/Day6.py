import numpy as np
from queue import Queue

with open('input.txt') as f:
    input_orbits = [x.split('\n')[0] for x in f.readlines()]

class Planet:
    
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        
    def add_child(self, planet):
        
        self.children.append(planet)

def create_tree(input_data):
    
    '''
    Creates planet-orbit tree from input data.
    
    Input:
        input_data (list): list of strings with each string in form of 'A)B', with A and B planets.
        
    Returns:
        all_planets (dict): dictionary containing every planet in the system as an object, each with parent (if any) and children (if any).
    '''

    all_planets = {}

    for p in input_data:

        p1 = p.split(')')[0]
        p2 = p.split(')')[1]

        if p1 not in all_planets: #If parent planet not yet in dictionary
            parent_planet = Planet(p1) #Create planet
            all_planets[p1] = parent_planet #Add to dictionary

        else:
            parent_planet = all_planets[p1]

        if p2 not in all_planets: #If child planet not yet in dictionary
            child_planet = Planet(p2, parent=parent_planet) #Create child planet, set parent planet as parent
            all_planets[p2] = child_planet

        else:
            child_planet = all_planets[p2]
            child_planet.parent = parent_planet


        parent_planet.add_child(child_planet) #Add child planet to children of parent planet
        
    return all_planets

def count_orbits(planets):
    
    '''
    Counts total number of indirect and direct orbits in planet system.
    
    Input:
        planets (dict): Dictionary containing every planet in the system, each planet containing its parent and children (if there are any).
    
    Returns:
        orbit_count: Total number of orbits.
    '''
    
    orbit_count = 0
    
    for name, planet in planets.items():
        
        while planet.parent != None:
            orbit_count += 1
            planet = planet.parent
                        
    return orbit_count

planet_dictionary = create_tree(input_orbits)
print('Total number of direct and indirect orbits (answer part 1): {}'.format(count_orbits(planet_dictionary)))

def roll_out(planet, find_planet = 'SAN'):
    
    '''
    Roll out from input planet to edges, checking for planet 'SAN'.
    '''
    
    current_node = planet
    visited = set()
    
    distance = 1
    to_visit = Queue()
    to_visit.put((0, planet))
    
    while to_visit.empty() != True: 
        
        distance, current_node = to_visit.get()
        for child in current_node.children:
            
            if child not in visited:
                to_visit.put((distance+1, child))
                if any(p.name == find_planet for p in child.children): return distance+1
                
    return None

current_planet = planet_dictionary['YOU'].parent
up_distance = 0 #Distance we go 'up' from parent planet of planet YOU
down_distance = roll_out(current_planet, find_planet = 'SAN') #Will be none, because SAN does not orbit the same planet


#Keep going up one planet from YOU until we find a path down to SAN
while down_distance == None:
    
    current_planet = current_planet.parent 
    up_distance += 1
    
    down_distance = roll_out(current_planet, find_planet = 'SAN')

print('Closest distance from YOU to SAN (answer part 2): {}'.format(down_distance+up_distance))