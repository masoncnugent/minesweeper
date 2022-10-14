#these are all the functions that increment board positions around a given tile.

#top left
def top_left_incrementer(board, pos, length):
    board[(pos + (-length - 1))] += 1

#top
def top_incrementer(board, pos, length):
    board[(pos + (-length))] += 1
    
#top right
def top_right_incrementer(board, pos, length):
    board[(pos + (-length + 1))] += 1

#left
def left_incrementer(board, pos, length):
    board[(pos - 1)] += 1

#right
def right_incrementer(board, pos, length):
    board[(pos + 1)] += 1

#bottom left
def bottom_left_incrementer(board, pos, length):
    board[(pos + (length - 1))] += 1

#bottom
def bottom_incrementer(board, pos, length):
    board[(pos + (length))] += 1

#bottom right
def bottom_right_incrementer(board, pos, length):
    board[(pos + (length + 1))] += 1

#these are all the functions that use the previous functions to increment around any given position type

def top_left_batch_incrementer(board, pos, length):
    right_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)
    bottom_right_incrementer(board, pos, length)

def top_row_batch_incrementer(board, pos, length):
    left_incrementer(board, pos, length)
    right_incrementer(board, pos, length)
    bottom_left_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)
    bottom_right_incrementer(board, pos, length)

def top_right_batch_incrementer(board, pos, length):
    left_incrementer(board, pos, length)
    bottom_left_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)

def left_column_batch_incrementer(board, pos, length):
    top_incrementer(board, pos, length)
    top_right_incrementer(board, pos, length)
    right_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)
    bottom_right_incrementer(board, pos, length)

def right_column_batch_incrementer(board, pos, length):
    top_left_incrementer(board, pos, length)
    top_incrementer(board, pos, length)
    left_incrementer(board, pos, length)
    bottom_left_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)

def bottom_left_batch_incrementer(board, pos, length):
    top_incrementer(board, pos, length)
    top_right_incrementer(board, pos, length)
    right_incrementer(board, pos, length)

def bottom_row_batch_incrementer(board, pos, length):
    top_left_incrementer(board, pos, length)
    top_incrementer(board, pos, length)
    top_right_incrementer(board, pos, length)
    left_incrementer(board, pos, length)
    right_incrementer(board, pos, length)

def bottom_right_batch_incrementer(board, pos, length):
    top_left_incrementer(board, pos, length)
    top_incrementer(board, pos, length)
    left_incrementer(board, pos, length)

def non_side_batch_incrementer(board, pos, length):
    top_left_incrementer(board, pos, length)
    top_incrementer(board, pos, length)
    top_right_incrementer(board, pos, length)
    left_incrementer(board, pos, length)
    right_incrementer(board, pos, length)
    bottom_left_incrementer(board, pos, length)
    bottom_incrementer(board, pos, length)
    bottom_right_incrementer(board, pos, length)

#and this is the function that determines what type of position is being looked at in order to determine when to use the previous functions.

def position_incrementer(board, pos, length, width):
    if pos == 0:
        top_left_batch_incrementer(board, pos, length)
    elif pos in range(1, length - 1):
        top_row_batch_incrementer(board, pos, length)
    elif pos == length - 1:
        top_right_batch_incrementer(board, pos, length)
    elif pos in range(length, ((length * width) - (2 * length)) + 1, length):
        left_column_batch_incrementer(board, pos, length)
    elif pos in range(length * 2 - 1, length * width - length, length):
        right_column_batch_incrementer(board, pos, length)
    elif pos == length * width - length:
        bottom_left_batch_incrementer(board, pos, length)
    elif pos in range(((length * (width -1)) + 1), length * width - 1):
        bottom_row_batch_incrementer(board, pos, length)
    elif pos == length * width - 1:  
        bottom_right_batch_incrementer(board, pos, length)
    else:
        non_side_batch_incrementer(board, pos, length)