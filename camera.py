from constants import *
from pygame import *
from gamestate import State

def camera_position(player):
    position = math.Vector2((0, 0))

    position.x = player.xcoordinate #nu gaat die heel precies volgen
    position.y = player.ycoordinate

# in each sprite class: move according to the camera instead of changing the sprite position
# pos_on_the_screen = (self.x_pos - camera.x, self.y_pos - camera.y)