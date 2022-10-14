#these are all the functions that update board positions around a given tile.

#obviously we're not gonna want this incrementing stuff. Instead, take the key at these locations in temp_dict and add it to fake_board_dict, so that it can 'display' those numbers. Make it so that it stops if it adds a number, which you can add to position_finder or to click_tiles. might be better to do here for simplicity


#change clicked_list to clicked_dict to reflect the changing times

#top left
def top_left_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (-length - 1))] = board_dict["tile"+ str(pos + (-length - 1))]

#top
def top_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (-length))] = board_dict["tile"+ str(pos + (-length))]
    
#top right
def top_right_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (-length + 1))] = board_dict["tile"+ str(pos + (-length + 1))]

#left
def left_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos - 1)] = board_dict["tile"+ str(pos - 1)]

#right
def right_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + 1)] = board_dict["tile"+ str(pos + 1)]

#bottom left
def bottom_left_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (length - 1))] = board_dict["tile"+ str(pos + (length - 1))]

#bottom
def bottom_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (length))] = board_dict["tile"+ str(pos + (length))]

#bottom right
def bottom_right_finder(board_dict, pos, length, chosen_click_dict):
    chosen_click_dict["tile"+ str(pos + (length + 1))] = board_dict["tile"+ str(pos + (length + 1))]

#these are all the functions that use the previous functions to check around any given position type

def top_left_batch_finder(board_dict, pos, length, chosen_click_dict):
    right_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)
    bottom_right_finder(board_dict, pos, length, chosen_click_dict)

def top_row_batch_finder(board_dict, pos, length, chosen_click_dict):
    left_finder(board_dict, pos, length, chosen_click_dict)
    right_finder(board_dict, pos, length, chosen_click_dict)
    bottom_left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)
    bottom_right_finder(board_dict, pos, length, chosen_click_dict)

def top_right_batch_finder(board_dict, pos, length, chosen_click_dict):
    left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)

def left_column_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_finder(board_dict, pos, length, chosen_click_dict)
    top_right_finder(board_dict, pos, length, chosen_click_dict)
    right_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)
    bottom_right_finder(board_dict, pos, length, chosen_click_dict)

def right_column_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_left_finder(board_dict, pos, length, chosen_click_dict)
    top_finder(board_dict, pos, length, chosen_click_dict)
    left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)

def bottom_left_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_finder(board_dict, pos, length, chosen_click_dict)
    top_right_finder(board_dict, pos, length, chosen_click_dict)
    right_finder(board_dict, pos, length, chosen_click_dict)

def bottom_row_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_left_finder(board_dict, pos, length, chosen_click_dict)
    top_finder(board_dict, pos, length, chosen_click_dict)
    top_right_finder(board_dict, pos, length, chosen_click_dict)
    left_finder(board_dict, pos, length, chosen_click_dict)
    right_finder(board_dict, pos, length, chosen_click_dict)

def bottom_right_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_left_finder(board_dict, pos, length, chosen_click_dict)
    top_finder(board_dict, pos, length, chosen_click_dict)
    left_finder(board_dict, pos, length, chosen_click_dict)

def non_side_batch_finder(board_dict, pos, length, chosen_click_dict):
    top_left_finder(board_dict, pos, length, chosen_click_dict)
    top_finder(board_dict, pos, length, chosen_click_dict)
    top_right_finder(board_dict, pos, length, chosen_click_dict)
    left_finder(board_dict, pos, length, chosen_click_dict)
    right_finder(board_dict, pos, length, chosen_click_dict)
    bottom_left_finder(board_dict, pos, length, chosen_click_dict)
    bottom_finder(board_dict, pos, length, chosen_click_dict)
    bottom_right_finder(board_dict, pos, length, chosen_click_dict)

#and this is the function that determines what type of position is being looked at in order to determine when to use the previous functions.

def position_finder(board_dict, pos, length, width, chosen_click_dict):
    if pos == 0:
        top_left_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos in range(1, length - 1):
        top_row_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos == length - 1:
        top_right_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos in range(length, ((length * width) - (2 * length)) + 1, length):
        left_column_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos in range(length * 2 - 1, (length * width) - length, length):
        right_column_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos == length * width - length:
        bottom_left_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos in range(((length * (width - 1)) + 1), length * width - 1):
        bottom_row_batch_finder(board_dict, pos, length, chosen_click_dict)
    elif pos == length * width - 1:  
        bottom_right_batch_finder(board_dict, pos, length, chosen_click_dict)
    else:
        non_side_batch_finder(board_dict, pos, length, chosen_click_dict)