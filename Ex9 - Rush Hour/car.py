class Car:
    """
    This class represents car in "rush-hour" game
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        row_head, col_head = self.__location[0], self.__location[1]
        return [(row_head + i, col_head) if self.__orientation == 0
                else (row_head, col_head + i)
                for i in range(self.__length)]

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        if self.__orientation == 1:
            return {'l': 'left',
                    'r': 'right'}
        return {'u': 'up',
                'd': 'down'}

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        l = self.__length  # car's length
        shift = {'u': [-1, 0], 'd': [l, 0], 'l': [0, -1], 'r': [0, l]}
        return [(self.__location[0] + shift[movekey][0],
                self.__location[1] + shift[movekey][1])]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey not in self.possible_moves():
            return False

        row_head, col_head = self.__location[0], self.__location[1]
        shift = {'u': [-1, 0], 'd': [1, 0], 'l': [0, -1], 'r': [0, 1]}
        self.__location = \
            (row_head + shift[movekey][0], col_head + shift[movekey][1])
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name


