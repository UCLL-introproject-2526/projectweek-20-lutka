from constants import *
from pygame import *

class Player: 
    def __init__(self, vector):
        self.Image = image.load("sub.png").convert()
        # position coords
        self.pos = Vector2(vector.x,vector.y)

        self.sprite_size = self.Image.get_size()

    def draw(self, game_display, map_size):
        window_size = game_display.get_size()
        center = window_size[0] // 2, window_size[1] // 2 

        pos = [self.pos.x, self.pos.y]
        for i in range(2):
            if center[i] < pos[i] <= map_size[i] - center[i]: 
                pos[i] = center[i]
            elif pos[i] > map_size[i] - center[i]:
                pos[i] = window_size[i] - map_size[i] + pos[i]
        game_display.blit(self.Image, (int(pos[0]), int(pos[1])))

    def process_key_input(self, map_size):
        pressed = key.get_pressed()

        # Borders #borders moeten ergensanders gecheckt worden
        if pressed[K_LEFT] and self.pos.x > 0:
            self.pos.x -= SPEED
        if pressed[K_RIGHT] and self.pos.x + self.sprite_size[0] < map_size[0]:
            self.pos.x += SPEED
        if pressed[K_UP] and self.pos.y > 0:
            self.pos.y -= SPEED
        if pressed[K_DOWN] and self.pos.y + self.sprite_size[1] < map_size[1]:
            self.pos.y += SPEED

