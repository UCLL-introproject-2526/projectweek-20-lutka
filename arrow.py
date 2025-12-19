from pygame import *
import math

class ArrowIndicator:
    def __init__(self):
        self.active = False
        self.pulse_time = 0
        self.duration = 0
        self.max_duration = 2.0
        self.has_been_activated = False 
        
    def activate(self):
        if not self.has_been_activated:
            self.active = True
            self.pulse_time = 0
            self.duration = 0
            self.has_been_activated = True
    
    def deactivate(self):
        self.active = False
    
    # reset voor nieuwe game
    def reset(self):
        self.active = False
        self.has_been_activated = False
        self.pulse_time = 0
        self.duration = 0
    
    # update timer
    def update(self, dt):
        if self.active:
            self.duration += dt
            if self.duration >= self.max_duration:
                self.deactivate()
    
    def draw(self, screen, player_screen_x, player_screen_y):
        if not self.active:
            return
        
        # Simpele pulse animatie
        self.pulse_time += 0.1
        bounce = abs(math.sin(self.pulse_time)) * 10
        
        # Pijl positie boven speler
        arrow_x = player_screen_x
        arrow_y = player_screen_y - 60 - bounce
        
        # Teken driehoek
        size = 15
        points = [
            (arrow_x, arrow_y),
            (arrow_x - size, arrow_y + size * 1.5),
            (arrow_x + size, arrow_y + size * 1.5)
        ]
        draw.polygon(screen, (255, 215, 0), points)