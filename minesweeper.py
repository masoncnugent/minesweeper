from random import shuffle
from datetime import datetime
from mineremover import mine_remover
from positionincrementer import position_incrementer
from positionfinder import position_finder

#class creation

class Tile:
    def __init__(self, identity, position, is_clicked = False, is_flagged = False):
        self.identity = identity
        self.position = position
        self.is_clicked = is_clicked
        self.is_flagged = is_flagged

    def clicked(self):
        self.is_clicked = True

    def __repr__(self):
        return "hello i am a " + str(self.identity) + " at position " + str(self.position) + " and I am " + str(self.is_clicked) + " clicked."


class Board:

    def __init__(self, length, width, mine_num, first_click):
        self.first_click = first_click
        self.length = length
        self.width = width
        self.mine_num = mine_num
        self.mine_list = []
        self.tile_data = self.board_to_tiles()
        self.player_tile_data = self.player_board_maker()
        self.turn_count = 0
        self.clicked_count = 0
        self.game_over = False
        self.win_condition = False
        self.creation_time = datetime.now()

    #sets all the functions in motion that will fill self.tile_data with the correct data structure for display and gameplay
    def board_to_tiles(self):
        return self.tile_maker(self.data_board_maker(self.add_mines(self.blank_board([]))))

    #makes a board with the dimensions of length x width
    def blank_board(self, board):
        for num in range(0, self.length * self.width):
            board.append(0)
        return board

    #adds 'mines', or rather, 9's to the board made by self.blank_board()
    def add_mines(self, board):
        #this if statement is an optimization for if you have more mines than regular tiles, at which point the regular tiles should be chosen randomly and not the mines
        if self.mine_num > self.length * self.width / 2:
            random_mine_option_list = []
            random_mine_option_removal_list = []
            for num in range(0, self.length * self.width):
                random_mine_option_list.append(num)

            random_mine_option_removal_list.append(self.first_click)
            mine_remover(random_mine_option_removal_list, self.first_click, self.length, self.width)

            #removes the areas where a mine can't be so the first click is a 0
            for non_mine in random_mine_option_removal_list:
                random_mine_option_list.remove(non_mine)

            #randomizes what areas can't be mines
            shuffle(random_mine_option_list)

            #this range and how self.mine_list is determined are the only differences between this case where there are more mines than tiles and the else case.
            for num in range(0, self.length * self.width - self.mine_num):
                non_mine = random_mine_option_list[0]
                random_mine_option_list.pop(0)
            
            self.mine_list = random_mine_option_list
        
        else:
            random_mine_option_list = []
            random_mine_option_removal_list = []
            for num in range(0, self.length * self.width):
                random_mine_option_list.append(num)

            random_mine_option_removal_list.append(self.first_click)
            mine_remover(random_mine_option_removal_list, self.first_click, self.length, self.width)

            #removes the areas where a mine can't be so the first click is a 0
            for non_mine in random_mine_option_removal_list:
                random_mine_option_list.remove(non_mine)

            #randomizes the random_mine_option_list once]
            shuffle(random_mine_option_list)

            #gives self.mine_list the chosen mines that are not around the self.first_click
            for num in range(0, self.mine_num):
                mine = random_mine_option_list[0]
                random_mine_option_list.pop(0)
                self.mine_list.append(mine)

        #this doesn't modify board yet, but it needs to be returned for data_board_maker()
        return board

    #runs position_incrementer() to fill out the board for the creation of tiles by self.tile_maker()
    def data_board_maker(self, board):
        for mine in self.mine_list:
            position_incrementer(board, mine, self.length, self.width)
        #prevents the mines from having a value greater than 9
        for mine in self.mine_list:
            board[mine] = 9
        return board

    #now that the board is set up as a list proper, self.tile_maker() can use it to update tile_dict, which will become self.tile_data. i did this because python tutorials espoused this to be the only way to make dynamic variables. otherwise, i would've just made a list of tile objects, (from the tile class,) which would be a lot easier to work with. the keys hold no information, and make syntax harder to read
    def tile_maker(self, data_set):
        tile_dict = {}
        counter = 0
        for data in data_set:
            tile_dict["tile{num}".format(num = str(counter))] = Tile(data, counter)
            counter += 1
        return tile_dict

    #displays a board in dictionary form, whether the self.tile_data or self.player_tile_data
    def display_board(self, dictionary):
        counter = 0
        temp_row = []
        for tile in dictionary:
            tile_id = dictionary["tile" + str(counter)].identity
            if dictionary["tile" + str(counter)].is_flagged == True:
                tile_id = "!"
            counter += 1
            if counter % self.length == 0:
                temp_row.append(str(tile_id))
                temp_row_no_quotes = '[' + ', '.join(temp_row) + ']'
                print(temp_row_no_quotes)
                temp_row = []
            else:
                temp_row.append(str(tile_id))

    #displays the board of question marks before the first click, since the board isn't made yet
    @classmethod
    def first_display_board(cls, length, width):
        counter = 0
        temp_row = []
        for num in range(length * width):
            counter += 1
            if counter % length == 0:
                temp_row.append("?")
                temp_row_no_quotes = '[' + ', '.join(temp_row) + ']'
                print(temp_row_no_quotes)
                temp_row = []
            else:
                temp_row.append("?")

    #makes the board that is displayed to the player
    def player_board_maker(self):
        player_board_dict = {}
        for num in range(0, self.length * self.width):
            player_board_dict["tile" + str(num)] = Tile("?", num)
        return player_board_dict

    #checks the positions around tiles systematically to determine which tiles should be shown to the player and which should be hidden. it also tracks revealed tiles for the win condition
    def click_tiles(self, click_choice):
        self.turn_count += 1

        clicked_tiles = {}

        #an optimization that allows us to not iterate over those tiles who already have a self.is_clicked value of True. they are removed from clicked_tiles so that the 'while dict_comparer...' loop has to iterate over fewer things. they are eventually added to player_tile_data in the end, but are not iterated over beyond being added once and then checked again at the end.
        checked_tiles = {}

        previous_clicked_tiles = {}

        clicked_tiles["tile" + str(click_choice)] = self.tile_data["tile" + str(click_choice)]

        #game_over condition. if the player clicked a mine, the game is over
        if clicked_tiles["tile" + str(click_choice)].identity == 9:
            self.set_game_over()

        #this is used to compare dictionaries such that position_finder() is actually adding new tiles to self.player_tile_data. if it isn't, and self.tile_data and self.player_tile_data have the same data in them, then position checking can stop, since all revealed tiles would already be revealed
        def dict_comparer(dicta, dictb):
            for data in dicta:
                if data in dictb:
                    continue
                else:
                    return False
            return True
        
        #clicks a given tile after it has had its position checked, which allows for resources to be saved over checking the same tiles each iteration of position_checker(). tiles that aren't 0 also don't get checked, although they get added to self.player_tile_data once clicked_tiles and previous_clicked_tiles are equivalent.
        def dict_data_is_clicked(dicta, dictb):
            for data in dicta:
                if data in dictb:
                    if dicta[data].is_clicked == False:
                        dicta[data].clicked()

        #clicks tiles only when position_finder() is finding new tiles
        while dict_comparer(clicked_tiles, previous_clicked_tiles) == False:
            previous_clicked_tiles = clicked_tiles.copy()
            for tile in clicked_tiles.copy():
                if clicked_tiles[tile].is_clicked == True:
                    checked_tiles["tile" + str(clicked_tiles[tile].position)] = clicked_tiles[tile]
                    del clicked_tiles[tile]
                    #previous_clicked_tiles has to have its tiles removed too, since otherwise dict_comparer would errantly think dicta and dictb are equivalent. it only compares dicta to dictb in the assumption that dicta is larger than dictb, which was always true before checked_tiles was implemented. this is an extra step, but a necessary one
                    del previous_clicked_tiles[tile]
                    continue
                
                self.clicked_count += 1
                if clicked_tiles[tile].identity != 0:
                    continue

                #this should work as before, except now clicked_tiles will only have non-checked tiles, allowing for huge datasets of clicked tiles to only be iterated over once and put into checked_tiles
                tile_pos = clicked_tiles[tile].position
                position_finder(self.tile_data, tile_pos, self.length, self.width, clicked_tiles)

            #clicks those in clicked_tiles that were in clicked_tiles for the previous iteration of the loop, so they can be moved into checked_tiles
            dict_data_is_clicked(clicked_tiles, previous_clicked_tiles)

        #one last run of position_finder() to get all the numbers in self.player_tile_data
        for tile in checked_tiles.copy():
            if checked_tiles[tile].identity != 0:
                continue

            tile_pos = checked_tiles[tile].position
            position_finder(self.tile_data, tile_pos, self.length, self.width, checked_tiles)

        #on any click after the first of the game, if it is not a 0, this fixes the fact that it wouldn't yet be .is_clicked == True to give to checked_tiles and therefore self.player_tile_data for display
        if tile in clicked_tiles:
            self.player_tile_data[tile] = clicked_tiles[tile]

        #updates self.player_tile_data with all the tiles in checked_tiles
        for tile in checked_tiles:
            self.player_tile_data[tile] = checked_tiles[tile]

        #checks to see if the player won after clicking
        if self.clicked_count == self.length * self.width - self.mine_num:
            self.set_win_condition()
    
    #allows players to flag tiles
    def flag_tile_toggle(self, flag_choice):
        if self.player_tile_data["tile" + str(flag_choice)].identity == "?":
            if self.player_tile_data["tile" + str(flag_choice)].is_flagged == False:
                self.player_tile_data["tile" + str(flag_choice)].is_flagged = True
            else:
                self.player_tile_data["tile" + str(flag_choice)].is_flagged = False

    #makes the instance of the board that the player plays on. it is a class method since it runs Board.game_first_move(), which makes sure the first move does not result in the game-over state
    @classmethod
    def board_instance_maker(cls):
        valid_board = False
        while valid_board == False:
            try:
                length = int(input("What is the length for the board you want? "))
                width = int(input("\nWhat is the width for the board you want? "))
                mine_num = int(input("\nHow many mines do you want? "))
                print("")
            except:
                print("")
                continue

            if mine_num > length * width - 9 or length > 1000 or width > 1000:
                print("Invalid minesweeper board dimensions:\nLength: 1 to 1000\nWidth: 1 to 1000\nMine Number: Length * Width - 9\n")
                continue
            else:
                valid_board = True

        #displays the board before it's made, so the player knows where they can click
        cls.first_display_board(length, width)
        print("")

        #makes sure the first click follows the correct formatting for entry into self.first_click in the final board instance
        first_click = cls.game_first_click(length, width)

        #makes the board_instance that the game is played on. it will be returned for assignment to the variable 'board'
        board_instance = Board(length, width, mine_num, first_click)

        #uses the first click made by the class method Board.game_first_click() so that the board instance knows where not to place mines
        board_instance.click_tiles(board_instance.first_click)

        #displays the board instance to the player
        board_instance.display_board(board_instance.player_tile_data)

        #returns the instance of the board so its methods can be used for the self.game_while_loop()
        return board_instance

    #this is the first move of the board, which makes sure the players first click isn't a mine. for this reason, it has to be a class method and not an instance method, since the instance is made wherein the first click is not a mine. otherwise, 're-rolling' large boards would be costly
    @classmethod
    def game_first_click(cls, length, width):
        first_click = input("Click a tile to start! Simply input \'c\' followed by a number between 0 and " + str(length * width - 1) + " to denote the tile you wish to click.\n")
        print("")
        try:
            if int(first_click[1:]) >= length * width or first_click[0] != "c":
                return cls.game_first_click(length, width)
            else:
                return int(first_click[1:])
        except:
            print("")
            cls.first_display_board(length, width)
            return cls.game_first_click(length, width)

    #this is the game loop for taking the bulk of input from the player
    def game_while_loop(self):
            while self.game_over == False and self.win_condition == False:
                choice = input("\nTo click a tile, input \'c\' followed by a number between 0 and " + str(self.length * self.width - 1) + " to denote the tile you wish to click.\nTo flag a tile, input \'f\' followed by a number between 0 and " + str(self.length * self.width - 1) + " to denote the tile you wish to flag.\nTo reset the game, input \'r\' by itself.\n")
                print("")
                try:
                    if choice[0].lower() == "c" and int(choice[1:]) < self.length * self.width:
                        self.click_tiles(int(choice[1:]))
                    elif choice[0].lower() == "f" and int(choice[1:]) < self.length * self.width:
                        self.flag_tile_toggle(int(choice[1:]))
                    elif (choice.lower()) == "r":
                        self.reset_board()
                        
                except:
                    self.display_board(self.player_tile_data)
                    self.game_while_loop()

                else:
                    self.display_board(self.player_tile_data)

    #resets the board instance at the players choosing
    def reset_board(self):
        valid_board = False
        while valid_board == False:
            try:
                length = int(input("What is the length for the board you want? "))
                width = int(input("\nWhat is the width for the board you want? "))
                mine_num = int(input("\nHow many mines do you want? "))
                print("")
            except:
                print("")
                continue

            if mine_num > length * width - 9 or length > 1000 or width > 1000:
                print("Invalid minesweeper board dimensions:\nLength: 1 to 1000\nWidth: 1 to 1000\nMine Number: Length * Width - 9\n")
                continue
            else:
                valid_board = True

        self.length = length
        self.width = width
        self.mine_num = mine_num
        Board.first_display_board(length, width)
        print("")

        self.first_click = Board.game_first_click(length, width)
        self.mine_list = []
        self.tile_data = self.board_to_tiles()
        self.player_tile_data = self.player_board_maker()
        self.turn_count = 0
        self.clicked_count = 0
        self.game_over = False
        self.win_condition = False
        self.creation_time = datetime.now()

        self.click_tiles(self.first_click)

    #sets the self.game_over instance variable to True, which ends the while loop in run_game, causing the 'game-over' screen
    def set_game_over(self):
        self.game_over = True
    
    #sets the self.win_condition instance variable to True, which ends the while loop in run_game, causing the 'win' screen
    def set_win_condition(self):
        self.win_condition = True

    def print_game_result(self):
        end_time = datetime.now()
        if self.game_over == True:
            reset_state = False
            while reset_state == False:
                    reset_input = input("\nYour game has ended in " + str(self.turn_count) + " clicks and " + str(end_time - self.creation_time) + " seconds. You lost. Input \'r\' to try again.\n")
                    try:
                        if reset_input.lower() == "r":
                            print("")
                            reset_state = True
                            self.reset_board()
                        else:
                            continue
                    except:
                        continue
        else:
            reset_state = False
            while reset_state == False:
                    reset_input = input("\nYour game has ended in " + str(self.turn_count) + " clicks and " + str(end_time - self.creation_time) + " seconds. You won! Input \'r\' to play again.\n")
                    try:
                        if reset_input.lower() == "r":
                            print("")
                            reset_state = True
                            self.reset_board()
                        else:
                            continue
                    except:
                        continue
        self.display_board(self.player_tile_data)
        self.game_while_loop()
        self.print_game_result()

def run_game():

    board = Board.board_instance_maker()
    #board.display_board(board.tile_data)
    #print("")

    board.game_while_loop()

    board.print_game_result()

run_game()

#footnotes ~

#oldest working implementation took 21 seconds to do boardtemp.click_tiles with unoptimized position checking of a 100x100 board
#optimization via memoization brought this down to 80ms on the building of the board and 280ms to process a click, for the same 100x100 board. roughly a 75x improvement. taking 21s with this more updated optimization requires a ~430x430 board.
#the 'real game' with its ui and everything takes ~.8-.9 of a second to check the center of a board of the 100x100 size
#checked_tiles optimization brought a 1000x1000 board with 10000 mines at c500500 from 70 seconds down to a consistent 27. checked_tiles scales with the size of the board as an optimization, possibly (unlikely) slowing down smaller boards. considering how mine creation follows this first click now, total optimizations might approach >100x
#updating how mines are created to a single time shuffle() greatly sped up mine creation. Creation of 500,000 mines still takes several minutes, likely due to how shuffle scales with list size, but the click is at most 27 seconds for a 1000x1000 board
#final build is harder to time with date_time()