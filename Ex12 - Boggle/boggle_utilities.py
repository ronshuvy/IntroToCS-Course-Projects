from board import Board
from boggle_config import GameConfig as Cfg


class Utilities:
    """
    This class is the logic unit in the app
    """
    def __init__(self, app):
        self.__app = app
        self.__board = Board()
        self.__score = Cfg.SCORE_BASE
        self.__correct_words = list()
        self.__wrong_words = list()

    def get_board(self):
        """
        :return: board (2D list)
        """
        return self.__board

    def get_score(self):
        """
        :return:
        """
        return self.__score

    def reset(self):
        """
        Reset game data and shuffles the board
        :return:
        """
        self.__board.shuffle_board()
        self.__score = 0
        self.__correct_words.clear()
        self.__wrong_words.clear()

    def add_score(self, score):
        """
        Adds more points to total score
        :param score: points to add (integer)
        :return: None
        """
        self.__score += score

    def buy_time(self):
        """
        Adds more time and subtracts score points,
        only if the player has enough score.
        :return: None
        """
        if not self.__app.get_time_left():
            return
        if self.__score >= Cfg.MIN_SCORE_FOR_BUY_TIME:
            self.__score -= Cfg.TIME_PRICE
            self.__app.add_time(Cfg.EXTRA_SECONDS)
            self.__app.show_message("Enjoy your extra 30 seconds!")
            self.__app.refresh()
        else:
            self.__app.show_message("You must have at least 20 points")

    def get_correct_words_list(self):
        """
        :return: the correct words list
        """
        return self.__correct_words

    def get_wrong_words_list(self):
        """
        :return: the wrong words list
        """
        return self.__wrong_words

    def add_word(self, word):
        """
        Check if the word is valid and add it to the fitting list
        :param word: word to add
        :return: Tuple (valid, msg)
        """
        if len(word) < 2:
            return False, "Please choose at least two letters."
        if word not in self.__correct_words and word not in self.__wrong_words:
            if self.check_valid_word(word):
                self.__correct_words.append(word)
                pts = Cfg.score_calc(word)
                self.__score += pts
                self.__app.refresh()
                return True, "Yes! "+str(pts)+" Points!"
            else:
                self.__wrong_words.append(word)
                return False, "Oops! Try again."
        return None, "You already tried that."

    @staticmethod
    def check_valid_word(word):
        """
        Checks if a given word is valid
        :return: boolean value
        """
        return word in Cfg.load_words()
