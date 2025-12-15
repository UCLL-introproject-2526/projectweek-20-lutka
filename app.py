import pygame
from pygame.display import flip

def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)

def clear_surface(surface):
    surface.fill((0, 0, 0))

class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0

    def update(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            self.xcoordinate -= 2
        if pressed[pygame.K_RIGHT]:
            self.xcoordinate += 2
        if pressed[pygame.K_UP]:
            self.ycoordinate -= 2
        if pressed[pygame.K_DOWN]:
            self.ycoordinate += 2

    def render(self, surface):
        pygame.draw.circle(
            surface,
            (250, 0, 0),
            (self.xcoordinate, self.ycoordinate),
            20
        )
        flip()

def main():
    pygame.init()
    surface = create_main_surface()
    state = State()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state.update()

        clear_surface(surface)
        state.render(surface)

    pygame.quit()

main()
