from pygame import *
import pygame

pygame.init()
window_width = 1024
window_height = 768
game_display = pygame.display.set_mode((window_width, window_height))

bg_image = pygame.image.load('BASECOLOURbg.png')


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

        state.update()
        clear_surface(surface)
        state.render(surface)


main()
