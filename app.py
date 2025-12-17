from pygame import *

submarine_image = image.load("submarine.png")
submarine_image = transform.scale(submarine_image, (80, 40))


# klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.pos = Vector2(10, 10)
        self.rect = submarine_image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
        self.hitbox = Rect(
            self.rect.x + 10,
            self.rect.y + 8,
            self.rect.width - 20,
            self.rect.height - 16,
        )
        self.rect.topleft = (10, 10)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 2
        self.friction = 0.05

        self.facing_right = True

    def update(self):
        pressed = key.get_pressed()
        direction = Vector2(0, 0)

        if pressed[K_LEFT]:
            direction.x = -1
            self.facing_right = False
        if pressed[K_RIGHT]:
            direction.x = 1
            self.facing_right = True
        if pressed[K_UP]:
            direction.y = -1
        if pressed[K_DOWN]:
            direction.y = 1

        if direction.length() != 0:
            direction = direction.normalize()

        self.velocity += direction * self.acceleration

        if direction.length() == 0:
            self.velocity *= 1 - self.friction

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.pos += self.velocity
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

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
