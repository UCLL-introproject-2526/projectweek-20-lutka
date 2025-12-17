import pygame
import pygame.freetype
from pygame import *

# klasse die de timer bijhoudt
class Timer:
    def __init__(self, max_time):
        self.max_time = max_time
        self.time_left = max_time
        self.TIMER_EVENT = USEREVENT + 1
        time.set_timer(self.TIMER_EVENT, 1000)

        self.bar_x = 680
        self.bar_y = 700
        self.bar_width = 300
        self.bar_height = 20

    def handle_event(self, event):
        if event.type == self.TIMER_EVENT:
            if self.time_left > 0:
                self.time_left -= 1
            else:
                time.set_timer(self.TIMER_EVENT, 0)

    def render(self, surface):
        draw.rect(surface, (100, 100, 100),
                  (self.bar_x, self.bar_y,
                   self.bar_width, self.bar_height))

        current_width = int(
            (self.time_left / self.max_time) * self.bar_width
        )

        draw.rect(surface, (117, 171, 217),
                  (self.bar_x, self.bar_y,
                   current_width, self.bar_height))
        


# klasse die de huidige staat van een object in de gamewereld bijhoudt
class State:
    def __init__(self):
        self.xcoordinate = 0
        self.ycoordinate = 0

    def update(self, allow_input):
        if not allow_input:
            return

        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.xcoordinate -= 2
        if pressed[K_RIGHT]:
            self.xcoordinate += 2
        if pressed[K_UP]:
            self.ycoordinate -= 2
        if pressed[K_DOWN]:
            self.ycoordinate += 2

    # maakt een nieuwe frame door over de oude te tekenen
    def render(self, surface):
        draw.circle(surface, (250, 0, 0),
                    (self.xcoordinate, self.ycoordinate), 20)


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
    pygame.freetype.init()

    surface = create_main_surface()
    GAME_FONT1 = pygame.font.SysFont("New Times Roman", 70, pygame.font.Font.bold)
    GAME_FONT2 = pygame.font.SysFont("Arial", 30)

    state = State()
    running = True
    t = Timer(10)

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

            if t.time_left == 0 and e.type == KEYDOWN and e.key == K_RETURN:
                time.set_timer(t.TIMER_EVENT, 0)
                state = State()
                t = Timer(10)

            t.handle_event(e)

        allow_input = t.time_left > 0
        state.update(allow_input)

        clear_surface(surface)

        state.render(surface)
        t.render(surface)

        if t.time_left == 0:
            text_surface1 = GAME_FONT1.render(
                "Game Over",
                True, (250, 0, 0)
            )
            surface.blit(text_surface1, (355, 300))
            text_surface2 = GAME_FONT2.render(
                "Geen zuurstof! Druk ENTER om opnieuw te beginnen.",
                True, (250, 250, 250)
            )
            surface.blit(text_surface2, (225, 380))

        display.flip()


main()
