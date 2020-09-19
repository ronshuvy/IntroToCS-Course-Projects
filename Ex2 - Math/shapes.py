# FILE : shapes.py
# WRITER : Ron Shuvy , ronshuvy , 206330193
# EXERCISE : intro2cs1 2019

import math


def shape_area():
    """ Calculates the area of a circle/rectangle/triangle (Input from user)
    :return: the area of a shape
    :rtype: float
    """

    def circle_area(r):
        """ Calculates the area of a circle
        :param r: circle radius
        :return: the area of the shape
        :rtype: float
        """
        return math.pi * (r**2)

    def rectangle_area(side_a, side_b):
        """ Calculates the area of a rectangle
        :param side_a: rectangle first side
        :param side_b: rectangle second side
        :return: the area of the shape
        :rtype: float
        """
        return side_a * side_b

    def triangle_area(side_a):
        """ Calculates the area of an equilateral triangle
        :param side_a: triangle side
        :return: the area of the shape
        :rtype: float
        """
        return (side_a**2) * (math.sqrt(3)/4)

    print('Choose shape (1=circle, 2=rectangle, 3=triangle):', end = " ")
    shape_type = float(input())
    if shape_type == 1:  # Circle
        radius = float(input())
        return circle_area(radius)
    elif shape_type == 2:  # Rectangle
        side1 = float(input())
        side2 = float(input())
        return rectangle_area(side1, side2)
    elif shape_type == 3:  # Triangle
        side = float(input())
        return triangle_area(side)
    else:
        return None
