import pygame


class Person:
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Create timestamps for a timer function
        self.current_time = 0
        self.hit_time = 0

        # Load the ship image and get its rect.
        self.image = pygame.image.load('person_2.png')
        self.rect = self.image.get_rect()

        # Start each new ship at the left center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position.
        self.y = float(self.rect.y)

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def coalision_check(self, settings, person, sprite_group):
        """Checks if there is a collision between the person and one of the bikes"""
        for bike in sprite_group:
            if pygame.Rect.colliderect(person.rect, bike.rect):
                settings.collision = True
                person.hit_time = pygame.time.get_ticks()
                break

    def stop_game(self, sc, person, settings):
        """After a collision: recenter the person and increase the counter by 5"""
        if person.current_time - person.hit_time > 1000:
            person.center_person()
            settings.lives -= 1
            sc.counter += 5
            self.settings.collision = False

    def person_at_end(self, sc):
        if sc.person.rect.x > 1200:
            return True

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.person_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.person_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.person_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.person_speed

        # Update rect object from self.y.
        self.rect.y = self.y
        # Update rect object from self.x.
        self.rect.x = self.x

    def center_person(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)