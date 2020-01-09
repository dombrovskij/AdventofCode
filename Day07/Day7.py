import numpy as np
from Intcode import *
from itertools import permutations

with open('./Day7/input.txt') as f:
    input_code = [int(s) for s in f.read().strip().split(',')]

possible_phase_settings = np.arange(5)
Intcode(input_code).RunIntcode([1,0]) #Set up the Intcode Computer with correct input.

all_permutations = permutations(possible_phase_settings, len(possible_phase_settings))
amps = ['A', 'B', 'C', 'D', 'E']

highest_output = 0
best_permutation = 0

for perm in all_permutations:
    for p, amp in zip(perm, amps):
        
        if amp == 'A':
            amp_output = Intcode(input_code).RunIntcode([p,0]) #Amp A gets input of 0
        
        else:
            amp_output = Intcode(input_code).RunIntcode([p,amp_output[0]]) #The other amps get the output from the previous amp
            
    if amp_output[0] > highest_output:
        highest_output = amp_output[0] #Save the highest output and best permutation
        best_permutation = perm

#Answer to part 1
print('Highest output: {}'.format(highest_output))
print('Best permutation: {}'.format(best_permutation))

#PART 2

def boost(code, amps, perm, initial_input):

    '''
    Boost amps until all amps have turned off. 

    Input:
        code: list containing input code
        amps: list containing all amp names (as strings) [A, B, C, E], needs to end with 'E' signifying the amp at the end.
        perm: list, the permutation to use
        initial_input: list, the initial input to the first amp

    Output:
        boosted: the final output
    '''
    
    amps_dict = {}
    amp_output = initial_input
    
    #Initiate each amp and add to dictionary
    for p, amp in zip(perm, amps):
        
        amps_dict[amp] = Intcode(code) #Initiate amp
        
        inputs = [p]
        inputs.extend(amp_output)
    
        amp_output = amps_dict[amp].RunIntcode(inputs)
    
    next_input = amp_output

    stopped_amps = [] #Keep track of stopped amps
    boosted = 0

    while len(stopped_amps) != len(amps): #As long as there is at least one amp still running
        for amp in amps:
            if not amps_dict[amp].stop:
            
                    amp_output = amps_dict[amp].RunIntcode(next_input)
                    if amp_output != None:
                        next_input = amp_output
                    
                        if amp == 'E': #Check output from the last amp 
                            if amp_output[0] > boosted:
                                boosted = amp_output[0]
                            
                    
        
            else:
                stopped_amps.append(amp)
                
    return boosted


amps = ['A', 'B', 'C', 'D', 'E']

possible_phase_settings = np.arange(5,10)
all_permutations = permutations(possible_phase_settings, len(possible_phase_settings))

highest_output = 0
best_permutation = 0

for perm in all_permutations:
    
    boosted = boost(input_code, amps, perm, [0])
    
    if boosted > highest_output:
        highest_output = boosted
        best_permutation = perm

#Answer part 2
print('Highest output (answer part 2): {}'.format(highest_output))
print('Corresponds to permutation: {}'.format(best_permutation))