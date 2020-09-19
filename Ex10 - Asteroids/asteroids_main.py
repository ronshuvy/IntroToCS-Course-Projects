from screen import Screen
from ship import Ship
from torpedo import Torpedo
from asteroid import Asteroid
from asteroids_config import GameConfiguration as Cfg
import random
import math
import sys


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(*self.rand_position(), 0)
        self.__asteroids = self.add_asteroids(asteroids_amount)
        self.__torpedos = list()
        self.__score = 0

    def add_asteroids(self, amount):
        """
        Adds the specified amount of asteroids to the game at random positions
        with random speeds , avoiding initial collision with the ship.
        :param amount: amount of asteroids
        :return: list of added asteroids
        """
        asteroids_lst = []

        for i in range(amount):
            # create asteroid
            asteroid = Asteroid(*self.rand_position(), self.rand_speed())

            # if the asteroid intersects with the ship, assigns other position
            while asteroid.has_intersection(self.__ship):
                asteroid.set_position(*self.rand_position())

            # add asteroid to 'Screen' class and asteroids list
            self.__screen.register_asteroid(asteroid, asteroid.get_size())
            asteroids_lst.append(asteroid)

        return asteroids_lst

    def add_points(self, points):
        """
        Adds points to total score
        :param points: integer
        :return: None
        """
        self.__score += points
        self.__screen.set_score(self.__score)

    def rand_position(self):
        """
        Generates random position on screen
        :return: tuple of position (x,y)
        """
        return random.randint(self.__screen_min_x, self.__screen_max_x), \
               random.randint(self.__screen_min_y, self.__screen_max_y)

    @staticmethod
    def rand_speed():
        """
        Generate random speed
        :return: tuple of (x_speed, y_speed)
        """
        return random.choice(Cfg.VALID_AST_SPEED), \
               random.choice(Cfg.VALID_AST_SPEED)

    def run(self):
        """

        :return: None
        """
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """
        a function running the game loop every 5 ms
        :return: None
        """
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        the loop handling all game i/o
        :return: None
        """
        # Ship - drawing, movement and input from keyboard
        self.__screen.draw_ship(*self.__ship.get_position(),
                                self.__ship.get_heading())
        self.move(self.__ship)
        self.user_input()

        # Torpedo - drawing and movement
        for torpedo in self.__torpedos:
            self.move(torpedo)
            torp_x, torp_y = torpedo.get_position()
            self.__screen.draw_torpedo(torpedo, torp_x, torp_y,
                                       torpedo.get_heading())

            if torpedo.get_age() > Cfg.TORP_LIFESPAN:
                self.destroy_torpedo(torpedo)

        # Asteroids - drawing and movement
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, *asteroid.get_position())
            self.move(asteroid)

            # check for asteroid-ship collision and handles collision
            has_collided = self.asteroid_ship_collision(asteroid)

            # collision handled, checks if player ran out of lives
            if has_collided:
                self.check_if_game_over()

            # check for asteroid collisions - torpedo
            self.asteroid_torpedo_collision(asteroid)

        self.check_if_game_over()

    def move(self, obj):
        """
        Moves a given object in space by a movement formula
        :param obj: ship / asteroid / torpedo
        :return: None
        """
        # Prepares all ingredients
        new_spot = [0, 0]
        speed = obj.get_speed()
        old_spot = obj.get_position()
        screen_min = (self.__screen_min_x, self.__screen_min_y)
        screen_width = self.__screen_max_x - self.__screen_min_x
        screen_height = self.__screen_max_y - self.__screen_min_y
        screen_size = (screen_width, screen_height)

        # Calculates the object's new position by a given formula
        for i in range(2):  # x,y coordinates
            new_spot[i] = \
                screen_min[i] + \
                (old_spot[i] + speed[i] - screen_min[i]) % screen_size[i]

        # Update the object position
        obj.set_position(*new_spot)

    def check_if_game_over(self):
        """
        Check if game is over
        :return: None
        """
        if self.__ship.is_dead():
            # player has lost
            self.end_game("Game Over!", "You have lost all of your lives.")

        if self.__screen.should_end():
            # user pressed 'q' to quit
            self.end_game("Goodbye", "See you tomorrow :)")

        if not self.__asteroids:
            # all asteroids were destroyed!
            self.end_game("WINNER!", "All asteroids were destroyed! Well done")

    def end_game(self, title, msg_content):
        """
        Game over! Prints goodbye message and exit game
        :param title: message title
        :param msg_content: message content
        :return: None
        """
        self.__screen.show_message(title, msg_content)
        self.__screen.end_game()
        sys.exit()

    def asteroid_ship_collision(self, asteroid):
        """
        Check if a given asteroid has collided our ship.
        if so -
        1. subtract 1 live from total amount
        2. print hit message
        :param asteroid: an asteroid object
        :return: True if collision occurred, False otherwise
        """
        if asteroid.has_intersection(self.__ship):
            self.destroy_asteroid(asteroid)
            self.__ship.lose_life()
            self.__screen.remove_life()
            self.__screen.show_message(
                "Oops!", "You have hit an asteroid and lost a life")
            return True
        return False

    def asteroid_torpedo_collision(self, asteroid):
        """
        Check if a given asteroid has collided with torpedos.
        if so -
        1. destroys the torpedo
        2. explodes the asteroid
        3. adds points to user
        :param asteroid: an asteroid object
        :return: None
        """
        for torpedo in self.__torpedos:
            if asteroid.has_intersection(torpedo):
                self.destroy_torpedo(torpedo)
                self.explode_asteroid(asteroid, torpedo)
                self.add_points(Cfg.SCORE_ADDITION[asteroid.get_size()])

    def explode_asteroid(self, asteroid, torpedo):
        """
        Handles the event when the player hits an asteroid with a torpedo
        :param asteroid: an asteroid object
        :param torpedo: torpedo object
        :return: None
        """

        self.destroy_asteroid(asteroid)

        if asteroid.get_size() > min(Cfg.AST_SIZES):
            # splits the asteroid into smaller asteroids

            # setting all parameters
            new_size = asteroid.get_size() - 1

            old_ast_pos = asteroid.get_position()
            old_ast_speed_x, old_ast_speed_y = asteroid.get_speed()
            torp_speed_x, torp_speed_y = torpedo.get_speed()

            numerator_x = torp_speed_x + old_ast_speed_x
            numerator_y = torp_speed_y + old_ast_speed_y
            denominator = math.sqrt(
                old_ast_speed_x ** 2 + old_ast_speed_y ** 2)
            new_speed_x, new_speed_y = \
                numerator_x / denominator, numerator_y / denominator

            # Adds smaller asteroids to game
            for i in range(Cfg.NUM_OF_TINY_ASTS):
                asteroid = Asteroid(
                    *old_ast_pos, (new_speed_x, new_speed_y), new_size)
                self.add_smaller_asteroid(asteroid)
                new_speed_x, new_speed_y = -new_speed_x, -new_speed_y

    def add_smaller_asteroid(self, asteroid):
        """
        Adds smaller asteroids which was created from the explosion
        :param asteroid: an asteroid object
        :return: None
        """
        self.__asteroids.append(asteroid)
        self.__screen.register_asteroid(asteroid, asteroid.get_size())

    def destroy_torpedo(self, torpedo):
        """
        Destroys a given torpedo
        :param torpedo: torpedo object
        :return: None
        """
        self.__torpedos.remove(torpedo)
        self.__screen.unregister_torpedo(torpedo)

    def destroy_asteroid(self, asteroid):
        """
        Destroys a given asteroid
        :param: an asteroid object
        :return: None
        """
        if asteroid in self.__asteroids:  # check for double hit
            self.__asteroids.remove(asteroid)
            self.__screen.unregister_asteroid(asteroid)

    def fire_torpedo(self):
        """
        Creates a new torpedo based on the ship's stats
        :return: None
        """
        #  setting parameters
        x, y = self.__ship.get_position()
        ship_heading = math.radians(self.__ship.get_heading())
        ship_speed_x, ship_speed_y = self.__ship.get_speed()

        # calculates torpedo's speed by formula
        torpedo_speed = (ship_speed_x + 2 * math.cos(ship_heading),
                         ship_speed_y + 2 * math.sin(ship_heading))

        # adds and draws the torpedo
        torp = Torpedo(x, y, torpedo_speed, self.__ship.get_heading())
        self.__torpedos.append(torp)
        self.__screen.register_torpedo(torp)
        self.__screen.draw_torpedo(torp, x, y, torp.get_heading())

    def user_input(self):
        """
        Handles user's input from keyboard by the following pressed buttons :
        Left / Right - change ships's heading
        Up - accelerate ships's speed
        :return: None
        """
        if self.__screen.is_left_pressed():  # User pressed - LEFT
            self.change_ship_heading(Cfg.LEFT_BUTTON)

        if self.__screen.is_right_pressed():  # User pressed - RIGHT
            self.change_ship_heading(Cfg.RIGHT_BUTTON)

        if self.__screen.is_up_pressed():  # User pressed - UP
            self.accelerate_ship()

        if self.__screen.is_space_pressed() and \
                len(self.__torpedos) < Cfg.MAX_TORPS:  # User pressed - SPACE
            self.fire_torpedo()

    def accelerate_ship(self):
        """
        Accelerates the ship's speed when the user presses UP button
        :return: None
        """
        x_speed, y_speed = self.__ship.get_speed()  # ship's old speed
        heading = math.radians(self.__ship.get_heading())

        # Calculate the ship's new speed by an acceleration formula
        new_speed = (x_speed + math.cos(heading),
                     y_speed + math.sin(heading))

        # Updates ship's speed
        self.__ship.set_speed(new_speed)

    def change_ship_heading(self, direction):
        """
        Rotates the ship's heading by a given direction
        Left : current heading + ROTATION_DEGREES
        Right : current heading - ROTATION_DEGREES
        :param direction: LEFT_BUTTON or RIGHT_BUTTON
        :return: None
        """
        rotation = Cfg.ROTATION_DEGREES if direction == Cfg.LEFT_BUTTON \
            else -Cfg.ROTATION_DEGREES
        self.__ship.set_heading(self.__ship.get_heading() + rotation)


def main(amount):
    """
    Creates game object and runs the game
    :param amount: amount of asteroids
    :return: None
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(Cfg.DEFAULT_ASTEROIDS_NUM)
