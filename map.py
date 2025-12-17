from constants import *
from pygame import *

class Map():
    def __init__(self, player):
        self.image = image.load("hi.png").convert()
        self.map_size = self.image.get_size()
        self.player = player

# zorgt dat de camera de sub volgt
    def draw(self, game_display):
        window_size = game_display.get_size()
        x = max(0, min(self.map_size[0] - window_size[0], self.player.pos.x - window_size[0] // 2))
        y = max(0, min(self.map_size[1] - window_size[1], self.player.pos.y - window_size[1] // 2))
        game_display.blit(self.image, (-x, -y))