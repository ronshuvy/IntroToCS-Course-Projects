
class Board:
    """
    This class represents board in "rush-hour" game
    """
    __ROW_SIZE = 7
    __COL_SIZE = 7
    __TARGET_LOC = (3, 7)

    def __init__(self):
        self.__board = [['_'] * self.__COL_SIZE for i in range(self.__ROW_SIZE)]
        self.__cars = dict()
        self.__car_in_target = None

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_status = ''
        target_cell = 'E'

        if self.__car_in_target:
            target_cell = self.__car_in_target

        for i in range(self.__ROW_SIZE):
            for j in range(self.__COL_SIZE):
                board_status += self.__board[i][j] + "  "
                if i == self.__TARGET_LOC[0] and j == self.__TARGET_LOC[1] - 1:
                    board_status += target_cell
            board_status += "\n"

        return board_status

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        return [(i, j) for i in range(self.__ROW_SIZE)
                for j in range(self.__COL_SIZE)] + [self.__TARGET_LOC]

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """

        return [(car.get_name(), key, value) for car in self.__cars.values()
                for key, value in car.possible_moves().items()]

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return self.__TARGET_LOC

    def cell_content(self, coordinate):

        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if coordinate == self.__TARGET_LOC:
            return None if not self.__car_in_target else self.__car_in_target

        row, col = coordinate[0], coordinate[1]
        return None if self.__board[row][col] == '_' else self.__board[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """

        if car.get_name() in self.__cars.keys():
            return False  # cars cannot have the same name (color)

        for coord in car.car_coordinates():
            cells_lst = self.cell_list()
            if coord not in cells_lst:
                return False  # Coordinate is out of board range

        for c in car.car_coordinates():
            if c == self.__TARGET_LOC:
                continue
            elif self.__board[c[0]][c[1]] != '_':
                return False  # Sorry, the cell is already taken

        # coordinates are available, placing car on board
        for c in car.car_coordinates():
            if c == self.__TARGET_LOC:
                self.__car_in_target = car.get_name()
            else:
                self.__board[c[0]][c[1]] = car.get_name()

        self.__cars[car.get_name()] = car

        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        if name not in self.__cars.keys():
            return False  # car is not on the board
        car = self.__cars[name]
        coordinate = car.movement_requirements(movekey)[0]

        # False if cell is already taken by another car,
        # or coordinate is out of board's range
        if coordinate not in self.cell_list() or self.cell_content(coordinate):
            return False

        coords_to_reset = car.car_coordinates()

        # If the player has won the game
        if coordinate == self.__TARGET_LOC:
            self.__car_in_target = car.get_name()
            self.__board[coords_to_reset[0][0]][coords_to_reset[0][1]] = "_"
            return True

        # Move the car
        car_has_moved = car.move(movekey)
        coords_to_fill = car.car_coordinates()
        if not car_has_moved:
            return False  # Car object could not make the move

        # Remove car from its old location
        for c in coords_to_reset:
            self.__board[c[0]][c[1]] = "_"
        # Add car to its new location
        for c in coords_to_fill:
            self.__board[c[0]][c[1]] = car.get_name()

        return True

    def check_valid_word(self, word):
        pass
