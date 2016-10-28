import numpy as np 
import sys
import copy
import time

#Black starts at top a.k.a y=0,1
#White starts at bottom a.k.a y=6,7
def initialize(): # try different initialization**********
    w=0
    white={}
    for j in range(board_height-2,board_height):
        for i in range(0,board_width):
            white[w]=(j,i)
            w+=1
    b=0
    black={}
    for j in range(0,2):
        for i in range(0,board_width):
            black[b]=(j,i)
            b+=1
    return white, black


# 0 is the y val and 1 is the x val
def end_case(black, white, char):
    if char=='W':
        for c in white:
            if white[c][0] == 0: # if a white piece has reached the end 
                return True
        if len(black) == 0: # if no other white piece
            return True
        return False
    elif char=='B':
        for c in black:
            if black[c][0] == 7: # if a black piece has reached the end of other side
                return True
        if len(white) == 0: #if no other white pieces
            return True
        return False      


def possible_action(black,white,char): #char tells us the possible action for whichever piece (B/W) we want to move
    action=[]
    direction={}
    possible_capture=0
    capture=0
    if char=='W':
        for w in white:
            #if(white[w][0]-1>=0 and white[w][1]+1<8 and white[w][1]-1>=0):
                #if nothing is in front and its insde the box
                if(((white[w][0]-1, white[w][1]) not in black.values()) and ((white[w][0]-1, white[w][1]) not in white.values()) and white[w][0]-1>=0):
                    action.append((w,(white[w][0]-1, white[w][1])))
                    #direction[w]=['F']
                #if possible move left
                if(((white[w][0]-1, white[w][1]-1) not in white.values()) and white[w][0]-1>=0 and white[w][1]-1>=0):
                    action.append((w, (white[w][0]-1, white[w][1]-1)))
                    #direction[w].append('L')
                #if possible move right
                if(((white[w][0]-1, white[w][1]+1) not in white.values()) and white[w][0]-1>=0 and white[w][1]+1<8):
                    action.append((w, (white[w][0]-1, white[w][1]+1)))
                    #direction[w].append('R')
                #check if there is a black piece on the rigth
                if(((white[w][0]-1, white[w][1]+1) in black.values())): # if there is a black player on the right increment possible_capture for the score
                    possible_capture+=1
                #check if there is a black piece on the left
                if(((white[w][0]-1, white[w][1]-1) in black.values())):
                    possible_capture+=1
                if (white[w][0], white[w][1]) in black.values():
                    capture += 1

        return action, possible_capture, capture
    elif char=='B':
        for b in black:
            #if(black[b][0]+1<8 and black[b][1]+1<8 and black[b][1]-1>=0):
                #if nothing is in front and its insde the box
                if(((black[b][0]+1, black[b][1]) not in black.values()) and ((black[b][0]+1, black[b][1]) not in white.values()) and black[b][0]+1<8):
                    action.append((b,(black[b][0]+1, black[b][1])))
                    #direction[b]=['F']
                #if possible move left
                if(((black[b][0]+1, black[b][1]-1) not in black.values()) and black[b][0]+1<8 and black[b][1]-1>=0):
                    action.append((b, (black[b][0]+1, black[b][1]-1)))
                    #direction[b].append('L')
                #if possible move right
                if(((black[b][0]+1, black[b][1]+1) not in black.values()) and black[b][0]+1<8 and black[b][1]+1<8):
                    action.append((b, (black[b][0]+1, black[b][1]+1)))
                    #direction[b].append('R')
                #check if there is a white piece on the right
                if(((black[b][0]+1, black[b][1]+1) in white.values())):# if there is a white player on the right increment possible_capture for the score
                    possible_capture+=1
                #check if there is a white piece on the left
                if(((black[b][0]+1, black[b][1]-1) in white.values())):
                    possible_capture+=1
                if (black[b][0], black[b][1]) in white.values():
                    capture += 1

        return action, possible_capture, capture


# write is goal state and weigh it to like 200
def goal_score(black,white,char):
    istrue=False
    if(char=='W'):
        action, possible_capture, capture=possible_action(black,white,'W')
        for vals in action:
            if(vals[1][0]==0):
                istrue=True
        if(istrue):
            return True
    elif(char=='B'):
        action, possible_capture, capture=possible_action(black,white,'B')
        for vals in action:
            if(vals[1][0]==7):
                istrue=True
        if(istrue):
            return True
    else:
        return False     

def score_o(black,white,char): #OFFENSIVE
    value=0
    if (char=='W'):
        action,possible_capture, capture=possible_action(black,white,'W')
        if(goal_score(black,white,'W')):
            value=100
        #return (7-min(white[c][0] for c in white))+len(white)
        return 10*possible_capture + len(white) + (7-min(white[c][0] for c in white)) - 0*(max(black[c][0] for c in black)) + value + sum(7-white[c][0] for c in white)
        #return possible_capture+len(white)
    elif (char=='B'):
        action,possible_capture, capture=possible_action(black,white,'B')
        if(goal_score(black,white,'B')):
            value=100
        #return max(black[c][0] for c in black)+len(black)
        return 10*possible_capture + len(black) + (max(black[c][0] for c in black)) - 0*(7-min(white[c][0] for c in white)) + value + sum(black[c][0] for c in black)
        #return possible_capture+len(black)


def score_d(black,white,char): #DEFENSIVE
    value=0
    if (char=='W'):
        action,possible_capture, capture=possible_action(black,white,'W')
        if(goal_score(black,white,'W')):
            value=100
        #return (7-min(white[c][0] for c in white))+len(white)
        return 1*possible_capture + len(white) + (7-min(white[c][0] for c in white)) - 0*(max(black[c][0] for c in black)) + value + sum(7-white[c][0] for c in white)
        #return possible_capture+len(white)
    elif (char=='B'):
        action,possible_capture, capture=possible_action(black,white,'B')
        if(goal_score(black,white,'B')):
            value=100
        #return max(black[c][0] for c in black)+len(black)
        return 1*possible_capture + len(black) + (max(black[c][0] for c in black)) - 0*(7-min(white[c][0] for c in white)) + value + sum(black[c][0] for c in black)
        #return possible_capture+len(black)


def heuristic_Offensive(black, white, char): #char is basically, whichever piece (B/W) you want to be offensive
    if (char=='W'):
        return(1.5*score_o(black,white,'W')-0.3*score_o(black,white,'B')) #if white is offensive then score of white is weighted higher than score of black
    if (char=='B'):
        return(1.5*score_o(black,white,'B')-0.3*score_o(black,white,'W')) #if black is offensive then score of black is weighted higher than score of white

def heuristic_Defensive(black,white, char): #char is basically, whichever piece (B/W) you want to be offensive
    if (char=='W'):
        return(0.3*score_d(black,white,'W')-1.5*score_d(black,white,'B')) 
    if (char=='B'):
        return(0.3*score_d(black,white,'B')-1.5*score_d(black,white,'W'))


def print_game(black, white):
    board=[]
    for x in range(8):
        array=[]
        for y in range(8):
            array.append('_')
        board.append(array)
    for c in black:
        board[black[c][0]][black[c][1]] = 'B'
    for c in white:
        board[white[c][0]][white[c][1]] = 'W'
    for line in board:
        print(line)


# Minimax search algorithm
def minimax(black, white, char, play_max, heuristic, depth, max_depth, nodes):
    nodes[0] += 1
    # Base Case: At recursion depth
    if depth == max_depth:
        if heuristic == 'offensive':
            return heuristic_Offensive(black, white, char)
        if heuristic == 'defensive':
            return heuristic_Defensive(black, white, char)

    # Recursive Case: Recurse through possible actions (child nodes)
    ret_val = possible_action(black, white, char)
    action = ret_val[0]
    children = {}
    # children = { (n, (y,x)) : value }
    # move = (n, (y,x))
    # act = (n, (y,x))

    # Evaluate children
    for move in action:
        new_white = copy.deepcopy(white)
        new_black = copy.deepcopy(black)
        if char == 'W':
            new_white[move[0]] = move[1]
        if char == 'B':
            new_black[move[0]] = move[1]
        #print_game(new_black, new_white)
        # Switch player and increment depth
        children[move] = minimax(new_black, new_white, char, not play_max, heuristic,
                                    depth + 1, max_depth, nodes)
        #print(children[act], '\n')

    # Update value based on player
    act = ()
    # Max
    if play_max:
        value = MIN
        for child in children:
            if children[child] > value:
                act = child
                value = children[child]
    # Min
    else:
        value = MAX
        for child in children:
            if children[child] < value:
                act = child
                value = children[child]

    # Update board
    captured = []
    if char == 'W':
        white[act[0]] = act[1]
        # Check if new position is in black. If so, remove black piece
        for key in black:
            if black[key] == act[1]:
                captured.append(key)
        for key in captured:
            del black[key]
    if char == 'B':
        black[act[0]] = act[1]
        # Check if new position is in white. If so, remove white piece
        for key in white:
            if white[key] == act[1]:
                captured.append(key)
        for key in captured:
            del white[key]

    return value


# Alpha-beta search algorithm
def alphabeta(black, white, char, play_max, heuristic, depth, max_depth, alpha, beta, nodes):
    nodes[0] += 1
    # Base Case: At recursion depth
    if depth == max_depth:
        if heuristic == 'offensive':
            return heuristic_Offensive(black, white, char)
        if heuristic == 'defensive':
            return heuristic_Defensive(black, white, char)

    # Recursive Case: Recurse through possible actions (child nodes)
    ret_val = possible_action(black, white, char)
    action = ret_val[0]
    children = {}
    act = ()
    # children = { (n, (y,x)) : value }
    # move = (n, (y,x))
    # act = (n, (y,x))

    # Max
    if play_max:
        value = MIN

        # Evaluate children
        for move in action:
            new_white = copy.deepcopy(white)
            new_black = copy.deepcopy(black)
            if char == 'W':
                new_white[move[0]] = move[1]
            if char == 'B':
                new_black[move[0]] = move[1]
            #print_game(new_black, new_white)
            # Switch player and increment depth
            children[move] = alphabeta(new_black, new_white, char, not play_max, heuristic,
                                        depth + 1, max_depth, alpha, beta, nodes)

            # Update value and alpha
            if children[move] > value:
                act = move
                value = children[move]
            alpha = max(value, alpha)
            if beta <= alpha:
                break
            #print(children[act], '\n')
    # Min
    else:
        value = MAX

        # Evaluate children
        for move in action:
            new_white = copy.deepcopy(white)
            new_black = copy.deepcopy(black)
            if char == 'W':
                new_white[move[0]] = move[1]
            if char == 'B':
                new_black[move[0]] = move[1]
            #print_game(new_black, new_white)
            # Switch player and increment depth
            children[move] = alphabeta(new_black, new_white, char, not play_max, heuristic,
                                        depth + 1, max_depth, alpha, beta, nodes)
            
            # Update value and alpha
            if children[move] < value:
                act = move
                value = children[move]
            alpha = min(value, alpha)
            if beta <= alpha:
                break
            #print(children[act], '\n')

    # Update board
    captured = []
    if char == 'W':
        white[act[0]] = act[1]
        # Check if new position is in black. If so, remove black piece
        for key in black:
            if black[key] == act[1]:
                captured.append(key)
        for key in captured:
            del black[key]
    if char == 'B':
        black[act[0]] = act[1]
        # Check if new position is in white. If so, remove white piece
        for key in white:
            if white[key] == act[1]:
                captured.append(key)
        for key in captured:
            del white[key]

    return value


#general running code
def play(search_w, search_b, heuristic_w, heuristic_b, max_depth):
    white,black=initialize()
    print_game(black,white)
    print()
    turn = 1 #change it to 1 if you want the other player to go first
    nodes_b = [0]
    nodes_w = [0]
    while (True):
        if (turn%2==0):

            #minmax player black
            if search_b == 'minimax':
                minimax(black, white, 'B', True, heuristic_b, 0, max_depth, nodes_b)
            #alphabeta player black
            if search_b == 'alphabeta':
                alphabeta(black, white, 'B', True, heuristic_b, 0, max_depth, MIN, MAX, nodes_b)

            turn+=1
            if(end_case(black,white,'B')):
                print("Black wins")
                print("Total turns: ", turn)
                print("Total number of white captured: ", 16-len(white))
                print("Total number of black captured: ", 16-len(black))
                print('Nodes expanded by black:', nodes_b[0])
                print('Nodes expanded by white:', nodes_w[0])
                print_game(black,white)
                break
            if search_w:
                pass
            print("Black's Turn")
            print_game(black,white)
            print()
        else:
            #minmax player white
            if search_w == 'minimax':
                minimax(black, white, 'W', True, heuristic_w, 0, max_depth, nodes_w)
            #alphabeta player white
            if search_w == 'alphabeta':
                alphabeta(black, white, 'W', True, heuristic_w, 0, max_depth, MIN, MAX, nodes_w)

            turn+=1
            if(end_case(black,white,'W')):
                print("White wins")
                print("Total turns: ", turn)
                print("Total number of white captured: ", 16-len(white))
                print("Total number of black captured: ", 16-len(black))
                print('Nodes expanded by black:', nodes_b[0])
                print('Nodes expanded by white:', nodes_w[0])
                print_game(black,white)
                break
            print("White's turn")
            print_game(black,white)
            print()
    total_nodes = nodes_b[0] + nodes_w[0]
    avg_nodes_per_move = total_nodes / turn
    print('Average nodes per move:', avg_nodes_per_move)
    return turn


###############################################################################


start_time=time.time()
board_width=8
board_height=8
MIN=-sys.maxsize-1
MAX=sys.maxsize
moves=play('alphabeta', 'minimax', 'defensive', 'defensive', 2)
end_time=time.time()
print("Total time: %s seconds" % (end_time - start_time))
print("Avg. time per move = ", ((time.time() - start_time)/moves))


