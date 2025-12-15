import pygame
from pygame.display import flip

def create_main_surface():
    screen_size = (1024, 768)
    screen = pygame.display.set_mode(screen_size)
    return screen 

def render_frame(xcoordinate):
    surface = create_main_surface()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.circle(surface, (250, 0, 0), (xcoordinate, 100), 20)  # radius 20
        flip()

    pygame.quit()

def main():
    pygame.init()
    render_frame(100)

main()