from pygame import *
from gamestate import State

#maakt het window waarin we dingen kunnen afbeelden
def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)

#maakt het scherm terug helemaal zwart
def clear_surface(surface):
    surface.fill((0, 0, 0))

#mainfunctie die al de rest zal oproepen
def main():
    #initializeert al de pygame modules
    init()

    surface = create_main_surface()

    state = State()

    running = True
    while running:

        #als er een event op de queue van type QUIT is, dan gaan we stoppen met deze whilelus
        for e in event.get():
            if e.type == QUIT:
                running = False

        state.update()
        
        clear_surface(surface)
        state.render(surface)

main()
