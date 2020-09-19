__author__ = 'ronshuvy'

#######################################################
#                  Exercise 7 Tests                   #
#######################################################

from Ex7.ex7 import *


def get_printed(capsys):
    captured = capsys.readouterr()
    return captured.out

########################
# A. 1                 #
# print_to_n           #
########################


def test_print_to_n(capsys):
    assertions = \
        [[0, ""], [1, "1\n"], [2, "1\n2\n"],
         [3, "1\n2\n3\n"], [4, "1\n2\n3\n4\n"]]

    for a in assertions:
        print_to_n(a[0])
        out = get_printed(capsys)
        assert out == a[1]

########################
# A. 2                 #
# digit_sum            #
########################


def test_digit_sum():
    assertions = \
        [[0, 0], [5, 5], [1000, 1], [479, 20], [12345, 15], [88888, 40]]

    for a in assertions:
        assert digit_sum(a[0]) == a[1]


########################
# A. 3                 #
# is_prime(n)          #
########################

def test_is_prime():
    assertions = \
        [[1, False], [2, True], [3, True], [4, False], [97, True], [49, False]
         , [1069, True], [2046, False]]

    for a in assertions:
        assert is_prime(a[0]) == a[1]


########################
# A. 5, A.6            #
# print_sequences      #
# + no_repetitions     #
########################


def test_print_sequences(capsys):
    assertions = [
        (['a', 'b', 'c'], 1),
        (['a', 'b', 'c'], 2),
        (['a'], 4),
        (['a','b', 'c'], 3)
    ]

    expected_with_rep = \
        [{'a', 'b', 'c'},
        {'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc'},
        {'aaaa'},
        {'aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'aca', 'acb', 'acc',
         'baa', 'bab', 'bac', 'bba', 'bbb', 'bbc', 'bca', 'bcb', 'bcc',
         'caa', 'cab', 'cac', 'cba', 'cbb', 'cbc', 'cca', 'ccb', 'ccc'}]

    expected_no_rep = \
        [{'a', 'b', 'c'},
        {'ab', 'ac', 'ba', 'bc', 'ca', 'cb'},
         set(),
        {'abc', 'acb', 'bac', 'bca', 'cab', 'cba'}]

    for i in range(len(assertions)):
        print_sequences(assertions[i][0], assertions[i][1])
        out = get_printed(capsys)
        result = set(out.split("\n"))-{""}
        assert result == expected_with_rep[i]
        # test with no repetitions
        print_no_repetition_sequences(assertions[i][0], assertions[i][1])
        out = get_printed(capsys)
        result = set(out.split("\n"))-{""}
        assert result == expected_no_rep[i]


########################
# A. 7                 #
# parentheses          #
########################


def test_parentheses():
    assertions = [
        (1, ["()"]),
        (2, ["()()", "(())"]),
        (3, ["()()()", "(())()", "()(())", "((()))", "(()())"]),
        (4, ['(((())))',
             '(())(())',
             '((()()))',
             '((())())',
             '((()))()',
             '(()(()))',
             '(()()())',
             '(()())()',
             '(())()()',
             '()((()))',
             '()(()())',
             '()(())()',
             '()()(())',
             '()()()()'])
    ]

    for a in assertions:
        result = parentheses(a[0])
        assert type(result) is list
        assert set(result) == set(a[1])
        # check for duplicates:
        for i in range(len(result)):
            for b in result[i+1:]:
                assert result[i] != b


########################
# A. 8                 #
# flood_fill           #
########################


def test_flood_fill():
    input_1 = (
        [
            ["*", "*", "*", "*", "*"],
            ["*", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*"]
        ],
        (1, 1)
    )
    output_1 = [
        ["*", "*", "*", "*", "*"],
        ["*", "*", "*", "*", "*"],
        ["*", "*", "*", "*", "*"],
        ["*", ".", ".", ".", "*"],
        ["*", "*", "*", "*", "*"]
    ]

    input_2 = (
        [
            ["*", "*", "*", "*", "*"],
            ["*", ".", "*", ".", "*"],
            ["*", ".", "*", "*", "*"],
            ["*", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*"]
        ],
        (1, 1)
    )
    output_2 = [
        ["*", "*", "*", "*", "*"],
        ["*", "*", "*", ".", "*"],
        ["*", "*", "*", "*", "*"],
        ["*", "*", "*", "*", "*"],
        ["*", "*", "*", "*", "*"]
    ]

    input_3 = (
        [
            ["*", "*", "*", "*", "*"],
            ["*", ".", "*", ".", "*"],
            ["*", ".", "*", "*", "*"],
            ["*", ".", ".", ".", "*"],
            ["*", "*", "*", "*", "*"]
        ],
        (1, 3)
    )

    output_3 = [
        ["*", "*", "*", "*", "*"],
        ["*", ".", "*", "*", "*"],
        ["*", ".", "*", "*", "*"],
        ["*", ".", ".", ".", "*"],
        ["*", "*", "*", "*", "*"]
    ]

    flood_fill(input_1[0], input_1[1])
    assert input_1[0] == output_1
    flood_fill(input_2[0], input_2[1])
    assert input_2[0] == output_2
    flood_fill(input_3[0], input_3[1])
    assert input_3[0] == output_3
