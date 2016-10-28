# AI2 Part 1
#
# Note: All tuples in this project are defined as (y,x)

from __future__ import print_function
import time
import copy


class words:
    def __init__(self, word, position, orientation):
        self.word = word
        self.position = position # y and x in the matrix
        self.orientation = orientation # either V or H


# Function to convert a sudoku grid
def cvt_matrix(n):
    f = open(n)
    lines = f.readlines()
    maze = []
    for line in lines:
        array = []
        for char in line:
            if char != '\n':
                array.append(char)
        maze.append(array)
    f.close()
    return maze


# Function to convert a bank of words
def cvt_words(n):
    f = open(n)
    lines = f.readlines()
    words = []
    for line in lines:
        words.append(line.strip().upper())
    f.close()
    return words


# Function to print a matrix
def print_m(matrix): 
    for y in range(9):
        for x in range(9):
            print((matrix[y][x]),end="")
        print("\n")


# Function to initialize the list of legal values for each word
# Legal values are a tuple ( (y,x), orientation )
def init_legal_values(word_list):
    legal_values = {}
    for word in word_list:
        legal_values[word] = []
        for a in range(10 - len(word)):
            for b in range(9):
                word_val = words(word, (a,b), 'V')
                legal_values[word].append(word_val)
            for b in range(9):
                word_val = words(word, (b,a), 'H')
                legal_values[word].append(word_val)
    return legal_values


# Function to choose the next word (variable) from the word list
# Based on the most constrained variable heuristic
def choose_word(matrix, word_list):
    hist = {}
    # Initilize histogram
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for char in letters:
        hist[char] = 0
    # Check the grid and update the 'hist' disctionary 
    for row in matrix:
        for char in row:
            if char != '_':
                hist[char] += 1
    # Each word has a histogram value and we update/increment it by
    # finding all the letters in the grid that match the word
    max_hist_val = 0
    ret_val = ''
    for word in word_list:
        hist_val = 0
        for char in word:
            hist_val += hist[char]
            # Pick the longest word or compare the histogram value to break ties
            if (len(word) > len(ret_val)) or (len(word) == len(ret_val) and hist_val > max_hist_val):
                max_hist_val = hist_val
                ret_val = word
    return ret_val


def word_placement(matrix, word, position, orientation):
    if orientation == 'H':
        for n in range(len(word)):
            matrix[position[0]][position[1] + n] = word[n]
    else:
        for n in range(len(word)):
            matrix[position[0] + n][position[1]] = word[n]
    return matrix


# Check constraints for a legal value
def check_constraints(matrix, word, position, orientation):
    y = position[0]
    x = position[1]

    if orientation == 'H':
        for i in range(len(word)):
            # Skip if letter is already in matrix
            if word[i] == matrix[y][x + i]:
                continue

            # 1. Check for consistency of characters
            if matrix[y][x + i] != '_':
                return False

            # 2. Check for duplicate letters along rows
            if word[i] in matrix[y]:
                return False

            # 3. Check for duplicate letters along columns
            for j in range(9):
                if word[i] in matrix[j][x + i]:
                    return False

            # 4. Check for duplicate letters in 3x3 blocks
            block_x = (x + i) // 3
            block_y = y // 3
            for ypos in range(3*block_y, 3*block_y + 3):
                for xpos in range(3*block_x, 3*block_x + 3):
                    if word[i] in matrix[ypos][xpos]:
                        return False
    else:
        for i in range(len(word)):
            # Skip if letter is already in matrix
            if word[i] == matrix[y + i][x]:
                continue

            # 1. Check for consistency of characters
            if matrix[y + i][x] != '_':
                return False

            # 2. Check for duplicate letters along rows
            for j in range(9):
                if word[i] in matrix[y + i][j]:
                        return False

            # 3. Check for duplicate letters along columns
            for j in range(9):
                if word[i] in matrix[j][x]:
                    return False

            # 4. Check for duplicate letters in 3x3 blocks
            block_x = x // 3
            block_y = (y + i) // 3
            for ypos in range(3*block_y, 3*block_y + 3):
                for xpos in range(3*block_x, 3*block_x + 3):
                    if word[i] in matrix[ypos][xpos]:
                        return False
    return True


# Forward checking function after making new assignment
def forward_checking(matrix, word_list, legal_values, word, position, orientation):
    # Temporarily assign word_val into matrix
    temp_matrix = copy.deepcopy(matrix)
    temp_matrix = word_placement(temp_matrix, word, position, orientation)
    # Create temporary word_list
    temp_word_list = copy.deepcopy(word_list)
    temp_word_list.remove(word)

    while temp_word_list:
        word1 = choose_word(matrix, temp_word_list)
        temp_word_list.remove(word1)
        trash = []

        # For each legal value for each word
        for word_val in legal_values[word1]:
            # If the value is no longer legal, add it to trash
            if not check_constraints(temp_matrix, word_val.word, word_val.position,
                                        word_val.orientation):
                trash.append(word_val)

        # If no legal values are left, return False
        if len(trash) == len(legal_values[word1]):
            return False

    return True


###############################################################################


# Recursive function to solve the word sudoku puzzle
def sudoku(matrix, word_list, nodes, path, legal_values):
    # Base Case: Check for completion of matrix
    complete = True
    for row in matrix:
        if '_' in row:
            complete = False
            break
    if complete:
        return (True, matrix)

    # Select the next word (variable) from the word list
    word = choose_word(matrix, word_list)
    
    queue = []
    trash = []

    # Find values for the word that satisfy the constraints
    for word_val in legal_values[word]:
        if check_constraints(matrix, word_val.word, word_val.position,
                                word_val.orientation):
            # If constraints are satisfied, perform forward checking
            if forward_checking(matrix, word_list, legal_values, word_val.word,
                                word_val.position, word_val.orientation):
                queue.append(word_val)
            else:
                trash.append(word_val)
        else:
            trash.append(word_val)

    # Copy legal_values and remove illegal values
    new_legal_values = copy.deepcopy(legal_values)
    for word_val in new_legal_values[word]:
        if word_val in trash:
            new_legal_values[word].remove(word_val)

    # Recurse for each value in the queue, copying all variables
    for word_val in queue:
        new_matrix = copy.deepcopy(matrix)
        new_matrix = word_placement(new_matrix, word_val.word, word_val.position,
                                    word_val.orientation)

        new_word_list = copy.deepcopy(word_list)
        new_word_list.remove(word)

        nodes[0] += 1
        path.append(word_val)

        ret_val = sudoku(new_matrix, new_word_list, nodes, path, new_legal_values)
        if ret_val[0]:
            return ret_val
        
        path.remove(word_val)

    return (False, [])


# Top level function to handle files and initialize variables
def solve(grid, bank, solution, sequence):
    t0 = time.clock()

    matrix = cvt_matrix(grid)
    word_list = cvt_words(bank)
    nodes = [0]
    path = []

    legal_values = init_legal_values(word_list)
    ret_val = sudoku(matrix, word_list, nodes, path, legal_values)

    if ret_val[0]:
        print('Successfully Completed!')
    matrix = ret_val[1]

    tf = time.clock()

    print('Time:', tf - t0, 'sec')
    print('Nodes:', nodes[0])

    # Print solution
    with open(solution, 'w') as f:
        for row in matrix:
            print(''.join(row), file = f)
    # Print sequence
    with open(sequence, 'w') as f:
        for step in path:
            print(step.orientation, ',', step.position[0], ',', step.position[1],
                    ':', step.word, file = f)

    print_m(matrix)


###############################################################################


solve('grid1.txt', 'bank1.txt', 'solution1.txt', 'sequence1.txt')
#solve('grid2.txt', 'bank2.txt', 'solution2.txt', 'sequence2.txt')

 	

