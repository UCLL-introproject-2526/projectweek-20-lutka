from pygame import *

#maakt het window waarin we dingen kunnen afbeelden
def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)

<<<<<<< HEAD
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
=======
#maakt een nieuwe frame door over de oude te tekenen
def render_frame(surface, xcoordinate):
    clear_surface(surface)
    draw.circle(surface, (250, 0, 0), (xcoordinate, 100), 20)
    
    #flip kopieert de backbuffer naar de frontbuffer zie "Drawing a Circle"
    display.flip()

#maakt het scherm terug helemaal zwart
def clear_surface(surface):
    surface.fill((0, 0, 0))

#mainfunctie die al de rest zal oproepen
def main():
    x = 1

    #initializeert al de pygame modules
    init()

>>>>>>> 0e9de51e65bda34918a5cdb31b01348d8f6b41a7
    surface = create_main_surface()
    state = State()

    running = True
    while running:

        #als er een event op de queue van type QUIT is, dan gaan we stoppen met deze whilelus
        for e in event.get():
            if e.type == QUIT:
                running = False     

<<<<<<< HEAD
        state.update()
=======
        render_frame(surface, x)
        x += 1
>>>>>>> 0e9de51e65bda34918a5cdb31b01348d8f6b41a7

        clear_surface(surface)
        state.render(surface)

    pygame.quit()

main()
