# FILE : calculate_mathematical_expression.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019


def calculate_mathematical_expression(num1, num2, operation):
    """ Calculates arithmetic operation between two numbers
    :param num1: first number
    :param num2: second number
    :param operation: addition/subtraction/multiplication/division
    :return: calculated result
    :rtype: float
    """
    if operation == "+":
        return num1 + num2
    if operation == "-":
        return num1 - num2
    if operation == "*":
        return num1 * num2
    if operation == "/" and num2 != 0:
        return num1 / num2
    else:
        return  # return none when trying to divide by zero or invalid input


def calculate_from_string(msg):
    """ Calculates from a message an arithmetic operation between two numbers
    :param msg: a string which contains two numbers and one operation
    :return: calculated result
    :rtype: float
    """
    # splits the message to numbers and operation
    split_msg = msg.split(" ")
    num1 = float(split_msg[0])
    operation = split_msg[1]
    num2 = float(split_msg[2])
    return calculate_mathematical_expression(num1, num2, operation)

