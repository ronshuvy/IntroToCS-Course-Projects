#######################################################
#                  Exercise 5 Tests                   #
#######################################################

from Ex5.wordsearch import *

########################
#         A. 1         #
# check_input_args     #
########################


def test_input_args():
    assert check_input_args(["file1.txt", "file2.txt", "file3.txt", "4", "5"]) \
           == "Error : Number of arguments should be 4."
    assert check_input_args(["file1.txt", "file2.txt", "file3.txt"]) == "Error : Number of arguments should be 4."
    assert check_input_args(["nowhere.txt", "file2.txt", "file3.txt", "file4.txt"])\
           == "Error : Words file doesn't found."
    assert check_input_args(["", "file2.txt", "file3.txt", "file4.txt"]) == "Error : Words file doesn't found."
    assert check_input_args \
               (["word_list.txt", "nowhere.txt", "output_file.txt", "l"])\
           == "Error : Matrix file doesn't found."
    assert check_input_args \
               (["word_list.txt", "mat.txt", "output_file.txt", "lrq"]) == "Error : Invalid direction values."
    assert check_input_args(["word_list.txt", "mat.txt", "output_file.txt", ""]) is None
    assert check_input_args(["word_list.txt", "mat.txt", "output_file.txt", "lrwu"]) is None


########################
#         A. 2         #
# read_wordlist_file  #
########################


def test_read_wordlist_file():
    assert read_wordlist_file("word_list1.txt") == ["Cat", "cAt", "dog", "ok"]
    assert read_wordlist_file("word_list2.txt") == []


########################
#         A. 3         #
# read_matrix_file     #
########################


def test_read_matrix_file():
    assert read_matrix_file("mat1.txt") == []
    assert read_matrix_file("mat.txt") ==\
           [['a','p','p','l','e'], ['a','g','o','d','o'], ['n','n','e','r','t'],
            ['g','a','T','A','C'], ['m','i','c','s','r'], ['P','o','P','o','P']]

########################
#         A. 4         #
# find_words_in_matrix #
########################


def test_search_for_words():
    matrix = read_matrix_file("mat_short.txt")
    words_expected = read_wordlist_file("search_expected.txt")
    assert search_for_words(matrix, "r") == words_expected

########################
#         A. 5         #
# find_words_in_matrix #
########################


def test_find_words():
    word_list = read_wordlist_file("word_list.txt")
    matrix = read_matrix_file("mat.txt")
    assert find_words_in_matrix(word_list, matrix, "r") == [("apple", 1), ("PoP", 2)]
    assert set(find_words_in_matrix(word_list, matrix, "l")) == {('dog', 1), ('CAT', 1), ('PoP', 2)}
    assert find_words_in_matrix(word_list, matrix, "w") == [("cAt", 1)]
    assert set(find_words_in_matrix(word_list, matrix, "udlrwxyz")) ==\
           {("anTs", 1), ("apple", 1), ("can", 1),("CAT", 1),
           ("cAt", 1), ("Crop", 1), ("dog", 1), ("long", 1), ("poeT",1), ("PoP", 4), ("toe", 1)}
    assert find_words_in_matrix(word_list, "matrix", "") == []
    assert find_words_in_matrix(word_list, [['q']], "rlz") == []
    assert find_words_in_matrix(word_list, [['h','e']], "rludwxyz") == [('he', 1)]


########################
#         A. 6         #
# write_output_files   #
########################


########################
#         A. 7         #
# Main Function        #
########################

