from constants import *
from pygame import *

class Player: 
    def __init__(self, x, y, map_size):
        self.Image = image.load("sub.png").convert()
        self.x = x
        self.y = y
        self.map_size = map_size
        self.sprite_size = self.Image.get_size()

    def draw(self, game_display, map_size):
        window_size = game_display.get_size()
        center = window_size[0] // 2, window_size[1] // 2 

        pos = [self.x, self.y]
        for i in range(2):
            if center[i] < pos[i] <= map_size[i] - center[i]: 
                pos[i] = center[i]
            elif pos[i] > map_size[i] - center[i]:
                pos[i] = window_size[i] - map_size[i] + pos[i]
        game_display.blit(self.Image, (int(pos[0]), int(pos[1])))

    def process_key_input(self):
        pressed = key.get_pressed()

        # Borders
        if pressed[K_LEFT] and self.x > 0:
            self.x -= SPEED
        if pressed[K_RIGHT] and self.x + self.sprite_size[0] < self.map_size[0]:
            self.x += SPEED
        if pressed[K_UP] and self.y > 0:
            self.y -= SPEED
        if pressed[K_DOWN] and self.y + self.sprite_size[1] < self.map_size[1]:
            self.y += SPEED

