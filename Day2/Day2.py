import numpy as np 

with open('input.txt') as f:
    content = f.readlines()

input_code = [int(x) for x in content[0].split(',')]

#restore the gravity assist program to the "1202 program alarm" state
restored_code = input_code.copy()
restored_code[1] = 12 #noun
restored_code[2] = 2 #verb

def Intcode(data):
    
    instruction_pointer = 0

    while instruction_pointer+4 <= len(data):

        data_block = data[instruction_pointer:instruction_pointer+4]
        opcode = data_block[0]

        if opcode == 1:
            data[data_block[3]] = data[data_block[1]] + data[data_block[2]]

        elif opcode == 2:
            data[data_block[3]] = data[data_block[1]] * data[data_block[2]]

        elif opcode == 99:
            return data

        else:
            raise Exception('Incorrect opcode: {}'.format(opcode))
            return None

        instruction_pointer += 4
        
    return data

output = Intcode(restored_code)
print('Answer question 1: {}'.format(output[0]))

#Part two, find which noun and verb combination produces the output 19690720
nouns = np.arange(0,100)
verbs = np.arange(0,100)

for noun in nouns:
    for verb in verbs:
        
        use_code = input_code.copy()
        use_code[1] = noun
        use_code[2] = verb
        
        intcode_output = Intcode(use_code)
        
        if intcode_output[0] == 19690720:
            correct_noun = noun
            correct_verb = verb
            print('Correct output produced with noun {} and verb {}.'.format(correct_noun, correct_verb))
            break

print('Answer to question 2: 100*noun+verb = {}'.format(100*correct_noun+correct_verb))