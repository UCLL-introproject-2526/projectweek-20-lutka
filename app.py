import pygame
from pygame.display import flip

def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)

def render_frame(surface, xcoordinate):
    pygame.draw.circle(surface, (250, 0, 0), (xcoordinate, 100), 20)
    flip()

def clear_surface(surface):
    surface.fill((0, 0, 0))

def main():
    x = 1
    pygame.init()
    surface = create_main_surface()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_frame(surface, x)
        x += 1
        clear_surface(surface)

main()