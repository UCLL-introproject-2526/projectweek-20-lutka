from pygame import *

def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)

def render_frame(surface, xcoordinate):
    clear_surface(surface)
    draw.circle(surface, (250, 0, 0), (xcoordinate, 100), 20)
    display.flip()

def clear_surface(surface):
    surface.fill((0, 0, 0))

def main():
    x = 1
    init()
    surface = create_main_surface()

    running = True
    while running:
        # for event in event.get():
        #     if event.type == QUIT:
        #         running = False
        #we voegen nog geen events toe aan de event queue dus ik heb dit even weggecomment tot we het gebruiken

        render_frame(surface, x)
        x += 1

main()