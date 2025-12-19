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
        
        # Momentum variabelen
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.5  # Hoe snel je optrek
        self.friction = 0.92     # Hoe snel je stopt (0.9-0.95 is realistisch)
        self.max_speed = 3       # Maximum snelheid

    def draw(self):
        cam_x = max(0, min(self.pos.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
        cam_y = max(0, min(self.pos.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))

        draw_pos = self.pos - Vector2(cam_x, cam_y)

        img = self.submarine_image if self.facing_right else transform.flip(self.submarine_image, True, False)
        GAME_DISPLAY.blit(img, draw_pos)

    def process_key_input(self, block_list):
        pressed = key.get_pressed()
        
        # Versnelling op basis van input
        input_x = 0
        input_y = 0
        
        if pressed[K_LEFT]:
            input_x = -1
            self.facing_right = False

        if pressed[K_RIGHT]:
            input_x = 1
            self.facing_right = True

        if pressed[K_UP]:
            input_y = -1

        if pressed[K_DOWN]:
            input_y = 1
        
        # Pas velocity aan op basis van input
        if input_x != 0:
            self.velocity.x += input_x * self.acceleration
        else:
            # Wrijving toepassen als er geen input is
            self.velocity.x *= self.friction
        
        if input_y != 0:
            self.velocity.y += input_y * self.acceleration
        else:
            # Wrijving toepassen als er geen input is
            self.velocity.y *= self.friction
        
        # Beperk snelheid tot maximum
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        
        # Stop volledig als snelheid heel klein is (voorkomt eeuwig doorglijden)
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0
        
        # Beweeg met velocity
        self.move(self.velocity.x, self.velocity.y, block_list)
        
        # Blijf binnen map grenzen
        self.pos.x = max(0, min(self.pos.x, MAP_SIZE[0] - self.sprite_size[0]))
        self.pos.y = max(0, min(self.pos.y, MAP_SIZE[1] - self.sprite_size[1]))

    def move(self, dx, dy, block_list):
        # Beweeg horizontaal
        if dx != 0:
            old_x = self.pos.x
            self.pos.x += dx
            
            # Check collision horizontaal
            hitbox = self.get_world_hitbox()
            for block in block_list:
                if hitbox.colliderect(block):
                    self.pos.x = old_x
                    self.velocity.x = 0
                    break
        
        # Beweeg verticaal
        if dy != 0:
            old_y = self.pos.y
            self.pos.y += dy
            
            # Check collision verticaal
            hitbox = self.get_world_hitbox()
            for block in block_list:
                if hitbox.colliderect(block):
                    self.pos.y = old_y
                    self.velocity.y = 0
                    break

    def get_world_hitbox(self):
        return Rect(
            int(self.pos.x + ADD_TO_HITBOX_X),
            int(self.pos.y + ADD_TO_HITBOX_Y),
            HITBOX_WIDTH,
            HITBOX_HEIGHT
        )
    
    def elf_system(self, elf_picked_up, elf_image, map_instance):
        # Elf positie berekenen
        elf_world_pos = Vector2(map_instance.elf_cell[1] * CELL_SIZE, map_instance.elf_cell[0] * CELL_SIZE)
        elf_hitbox = Rect(elf_world_pos.x, elf_world_pos.y, CELL_SIZE, CELL_SIZE)
        
        # Check pickup
        if not elf_picked_up and self.get_world_hitbox().colliderect(elf_hitbox):
            elf_picked_up = True
        
        # Teken elf in wereld (als niet opgepikt)
        if not elf_picked_up:
            cam_x = max(0, min(self.pos.x - DISPLAY_WIDTH // 2, MAP_SIZE[0] - DISPLAY_WIDTH))
            cam_y = max(0, min(self.pos.y - DISPLAY_HEIGHT // 2, MAP_SIZE[1] - DISPLAY_HEIGHT))
            screen_pos = elf_world_pos - Vector2(cam_x, cam_y)
            GAME_DISPLAY.blit(elf_image, screen_pos)
        else:
            # Teken elf rechtsboven in inventory
            GAME_DISPLAY.blit(elf_image, (DISPLAY_WIDTH - 74, 10))
        
        # Check win
        has_won = elf_picked_up and self.pos.y < CELL_SIZE
        
        return elf_picked_up, has_won