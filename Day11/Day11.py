from Intcode import *
import matplotlib.pyplot as plt

with open("Day11/input.txt") as file:
    input_code = [int(s) for s in file.read().strip().split(',')]

class robot:

    '''
    This robot paints panels. It starts on panel (0,0) which is either black (0) or white (1).
    Then it asks the Intcode computer for input. This returns the color to paint the current panel and the direction to take.
    The robot will keep moving and painting until the Intcode computer is done running the input code.
    '''

    def __init__(self, start_c):

        self.dir = np.array((1,0)) #Left: (0,-1), Down: (-1,0), Right: (0,1), Up: (1,0)
        self.panels = {}
        self.panels[(0,0)] = start_c #Start on panel that is black or white
        self.cur_pos = np.array((0,0))
        self.brain = Intcode(input_code)

        self.anti_clockwise = {(-1,0): (0,-1), (0,-1): (1,0), (1,0): (0,1), (0,1): (-1,0)}
        self.clockwise = {(-1,0): (0,1), (0,1): (1,0), (1,0): (0,-1), (0,-1): (-1,0)}

    def next_instruction(self):

        return self.brain.RunIntcode([self.cur_color])

    def paint(self, c):

        self.panels[tuple(self.cur_pos)] = c

    def move(self, d):

        if d == 0: #Anti-clockwise (turn 90 degrees left)
            self.dir = np.array(self.anti_clockwise[tuple(self.dir)])
        elif d ==1: #turn 90 degrees right
            self.dir = np.array(self.clockwise[tuple(self.dir)])
        else:
            raise Exception('Invalid direction encountered.')

        #Update position based on this direction
        self.cur_pos = self.cur_pos + self.dir
        if tuple(self.cur_pos) not in self.panels:
            self.panels[tuple(self.cur_pos)] = 0 #Initiate this panel to black
        
        self.cur_color = self.panels[tuple(self.cur_pos)]


    def run(self):

        self.cur_color = self.panels[tuple(self.cur_pos)] #0 is black, 1 is white
        
        next_inst = self.next_instruction()

        while len(next_inst) != 0:

            c, d = next_inst #Color to paint and direction to turn
            self.paint(c)
            self.move(d)

            next_inst = self.next_instruction()

    def paint_panels(self):

        #Paint the panels on a grid and show result

        all_y = [a[0] for a in self.panels.keys()]
        all_x = [a[1] for a in self.panels.keys()]

        min_x = np.min(all_x)
        max_x = np.max(all_x)
        diff_x = max_x-min_x+1

        min_y = np.min(all_y)
        max_y = np.max(all_y)
        diff_y = max_y-min_y+1

        grid = np.zeros((diff_y, diff_x))
        for i, y_i in enumerate(range(min_y, max_y+1)):
            row = []
            for x_i in range(min_x, max_x+1):
                if (y_i, x_i) in self.panels:
                    row.append(self.panels[(y_i, x_i)])
                else:
                    row.append(0)
            
            grid[i,:] = row

        plt.imshow(grid.T, origin='lower')
        plt.savefig('./Day11/message.png')
        #plt.show()

        
if __name__ == "__main__":
    R = robot(0) #Initiate robot on a black panel
    R.run()
    print('Number of painted panels (Answer Part 1): {}'.format(len(R.panels.keys())))
    R_2 = robot(1) #Initiate robot on a white panel
    R_2.run()
    R_2.paint_panels()



        


