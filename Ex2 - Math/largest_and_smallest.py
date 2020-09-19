# FILE : largest_and_smallest.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019
# DESCRIPTION: 2 personal tests - edge cases is more likely to appear
# when two numbers are equals to each other,
# so I chose the cases in which num1=num2 and num1=num3,
# when they bigger and smaller then the third.


def largest_and_smallest(num1, num2, num3):
    """ Finds the maximum value and the minimum value between 3 numbers
    :param num1: first number
    :param num2: second number
    :param num3: third number
    :return: the largest number and the smallest number
    :rtype: list
    """

    # Finds the maximum value
    maximum = num1 if (num1 >= num2) else num2
    if num3 >= maximum:
        maximum = num3

    # Finds the minimum value
    minimum = num1 if (num1 <= num2) else num2
    if num3 <= minimum:
        minimum = num3

    return maximum, minimum


def check_largest_and_smallest():
    """ Tests the function "largest_and_smallest" with different inputs
    :return: true if the function has passed all the tests successfully,
     false otherwise.
    :rtype: boolean
    """
    if largest_and_smallest(17, 1, 6) != (17, 1):
        return False
    if largest_and_smallest(1, 17, 6) != (17, 1):
        return False
    if largest_and_smallest(1, 1, 2) != (2, 1):
        return False
    if largest_and_smallest(1, 3, 3) != (3, 1):
        return False
    if largest_and_smallest(5, 2, 5) != (5, 2):
        return False
    return True

