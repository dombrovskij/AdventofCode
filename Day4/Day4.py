import numpy as np 

#We are looking for all valid passwords in range:
input_start = 356261
input_end = 846303

input_range = np.arange(input_start, input_end+1)

def get_double(number, find_n=None):
    
    '''
    Input:
        number: integer
        find_n: find integer with any digit repeating find_n times
        
    Output:
        boolean
        if no find_n specified, return True if input number contains any repeating digit
        if find_n specified, return True if input number contains any digit repeating find_n times
        else return False
    '''
    
    number = str(number)
    prev_num = number[0]
    
    double_label = False #Contains repeating digit
    
    counter_list = [] #Contains al counts of digits
    counter = 1 #Counts number of repetitions of current digit
    
    for n in number[1:]:
        
        if n == prev_num:
            double_label = True #Input number contains repeating digit
            counter+= 1
            
        else:
            counter_list.append(counter) #Remember the count of this digit
            counter = 1 #Set counter back to 1
        
        prev_num = n
    
    counter_list.append(counter) #Append last counter to list
    
    if find_n: #If find_n is specified, check if input number contained a digit repeating exactly find_n times
        if find_n in counter_list: return True 
        else: return False
    else: #Else just return whether or not input number contained a digit repeating at least two times
        return double_label
        

#Part 1
#A valid password contains a repeating digit and every subsequent digit is either equal or larger than the previous one

valid_passwords_part1 = []

for i in input_range:
    
    double_label = get_double(i) #Repeating digit boolean
    equal_or_increasing = all(i <= j for i, j in zip(str(i), str(i)[1:]))
    
    if (double_label) & (equal_or_increasing): #If both conditions are met, valid password
        valid_passwords_part1.append(i)
    
    else:
        pass

print('Number of valid passwords (answer to part 1) {}'.format(len(valid_passwords_part1)))

#Part 2
#A valid password contains a digit repeating exactly 2 times 
#and every subsequent digit is either equal or larger than the previous one

valid_passwords_part2 = []

for i in input_range:
    
    double_label = get_double(i, 2) #Digit repeating exactly 2 times boolean
    equal_or_increasing = all(i <= j for i, j in zip(str(i), str(i)[1:]))

    
    if (double_label) & (equal_or_increasing): #If both conditions are met, valid password
        valid_passwords_part2.append(i) 
    
    else:
        pass

print('Number of valid passwords (answer to part 2) {}'.format(len(valid_passwords_part2)))