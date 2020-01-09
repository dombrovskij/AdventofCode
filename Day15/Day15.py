import numpy as np 
from Intcode import *
import random
import matplotlib.pyplot as plt

from queue import LifoQueue

with open("Day15/input.txt") as file:
    input_code = [int(s) for s in file.read().strip().split(',')]


class droid:

    '''
    Droid class that will explore the maze.
    '''

    def __init__(self):

        self.cur_pos = np.array([0,0]) #Current position of the droid (2D coordinate)
        self.game = Intcode(input_code)

        #north (1), south (2), west (3), and east (4)
        self.in_to_dirs = {1:tuple([1,0]), 2:tuple([-1,0]), 3:tuple([0,-1]), 4:tuple([0,1])}
        self.dirs_to_in = {tuple(v): int(k) for k, v in self.in_to_dirs.items()} #Reverse dictionary

        self.unexplored = [] #Buffer list for unexplored tiles adjacent to original position 

        self.anti_clockwise = {1:3, 3:2, 2:4, 4:1}
        self.clockwise = {1:4, 4:2, 2:3, 3:1}
        self.reverse_dir = {1:2, 2:1, 3:4, 4:3}

        #0 = wall, 1=empty, 2=oxygen
        self.panels = {tuple(self.cur_pos): 0} #Panels of which we know the identity
        self.grid_num = 0 #counter for plots

    def move(self, dir):

        #Move in direction north (1), south (2), west (3), and east (4).

        output = self.game.RunIntcode([dir]) #Gives back 0 for wall, 1 for open space, 2 for oxygen system in list of length 1
        
        assert len(output) == 1
        
        return output[0]
    
    def test_move(self, dir):

        #Test a move but do not actually move there (so move droid back to original position)

        output = self.game.RunIntcode([dir]) #Move in dir

        assert len(output) == 1

        if output[0] != 0: #If it was not a wall, move back (if it was a wall droid is still in original position)
            revdir = self.reverse_dir[dir]
            self.game.RunIntcode([revdir]) #move back

        return output

    def fill_unexplored(self):

        for r in [1,2,3,4]: #Check every direction
            possible_next = self.cur_pos + np.array(self.in_to_dirs[r])
            if tuple(possible_next) not in self.panels:
                self.unexplored.append(tuple(possible_next))

    def explore(self):

        #Returns a list of possible next positions from self.cur_pos

        self.fill_unexplored() #Get surrounding unexplored positions
        possible_next = []

        while len(self.unexplored) != 0: #As long as there are unexplored surrounding positions to go to

            next_pos = np.array(self.unexplored.pop())

            input_dir = self.dirs_to_in[tuple(next_pos - self.cur_pos)]

            out = self.test_move(input_dir)[0] #Check what's at the position

            if out == 0: #not moved, destination was a wall
                self.panels[tuple(next_pos)] = 0.5 #WALL
            elif out == 1: #moved to position
                possible_next.append(next_pos)
            elif out == 2: #moved to position, oxygen system is here
                possible_next.append(next_pos)
        
        return possible_next

    def show_grid(self, save=False):

        #Convert coordinates to only positive numbers
        y_map = np.arange(-19, 22) #-19 - 21, 41 numbers
        x_map = np.arange(-21, 20) #-21 - 20, 41 numbers

        grid = np.zeros((41,41))

        for i in range(grid.shape[0]):
            row = np.zeros(grid.shape[1])

            for k in self.panels.keys():

                if int(np.where(y_map == k[0])[0]) == i:
                    row[int(np.where(x_map == k[1])[0])] = self.panels[k]
            
            grid[i,:] = row

        plt.xticks([])
        plt.yticks([])

        plt.imshow(grid, origin='lower', vmin=0, vmax=3, cmap='Greys')


        if save:
            plt.savefig('./Day15/grids/'+str(self.grid_num)+'.png', format="png")
            plt.clf()
            self.grid_num+=1
        else:
            plt.show()
    
    def run(self):

        path_taken = LifoQueue()
        path_taken.put(self.cur_pos)
        split_points = [] #Coordinates from which two or more directions can be taken
        counter = 0

        while not path_taken.empty():

            counter+=1
            if counter % 10 == 0:
                print('Counter: {}'.format(counter))

            pn = self.explore()

            if len(pn) > 1: #More than 1 unexplored path to take
                split_points.append(tuple(self.cur_pos))

                next_pos = pn.pop()
                output = self.move(self.dirs_to_in[tuple(next_pos - self.cur_pos)])

                if output == 1:
                    self.panels[tuple(next_pos)] = 1
                elif output == 2:
                    self.panels[tuple(next_pos)] = 2
                
                self.cur_pos = next_pos
                path_taken.put(tuple(self.cur_pos))
            
            elif len(pn) == 1: #One unexplored path to take

                next_pos = pn.pop()
                output = self.move(self.dirs_to_in[tuple(next_pos - self.cur_pos)])

                if output == 1:
                    self.panels[tuple(next_pos)] = 1
                elif output == 2:
                    self.panels[tuple(next_pos)] = 2

                self.cur_pos = next_pos
                path_taken.put(tuple(self.cur_pos))
            
            else: #Need to go back to split point

                last_step = self.cur_pos
                while (tuple(last_step) not in split_points) & (not path_taken.empty()):

                    last_step = path_taken.get()

                    #If previous position not the same as current position, move back to previous position
                    if tuple(np.array(last_step) - np.array(self.cur_pos)) != (0,0): 
                        input_dir = self.dirs_to_in[tuple(np.array(last_step) - np.array(self.cur_pos))]
                        out = self.move(input_dir)
                        self.cur_pos = last_step

                if not path_taken.empty():
                    path_taken.put(last_step)
                    split_points.remove(last_step)
                    self.cur_pos = last_step
            

maze_explore = droid()
print('Exloring maze...')
maze_explore.run()
#maze_explore.show_grid() #Show final grid of maze

#Now we know the full maze
maze = maze_explore.panels

start_pos = (0,0)
oxygen_system_pos = [k for k,v in maze.items() if v == 2][0]

#A* Algorithm Implementation

class Node:

    def __init__(self, parent = None, position = None):

        self.parent = parent
        self.position = position

        #g = sum of cost from start to current node
        #h = heuristic, a^2 + b^2
        #cost = g+h

        self.H = 0
        self.G = 0
        self.cost = 0

    def __hash__(self):
        return hash(self.position)
    
    def __eq__(self, other):
        return self.position == other.position

class Astar:

    def __init__(self, maze, start_pos, end_pos):

        self.maze = maze

        self.start = start_pos
        self.end = end_pos

        self.visit = set()
        self.visited = set()

        self.cur_node = Node(position=self.start)
        self.visit.add(self.cur_node)
        self.end_node = Node(position=self.end)
        

    def child_coordinates(self):

        #Return child coordinates of current node

        dirs = [np.array([1,0]), np.array([-1,0]), np.array([0,-1]), np.array([0,1])]
        potential_children = []

        for d in dirs:
            potential_child = np.array(self.cur_node.position) + d
            if tuple(potential_child) in self.maze:
                if self.maze[tuple(potential_child)] != 0.5: #If it is not a wall
                    potential_children.append(tuple(potential_child))

        return potential_children

    def get_g(self, n):

        g = 0
        p = n.parent
        while p:
            g+= p.cost
            p = p.parent
        
        return g

    def get_h(self, n):

        y = n.position[0]
        x = n.position[1]

        return (self.end[0] - y)**2 + (self.end[1] - x)**2

    def shortest_path(self):

        path = [self.cur_node.position]
        p = self.cur_node.parent
        print('Retracing path...')
        while p:
            path.append(p.position)
            p = p.parent
        
        return path[::-1]

    def find_path(self):

        while self.visit:
            
            #Set current node to known node with lowest cost
            self.cur_node = min(self.visit, key=lambda o: o.G+o.H)

            if self.cur_node == self.end_node:
                print('Path found!')
                return self.shortest_path()

            self.visit.remove(self.cur_node)
            self.visited.add(self.cur_node)

            for pc in self.child_coordinates():

                child = Node(parent=self.cur_node, position=pc)

                if child in self.visited:
                    continue
                
                if child in self.visit:
                    new_g = self.get_g(child)
                        
                    if new_g < child.G:
                        #This path to child is better than any previous one
                        child.G = new_g
                        child.parent = self.cur_node
                        

                else:
                    child.G = self.get_g(child)
                    child.H = self.get_h(child)
                    child.parent = self.cur_node
                    self.visit.add(child)

        print('Path not found.')


Astar_algorithm = Astar(maze, start_pos, oxygen_system_pos)
best_path = Astar_algorithm.find_path()

print('Number of steps required: {}'.format(len(best_path)-1))

def plot_path_on_maze(path_coordinates, save=False):

    #Plots a red path on the maze

    y_map = np.arange(-19, 22) #-19 - 21, 41 numbers
    x_map = np.arange(-21, 20) #-21 - 20, 41 numbers

    grid = np.zeros((41,41))

    for i in range(grid.shape[0]):
        row = np.zeros(grid.shape[1])

        for k in maze.keys():

            if int(np.where(y_map == k[0])[0]) == i:
                row[int(np.where(x_map == k[1])[0])] = maze[k]
                
        grid[i,:] = row

    plt.xticks([])
    plt.yticks([])

    cmap = plt.cm.gray
    norm = plt.Normalize(grid.min(), grid.max())
    rgba = cmap(norm(grid))

    for k in path_coordinates[:-1]:
        rgba[int(np.where(y_map == k[0])[0]), int(np.where(x_map == k[1])[0]), :3] = 1,0,0

    plt.imshow(rgba, origin='lower', interpolation='nearest')
    if save:
        plt.savefig('./Day15/grids/best_path.png', format="png")
    else:
        plt.show()

plot_path_on_maze(best_path, save=True)

#PART 2

def neighbours(pos):

        #Return neighbours of a position tuple

        dirs = [np.array([1,0]), np.array([-1,0]), np.array([0,-1]), np.array([0,1])]
        neighbours = []
        
        for d in dirs:
            neighbour_pos = np.array(pos) + d
            neighbours.append(tuple(neighbour_pos))

        return neighbours


to_be_filled = [k for k,m in maze.items() if (m == 1)]
plot_path_on_maze([oxygen_system_pos, (20,-17), (20,-18)])
last_filled = [oxygen_system_pos]
minutes = 0

while to_be_filled:
    
    minutes += 1
    all_neighbours = []
    for lf in last_filled:
        all_neighbours.extend(neighbours(lf))
    
    spread_to = []
    for n in all_neighbours:
        if n in to_be_filled:
            to_be_filled.remove(n)
            spread_to.append(n)

    last_filled = spread_to


print('Minutes it takes to fill with oxygen: {}'.format(minutes))



