from pygame import *

submarine_image = image.load("submarine.png")
submarine_image = transform.scale(submarine_image, (80, 40))


# klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.rect = submarine_image.get_rect()
        self.rect.topleft = (10, 10)

        self.hitbox = Rect(
            self.rect.x + 10,
            self.rect.y + 8,
            self.rect.width - 20,
            self.rect.height - 16,
        )

        self.facing_right = True

    def update(self):
        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.rect.x -= 2
            self.facing_right = False
        if pressed[K_RIGHT]:
            self.rect.x += 2
            self.facing_right = True
        if pressed[K_UP]:
            self.rect.y -= 2
        if pressed[K_DOWN]:
            self.rect.y += 2

        self.hitbox.topleft = (self.rect.x + 10, self.rect.y + 8)

    # maakt een nieuwe frame door over de oude te tekenen
    def render(self, surface):
        if self.facing_right:
            surface.blit(submarine_image, self.rect)
        else:
            flipped_img = transform.flip(submarine_image, True, False)
            surface.blit(flipped_img, self.rect)
        # flip kopieert de backbuffer naar de frontbuffer zie "Drawing a Circle"
        display.flip()


# maakt het window waarin we dingen kunnen afbeelden
def create_main_surface():
    screen_size = (1024, 768)
    return display.set_mode(screen_size)


# maakt het scherm terug helemaal zwart
def clear_surface(surface):
    surface.fill((0, 0, 0))


# mainfunctie die al de rest zal oproepen
def main():
    # initializeert al de pygame modules
    init()

    surface = create_main_surface()

    state = State()

    running = True
    while running:

        # als er een event op de queue van type QUIT is, dan gaan we stoppen met deze whilelus
        for e in event.get():
            if e.type == QUIT:
                running = False
            time.wait(60)

        state.update()

        clear_surface(surface)
        state.render(surface)


main()
