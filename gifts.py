from pygame import *
import random as r
from constants import *

# Constanten
WATER = 0
ROCK = 1
GIFT1 = 7
GIFT2 = 8 

# Laad en schaal pakje afbeeldingen
package_image1 = transform.scale(
    image.load('assets/images/pakje1.png'), 
    (CELL_SIZE - 30, CELL_SIZE - 30)
)
package_image2 = transform.scale(
    image.load('assets/images/pakje2.png'), 
    (CELL_SIZE - 30, CELL_SIZE - 30)
)

# Globale teller voor opgepakte pakjes
packages_collected = 0

# reset de pakjes counter naar 0
def reset_package_counter():
    global packages_collected
    packages_collected = 0

# aantel opgepakte pakjes terug krijgen
def get_package_count():
    return packages_collected

# spawn pakje op een willekeurige positie in het water
def spawn_gift_in_matrix(world_matrix):
    water_positions = []
    
    for row in range(ROWS):
        for col in range(COLS):
            if world_matrix[row][col] == WATER:
                water_positions.append((row, col))
    
    if water_positions:
        row, col = r.choice(water_positions)
        world_matrix[row][col] = r.choice([GIFT1, GIFT2])
        return True
    return False

# spawn meerdere gifts
def spawn_multiple_gifts(world_matrix, amount=20):
    spawned = 0
    for _ in range(amount):
        if spawn_gift_in_matrix(world_matrix):
            spawned += 1
    return spawned

# collision voor alle pakjes maken (met WORLD COORDINATES)
def get_gift_rects(world_matrix):
    gift_rects = []
    current_cell_origin = Vector2(0, 0)
    
    for row in range(ROWS):
        for col in range(COLS):
            cell = world_matrix[row][col]
            if cell == GIFT1 or cell == GIFT2:
                # Maak rect in world coordinates
                gift_rect = Rect(
                    current_cell_origin.x,
                    current_cell_origin.y,
                    CELL_SIZE,
                    CELL_SIZE
                )
                gift_rects.append((gift_rect, cell, row, col))
            
            current_cell_origin.x += CELL_SIZE
        
        current_cell_origin.x = 0
        current_cell_origin.y += CELL_SIZE
    
    return gift_rects

# Gift teken op het scherm met camera offset
# world_materix = wereld grid
# capera_pos = Vector2 met camera positie 
def draw_all_gifts(world_matrix, camera_pos):
    gift_rects = get_gift_rects(world_matrix)
    
    for gift_rect, gift_type, row, col in gift_rects:
        # Converteer world coordinates naar screen coordinates
        screen_x = gift_rect.x - camera_pos.x + 15
        screen_y = gift_rect.y - camera_pos.y + 15
        
        # Teken alleen als op scherm zichtbaar
        if (-CELL_SIZE < screen_x < DISPLAY_WIDTH and 
            -CELL_SIZE < screen_y < DISPLAY_HEIGHT):
            
            if gift_type == GIFT1:
                GAME_DISPLAY.blit(package_image1, (screen_x, screen_y))
            else:
                GAME_DISPLAY.blit(package_image2, (screen_x, screen_y))

# check gift collision + update game state
def update_game_with_gifts(world_matrix, player, timer, state):
    global packages_collected
    
    # Get player hitbox in world coordinates
    player_hitbox = player.get_world_hitbox()
    
    # Get alle gift rects
    gift_rects = get_gift_rects(world_matrix)
    
    for gift_rect, gift_type, row, col in gift_rects:
        if player_hitbox.colliderect(gift_rect):
            # 1. Verwijder gift van map
            world_matrix[row][col] = WATER
            
            # 2. Voeg oxygen toe
            timer.add_oxygen(5)
            
            # 3. Verhoog counter
            packages_collected += 1
            
            # 4. Update state score
            state.score += 1

            pickup_sound = mixer.Sound("assets/Sounds/pickup.mp3")
            pickup_sound.set_volume(0.5)
            pickup_sound.play()
            
            return True
    
    return False

# check of pakje is opgepakt
def check_player_gift_collision(world_matrix, player_rect, timer=None, oxygen_amount=5):
    global packages_collected
    
    # Get alle gift rects in world coordinates
    gift_rects = get_gift_rects(world_matrix)
    
    for gift_rect, gift_type, row, col in gift_rects:
        # Check collision tussen player en gift (beide in world coordinates)
        if player_rect.colliderect(gift_rect):
            # 1. Verwijder gift van map (zet terug naar water)
            world_matrix[row][col] = WATER
            
            # 2. Voeg oxygen toe
            if timer and hasattr(timer, 'add_oxygen'):
                timer.add_oxygen(oxygen_amount)
            
            # 3. Verhoog de teller
            packages_collected += 1
            
            return True
    
    return False

# aantal pakjes tellen op de map
def count_gifts_on_map(world_matrix):
    count = 0
    for row in world_matrix:
        for cell in row:
            if cell == GIFT1 or cell == GIFT2: 
                count += 1
    return count

# teken de pakjes op het scherm
def draw_package_counter(font, x=10, y=10):
    counter_text = f"Pakjes: {packages_collected}"
    text_surface = font.render(counter_text, True, (255, 255, 255))
    
    # Teken achtergrond voor leesbaarheid
    bg_rect = text_surface.get_rect()
    bg_rect.topleft = (x, y)
    bg_rect.inflate_ip(20, 10)
    draw.rect(GAME_DISPLAY, (0, 0, 0, 180), bg_rect)
    
    # Teken tekst
    GAME_DISPLAY.blit(text_surface, (x + 10, y + 5))