from pygame import *
import pygame

pygame.init()
window_width = 1024
window_height = 768
game_display = pygame.display.set_mode((window_width, window_height))

bg_image = pygame.image.load('hi.png')

class Map():
    def __init__(self, player):
        self.Image = pygame.image.load("hi.png").convert()
        self.player = player

    def draw(self, game_display):
        window_size = game_display.get_size()
        map_size = self.Image.get_size()
        x = max(0, min(map_size[0] - window_size[0], self.player.x - 200))
        y = max(0, min(map_size[1] - window_size[1], self.player.y - 200))
        return game_display.blit(self.Image, (-x, -y))


class Player: 
    def __init__(self, x, y):
        time_passed = 0
        self.Image = pygame.image.load("sub.png").convert()
        self.x = x
        self.y = y
        """
        map_size = self.Image.get_size()
        self.x += (key[K_RIGHT] - key[K_LEFT]) * 500 * time_passed
        self.y += (key[K_DOWN] - key[K_UP]) * 500 * time_passed
        self.x = max(0, min(map_size[0]-20, self.x))
        self.y = max(0, min(map_size[1]-20, self.y))"""

    def draw(self, game_display, map_size):
        window_size = game_display.get_size()
        center = window_size[0] // 2, window_size[0] // 2

        pos = [self.x, self.y]
        for i in range(2):
            if center[i] < pos[1] <= map_size[i]-center[i]:
                pos[i] = center[i]
            elif pos[1] > map_size[i] - center[i]:
                 pos[i] = window_size[i] - map_size[i] + pos[i]
        game_display.blit(self.Image, (int(pos[0]), int(pos[1])))


class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0

    def update(self, player):
        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.xcoordinate -= 2
            player.x -= 2
        if pressed[K_RIGHT]:
            self.xcoordinate += 2
            player.x += 2
        if pressed[K_UP]:
            self.ycoordinate -= 2
            player.y -= 2
        if pressed[K_DOWN]:
            self.ycoordinate += 2
            player.y += 2

    def render(self, surface):
        """draw.circle(
            surface,
            (250, 0, 0),
            (self.xcoordinate, self.ycoordinate),
            20
        )"""
        display.update()
        display.flip()


def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)


def clear_surface(surface):
    surface.blit(bg_image, (0, 0))


def main():
    init()
    surface = create_main_surface()
    state = State()

    p = Player(50,50)

    m = Map(p)
    
    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        clear_surface(surface)
        m.draw(game_display)

        p.draw(game_display, m.Image.get_size())
        state.update(p)

        state.render(surface)

    # time_passed = clock.tick() / 1000

main()
