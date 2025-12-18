from constants import *
from pygame import *

SPRITE_WIDTH = 64
SPRITE_HEIGHT = SPRITE_WIDTH*3//4  

# Hitbox
HITBOX_WIDTH = 36
HITBOX_HEIGHT = 24
ADD_TO_HITBOX_X = (SPRITE_WIDTH - HITBOX_WIDTH) // 2
ADD_TO_HITBOX_Y = (SPRITE_HEIGHT - HITBOX_HEIGHT) // 2

class Player: 
    def __init__(self, vector):
        self.pos = Vector2(vector.x, vector.y)
        sub_image = image.load("assets/Images/submarine.png")
        self.submarine_image = transform.scale(sub_image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.sprite_size = self.submarine_image.get_size()
        self.speed = 3 
        self.facing_right = True

    def draw(self):
        cam_x = max(0, min(self.pos.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
        cam_y = max(0, min(self.pos.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))

        draw_pos = self.pos - Vector2(cam_x, cam_y)

        img = self.submarine_image if self.facing_right else transform.flip(self.submarine_image, True, False)
        GAME_DISPLAY.blit(img, draw_pos)

    def process_key_input(self, block_list):
        pressed = key.get_pressed()
        
        # simpele beweging - elke richting apart
        if pressed[K_LEFT]:
            self.move(-self.speed, 0, block_list)
            self.facing_right = False

        if pressed[K_RIGHT]:
            self.move(self.speed, 0, block_list)
            self.facing_right = True

        if pressed[K_UP]:
            self.move(0, -self.speed, block_list)

        if pressed[K_DOWN]:
            self.move(0, self.speed, block_list)

        # blijf binnen map grenzen
        self.pos.x = max(0, min(self.pos.x, MAP_SIZE[0] - self.sprite_size[0]))
        self.pos.y = max(0, min(self.pos.y, MAP_SIZE[1] - self.sprite_size[1]))

    def move(self, dx, dy, block_list):
        # oude positie
        old_x = self.pos.x
        old_y = self.pos.y
        
        # Probeer te bewegen
        self.pos.x += dx
        self.pos.y += dy
        
        # Check collision
        hitbox = self.get_world_hitbox()
        
        collision = False
        for block in block_list:
            if hitbox.colliderect(block):
                collision = True
                break
        
        # als collision, ga terug naar oude positie
        if collision:
            self.pos.x = old_x
            self.pos.y = old_y

    def get_world_hitbox(self):
        return Rect(
            int(self.pos.x + ADD_TO_HITBOX_X),
            int(self.pos.y + ADD_TO_HITBOX_Y),
            HITBOX_WIDTH,
            HITBOX_HEIGHT
        )