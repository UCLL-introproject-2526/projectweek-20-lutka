from pygame import *
from gamestate import State

# CONSTANTEN
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

CIRCLE_RADIUS = 20
SPEED = 5

RED = (225, 0, 0)
BLACK = (0, 0, 0)

# MAAKT HET WINDOW
def create_main_surface():
    return display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# MAAKT SCHERM ZWART
def clear_surface(surface):
    surface.fill(BLACK)

# MAIN
def main():
    init()

    surface = create_main_surface()
    clock = time.Clock()

    # Startpositie cirkel (middelpunt)
    x = 50
    y = 50

    state = State()

    running = True
    while running:
        clock.tick(60)

        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        # Input
        keys = key.get_pressed()

        if keys[K_LEFT] and x - CIRCLE_RADIUS > 0:
            x -= SPEED
        if keys[K_RIGHT] and x + CIRCLE_RADIUS < SCREEN_WIDTH:
            x += SPEED
        if keys[K_UP] and y - CIRCLE_RADIUS > 0:
            y -= SPEED
        if keys[K_DOWN] and y + CIRCLE_RADIUS < SCREEN_HEIGHT:
            y += SPEED

        # Render
        clear_surface(surface)
        draw.circle(surface, RED, (x, y), CIRCLE_RADIUS)
        display.update()

        # State-logica (zoals in jouw originele code)
        state.process_key_input(state, key)
        state.render(surface)

    quit()

main()
