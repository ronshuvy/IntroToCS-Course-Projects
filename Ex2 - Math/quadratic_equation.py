# FILE : quadratic_equation.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019

import math


def quadratic_equation(a, b, c):
    """ Solves quadratic equation (ax^2+bx+c=0)
    :param a: coefficient of x^2 (a != 0)
    :param b: coefficient of x
    :param c: free coefficient
    :return: 2 values : x1, x2 (x can be none)
    :rtype: list
    """
    d = (b**2) - (4*a*c)  # calculate the determinant
    if d < 0:  # equation with negative determinant has no solution
        return None, None
    if d == 0:  # equation with determinant equals to zero has 1 solution
        return (-b) / (2*a), None
    # equation with positive determinant
    x1 = (-b + math.sqrt(d)) / (2*a)
    x2 = (-b - math.sqrt(d)) / (2*a)
    return x1,x2


def quadratic_equation_user_input():
    """ Solves quadratic equation (ax^2+bx+c=0) with User Interface
    :return: none
    """
    print("Insert coefficients a, b, and c:", end = " ")
    coefficients = input()
    # splits the input to numbers and operation
    a = float(coefficients.split(" ")[0])
    b = float(coefficients.split(" ")[1])
    c = float(coefficients.split(" ")[2])
    if a == 0:  # checks if input is invalid
        print("The parameter 'a' may not equal 0")
    else:
        solutions = quadratic_equation(a, b, c)
        x, y = solutions[0], solutions[1]
        if x is not None and y is not None:  # found 2 solutions
            print("The equation has 2 solutions:", x, "and", y)
        elif x is not None:  # found 1 solution
            print("The equation has 1 solution:", x)
        elif y is not None:  # found 1 solution
            print("The equation has 1 solution:", y)
        else:  # there is no solution
            print("The equation has no solutions")

