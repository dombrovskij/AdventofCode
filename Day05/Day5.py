import numpy as np

def read_input():

    with open('input.txt') as f:
        content = f.readlines()

    input_code = [int(x) for x in content[0].split(',')]
    
    return input_code

def split_instruction_base(instruction_base):
    
    '''
    Input:
        instruction_base: (integer)
    Splits an instruction base into the opcode (last two digits) and the parameter modes (all preceeding digits)
    
    '''
    
    opcode = int(instruction_base[-2:])
    parameter_modes = [int(x) for x in instruction_base[::-1][2:]]
    parameter_modes.extend([0]*(4-len(parameter_modes))) #Add leading zeros if necessary (should be total of four parameter modes)
    
    return opcode, parameter_modes

def convert(from_data, p_modes, numbers):
    
    '''
    Convert parameters based on parameter modes. 
    If a parameter has parameter mode 0: the parameter is the index (adress) of the actual value
    If a parameter has parameter mode 1: the parameter is the actual value
    
    Input:
        from_data: the input data from which the numbers are
        p_modes: list of the parameter modes of the input numbers (should have the same length as the input numbers list)
        numbers: list of the numbers to be converted
        
    Returns:
        result: list with the converted numbers (same length as input numbers)
    '''
        
    result = []
    
    for p_mode, num in zip(p_modes, numbers):
        
        if p_mode == 0:
            result.append(from_data[num])
        elif p_mode == 1:
            result.append(num)
        else:
            raise Exception('Incorrect parameter mode: {}'.format(p_mode))
    
    return result
        
        
def execute_instruction(data, instruction_pointer):
    
    '''
    Executes an instruction.
    
    Input:
        data: the input data (array or list)
        instruction_pointer: the pointer/index of the (first entry of the) instruction to execute
        
    Returns:
        The next instruction pointer
    
    '''
    
    instruction_base = str(data[instruction_pointer]) #Get instruction base
    opcode, parameter_modes = split_instruction_base(instruction_base) #Obtain opcode and parameter modes from instruction base
        
    if opcode == 1:
        
        #Addition
        
        instruction = data[instruction_pointer+1:instruction_pointer+4]

        converted = convert(data, parameter_modes, instruction[0:2])
        data[instruction[2]] = converted[0] + converted[1]
        
        return instruction_pointer+4

    elif opcode == 2:
        
        #Multiplication
        
        instruction = data[instruction_pointer+1:instruction_pointer+4]
        converted = convert(data, parameter_modes, instruction[0:2])

        data[instruction[2]] = converted[0] * converted[1]
        
        return instruction_pointer+4

    elif opcode == 3:
        
        #Get user input and place it at index given in instruction
        
        instruction = [data[instruction_pointer+1]]

        while True:
            try:
                systemID = int(input('Please enter ID of the system to test (integer).'))
                break
            except:
                print("SystemID should be an integer.")

        data[instruction[0]] = systemID
        
        return instruction_pointer+2

    elif opcode == 4:
        
        #Output value at index given in instruction
        
        instruction = [data[instruction_pointer+1]]
        print('Output: {}'.format(data[instruction[0]]))
        
        return instruction_pointer+2
    
    elif opcode == 5:
        
        #If first parameter of instruction is not zero, new instruction pointer is the second parameter
        #else do nothing, go to next instruction as usual
        
        instruction = data[instruction_pointer+1:instruction_pointer+3]
        converted = convert(data, parameter_modes, instruction[0:2])
        
        if converted[0] != 0:
            return converted[1] #New instruction pointer
        else:
            return instruction_pointer+3
    
    elif opcode == 6:
        
        #If first parameter of instruction is zero, new instruction pointer is the second parameter
        #else do nothing, go to next instruction as usual
        
        instruction = data[instruction_pointer+1:instruction_pointer+3]
        converted = convert(data, parameter_modes, instruction)
        
        if converted[0] == 0:
            return converted[1] #New instruction pointer
        else:
            return instruction_pointer+3 
        
    elif opcode == 7:
        
        #If first parameter is smaller than second parameter, value at index of the third parameter is 1
        #else it is 0
        
        instruction = data[instruction_pointer+1:instruction_pointer+4]
        converted = convert(data, parameter_modes, instruction[0:2])

        if converted[0] < converted[1]:
            data[instruction[2]] = 1
        else:
            data[instruction[2]] = 0
            
        return instruction_pointer+4
            
    elif opcode == 8:
        
        #If first parameter is equal to second parameter, value at index of the third parameter is 1
        #else it is 0
        
        instruction = data[instruction_pointer+1:instruction_pointer+4]
        converted = convert(data, parameter_modes, instruction[0:2])

        if converted[0] == converted[1]:
            data[instruction[2]] = 1
        else:
            data[instruction[2]] = 0  
        
        return instruction_pointer+4

        
    elif opcode == 99:
        return None

    else:
        raise Exception('Incorrect opcode encountered: {}'.format(opcode))
        return None

def Intcode(data):
    
    '''
    Run the Intcode on data.
    '''
        
    instruction_pointer = 0

    while (instruction_pointer+4 <= len(data)): #As long as end of data not reached
        
        instruction_pointer = execute_instruction(data, instruction_pointer)
        if instruction_pointer == None: #Incorrect opcode or opcode was 99, stop processing.
            break
        else: pass

if __name__ == "__main__":

    #Part 1, give input ID 1
    print('Running TEST diagnostic system...')
    input_code = read_input()
    Intcode(input_code)

    #Part 2, give input ID 5
    print('Running TEST diagnostic system...')
    input_code = read_input()
    Intcode(input_code)