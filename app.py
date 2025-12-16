from constants import *
from pygame import *
from gamestate import State

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