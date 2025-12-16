from pygame import *
import pygame

pygame.init()
window_width = 1024
window_height = 768
game_display = pygame.display.set_mode((window_width, window_height))

bg_image = pygame.image.load('hi.png')

class Map():
    def __init__(self):
        self.Image = pygame.image.load("hi.png").convert()

    def draw(self, game_display):
        window_size = game_display.get_size()
        map_size = self.Image.get_size()
        x = max(0, min(map_size[0] - window_size[0], self.player.x - 200))
        y = max(0, min(map_size[1] - window_size[1], self.player.y - 200))
        return game_display.blit(self.Image, (-x, -y))


class Player: 
    def __init__(self, x, y):
        time_passed = 0
        map_size = self.Image.get_size()
        self.x += (key[K_RIGHT] - key[K_LEFT]) * 500 * time_passed
        self.y += (key[K_DOWN] - key[K_UP]) * 500 * time_passed
        self.x = max(0, min(map_size[0]-20, self.x))
        self.y = max(0, min(map_size[1]-20, self.y))

    def draw(self, game_display, map_size):
        window_size = game_display.get_size()
        center = window_size[0] // 2, window_size[0] // 2

        pos = [self.x, self.y]
        for i in range(2):
            if center[i] < pos[1] <= map_size[i]-center[i]:
                pos[i] = center[i]
            elif pos[1] > map_size[i] - center[i]:
                 pos[i] = window_size[i] - map_size[i] + pos[i]
        game_display.blit(bg_image, (int(pos[0]), int(pos[1])))


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

    def render(self, surface):
        draw.circle(
            surface,
            (250, 0, 0),
            (self.xcoordinate, self.ycoordinate),
            20
        )
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

    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

        clear_surface(surface)
        state.update()
        state.render(surface)

        Map.draw(game_display)
        Player.draw(game_display, map.Image.get_size())

    # time_passed = clock.tick() / 1000

main()
