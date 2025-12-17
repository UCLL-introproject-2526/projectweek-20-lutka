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
        window_width, window_height = game_display.get_size()
        cam_x = max(0, min(self.pos.x - window_width // 2, map_size[0] - window_width))
        cam_y = max(0, min(self.pos.y - window_height // 2, map_size[1] - window_height))

        draw_pos = self.pos - Vector2(cam_x, cam_y)

        if self.facing_right:
            game_display.blit(self.submarine_image, draw_pos)
        else:
            flipped_img = transform.flip(self.submarine_image, True, False)
            game_display.blit(flipped_img, draw_pos)

    def process_key_input(self, map_size):
        pressed = key.get_pressed()
        direction = Vector2(0, 0)

        #checkt ook borders
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
        else:
            self.velocity *= 1 - self.friction

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.pos += self.velocity
        self.pos.x = max(0, min(self.pos.x, map_size[0] - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, map_size[1] - self.rect.height))

        if self.pos.x == 0 or self.pos.x == map_size[0] - self.rect.width:
            self.velocity.x = 0
        if self.pos.y == 0 or self.pos.y == map_size[1] - self.rect.height:
            self.velocity.y = 0

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        self.hitbox.topleft = (self.rect.x + 10, self.rect.y + 8)
