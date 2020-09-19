from asteroids_config import GameConfiguration as Cfg
from game_object import GameObject


class Torpedo(GameObject):
    """
    Class for asteroids game torpedo
    """
    def __init__(self, x, y, speed, heading):
        GameObject.__init__(self, x, y, speed=speed, heading=heading)
        self.__age = 0

    @staticmethod
    def get_radius():
        """
        :return: Torpedo's radius
        """
        return Cfg.TORP_RADIUS

    def set_position(self, x, y):
        """
        Advances a torpedo while aging it.
        :param x: new x coordinate
        :param y: new y coordinate
        :return: None
        """
        GameObject.set_position(self, x, y)
        self.__age += 1

    def get_age(self):
        """
        :return: Torpedo's age (advancements)
        """
        return self.__age
