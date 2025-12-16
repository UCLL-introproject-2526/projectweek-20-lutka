from constants import *
from pygame import *

#klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0
        self.xtime = 0 
            
    #maakt een nieuwe frame door over de oude te tekenen
    def render(self, surface):
        #flip kopieert de backbuffer naar de frontbuffer zie "Drawing a Circle"
        display.flip()