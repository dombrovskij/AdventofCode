import numpy as np 
import re
import math
from queue import Queue


class reaction:

    '''
    A reaction keeps track of its input chemicals, output chemicals and their amounts.
    '''

    def __init__(self, txt_react, input_chems, input_nums, output_chem, output_num):

        self.input_chems = input_chems
        self.input_nums = input_nums
        
        self.output_chem = output_chem
        self.output_num = output_num

        self.full_reaction = txt_react


class nanofactory:


    def __init__(self, txt_reactions):

        self.all_reactions = {}

        #Extract all reactions from input and create a class object for each
        for txt_react in txt_reactions:
            input_chems, input_nums, output_chem, output_num = self.split_reaction(txt_react)

            self.all_reactions[output_chem] = reaction(txt_react, input_chems, input_nums, output_chem, output_num)


    def split_reaction(self, r):

        '''
        Input string reaction (as in input file) and use regex to split into in/out chemicals and their amounts.
        '''

        input_r = r.replace(" ", "").split('=>')[0]
        output_r = r.replace(" ", "").split('=>')[1]

        inputs = input_r.split(',')

        in_num = [int(re.findall(r'\d+', i)[0]) for i in inputs]
        in_chem = [re.findall(r'[a-zA-Z]+', i)[0] for i in inputs]

        out_num = int(re.findall(r'\d+', output_r)[0])
        out_chem = re.findall(r'[a-zA-Z]+', output_r)[0]


        return in_chem, np.array(in_num), out_chem, out_num

    def required_chems(self, chem, num):

        '''
        Returns input chems and amount of those input chems needed as input to the reaction to which chem is the output, 
        in order to create c*chem3 (num*chem)

        a*chem1 + b*chem2 => c*chem3

        If num is less than c, the input amounts are given to create c*chem3, not num*chem3. 
        If num is not a multitude of c, the input amounts are given that create the closest multitude of c (rounded up).
        '''

        current_reaction = self.all_reactions[chem]

        r_repeats = math.ceil(num/current_reaction.output_num)
        reaction_result_amount = current_reaction.output_num * r_repeats
        waste = reaction_result_amount - num

        return r_repeats * current_reaction.input_nums, current_reaction.input_chems, waste

    def required_ore(self, chem, num):

        '''
        Calculate the amount of ore needed to produce the input num amount of the input chemical (chem).
        '''

        needed_chem = chem
        needed_amount = num

        if needed_chem not in self.leftover:
            self.leftover[needed_chem] = 0
        else:
            if self.leftover[needed_chem] >= needed_amount:
                #We already have enough, don't need to make more
                self.leftover[needed_chem] = self.leftover[needed_chem] - needed_amount
                return
            else:
                #We still need to make some
                needed_amount = needed_amount - self.leftover[needed_chem]
                self.leftover[needed_chem] = 0
            
        req_nums, req_chems, waste = self.required_chems(needed_chem, needed_amount)
        self.leftover[needed_chem] += waste

        for c, n in zip(req_chems, req_nums):

            if c == 'ORE':
                self.orecount += n #If we worked back to ore, add this to orecount
            else:
                self.required_ore(c,n) #If not ore, recursively call function again
        return None
            
    def find_ore(self, c, n):

        self.leftover = {}
        self.orecount = 0

        self.required_ore(c,n)

        if 'ORE' in self.leftover:
            self.orecount += self.leftover['ORE']

        return self.orecount 

with open("Day14/input.txt") as file:
    input_code = [x.split('\n')[0] for x in file.readlines()]

Factory = nanofactory(input_code)
print('Answer to part 1: {}'.format(Factory.find_ore('FUEL',1)))

#PART 2
#How much fuel can we make with 1000000000000 ore

amount_ore = 10**12
fuel_produced = 2
answer = 0

#This will restrict it to 1
while True:
    print('Producing {} fuel'.format(fuel_produced))
    needed_ore = Factory.find_ore('FUEL', fuel_produced)
    print('Needed {} ore'.format(needed_ore))
    if needed_ore > amount_ore:
        answer = fuel_produced
        break
    
    fuel_produced = round(fuel_produced*amount_ore/needed_ore)

print('Answer to part 2: {}'.format(answer-1))



