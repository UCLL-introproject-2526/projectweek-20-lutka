from constants import *
from pygame import *

#klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0

    def update(self):
        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.xcoordinate -= 2
        if pressed[K_RIGHT]:
            self.xcoordinate += 2
        if pressed[K_UP]:
            self.ycoordinate -= 2
        if pressed[K_DOWN]:
            self.ycoordinate += 2
            
    #maakt een nieuwe frame door over de oude te tekenen
    def render(self, surface):
        draw.circle(
            surface,
            (250, 0, 0),
            (self.xcoordinate, self.ycoordinate),
            20
        )
        #flip kopieert de backbuffer naar de frontbuffer zie "Drawing a Circle"
        display.flip()