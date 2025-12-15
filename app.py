import pygame
def create_main_surface():
        # Initialize Pygame
        pygame.init()

        # Tuple representing width and height in pixels
        screen_size = (1024, 768)

        # Create window with given size
        pygame.display.set_mode(screen_size)

        while True:
            pass  # Busy-wait for keyboard interrupt (Ctrl+C)

print(create_main_surface())