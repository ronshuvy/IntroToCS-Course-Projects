from vector import Vector


class GameObject:
    """
    Parent class to all game objects
    """
    def __init__(self, x, y, speed=None, heading=None):
        self.__position = Vector(x, y)
        self.__speed = Vector(*speed)
        self.__heading = heading

    def get_heading(self):
        """
        :return: direction of the object in radians
        """
        return self.__heading

    def set_heading(self, heading):
        """
        set the direction of the heading
        :param heading: new heading (radians)
        :return: None
        """
        self.__heading = heading

    def get_position(self):
        """
        get object's position
        :return: tuple (x,y)
        """
        return self.__position.get_x(), self.__position.get_y()

    def set_position(self, x, y):
        """
        set object's position
        :param x: x axis
        :param y: y axis
        :return: None
        """
        self.__position.set_coordinates(x, y)

    def get_speed(self):
        """
        Get object's speed on two axes
        :return: tuple x_speed,y_speed
        """
        return self.__speed.get_x(), self.__speed.get_y()

    def set_speed(self, speed):
        """
        Set object's speed on two axes
        :param speed: expected tuple (x,y)
        :return: None
        """
        self.__speed.set_coordinates(*speed)
