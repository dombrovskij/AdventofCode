import numpy as np
from scipy.spatial import distance

#Read input data
with open('input.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

wire1 = content[0].split(',')
wire2 = content[1].split(',')

central_port = (0,0) #Set coordinate location of central port on grid

print('Example of the first ten instructions for the first wire:')
print(wire1[0:10], end='')

numeric_direction = {'R':+1, 'L':-1, 'U':+1, 'D':-1}

def execute_instruction(instruction, current_coordinate):
    
    '''
    Executes an instruction. 
    Returns the visited coordinates and new current coordinate.
    '''
    
    direction = instruction[0]
    n_steps = int(instruction[1:])
    steps = np.arange(1, n_steps+1)
    
    x = current_coordinate[0]
    y = current_coordinate[1]
    
    num_dir = numeric_direction[direction]
    
    if (direction == 'L') | (direction == 'R'):
        
        new_x = num_dir*steps+x
        add_coordinates = [(nx, y) for nx in new_x]        
        new_coordinate = (x+(num_dir*n_steps), y)
        
    elif (direction == 'U') | (direction == 'D'):
        
        new_y = num_dir*steps+y
        add_coordinates = [(x, ny) for ny in new_y]        
        new_coordinate = (x, y+(num_dir*n_steps))
        
    
    return add_coordinates, new_coordinate
    
def get_coordinates(wire, start_coordinate):
    
    '''
    Executes a list of instructions and returns all the visited coordinates.
    '''
    
    final_coordinates = []
    current_coordinate = start_coordinate
    
    for instruction in wire:
        
        add_coord, new_coord = execute_instruction(instruction, current_coordinate)
        final_coordinates.extend(add_coord)
        current_coordinate = new_coord
    
    return final_coordinates
        

#Get all visited coordinates of both the wires
wire1_coordinates = get_coordinates(wire1, central_port) 
wire2_coordinates = get_coordinates(wire2, central_port)

print('Number of visited coordinates by wire 1: {}'.format(len(wire1_coordinates)))
print('Number of visited coordinates by wire 2: {}'.format(len(wire2_coordinates)))

#Get the wire intersections
a = set(wire1_coordinates)
b = set(wire2_coordinates)
wire_intersections = list(a.intersection(b))

print('Number of wire intersections: {}'.format(len(wire_intersections)))

#Get the manhattan distances from the central port to each intersection
manhattan_distances = [distance.cityblock((0,0), intersection) for intersection in wire_intersections]

closest_intersection = wire_intersections[np.argmin(manhattan_distances)]
closest_distance = np.min(manhattan_distances)

print('Answer to part 1.')
print('The intersection with the smallest Manhattan distance is {}. It has a Manhattan distance of {}.'.format(closest_intersection, closest_distance))

#Part 2
#Get sum of number of steps needed by both wires to reach each respective intersection
wire_steps = []
for intersection in wire_intersections:
    #Plus two because it is including the step to the intersection
    wire_steps.append(wire1_coordinates.index(intersection) + wire2_coordinates.index(intersection) +2)

smallest_steps_intersection = wire_intersections[np.argmin(wire_steps)]
smallest_steps = np.min(wire_steps)

print('Answer to part 2.')
print('The intersection with the smallest collective number of steps taken to it by the two wires is {}'.format(smallest_steps_intersection))
print('The collective number of steps taken by the two wires to this intersection is: {}'.format(smallest_steps))