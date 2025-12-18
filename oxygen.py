import pygame
import pygame.freetype
from pygame import *


# klasse die de timer bijhoudt
class Timer:
    def __init__(self, max_time):
        self.max_time = max_time
        self.time_left = max_time
        # self.TIMER_EVENT = USEREVENT + 1
        # time.set_timer(self.TIMER_EVENT, 1000)

        self.bar_x = 680
        self.bar_y = 700
        self.bar_width = 300
        self.bar_height = 20

        # def handle_event(self, event):
        # if event.type == self.TIMER_EVENT:
        # if self.time_left > 0:
        # self.time_left -= 1
        # else:
        # time.set_timer(self.TIMER_EVENT, 0)

    def update(self, dt):
        if self.time_left > 0:
            self.time_left -= dt
            if self.time_left < 0:
                self.time_left = 0

    def refill(self):
        self.time_left = self.max_time

    def render(self, surface):
        draw.rect(
            surface,
            (87, 89, 91),
            (self.bar_x, self.bar_y, self.bar_width, self.bar_height),
        )

        current_width = round((self.time_left / self.max_time) * self.bar_width)

        draw.rect(
            surface,
            (21, 129, 191),
            (self.bar_x, self.bar_y, current_width, self.bar_height),
        )
