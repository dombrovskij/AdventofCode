import numpy as np
from queue import Queue

class Intcode:
    
    def __init__(self, data):
              
        self.memory = dict()
        self.inputs = Queue()
        self.instruction_pointer=0
        self.base = 0
        self.done = False
        self.stop = False
        
        for pointer, c in enumerate(data):
            self.memory[pointer] = c

    def split_instruction_base(self):

        '''
        Input:
            instruction_base: (integer)
        Splits an instruction base into the opcode (last two digits) and the parameter modes (all preceeding digits)

        '''
        instruction_base = str(self.memory[self.instruction_pointer]) #Get instruction base
       
        opcode = int(instruction_base[-2:])
        parameter_modes = [int(x) for x in instruction_base[::-1][2:]]
        parameter_modes.extend([0]*(3-len(parameter_modes))) #Add leading zeros if necessary (should be total of four parameter modes)

        return opcode, parameter_modes

    def convert(self, p_modes, numbers):

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
                if num in self.memory:
                    result.append(self.memory[num])
                else: result.append(0)
            elif p_mode == 1:
                result.append(num)
            elif p_mode == 2:
                if self.base+num in self.memory:
                    result.append(self.memory[self.base+num])
                else: result.append(0)
            else:
                raise Exception('Incorrect parameter mode: {}'.format(p_mode))
                

        return result
    
    def read_params(self):
        
        params = [self.memory[self.instruction_pointer+1+i] if self.instruction_pointer+1+i in self.memory else 0 for i in range(3)]
        
        _, parameter_modes = self.split_instruction_base()
        
        converted_params = self.convert(parameter_modes, params)
        
        return params, converted_params
        
    def advance_pointer(self, op_code):
        """
        Advance the program counter depending on the number of
        parameters for the give op code.
        """
        self.instruction_pointer += {
                1:  3,
                2:  3,
                3:  1,
                4:  1,
                5:  2,
                6:  2,
                7:  3,
                8:  3,
                9:  1,
                99: 0
            }[op_code] + 1


    def execute_instruction(self):

        '''
        Executes an instruction.

        Input:
            data: the input data (array or list)
            instruction_pointer: the pointer/index of the (first entry of the) instruction to execute

        Returns:
            The next instruction pointer

        '''

        opcode, parameter_modes = self.split_instruction_base() #Obtain opcode and parameter modes
        
        params, converted_params = self.read_params()
        
        self.advance_pointer(opcode)


        if opcode == 1:

            #Addition
            if parameter_modes[2] == 2:
                self.memory[self.base + params[2]] = converted_params[0] + converted_params[1]
            else:
                self.memory[params[2]] = converted_params[0] + converted_params[1]

        elif opcode == 2:

            #Multiplication
            if parameter_modes[2] == 2:
                self.memory[self.base + params[2]] = converted_params[0] * converted_params[1]
            else:
                self.memory[params[2]] = converted_params[0] * converted_params[1]

        elif opcode == 3:

            #Get user input and place it at index given in instruction
            
            if self.inputs.empty():
                print('NO INPUT')
            
            if parameter_modes[0] == 2:
                self.memory[self.base + params[0]] = self.inputs.get()
            else:
                self.memory[params[0]] = self.inputs.get()

        elif opcode == 4:

            #Output value at index given in instruction

            self.output = converted_params[0]
            

        elif opcode == 5:

            #If first parameter of instruction is not zero, new instruction pointer is the second parameter

            if converted_params[0] != 0:
                self.instruction_pointer = converted_params[1] #New instruction pointer

        elif opcode == 6:

            #If first parameter of instruction is zero, new instruction pointer is the second parameter
            
            if converted_params[0] == 0:
                self.instruction_pointer = converted_params[1] #New instruction pointer

        elif opcode == 7:

            #If first parameter is smaller than second parameter, value at index of the third parameter is 1
            #else it is 0

            if converted_params[0] < converted_params[1]:
                if parameter_modes[2] == 2:
                    self.memory[self.base + params[2]] = 1
                else:
                    self.memory[params[2]] = 1
            else:
                if parameter_modes[2] == 2:
                    self.memory[self.base + params[2]] = 0
                else:
                    self.memory[params[2]] = 0

        elif opcode == 8:

            #If first parameter is equal to second parameter, value at index of the third parameter is 1
            #else it is 0

            if converted_params[0] == converted_params[1]:
                if parameter_modes[2] == 2:
                    self.memory[self.base + params[2]] = 1
                else:
                    self.memory[params[2]] = 1
            else:
                if parameter_modes[2] == 2:
                    self.memory[self.base + params[2]] = 0
                else:
                    self.memory[params[2]] = 0  
            
        elif opcode == 9:
            
            #Opcode 9 adjusts the relative base by the value of its only parameter.
            
            self.base += converted_params[0]


        elif opcode == 99:
            self.stop = True

        else:
            raise Exception('Incorrect opcode encountered: {}'.format(opcode))

    def RunIntcode(self, inputID):

        '''
        Run the Intcode on data.
        '''
        
        self.output = None
        outputs = []
        if len(inputID) > 0:
            for x in inputID:
                self.inputs.put(x)
                
        while not (self.done or self.stop):
            self.execute_instruction()
            
            if self.output is not None:
                outputs.append(self.output)
                self.output=None
                
                
        return outputs