from constants import *
from pygame import *

class Player: 
    def __init__(self, vector):
        # position coords
        self.pos = Vector2(vector.x,vector.y)

        sub_image = image.load("submarine.png")
        self.submarine_image = transform.scale(sub_image, (80, 40))
        self.sprite_size = self.submarine_image.get_size()

        self.rect = self.submarine_image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
        self.hitbox = Rect(
            self.rect.x + 10,
            self.rect.y + 8,
            self.rect.width - 20,
            self.rect.height - 16,
        )
        self.rect.topleft = (10, 10)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 4
        self.friction = 0.05
        self.facing_right = True


    def draw(self, game_display, map_size):
        window_size = game_display.get_size()
        center = window_size[0] // 2, window_size[1] // 2 

        pos = [self.pos.x, self.pos.y]
        for i in range(2):
            if center[i] < pos[i] <= map_size[i] - center[i]: 
                pos[i] = center[i]
            elif pos[i] > map_size[i] - center[i]:
                pos[i] = window_size[i] - map_size[i] + pos[i]
        

        if self.facing_right:
            game_display.blit(self.submarine_image, self.rect)
        else:
            flipped_img = transform.flip(self.submarine_image, True, False)
            game_display.blit(flipped_img, self.rect)

    def process_key_input(self, map_size):
        pressed = key.get_pressed()
        direction = Vector2(0, 0)

        #checkt ook borders
        if pressed[K_LEFT] and self.pos.x > 0:
            direction.x = -1
            self.facing_right = False
        if pressed[K_RIGHT] and self.pos.x + self.sprite_size[0] < map_size[0]:
            direction.x = 1
            self.facing_right = True
        if pressed[K_UP] and self.pos.y > 0:
            direction.y = -1
        if pressed[K_DOWN] and self.pos.y + self.sprite_size[1] < map_size[1]:
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