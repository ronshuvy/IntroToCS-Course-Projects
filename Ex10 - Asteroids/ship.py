from asteroids_config import GameConfiguration as Cfg
from game_object import GameObject


class Ship(GameObject):
    """
    A class for asteroids game ship
    """
    def __init__(self, x, y, heading=0):
        GameObject.__init__(self, x, y, speed=(0, 0), heading=heading)
        self.__lives = Cfg.INIT_LIVES

    @staticmethod
    def get_radius():
        """
        :return: Ship's radius
        """
        return Cfg.SHIP_RADIUS

    def is_dead(self):
        """
        :return: True if the ship has no more lives.
        """
        return True if self.__lives <= 0 else False

    def lose_life(self):
        """
        :return: subtract one life
        """
        self.__lives -= 1
