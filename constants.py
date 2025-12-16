from pygame import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CIRCLE_RADIUS = 20
SPEED = 5

RED = (225, 0, 0)
BLACK = (0, 0, 0)


MAP_LEFTTOP = Vector2((0,0))
MAP_RIGHTBOTTOM = Vector2((SCREEN_WIDTH*5,SCREEN_HEIGHT*5)) #moet anders eenmaal we weten hoe breed en diep onze achtergrondafbeelding/map is