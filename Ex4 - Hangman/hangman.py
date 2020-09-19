# FILE : hangman.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019 ex4

from hangman_helper import *


def letter_guess(letter, wrong_guess_lst, score, pattern, chosen_word):
    """
    Check if the player's letter appears in the chosen word.
    :param letter: player's guess
    :param wrong_guess_lst: letters which doesnt' appear in chosen word
    :param score: player's current score
    :param pattern: current pattern in game
    :param chosen_word: the randomized word
    :return: score, pattern, wrong guess list and message to user
    """
    letter = str(letter)
    if len(letter) != 1 or str.islower(letter) is False:  # Input check
        msg_to_user = "Wrong input! only one letter each time. Try again :"
    elif letter in wrong_guess_lst or letter in pattern:
        msg_to_user = "Oops! you already guessed this letter. Try a new one :"
    else:
        score -= 1
        if letter in chosen_word:
            pattern = update_word_pattern(chosen_word, pattern, letter)
            # counts how many times letter inside chosen word
            count_letter = chosen_word.count(letter)
            score += (count_letter * (count_letter + 1)) // 2
            msg_to_user = "That's right! What is your next guess ?"
        else:  # letter is not in chosen word
            wrong_guess_lst.append(letter)
            msg_to_user = "No luck this time. What is your next guess ?"
    return score, pattern, wrong_guess_lst, msg_to_user


def word_guess(word, score, chosen_word, pattern):
    """
    Checks if the word which guessed by the player is the chosen one
    and updates score and pattern
    :param word: player's guess
    :param score: player's score
    :param chosen_word: the selected word
    :param pattern: current pattern in game
    :return: score and pattern
    """
    score -= 1
    if word == chosen_word:
        # checks how many letters were revealed
        hidden_letters = pattern.count("_")
        score += (hidden_letters * (hidden_letters + 1)) // 2
        pattern = chosen_word  # all letters were found
    return score, pattern


def hint_request(score, suggested_words):
    """
    Prints suggested words as hints (the amount of words is HINT_LENGTH)
    :param score: player's current score
    :param suggested_words: list of suitable words
    :return: updated score and message to user
    """
    score -= 1

    if len(suggested_words) > HINT_LENGTH:
        fixed_sugg_words = []  # copying suggested words to new list
        n = len(suggested_words)  # n is the length of suggested words list
        for i in range(HINT_LENGTH):
            word = suggested_words[n * i // HINT_LENGTH]
            fixed_sugg_words.append(word)
        suggested_words = fixed_sugg_words

    show_suggestions(suggested_words)
    msg_to_user = "Helpful enough? then what is your next guess?"
    return score, msg_to_user


def filter_words_list(words, pattern, wrong_guess_list):
    """
    Filters words which doesn't match the pattern
    :param words: list of potential words
    :param pattern: the current pattern in-game
    :param wrong_guess_list: letters which doesn't appear inside the word
    :return: words which matches the pattern
    """
    potential_words = []
    for word in words:
        valid_word = True  # every word has a potential to match the pattern
        if len(word) != len(pattern):
            continue  # current word doesn't match, move to the next word
        for char in wrong_guess_list:
            if char in word:
                valid_word = False  # current word doesn't match
                break
        if not valid_word:
            continue  # found wrong letter, move on to the next word
        for i in range(len(pattern)):
            if (pattern[i] != "_" and pattern[i] != word[i])\
                    or (pattern[i] == "_" and word[i] in pattern):
                valid_word = False  # current word doesn't match
                break
        if valid_word:  # word does match!
            potential_words.append(word)
    return potential_words


def update_word_pattern(word, pattern, letter):
    """
    Fills in the pattern with a given letter
    :param word: the selected word
    :param pattern: the current pattern
    :param letter: correct guess of letter by the user
    :return: updated pattern
    """
    for i in range(len(word)):
        if letter == word[i]:
            pattern = pattern[:i] + letter + pattern[i + 1:]
    return pattern


def run_single_game(words_list, score):
    """
    Runs single game
    :param words_list: list of words from which we choose random word
    :param score: amount of points belongs to player
    :return: total player's score
    """

    # Game initialization
    chosen_word = get_random_word(words_list)
    wrong_guess_lst = []
    pattern = "_" * len(chosen_word)
    msg_to_user = "LET'S GO! What is your first guess ? "

    # Game starts
    while (score > 0) and ("_" in pattern):
        display_state(pattern, wrong_guess_lst, score, msg_to_user)
        guess = get_input()

        # Player guessed a letter
        if guess[0] == LETTER:
            score, pattern, wrong_guess_lst, msg_to_user = letter_guess\
                (guess[1], wrong_guess_lst, score, pattern, chosen_word)
            continue

        # Player guessed a word
        elif guess[0] == WORD:
            score, pattern = word_guess\
                (guess[1], score, chosen_word, pattern)
            if pattern != chosen_word:
                msg_to_user = "Incorrect! What is your next guess?"
            continue

        # Player asks for a hint
        elif guess[0] == HINT:
            suggested_words = filter_words_list(words_list, pattern,
                                                wrong_guess_lst)
            score, msg_to_user = hint_request(score, suggested_words)

    # Game ends
    if "_" not in pattern:
        msg_to_user = "Congratulations! You guessed it right!"
        display_state(pattern, wrong_guess_lst, score, msg_to_user)
    else:
        msg_to_user = "Game over! the mysterious word was : " + chosen_word
        display_state(pattern, wrong_guess_lst, score, msg_to_user)
    return score


def main():
    """
    Main function
    :return: none
    """
    words_list = load_words()
    points = POINTS_INITIAL
    games_played = 0
    game_on = True

    while game_on:
        # Start game
        points = run_single_game(words_list, points)
        games_played += 1

        # End game
        if points > 0:  # Player has points
            game_on = play_again("Games played so far : " + str(games_played)
                                 + " , Current amount of points :" +
                                 str(points) + " Continue playing?")

        else:  # No points were left
            game_on = play_again("Total games played : "
                                 + str(games_played) + " , Play again?")
            if game_on:
                games_played = 0
                points = POINTS_INITIAL


if __name__ == "__main__":
    main()
