import pygame
import sys

from person import Person
from settings import Settings
from bikes import Bike
from collision_button import Collision
from start_button import Start
from level_up_button import Next_Level
from score_button import Score_Button
from scoreboard import Scoreboard


class SurvivingCotonou:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Initialize Settings:
        self.settings = Settings()

        # Load the background picture
        self.bg = pygame.image.load("bg.png")
        self.start = pygame.image.load("start.jpg")
        self.game_over = pygame.image.load("GO.jpg")
        self.success = pygame.image.load("success.jpg")

        # Initialize pygame.time
        self.clock = pygame.time.Clock()

        # Time stamps
        self.next_level_time = 0
        self.game_over_time = 0
        self.success_time = 0

        # Timer
        self.counter = 0

        # Create the screen
        self.screen = pygame.display.set_mode((self.bg.get_rect().width, self.bg.get_rect().height))
        pygame.display.set_caption("Surviving Cotonou")

        # Make the buttons
        self.collision = Collision(self, "CRAASH!")
        self.start_button = Start(self, "Start")
        self.next_level_button = Next_Level(self, "Next Level")
        self.score_button = Score_Button(self, str(self.settings.total_score))

        # Create a Scoreboard
        self.scoreboard = Scoreboard(self)

        # Create an instance of Person
        self.person = Person(self)

        # Create an instance of Bike
        self.bike = Bike(self)

        # Create a sprite-group for the bikes going up:
        self.bikes_up = pygame.sprite.Group()
        # Create a sprite-group for the bikes going down:
        self.bikes_down = pygame.sprite.Group()

        # Create the bikes for the beginning
        self.bike.create_bikes_for_beginning(10, self.bikes_down)
        self.bike.create_bikes_for_beginning(10, self.bikes_up)

        # Position the initial bikes on the screen
        self.bike.position_bike_down(self.bikes_down)
        self.bike.position_bike_up(self.bikes_up)

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            self._check_events()
            self.person.current_time = pygame.time.get_ticks()

            if not (self.settings.collision or self.settings.next_level or self.settings.start_screen):
                # If there is no collision and the player has not reached the end: continue the game
                self.person.coalision_check(self.settings, self.person, self.bikes_down)
                self.person.coalision_check(self.settings, self.person, self.bikes_up)
                self.person.update()
                self._update_bikes()
                self.next_level_detection()
                self.reduce_score()

            if self.settings.collision:
                # If there is a collision stop the game and prep the scoreboard
                self.person.stop_game(self, self.person, self.settings)
                self.scoreboard.prep_amount_lifes()
                if self.settings.lives == 0:
                    # If no lives remain set settings.game_over to 'True'
                    self.game_over_time = pygame.time.get_ticks()
                    self.settings.game_over = True

            if self.settings.next_level:
                if self.settings.level < 3:
                    self.next_level_preparation()

            if self.settings.score == 0:
                self.game_over_time = pygame.time.get_ticks()
                self.settings.game_over = True

            if not self.settings.end_screen:
                if self.settings.level == 3 and self.person.person_at_end(self):
                    self.settings.total_score += self.settings.score
                    self.success_time = pygame.time.get_ticks()
                    self.settings.end_screen = True

            self._update_screen()

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.start_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.settings.start_screen = False
            self.set_initial_counter()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.person.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.person.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.person.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.person.moving_left = True
        # elif event.key == pygame.K_p:
        #     self._start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.person.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.person.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.person.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.person.moving_left = False

    def _update_bikes(self):
        """Execute all bike related functions"""
        self.bike.update_position_down(self.bikes_down, self.settings.bike_speed)
        self.bike.update_position_up(self.bikes_up, self.settings.bike_speed)
        self.bike.create_bike_down(self.bikes_down)
        self.bike.create_bike_up(self.bikes_up)
        self.bike.remove_bikes_down(self.bikes_down, self.settings.remove_down)
        self.bike.remove_bikes_up(self.bikes_up, self.settings.remove_up)

    def next_level_detection(self):
        if self.person.person_at_end(self) and self.settings.level < 3:
            self.next_level_time = pygame.time.get_ticks()
            self.settings.next_level = True

    def next_level_preparation(self):
        if self.person.current_time - self.next_level_time > 1000:
            self.settings.level += 1
            self.person.center_person()
            self.settings.bike_speed += 3
            self.settings.randint -= 25
            self.settings.total_score += self.settings.score
            self.settings.score = 1000 * self.settings.level
            self.settings.reduction_score *= 5
            self.counter += 5
            self.scoreboard.prep_score()
            self.scoreboard.prep_total_score()
            self.scoreboard.prep_level()
            self.settings.next_level = False

    def _update_screen(self):
        if self.settings.start_screen:
            self.screen.blit(self.start, [0, 0])
            self.start_button.draw_button()

        elif self.settings.end_screen:
            self.screen.blit(self.success, [0, 0])
            total_score = self.settings.total_score
            score = "{:,}".format(total_score)
            self.score_button = Score_Button(self, str(score))
            self.score_button.draw_button()
            if self.person.current_time - self.success_time > 15000:
                sys.exit()

        elif self.settings.game_over:
            # Blit the game over screen and end it after four seconds
            self.screen.blit(self.game_over, [0, 0])

            if self.person.current_time - self.game_over_time > 4000:
                sys.exit()

        else:
            # Redraw the screen during each pass through the loop.
            self.screen.blit(self.bg, [0, 0])

            # Blit the Person
            self.person.blitme()

            # Blit the bike
            self.bikes_down.draw(self.screen)
            self.bikes_up.draw(self.screen)

            # Blit the scoreboard
            self.scoreboard.show_score()

            if self.settings.collision:
                self.collision.draw_button()

            if self.settings.next_level:
                self.next_level_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
        self.clock.tick(60)

    def reset_game(self):
        """Center the personen on the center left position of the screen"""
        self.person.center_person()

    def set_initial_counter(self):
        """Set the initial counter that is needed for the function to reduce the score every second"""
        time = str(self.person.current_time)
        if len(time) == 4:
            self.counter = int(time[0])
        else:
            self.counter = int(time[0:2])

    def reduce_score(self):
        """Reduce the score each time the 'current time' increases by one second"""
        time = str(self.person.current_time)
        if len(time) == 4:
            if time[0] == str(self.counter):
                self.counter += 1
                self.settings.score -= self.settings.reduction_score
                self.scoreboard.prep_score()
        else:
            if time[0:2] == str(self.counter):
                self.counter += 1
                self.settings.score -= self.settings.reduction_score
                self.scoreboard.prep_score()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    sc = SurvivingCotonou()
    sc.run_game()