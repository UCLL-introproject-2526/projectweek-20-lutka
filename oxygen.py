import pygame
import pygame.freetype
from pygame import *

# klasse die de timer bijhoudt
class Timer:
    def __init__(self, max_time):
        self.max_time = max_time
        self.time_left = max_time

        self.bar_x = 680
        self.bar_y = 700
        self.bar_width = 300
        self.bar_height = 20
        
        # Laad de achtergrondafbeelding 1 keer
        self.background = image.load('assets/images/achtergrong_oxygen.png')
    
    def update(self, dt):
        if self.time_left > 0:
            self.time_left -= dt
            if self.time_left < 0:
                self.time_left = 0

    def refill(self):
        self.time_left = self.max_time

    def add_oxygen(self, amount):
        self.time_left = min(self.time_left + amount, self.max_time)

    def render(self, surface):
        # Bereken de gecentreerde positie voor de achtergrond
        bg_width = self.background.get_width()
        bg_height = self.background.get_height()
        
        centered_x = self.bar_x + (self.bar_width - bg_width) // 2
        centered_y = self.bar_y + (self.bar_height - bg_height) // 2
        
        # Teken de gecentreerde achtergrondafbeelding
        surface.blit(self.background, (centered_x, centered_y))

        current_width = round(
            (self.time_left / self.max_time) * self.bar_width
        )

        # Blauwe voorgrond (oxygen level)
        draw.rect(surface, (21, 129, 191),
                  (self.bar_x, self.bar_y,
                   current_width, self.bar_height))