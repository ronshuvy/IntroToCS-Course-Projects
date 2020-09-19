
class GameConfig:

    @staticmethod
    def load_words(file='boggle_dict.txt'):
        """
        Loads a list of words from boggle_dict.txt file
        :param file: The file of words
        :return: A list containing all the words from the file
        """
        with open(file) as f:
            words = {line.strip() for line in f}
        return words

    @staticmethod
    def score_calc(word):
        length = len(word)
        return length ** 2

    MIN_SCORE_FOR_BUY_TIME = 20
    TIME_PRICE = 10
    EXTRA_SECONDS = 30
    GAME_TIME = 180  # seconds
    SCORE_BASE = 0
    WELCOME_MSG = "Welcome to Boggle! :)"

