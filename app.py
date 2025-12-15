from pygame import *

#maakt het window waarin we dingen kunnen afbeelden
def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)

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

    surface = create_main_surface()

    running = True
    while running:
        # for event in event.get():
        #     if event.type == QUIT:
        #         running = False
        #we voegen nog geen events toe aan de event queue dus ik heb dit even weggecomment tot we het gebruiken
        
        #pump verwerkt automatisch bepaalde events
        event.pump()        

        render_frame(surface, x)
        x += 1

main()