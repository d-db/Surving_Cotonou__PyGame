import pygame
import random

from pygame.sprite import Sprite


class Bike(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.bikes_possibilities = ["bild_1.png", "bild_2.png", "bild_3.png", "bild_4.png"]

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(random.choice(self.bikes_possibilities))
        self.rect = self.image.get_rect()

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        # Store the alien's exact vertical position.
        self.y = float(self.rect.y)

    def create_bikes_for_beginning(self, nr, sprite_group):
        """Create a specific number of bikes that should be generated at the beginning"""
        for i in range(nr):
            new_bike = Bike(self)
            sprite_group.add(new_bike)

    def position_bike_up(self, sprite_group):
        """Position all sprites in the group. If a collision is detected, repeat the process."""
        for bike in sprite_group:
            flag = True
            while flag:
                bike.rect.x = random.randint(self.settings.bike_up_x_min, self.settings.bike_up_x_max)
                bike.rect.y = random.randint(self.settings.bike_y_top, self.settings.bike_y_bottom)
                for y in sprite_group:
                    if bike.rect != y.rect:
                        if pygame.Rect.colliderect(bike.rect, y.rect):
                            flag = True
                            break
                        else:
                            flag = False

    def position_bike_down(self, sprite_group):
        """Position all sprites in the group. If a collision is detected, repeat the process."""
        for bike in sprite_group:
            flag = True
            while flag:
                bike.rect.x = random.randint(self.settings.bike_down_x_min, self.settings.bike_down_x_max)
                bike.rect.y = random.randint(self.settings.bike_y_top, self.settings.bike_y_bottom)
                for y in sprite_group:
                    if bike.rect != y.rect:
                        if pygame.Rect.colliderect(bike.rect, y.rect):
                            flag = True
                            break
                        else:
                            flag = False

    def update_position_up(self, sprite_group, speed):
        """Update the position of the bikes going up"""
        for i in sprite_group:
            i.rect.y -= speed

    def update_position_down(self, sprite_group, speed):
        """Update the position of the bikes going down"""
        for i in sprite_group:
            i.rect.y += speed

    def create_bike_up(self, sprite_group):
        """Create new bikes going up - using randint in order to influence the rhythm"""
        number = random.randint(0, self.settings.randint)
        if number == 1:
            flag = True
            while flag:
                new_bike = Bike(self)
                new_bike.rect.y = random.randint(self.settings.bike_up_y_min, self.settings.bike_up_y_max)
                new_bike.rect.x = random.randint(self.settings.bike_up_x_min, self.settings.bike_up_x_max)

                if self._collision_check_running(new_bike, sprite_group):
                    sprite_group.add(new_bike)
                    flag = False

    def create_bike_down(self, sprite_group):
        """Create new bikes going down - using randint in order to influence the rhythm"""
        number = random.randint(0, self.settings.randint)
        if number == 1:
            flag = True
            while flag:
                new_bike = Bike(self)
                new_bike.rect.y = random.randint(self.settings.bike_down_y_min, self.settings.bike_down_y_max)
                new_bike.rect.x = random.randint(self.settings.bike_down_x_min, self.settings.bike_down_x_max)

                if self._collision_check_running(new_bike, sprite_group):
                    sprite_group.add(new_bike)
                    flag = False

    def _collision_check_running(self, new_bike, sprite_group):
        """Checking if new bikes collide with existing ones"""
        for bike in sprite_group:
            if pygame.Rect.colliderect(new_bike.rect, bike.rect):
                return False
        return True

    def remove_bikes_down(self, sprite_group, y_coor):
        """Removing bikes going down from the group if they meet the condition"""
        for bike in sprite_group.copy():
            if bike.rect.y > y_coor:
                sprite_group.remove(bike)

    def remove_bikes_up(self, sprite_group, y_coor):
        """Removing bikes going up from the group if they meet the condition"""
        for bike in sprite_group.copy():
            if bike.rect.y < y_coor:
                sprite_group.remove(bike)

    def blitme(self):
        """Draw the bike at its current location."""
        self.screen.blit(self.image, self.rect)