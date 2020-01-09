import numpy as np 
from queue import Queue
import math
import pandas as pd

with open('Day10/input.txt') as f:
    content = [x.strip() for x in f.readlines()] 

n_cols = len(content[0])
n_rows = len(content)

#Create the grid (empty)
grid = np.zeros((n_cols,n_rows))

#Fill the grid 1 = astroid
for i, row in enumerate(content):
    grid[i,:] = [1 if x == '#' else 0 for x in row]

#Get the astroid coordinates
astroid_coordinates = np.where(grid == 1)
astroid_coordinates = [(x,y) for x,y in zip(astroid_coordinates[0], astroid_coordinates[1])]
#(0,3) = 0 row, 3 column

def get_slope(coordinate1, coordinate2):

    '''
    Get slope between two 2D coordinates.
    '''

    dx = coordinate2[0] - coordinate1[0]
    dy = coordinate2[1] - coordinate1[1]

    gcd = math.gcd(dy, dx) #Reduce fraction
    if gcd != 0:
        dy = dy/gcd
        dx = dx/gcd

    return (int(dx), int(dy))


def distance(coordinate1, coordinate2):

    '''
    Get the distance between two astroids (two 2D coordinates).
    '''

    a = coordinate2[0] - coordinate1[0]
    b = coordinate2[1] - coordinate1[1]

    c = np.sqrt((a**2+b**2))

    return c

def get_all_slopes(astr_i):

    '''
    Get all slopes of other astroids.
    '''
    slopes = []
    distances = []

    for astr_j in astroid_coordinates: #Loop through every astroid

        if astr_j != astr_i:

            if (astr_i[0] != astr_j[0]) & (astr_i[1] != astr_j[1]): #get slope
                dxdy = get_slope(astr_i, astr_j)
                slopes.append(dxdy)
        
            elif astr_i[0] == astr_j[0]: #astroids are on same x line
                if astr_j[1] < astr_i[1]:
                    slopes.append((-1,0))
                else:
                    slopes.append((1,0))

            elif astr_i[1] == astr_j[1]: #Astroids are on same y line
                if astr_j[0] < astr_i[0]:
                    slopes.append((0,-1))
                else:
                    slopes.append((0,1))

            distances.append(distance(astr_i, astr_j))

    return distances, slopes

astroid_slopes = {}
astroid_distances = {}

#For every astroid, get slopes and distances to every other astroid
for x in astroid_coordinates: 
    d, s = get_all_slopes(x)
    astroid_slopes[x] = s
    astroid_distances[x] = d


#Find astroid that has most visible astroids

most_visible = 0 #Number of most visible astroids
astr_final = None #Astroid that has most visible astroids

for i, p in astroid_slopes.items():

    if len(list(set(p))) > most_visible: #If number of unique slopes (= number of visible astroids) larger

        most_visible = len(list(set(p))) #Set new number of most visible astroids
        astr_final = i #Set new astroid with most visible

print('Astroid with most visible: {}'.format(astr_final))
print('Most visible (Answer part 1): {}'.format(most_visible))

#Part 2

#Laser start_position relative to astr_final (being (0,0))
start_pos = (-1, 0)

#All unique slopes with other astroids for monitoring station (astr_final)
unique_slopes = list(set(astroid_slopes[astr_final]))

#Convert slopes to angles
slope_to_ang = {}

for u in unique_slopes:
    slope_to_ang[u] = math.atan2(u[0],u[1])

sorted_angles = sorted(list(slope_to_ang.values())) #Sort angles
start_index = sorted_angles.index(slope_to_ang[start_pos]) #Find angle corresponding to start position of laser
correct_angle_order = np.roll(np.array(sorted_angles), len(sorted_angles)-start_index) #Roll angles so it starts with start position of laser
    
astroid_coordinates.remove(astr_final)

#Put everything in Pandas DataFrame
full_frame = pd.DataFrame({'astroid': astroid_coordinates, 'slope': astroid_slopes[astr_final], 
    'distance': astroid_distances[astr_final]})    

full_frame['angle'] = full_frame.slope.apply(lambda x: slope_to_ang[x])


lasered_astroids = [] #Track lasered astroids

for a in correct_angle_order:

        if a in full_frame.angle.values: #If still astroid in this direction

            astroids_in_the_way = full_frame.loc[full_frame.angle == a].copy()

            #Get closest astroid to monitoring station
            closest = astroids_in_the_way.sort_values(by='distance', ascending=True).iloc[0].astroid
            
            #Laser it away
            lasered_astroids.append(closest)
            full_frame.drop(full_frame.loc[full_frame.astroid == closest].index, inplace=True)
        
        #We want to find the 200th lasered astroid
        if len(lasered_astroids) == 200:
            break

print('Answer part 2: {}'.format(lasered_astroids[199][1]*100 + lasered_astroids[199][0]))


        



        

        
        

        
        




        


        
        



