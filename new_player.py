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

        self.hitbox = Rect(vector.x, vector.y, SPRITE_WIDTH - SUBTRACT_FROM_HITBOX_WIDTH, SPRITE_HEIGHT - SUBTRACT_FROM_HITBOX_HEIGHT)

        self.velocity_vector = math.Vector2(0, 0)
        self.acceleration_direction = math.Vector2(0,0)        
        self.acceleration_magnitude = 0.1
        self.max_speed = 4
        self.friction_magnitude = 0.05
        self.facing_right = True


    def update_hitbox(self):

        cam_x = max(0, min(self.hitbox.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
        cam_y = max(0, min(self.hitbox.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))

        self.hitbox.x -= cam_x
        self.hitbox.y -= cam_y


    def draw(self):

        draw.rect(GAME_DISPLAY, RED, self.hitbox) #moet uiteindelijk weg


    def process_key_input(self, dt, block_list):

        self.update_hitbox() 

        pressed = key.get_pressed()

        if pressed[K_LEFT]:
            self.acceleration_direction = math.Vector2(-1,0)
            self.facing_right = False
        if pressed[K_RIGHT]:
            self.acceleration_direction = math.Vector2(1,0)
            self.facing_right = True
        if pressed[K_UP]:
            self.acceleration_direction = math.Vector2(0,-1)
        if pressed[K_DOWN]:
            self.acceleration_direction = math.Vector2(0,1)

        # if self.acceleration_direction.magnitude() != 0:

        position = math.Vector2(self.hitbox.x, self.hitbox.y)
        movement = math.Vector2(0,0)


        movement = position + self.velocity_vector*dt + self.acceleration_magnitude*self.normalize(self.acceleration_direction)*dt*dt
        
        self.velocity_vector = self.velocity_vector + self.acceleration_magnitude*self.normalize(self.acceleration_direction)*dt - self.friction_magnitude*self.normalize(self.velocity_vector)

        if self.velocity_vector.magnitude() <= 0.01:
            self.velocity_vector = math.Vector2(0,0)

        if self.velocity_vector.magnitude() > self.max_speed:
            self.velocity_vector = self.normalize(self.velocity_vector) * self.max_speed



        self.move(movement.x, movement.y, block_list)


        #voor de map borders denk ik
        self.hitbox.x = max(0, min(self.hitbox.x, MAP_SIZE[0] - self.hitbox.width))
        self.hitbox.y = max(0, min(self.hitbox.y, MAP_SIZE[1] - self.hitbox.height))

        if self.hitbox.x == 0 or self.hitbox.x == MAP_SIZE[0] - self.hitbox.width:
            self.velocity_vector.x = 0
        if self.hitbox.y == 0 or self.hitbox.y == MAP_SIZE[1] - self.hitbox.height:
            self.velocity_vector.y = 0

    def normalize(self, vector):
        if vector != math.Vector2(0,0):
            vector.normalize()
        return vector



    def move(self, dx, dy, block_list):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, block_list)
        if dy != 0:
            self.move_single_axis(0, dy, block_list)

    def move_single_axis(self, dx, dy, block_list):
        
        # Move the rect
        self.hitbox.x += dx
        self.hitbox.y += dy

        # If you collide with a wall, move out based on velocity
        for block in block_list:
            if self.hitbox.colliderect(block):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.hitbox.right = block.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.hitbox.left = block.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.hitbox.bottom = block.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.hitbox.top = block.bottom        