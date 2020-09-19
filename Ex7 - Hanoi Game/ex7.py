# FILE : ex7.py
# WRITER : Ron Shuvy, ronshuvy, 206330193
# EXERCISE : intro2cs1 2019 ex7


def print_to_n(n):
    """
    Prints all integers between 1 to n
    :param n: last natural number to print
    :return: None
    """
    if n < 1:
        return
    print_to_n(n-1)
    print(n)


def digit_sum(n):
    """
    Returns the sum of all the number digits
    :param n: an integer
    :return: None
    """
    if n < 10:
        return n
    return digit_sum(n//10) + (n % 10)


def is_prime(n):
    """
    Checks if n is a prime number
    :param n: an integer
    :return: True if n is a prime number, False otherwise.
    """
    if n < 2:
        return False
    return _is_prime_helper(n, 2, int(n**(1/2)))


def _is_prime_helper(n, i, last):
    """
    Checks if n is a prime number
    :param n:  a given integer
    :param i: the integer we divide by each time
    :param last: the last integer to divide by
    :return: True if n is a prime, False otherwise
    """
    if last < 2 or last < i:
        return True  # n is prime
    if n % i == 0:
        return False  # n is not a prime

    return _is_prime_helper(n, i+1, last)


def play_hanoi(hanoi, n, src, dst, temp):
    """
    Solves the Tower of Hanoi puzzle by moving all the disks from the source
    rod to the destination rod.
    :param hanoi: the graphical game object
    :param n: number of disks to move
    :param src: the rod from which we move the disks
    :param dst: the rod we move the disks to
    :param temp: a temporary rod
    :return: None

    author's note :
    "“Simplicity is the final achievement.
    After one has played a vast quantity of notes and more notes,
    it is simplicity that emerges as the crowning reward of art.”
    - Frederic Chopin
    """
    # objective reached
    if n < 1:
        return

    # objective is not reached yet

    # arrange (n-1) discs on a temporary rod
    play_hanoi(hanoi, n-1, src, temp, dst)

    # move the biggest disc to the destination rod
    hanoi.move(src, dst)

    # move (n-1) discs to the destination rod
    play_hanoi(hanoi, n-1, temp, dst, src)


def print_sequences(char_list, n):
    """
    Prints all combinations in size of n of chars in a given list by using
    helper function
    :param char_list: list of chars
    :param n: number of chars in each combination
    :return:
    """
    if n < 1:
        return
    _print_sequences_helper(char_list, n, "")


def _print_sequences_helper(char_list, n, word):
    """
    Prints all combinations in size of n of chars in a given list
    :param char_list: list of chars
    :param n: number of chars in each combination
    :param word: the printed word each time
    :return:
    """
    if n == 1:
        for char in char_list:
            print(word + char)
        return

    for char in char_list:
        word += char
        _print_sequences_helper(char_list, n-1, word)
        word = word[:-1]


def print_no_repetition_sequences(char_list, n):
    """
    Prints all combinations in size of n of chars in a given list with no
    repetition
    :param char_list: list of chars
    :param n: number of chars in each combination
    :return:
    """
    if n < 1:
        return
    _print_no_repetition_sequences_helper(char_list, n, "")


def _print_no_repetition_sequences_helper(char_list, n, word):
    """
    Prints all combinations in size of n of chars in a given list with no
    repetition
    :param char_list: list of chars
    :param n: number of chars in each combination
    :param word: the printed word each time
    :return:
    """
    if n == 1:
        for char in char_list:
            print(word + char)
        return

    for char in char_list:
        word += char
        char_list_updated = char_list[:]
        char_list_updated.remove(char)
        _print_no_repetition_sequences_helper(char_list_updated, n-1, word)
        word = word[:-1]


def parentheses(n):
    """
    Returns a list with n valid paris of parentheses.
    :param n: number of parentheses pairs.
    :return: list of strings
    """
    if n < 1:
        return []

    # initialize basic pattern
    paren_str = "(" * n + ")"
    return _parentheses_helper([], paren_str, n-1, n-1)


def _parentheses_helper(paren_lst, paren_str, n, total_n):
    """
    Returns a list with n valid paris of parentheses.
    :param paren_lst: list of all possible combinations
    :param paren_str: holds the current combination
    :param n: number of ) to insert into a string
    :param total_n: the total number of ) to insert into a string
    :return: list
    """

    # adds one combination to the list
    if n < 1:
        paren_lst.append(paren_str)
        return paren_lst

    first_ind = paren_str.index(')')  # index of the first right parentheses )

    # if the string starts with (), we cannot insert ) between ()
    if first_ind < 2:
        return paren_lst

    # adds right parenthesis to the string each time
    for i in range(first_ind):
        if n == total_n and (first_ind - i) < len(paren_str) - 2:
            break  # makes sure we follows the rules
        paren_str_next = paren_str[:first_ind-i] + ")" + paren_str[first_ind-i:]
        paren_lst = \
            (_parentheses_helper(paren_lst, paren_str_next, n - 1, total_n))

    # returns all possible combinations
    return paren_lst


def flood_fill(image, start):
    """
    Replaces '.' by '*' in a given array, starts from a given index and
    only the adjacent '.' cells each time.
    :param image: 2D list
    :param start: a tuple of indexes : (row,col) which indicated the
    starting point in the array
    :return: None
    """

    curr_row, curr_col = start[0], start[1]

    # if the cell hold '*' then we reached a dead end
    if image[curr_row][curr_col] == '*':
        return

    # replace '.' by '*' in the current cell
    image[curr_row][curr_col] = '*'

    # move to adjacent cells (up, down, right, left)
    flood_fill(image, (curr_row, curr_col - 1))
    flood_fill(image, (curr_row, curr_col + 1))
    flood_fill(image, (curr_row + 1, curr_col))
    flood_fill(image, (curr_row - 1, curr_col))
