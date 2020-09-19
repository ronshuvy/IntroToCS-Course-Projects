from boggle_board_randomizer import randomize_board
from boggle_config import GameConfig as Cfg
import math


class Board:
    """
    This class represents a letters board
    """

    def __init__(self):
        self.__board = None
        self.shuffle_board()
        self.__valid_words = Cfg.load_words()
        self.__current_word = str()
        self.__selected_indices = list()  # list of tuples [(1,2), (3,4),...]

    def shuffle_board(self):
        """
        Randomizes board
        :return:
        """
        self.__board = randomize_board()

    def reset_selection(self):
        """
        Reset current letters combination
        """
        self.__current_word = str()
        self.__selected_indices.clear()

    def get_selected_indices(self):
        """
        :return: list of tuples of all selected letters indices
        """
        return self.__selected_indices.copy()

    def get_board(self):
        """
        :return: board (2D List)
        """
        return self.__board

    def get_current_word(self):
        """
        :return: current combination (string)
        """
        return self.__current_word

    def clear_current_word(self):
        self.__current_word = ""
        self.__selected_indices = []

    def cancel_letter(self, i, j):
        """
        Cancels last selection by index, if index really was the last selection.
        :param i: row
        :param j: col
        :return: True if canceled, False if not
        """
        last_selected = self.__selected_indices[-1]
        if (i, j) == last_selected:
            letter = self.__board[last_selected[0]][last_selected[1]]
            self.__selected_indices.remove(self.__selected_indices[-1])
            self.__current_word = self.__current_word[0:-len(letter)]
            return True
        return False

    def check_valid_position(self, row, col):
        """
        Checks if a given letter is adjacent to the last selected
        letter in board.
        :return: boolean value
        """
        # no possible constraints if current word combination is empty
        if not self.__selected_indices:
            return True

        # makes sure we don't add the same letter twice
        if (row, col) in self.__selected_indices:
            return False

        # stores the last selected letter's index
        i, j = self.__selected_indices[-1][0], self.__selected_indices[-1][1]

        # checks if current letter position is adjacent to last one
        if math.fabs(row - i) <= 1 and math.fabs(col - j) <= 1:
            return True
        return False

    def add_letter(self, position):
        """
        Adds a single letter to the current word combination and updates
        the indices list by the given letter position in board,
        only if letter is valid.
        :param position: index of a letter in board (row,col)
        :return: Boolean
        """
        try:  # checks position's range
            letter = self.__board[position[0]][position[1]]
        except IndexError:
            return False  # there is no such position in board

        # check proximity
        if self.check_valid_position(*position):
            self.__current_word += letter
            self.__selected_indices.append(position)
            return True
        return False

    def check_valid_word(self, word):
        """
        Checks if a given word is valid.
        :return: boolean value
        """
        return word in self.__valid_words








