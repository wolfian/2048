# 2048 text-mode

import random, os, copy
from tabulate import tabulate

random_index = lambda : random.randint(0,3)

# weights set the probablity of occurence for elements from list
# k is how many elements to return
# random.choices(,,) returns a list
random_value = lambda : (random.choices([2,4], weights=(75, 25), k=1))[0]

def initialize(box): # provides starting numbers for the game
    filled = 1
    while filled <= 2:
        row = random_index()
        col = random_index()
        if box[row][col] == '-':
            box[row][col] = random_value()
            filled += 1
    return box

def add_new_number(box): # add any of 2 or 4 and random empty spot
    while True:
        row = random_index()
        col = random_index()
        if box[row][col] == '-':
            box[row][col] = random_value()
            break

def display_box(box): # displays 2x2 list (gamebox)
    print(f'\n{tabulate(box, tablefmt="grid")}')

def left_shift(row): # helper recursive function for left_play()
    for col in range(0, len(row)-1, 1): # shift elements left
        if row[col] == '-' and row[col+1] != '-':
            row[col] = row[col+1]
            row[col+1] = '-'
            left_shift(row)
    return row

def left_play(mode, box): # score is added only when mode is 1
    # 1. if 2 same numbers are in consecutive place, merge them onto left spot
    # 2. move all elements to empty left places
    for row in range(len(box)):
        # shifting left
        left_shift(box[row])
        # add same numbers
        for col in range(0, len(box[0])-1, 1): 
            if box[row][col+1] == box[row][col] and (box[row][col] != '-' or box[row][col+1] != '-'):
                box[row][col] = 2*box[row][col]
                box[row][col+1] = '-'
                # inrementing score
                if mode == 1:
                    globals()['score'] += box[row][col]
        # shifting left again to fill new middle spaces
        left_shift(box[row]) 
    return box

def right_shift(row): # helper recursive function for right_play()
    for col in range(len(row)-1, 0, -1): # right shift elements
        if row[col] == '-' and row[col-1] != '-':
            row[col] = row[col-1]
            row[col-1] = '-'
            right_shift(row)
    return row 

def right_play(mode, box): # score is added only when mode is 1
    # 1. if 2 same numbers are in consecutive places, merge them onto right spot
    # 2. move all elements to empty right places
    for row in range(len(box)):
        # shifting right
        right_shift(box[row])
        # add same numbers
        for col in range(len(box[0])-1, 0, -1):
            if  box[row][col-1] ==  box[row][col] and  box[row][col] != '-':
                box[row][col] = 2*box[row][col]
                box[row][col-1] = '-'
                # inrementing score
                if mode == 1:
                    globals()['score'] += box[row][col]
        # shifting right again to fill new middle spaces
        right_shift(box[row])
    return box

def up_play(mode, box): # score is added only when mode is 1
    # 1. if 2 same numbers are in consecutive places, merge them onto upper spot
    # 2. move all elements to empty upper places
    for col in range(len(box[0])):
        currentCol = [] # taking each column one by one
        for row in range(len(box)):
            currentCol.append(box[row][col])
        # performing left_play() pattern on current row
        left_shift(currentCol)
        for row in range(0, len(box)-1, 1):
            if currentCol[row+1] == currentCol[row] and currentCol[row] != '-':
                currentCol[row] = 2*currentCol[row]
                currentCol[row+1] = '-'
                # inrementing score
                if mode == 1:
                    globals()['score'] += currentCol[row]
        left_shift(currentCol)
        #storing new column values back in box
        for row in range(len(box)):
            box[row][col] = currentCol[row]
    return box

def down_play(mode, box): # score is added only when mode is 1
    # 1. if 2 same numbers are in consecutive places, merge them onto lower spot
    # 2. move all elements to empty lower places
    for col in range(len(box[0])):
        currentCol = [] # taking each column one by one
        for row in range(len(box)):
            currentCol.append(box[row][col])
        # performing right_play() pattern on current row
        right_shift(currentCol)
        for row in range(len(box)-1, 0, -1):
            if currentCol[row-1] == currentCol[row] and currentCol[row] != '-':
                currentCol[row] = 2*currentCol[row]
                currentCol[row-1] = '-'
                # inrementing score
                if mode == 1:
                    globals()['score'] += currentCol[row]
        right_shift(currentCol)
        #storing new column values back in box
        for row in range(len(box)):
            box[row][col] = currentCol[row]
    return box

def game_over(temp):
    # create 4 copies of existing copy to check if any more moves possible at all
    temp1 = copy.deepcopy(temp)
    temp2 = copy.deepcopy(temp)
    temp3 = copy.deepcopy(temp)
    temp4 = copy.deepcopy(temp)
    left_play(0, temp1)
    right_play(0, temp2)
    up_play(0, temp3)
    down_play(0, temp4)
    if temp == temp1 == temp2 == temp3 == temp4:
        # if all the moves give similar table back, game over
        return True
    else:
        return False

# title = ''' _____   _____    ___  _____
# / __  \ |  _  |  /   ||  _  |
# `'  / /'| |/' | / /| | \ V / 
#    / /  |  /| |/ /_| | / _ \ 
#  ./ /___\ |_/ /\___  || |_| |
#  \_____/ \___/     |_/\_____/'''

title = ''' ___   ___    __   ___ 
(__ \ / _ \  /. | ( _ )
 / _/( (_) )(_  _)/ _ \\
(____)\___/   (_) \___/'''

box = [
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-']
]

box = initialize(box)

score = 0

while True: # main loop
    os.system('clear')
    print(title)
    print(f"\n\nScore: {score}")
    display_box(box)

    while True: # loop for user input
        try:
            swipe = input("\nIn which direction you want to swipe?\n\nW = Up\nA = Left\nS = Down\nD = Right\n\n> ")
            if swipe not in ['w', 'a', 's', 'd', 'W', 'A', 'S', 'D']:
                raise Exception("Invalid option!\nYou can only choose from W, A, S or D\n")
            else:
                break
        except Exception as err:
            print(err)

    temp = copy.deepcopy(box) # copy to check whether anymore moves in a particular direction possible

    addNewValue = True # bool to check whether to add new value or not

    if swipe == 'a' or swipe == 'A': #left
        left_play(1, box)
        if temp == box:
            addNewValue = False

    elif swipe == 'd' or swipe == 'D': # right
        right_play(1, box)
        if temp == box:
            addNewValue = False
    
    elif swipe == 'w' or swipe == 'W': # up
        up_play(1, box)
        if temp == box:
            addNewValue = False
    
    elif swipe == 's' or swipe == 'S': # down
        down_play(1, box)
        if temp == box:
            addNewValue = False
    
    if addNewValue == True:
        add_new_number(box) # to add new value 

    check = game_over(temp) # passing copy of box to check if anymore moves are possibe

    if check == True:
        break

os.system('clear')
print(title)
print(f"\n\nScore: {score}")
display_box(box)
print(f"\nGAME OVER")
quit()
