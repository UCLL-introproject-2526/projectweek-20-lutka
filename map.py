from constants import *
from pygame import *

class Map():
    def __init__(self, player):
        self.Image = image.load("hi.png").convert()
        self.player = player

    def draw(self, game_display):
        window_size = game_display.get_size()
        map_size = self.Image.get_size()
        x = max(0, min(map_size[0] - window_size[0], self.player.x - window_size[0] // 2))
        y = max(0, min(map_size[1] - window_size[1], self.player.y - window_size[1] // 2))
        game_display.blit(self.Image, (-x, -y))