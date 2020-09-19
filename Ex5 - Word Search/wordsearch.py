# FILE : wordsearch.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019 ex5


import sys
import os


def check_input_args(args):
    """
    Tests for input validation (program's arguments)
    and returns a message accordingly
    :param args: list of strings which contains file names of the arguments
    :return: error message if error was found, None value otherwise.
    """

    if len(args) != 4:
        return "Error : Number of arguments should be 4."
    elif os.path.isfile(args[0]) is False:
        return "Error : Words file doesn't found."
    elif os.path.isfile(args[1]) is False:
        return "Error : Matrix file doesn't found."
    for direction in args[3]:
        if direction not in "lrudwxyz":
            return "Error : Invalid direction values."
    return None


def read_wordlist_file(filename):
    """
    Loads a lists of words in a file into a list
    :param filename: list of words' filename
    :return: list containing all words
    """
    words_file = open(filename, 'r')
    words_lst = [line.strip() for line in words_file]
    words_file.close()
    return words_lst


def read_matrix_file(filename):
    """
    Reads the matrix letters of a file and convert to a list
    :param filename: name of input file which contains all matrix's letters
    :return: matrix letters in 2D list
    """
    matrix_file = open(filename, 'r')
    matrix_lst = [line.strip().split(",") for line in matrix_file]
    matrix_file.close()
    return matrix_lst


def search_for_words(mat, direction):
    """ Searches for words in matrix in a given direction
     and return list of all words
    :param mat: 2D list which contains letters
    :param direction: letter as a direction
    :return: list of all strings found with the direction
    """

    def direction_instruction\
                    (direc, curr_row, curr_colm, total_rows, total_colms):
        """
        Sends back an instruction of behavior about a specific direction
        :param direc: direction
        :param curr_row: the element's row id
        :param curr_colm: the element's column id
        :param total_rows: number of matrix rows
        :param total_colms: number of matrix columns
        :return: two integers : step (how many times to move on) and jump
        (in which order to scan) in a loop
        jump's value : 1 or -1
        """
        if direc == 'r':
            return (total_colms - curr_colm), 1
        if direc == 'l':
            return -(curr_colm + 1), -1
        if direc == 'u':
            return -(curr_row + 1), -1
        if direc == 'd':
            return total_rows - curr_row, 1
        if direc == 'w':
            return -(curr_row + 1), -1
        if direc == 'x':
            return -(curr_row + 1), -1
        if direc == 'y':
            return total_rows - curr_row, 1
        return total_rows - curr_row, 1  # for 'z' direction

    def set_shifts(direc, curr_colm, curr_shift):
        """
        Determines the number of shifts of the i-row and the j-column of an
        element
        :param direc: direction
        :param curr_colm: the element's column id
        :param curr_shift: the current iteration in loop, i.e how much to move
        :return: 4 integers :
        shift of i-row, shift of j-column,
        position in matrix and halt(final) position
        Notice: position and final position are only relevant to diagonal
        shifts.
        """
        if direc in 'r':
            return 0, curr_shift, None, None
        if direc in 'l':
            return 0, curr_shift, None, None
        if direc in "ud":
            return curr_shift, 0, None, None
        if direc in 'w':
            return curr_shift, -curr_shift, (curr_colm - curr_shift),\
                   (cols - 1)
        if direc in 'x':
            return curr_shift, curr_shift, (curr_colm + curr_shift), 0
        if direc in 'y':
            return curr_shift, curr_shift, (curr_colm + curr_shift),\
                   (cols - 1)
        return curr_shift, -curr_shift,\
               (curr_colm - curr_shift), 0  # for 'z' direction

    strings_lst = []  # all collected words in the matrix
    rows = len(mat)  # number of rows in matrix
    cols = len(mat[0])  # number of columns in matrix
    for i in range(rows):
        for j in range(cols):
            # scans all the words for an element[i][j]
            steps, jump = direction_instruction(direction, i, j, rows, cols)
            mat_str = ""  # represents a single word each time

            for shift in range(0, steps, jump):
                shift_i, shift_j, pos, final_pos =\
                    set_shifts(direction, j, shift)

                # only for diagonal shifts
                if direction in "wxyz" and pos == final_pos:
                    mat_str += mat[i + shift_i][j + shift_j]
                    strings_lst.append(mat_str)
                    break
                mat_str += mat[i + shift_i][j + shift_j]
                strings_lst.append(mat_str)
    return strings_lst


def find_words_in_matrix(word_list, matrix, directions):
    """
    Finds words from a given list in a matrix, searched by a given directions.
    :param word_list: list of words to search in a matrix
    :param matrix: 2D list which contains letters
    :param directions: string of letters represents directions :
    u - up, d - down, l - left, r - right,
    w - up right diagonal, x - up left diagonal, y - down right diagonal,
     z - down left diagonal
    :return: list of pairs, each pair is a tuple of 2 elements : (word,count)
    """

    if not matrix:  # matrix is empty
        return []

    directions = set(directions)  # no duplicates is needed
    word_in_matrix = []  # list of all string's combinations in a matrix

    # Finds all potential strings in a matrix
    for d in directions:
        word_in_matrix.extend(search_for_words(matrix, d))

    # Counts how many time every word appears on the combinations list
    result = [(word, word_in_matrix.count(word))
              for word in word_list if word_in_matrix.count(word) > 0]

    return result


def write_output_file(results, output_filename):
    """
    Writes the results to an output file
    :param results: list of given words with num of instances in the matrix
    :param output_filename: name of the output file
    :return: None
    """
    results_file = open(output_filename, "w")
    for i in range(len(results)):
        results_file.write(results[i][0] + "," + str(results[i][1]))
        if i != len(results)-1:
            results_file.write('\n')
    results_file.close()


def wordsearch_main():
    """
    This program searches for words in a matrix by a given directions
    and writes the results (pairs of word and counter) into a given output
     file.
    :argument arg[0] : path of words list file
    :argument arg[1] : path of matrix file
    :argument arg[2] : path of output file
    :argument arg[3] : string of directions

    """
    args = [arg for arg in sys.argv][1:]
    error_msg = check_input_args(args)
    if error_msg is not None:  # wrong arguments were given
        print(error_msg)
        sys.exit()
    words = read_wordlist_file(args[0])  # Loading words to a list
    matrix = read_matrix_file(args[1])  # Loading matrix into 2D list

    # Searching for words in matrix and return match results
    result = find_words_in_matrix(words, matrix, args[3])

    # Writing the results into a given file
    write_output_file(result, args[2])


if __name__ == "__main__":
    wordsearch_main()




