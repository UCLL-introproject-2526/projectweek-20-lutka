from pygame import *
from gamestate import State

# CONSTANTEN
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

CIRCLE_RADIUS = 20
SPEED = 5

RED = (225, 0, 0)
BLACK = (0, 0, 0)

window_width = 1024
window_height = 768
game_display = display.set_mode((window_width, window_height))

bg_image = image.load('hi.png')

class Map():
    def __init__(self, player):
        self.Image = image.load("hi.png").convert()
        self.player = player

    def draw(self, game_display):
        window_size = game_display.get_size()
        map_size = self.Image.get_size()
        x = max(0, min(map_size[0] - window_size[0], self.player.x - 200))
        y = max(0, min(map_size[1] - window_size[1], self.player.y - 200))
        game_display.blit(self.Image, (-x, -y))


class Player: 
    def __init__(self, x, y):
        time_passed = 0
        self.Image = image.load("sub.png").convert()
        self.x = x
        self.y = y

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

        if pressed[K_LEFT]:
            self.x -= 2
        if pressed[K_RIGHT]:
            self.x += 2
        if pressed[K_UP]:
            self.y -= 2
        if pressed[K_DOWN]:
            self.y += 2


# MAAKT HET WINDOW
def create_main_surface():
    return display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def clear_surface(surface):
    surface.blit(bg_image, (0, 0))


# MAIN
def main():
    init()
    surface = create_main_surface()
    clock = time.Clock()

    # Startpositie cirkel (middelpunt)
    x = 50
    y = 50

    state = State()

    p = Player(50, 50)
    m = Map(p)
    
    running = True
    while running:

        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        clear_surface(surface)
        
        # Process input
        p.process_key_input()
        
        # Draw everything
        m.draw(game_display)
        p.draw(game_display, m.Image.get_size())

        state.render(surface)
        
        display.flip()  
        clock.tick(60)  

main()