class GameConfiguration:
    # General constants
    LEFT_BUTTON = 'l'
    RIGHT_BUTTON = 'r'
    SCORE_ADDITION = {
        # asteroid size: score addition
        3: 20,
        2: 50,
        1: 100
    }

    # Asteroids constants
    DEFAULT_ASTEROIDS_NUM = 5
    DEFAULT_AST_SIZE = 3
    NUM_OF_TINY_ASTS = 2
    AST_SIZES = {1, 2, 3}
    # |integers| = 1-4 excluding 0
    VALID_AST_SPEED = list(range(-4, 0)) + list(range(1, 5))

    # Ship constants
    SHIP_RADIUS = 1
    INIT_LIVES = 3
    ROTATION_DEGREES = 7

    # Torpedo constants
    TORP_RADIUS = 4
    TORP_LIFESPAN = 200
    MAX_TORPS = 10

    @staticmethod
    def get_asteroid_radius(size):
        return size * 10 - 5
