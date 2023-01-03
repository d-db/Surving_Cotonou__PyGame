class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""

        self.start_screen = True
        self.next_level = False
        self.end_screen = False
        self.collision = False
        self.game_over = False

        self.bg_color = (230, 230, 230)

        # Level
        self.level = 1

        # Score at the Beginning of a Level
        self.score = 1000
        self.reduction_score = 10

        # Totalscore
        self.total_score = 0

        # Number of lives
        self.lives = 3

        # Number of bikes right at the beginning
        self.start_bikes = 10

        # Motorcycle settings
        self.bike_speed = 4

        # Person settings
        self.person_speed = 10

        # In which area are bikes going up created
        self.bike_y_top = 10
        self.bike_y_bottom = 900

        self.bike_up_x_min = 660
        self.bike_up_x_max = 980

        self.bike_up_y_min = 950
        self.bike_up_y_max = 1200

        # In which area are bikes going down created
        self.bike_down_x_min = 220
        self.bike_down_x_max = 530

        self.bike_down_y_min = -300
        self.bike_down_y_max = -20

        # Beyond which y_coordinates bikes should be removed
        self.remove_up = -120
        self.remove_down = 1000

        # How quickly the game speeds up
        self.speedup_scale = 1

        # Randint for bike creation
        self.randint = 60

    def reduce_score(self):
        self.score -= 10
