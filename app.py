from pygame import *

#klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0

    def update(self):
        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.xcoordinate -= 2
        if pressed[K_RIGHT]:
            self.xcoordinate += 2
        if pressed[K_UP]:
            self.ycoordinate -= 2
        if pressed[K_DOWN]:
            self.ycoordinate += 2
            
    #maakt een nieuwe frame door over de oude te tekenen
    def render(self, surface):
        draw.circle(
            surface,
            (250, 0, 0),
            (self.xcoordinate, self.ycoordinate),
            20
        )
        #flip kopieert de backbuffer naar de frontbuffer zie "Drawing a Circle"
        display.flip()

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
            time.wait(60)

        state.update()
        
        clear_surface(surface)
        state.render(surface)

main()
