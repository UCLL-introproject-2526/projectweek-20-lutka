from constants import *
from pygame import *


class Player: 
    def __init__(self, vector):
        # position coords
        self.pos = Vector2(vector.x,vector.y)

        sub_image = image.load("submarine.png")
        self.submarine_image = transform.scale(sub_image, (64, 48))
        self.sprite_size = self.submarine_image.get_size()

        # self.rect = self.submarine_image.get_rect(topleft=(int(self.pos.x), int(self.pos.y)))
        # self.hitbox = Rect(
        #     self.rect.x + 16,
        #     self.rect.y + 12,
        #     self.rect.width - 32,
        #     self.rect.height - 24,
        # )
        # self.rect.topleft = (10, 10)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 4
        self.friction = 0.05
        self.facing_right = True

    def updated_hitbox(self, map_size):

        window_width, window_height = GAME_DISPLAY.get_size()
        cam_x = max(0, min(self.pos.x - window_width // 2, map_size[0] - window_width))
        cam_y = max(0, min(self.pos.y - window_height // 2, map_size[1] - window_height))
        draw_pos = self.pos - Vector2(cam_x, cam_y)

        return self.submarine_image.get_rect(topleft=(draw_pos.x, draw_pos.y))


    def draw(self, map_size):

        draw.rect(GAME_DISPLAY, RED, Player.updated_hitbox(self, map_size))

        window_width, window_height = GAME_DISPLAY.get_size()
        cam_x = max(0, min(self.pos.x - window_width // 2, map_size[0] - window_width))
        cam_y = max(0, min(self.pos.y - window_height // 2, map_size[1] - window_height))

        draw_pos = self.pos - Vector2(cam_x, cam_y)

        if self.facing_right:
            GAME_DISPLAY.blit(self.submarine_image, draw_pos)
        else:
            flipped_img = transform.flip(self.submarine_image, True, False)
            GAME_DISPLAY.blit(flipped_img, draw_pos)

    def process_key_input(self, map_size, block_list):

        hitbox = Player.updated_hitbox(self, map_size)
        if hitbox != Rect(992,0,64,48):
            pass

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

        if hitbox.collidelist(block_list) == -1:
            self.pos += self.velocity

        self.pos.x = max(0, min(self.pos.x, map_size[0] - hitbox.width))
        self.pos.y = max(0, min(self.pos.y, map_size[1] - hitbox.height))

        if self.pos.x == 0 or self.pos.x == map_size[0] - hitbox.width:
            self.velocity.x = 0
        if self.pos.y == 0 or self.pos.y == map_size[1] - hitbox.height:
            self.velocity.y = 0

        # self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # self.hitbox.topleft = (self.rect.x + 16, self.rect.y + 12)
