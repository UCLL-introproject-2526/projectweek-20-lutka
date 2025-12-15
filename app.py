import pygame
from pygame.display import flip

def create_main_surface():
        # Initialize Pygame
        pygame.init()

        # Tuple representing width and height in pixels
        screen_size = (1024, 768)

        # Create window with given size
        pygame.display.set_mode(screen_size)

        while True:
            pass  # Busy-wait for keyboard interrupt (Ctrl+C)

surface = create_main_surface()
pygame.draw.circle(surface, (250,0,0), (100,100), 20, 50)
flip()