import numpy as np 
import itertools
import math

with open('Day16/input.txt') as f:
    content = int(f.read())


class FFT:

    def __init__(self, base_pattern):

        self.base_pattern = base_pattern
    
    def repeating_pattern(self, n, final_len):

        '''
        Return base patern n times repeating, cropped to be final_len.
        '''

        if n > final_len: #Then it will just all be the first element of the base pattern
            return np.array(list(itertools.chain.from_iterable(itertools.repeat(self.base_pattern[0],final_len))))

        repeats = math.ceil(final_len/n)
        base = list(itertools.chain.from_iterable(itertools.repeat(x, n) for x in self.base_pattern)) #First repeat every element n times

        final = list(itertools.chain.from_iterable(itertools.repeat(base,repeats))) #Then repeat that pattern 

        return np.array(final[1:final_len+1])

    def create_matrix(self):

        '''
        Create the FFT matrix to be multiplied with the signal.
        '''

        FFT_matrix = np.zeros((self.input_len, self.input_len))

        for i in range(self.input_len):
            np.insert(FFT_matrix, i, self.repeating_pattern(i+1, self.input_len), 0)  
            FFT_matrix[i,:] = self.repeating_pattern(i+1, self.input_len)
        
        return FFT_matrix

    def run(self, n_phase, input_signal):
        
        self.input_signal = [int(x) for x in str(input_signal)]
        self.input_len = len(self.input_signal)

        FFT_matrix = self.create_matrix()
        output = self.input_signal.copy()

        for n in range(n_phase):
            output = np.abs(np.dot(FFT_matrix, np.array(output))) % 10
            
        return output

FFT_instance = FFT([0, 1, 0, -1])
xx = FFT_instance.test_matrix(100, content)
print("Part 1:", ''.join(xx.astype(int).astype(str))[:8])

#PART 2

signal = str(content)
message_offset = int(signal[0:7].lstrip('0'))

assert message_offset > (len(signal)*10000) / 2

use_signal = [int(x) for x in (str(signal)*10000)[message_offset:]]

for n in range(100):
    final_sum = 0
    for i in range(len(use_signal)-1, -1, -1):

        final_sum += use_signal[i]
        use_signal[i] = final_sum % 10

print('Part 2: {}'.format(use_signal[0:8]))
