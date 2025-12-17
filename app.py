from pygame import *
from gamestate import State


1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
import pygame as pg
import sys
  
class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
  
class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
    def cleanup(self):
        print('cleaning up Menu state stuff')
    def startup(self):
        print('starting Menu state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
  
class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            print('Game State keydown')
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
  
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()
  
  
settings = {
    'size':(600,400),
    'fps' :60
}
  
app = Control(**settings)
state_dict = {
    'menu': Menu(),
    'game': Game()
}
app.setup_states(state_dict, 'menu')
app.main_game_loop()
pg.quit()
sys.exit()

# CONSTANTEN
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

CIRCLE_RADIUS = 20
SPEED = 5

RED = (225, 0, 0)
BLACK = (0, 0, 0)


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


def main():
    init()
    game_display = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = time.Clock()

    state = State()

    # Create map
    bg_image = image.load('hi.png')
    map_size = bg_image.get_size()
    
    # Create player with map size for boundary checking
    p = Player(50, 50, map_size)
    m = Map(p)
    
    running = True
    while running:
        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        # Process input
        p.process_key_input()
        
        # Draw everything
        m.draw(game_display)
        p.draw(game_display, m.Image.get_size())
        state.render(game_display)
        
        display.flip()  
        clock.tick(60)  

main()