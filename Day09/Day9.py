import numpy as np
from Intcode import *
from itertools import permutations

with open("./Day9/input.txt") as file:
    input_code = [int(s) for s in file.read().strip().split(',')]

IntComputer1 = Intcode(input_code)
answer_part1 = IntComputer1.RunIntcode([1])[0]
IntComputer2 = Intcode(input_code)
answer_part2 = IntComputer2.RunIntcode([2])[0]

print('Answer part 1: {}'.format(answer_part1))
print('Answer part 2: {}'.format(answer_part2))

