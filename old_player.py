from constants import *
from pygame import *

SPRITE_WIDTH = 64
SPRITE_HEIGHT = SPRITE_WIDTH*3//4
ADD_TO_HITBOX_X = SPRITE_WIDTH//8
ADD_TO_HITBOX_Y = SPRITE_WIDTH//4
SUBTRACT_FROM_HITBOX_WIDTH = SPRITE_WIDTH//4
SUBTRACT_FROM_HITBOX_HEIGHT = SPRITE_WIDTH*5//16

class Player: 
    def __init__(self, vector):
        # position coords
        self.pos = Vector2(vector.x,vector.y)
        sub_image = image.load("submarine.png")
        self.submarine_image = transform.scale(sub_image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        self.sprite_size = self.submarine_image.get_size()
        self.hitbox = self.updated_hitbox()
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.1
        self.max_speed = 4
        self.friction = 0.05
        self.facing_right = True


    def updated_hitbox(self):

        cam_x = max(0, min(self.pos.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
        cam_y = max(0, min(self.pos.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))
        draw_pos = self.pos - Vector2(cam_x, cam_y)

        big_hitbox = self.submarine_image.get_rect(topleft=(draw_pos.x, draw_pos.y))

        return Rect(big_hitbox.x + ADD_TO_HITBOX_X, big_hitbox.y + ADD_TO_HITBOX_Y, big_hitbox.width - SUBTRACT_FROM_HITBOX_WIDTH, big_hitbox.height - SUBTRACT_FROM_HITBOX_HEIGHT)


    def draw(self):

        cam_x = max(0, min(self.pos.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
        cam_y = max(0, min(self.pos.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))

        draw_pos = self.pos - Vector2(cam_x, cam_y)

        if self.facing_right:
            GAME_DISPLAY.blit(self.submarine_image, draw_pos)
        else:
            flipped_img = transform.flip(self.submarine_image, True, False)
            GAME_DISPLAY.blit(flipped_img, draw_pos)

        draw.rect(GAME_DISPLAY, RED, self.updated_hitbox()) #moet uiteindelijk weg


    def process_key_input(self, block_list):

        self.hitbox= self.updated_hitbox() 

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


        # colliding_blocks = self.hitbox.collidelistall(block_list)
        # if colliding_blocks != []:
        #     for i in colliding_blocks:
        #         if dx > 0: # Moving right; Hit the left side of the block
        #             self.pos.right = block_list[i].left
        #         if dx < 0: # Moving left; Hit the right side of the block
        #             self.pos.left = block_list[i].right
        #         if dy > 0: # Moving down; Hit the top side of the block
        #             self.pos.bottom = block_list[i].top
        #         if dy < 0: # Moving up; Hit the bottom side of the block
        #             self.pos.top = block_list[i].bottom

        #         if 
        # else:
        #     self.pos += self.velocity


        # we checken de indices om te zien met welke rect er gebots wordt en dan zetten we de position(dus niet die van de hitbox juist)
        # we gaan moeten kijken langs welke kant er geraakt is
        # we gaan kijken welk hoekpunt van de hitbox collide en dan de kortste weg naar buiten berekenen

        self.move(self.velocity.x, self.velocity.y, block_list)


        #voor de map borders denk ik
        self.pos.x = max(0, min(self.pos.x, MAP_SIZE[0] - self.hitbox.width))
        self.pos.y = max(0, min(self.pos.y, MAP_SIZE[1] - self.hitbox.height))

        if self.pos.x == 0 or self.pos.x == MAP_SIZE[0] - self.hitbox.width:
            self.velocity.x = 0
        if self.pos.y == 0 or self.pos.y == MAP_SIZE[1] - self.hitbox.height:
            self.velocity.y = 0


    def move(self, dx, dy, block_list):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, block_list)
        if dy != 0:
            self.move_single_axis(0, dy, block_list)

    def move_single_axis(self, dx, dy, block_list):
        
        # Move the rect
        self.pos.x += dx
        self.pos.y += dy
        
        sprite_rect = self.submarine_image.get_rect(topleft=(self.pos.x, self.pos.y))

        # If you collide with a block, move out based on velocity
        for block in block_list:
            if self.hitbox.colliderect(block):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.hitbox.right = block.left
                    self.pos.x = self.hitbox.x - (ADD_TO_HITBOX_X + 1)
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.hitbox.left = block.right
                    self.pos.x = self.hitbox.x - (ADD_TO_HITBOX_X + 1)
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.hitbox.bottom = block.top
                    self.pos.y = self.hitbox.y - (ADD_TO_HITBOX_Y + 1)
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.hitbox.top = block.bottom
                    self.pos.y = self.hitbox.y - (ADD_TO_HITBOX_Y + 1)
                self.velocity = Vector2(0,0)

        