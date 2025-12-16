from constants import *
from pygame import *
from gamestate import State
import camera

#maakt het window waarin we dingen kunnen afbeelden
def create_main_surface():
    screen_size = (VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
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

    clock = time.Clock()

    running = True
    while running:

        #als er een event op de queue van type QUIT is, dan gaan we stoppen met deze whilelus
        for e in event.get():
            if e.type == QUIT:
                running = False
            # wacht 60s
            clock.tick(15)

        state.update()
        # camera(state) #dit werkt niet ik zal de coords moeten oproepen ma kga daar dan eerst een vector van maken in de state klasse
        # nu wil ik dat de camera zorgt dat er iets anders wordt weergegeven
        
        clear_surface(surface)
        state.render(surface)

main()
