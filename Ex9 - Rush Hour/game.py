import helper
import sys
from board import *
from car import *

# Game constants
VALID_CAR_NAMES = {'Y', 'G', 'B', 'O', 'W', 'R'}
VALID_CAR_DIRECT = {'u', 'd', 'l', 'r'}
VALID_ORIENTATION = [1, 0]
VALID_LOCATION_IND = [i for i in range(7)]
MIN_CAR_LEN = 2
MAX_CAR_LEN = 4


class Game:
    """
    This class represents the game itself
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self, name, movekey):
        """
        Execute one single turn of car movement
        :return:
        """
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        car_moved = self.__board.move_car(name, movekey)
        if car_moved:
            print("\nDone.")
            print(self.__board)
        else:
            print("Accidents are not allowed! Try another move :")

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        self.print_welcome()
        while True:  # iterates until goal achieved or player entered '!'
            if self.__board.cell_content(self.__board.target_location()):
                # Goal achieved !
                print("Bravoooooo!")
                break
            move_input = self.player_input()
            if move_input == '!':
                print("Goodbye!")
                break
            self.__single_turn(move_input[0], move_input[1])

    def print_welcome(self):
        """
        Prints welcome message
        :return: None
        """
        msg = "Welcome to Rush-Hour! \nCould you get one of the cars " \
              "outside the busy parking lot? \nTo move a car, enter the " \
              "car's name and direction. \nValid names : Y,B,G,O,W,R \n" \
              "Valid directions : u,d,l,r \nExit command : !\n"
        frame = "----------------------- \n"
        print(frame + msg + frame + "Game On!\n")
        print(self.__board)

    def player_input(self):
        """
        Gets valid instruction from the player : 2 letters separated by comma.
        For example : "Y,d"
        Valid names : Y,B,O,G,W,R
        Valid directions : u,d,l,r
        :return: tuple of (name, direction)
        """

        msg = "Enter your move here : "
        while True:
            player_input = input(msg)
            if player_input == '!':
                return '!'

            # Check input validity
            if len(player_input) == 3 and player_input[1] == ',':
                player_input = player_input.split(",")
                cars_poss_moves = self.__board.possible_moves()
                for move in cars_poss_moves:  # check valid name and direction
                    if player_input[0] == move[0] and player_input[1] == move[1]:
                        return player_input  # Input is valid

            msg = "Wrong name or direction were given. Please try again : "


def place_cars_in_board(board, cars):
    """
    Places cars inside the game board
    :param board: game board
    :type cars: cars to add (from class 'Car')
    :return: filled board (from class 'Board)
    """
    board = Board()
    for car in cars:
        board.add_car(car)
    return board


def create_cars(cars):
    """
    Creates cars objects from board configurations
    :param cars: dictionary of cars
    For example - {'O': [2, [2, 3], 0], 'R': [2, [0, 0], 1]}
    :return: cars list from class 'Car'
    """
    cars_list = []
    for car in cars:
        # boolean variables

        length = cars[car][0]
        location = cars[car][1]
        orientation = cars[car][2]

        is_valid_car = car in VALID_CAR_NAMES and \
                       MIN_CAR_LEN <= length <= MAX_CAR_LEN and \
                       location[0] in VALID_LOCATION_IND and \
                       location[1] in VALID_LOCATION_IND and \
                       orientation in VALID_ORIENTATION

        if is_valid_car:
            cars_list.append(Car(car, length, location, orientation))

    return cars_list


if __name__ == "__main__":
    # Creating board
    board1 = Board()

    # Loading board configurations (Cars information)
    json_file = [arg for arg in sys.argv][1]  # imports file path
    board_config = helper.load_json(json_file)  # loads json file to dict

    # Creating cars
    cars_lst = create_cars(board_config)

    # Placing cars in board
    board1 = place_cars_in_board(board1, cars_lst)

    # Running game
    rush_hour = Game(board1)  # creates game object
    rush_hour.play()  # starts game
