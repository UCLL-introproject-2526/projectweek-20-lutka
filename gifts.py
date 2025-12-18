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


def reset_package_counter():
    """Reset de pakjes teller naar 0"""
    global packages_collected
    packages_collected = 0


def get_package_count():
    """Krijg het huidige aantal opgepakte pakjes"""
    return packages_collected


def spawn_gift_in_matrix(world_matrix):
    """Spawn één gift op een willekeurige water positie"""
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


def spawn_multiple_gifts(world_matrix, amount=5):
    """Spawn meerdere gifts op de map"""
    spawned = 0
    for _ in range(amount):
        if spawn_gift_in_matrix(world_matrix):
            spawned += 1
    print(f"{spawned} pakjes gespawned op de map")
    return spawned


def get_gift_rects(world_matrix):
    """
    Maak collision rects voor alle gifts in WORLD COORDINATES
    (net zoals get_world_rects voor rocks)
    
    Returns: list van (rect, gift_type, row, col) tuples
    """
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


def draw_all_gifts(world_matrix, camera_pos):
    """
    Teken alle gifts op het scherm met camera offset
    (net zoals draw_world voor rocks)
    
    Args:
        world_matrix: De wereld grid
        camera_pos: Vector2 met camera positie (van tracking_player)
    """
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


def update_game_with_gifts(world_matrix, player, timer, state):
    """
    Check gift collision en update game state
    Roep deze functie aan in je main game loop!
    
    Args:
        world_matrix: De wereld grid
        player: Player object met .rect of .get_world_hitbox()
        timer: Timer object
        state: State object met .score
    
    Returns:
        True als een pakje is opgepakt
    """
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
            
            print(f"✓ Pakje opgepakt! Score: {state.score} | Oxygen +5")
            return True
    
    return False


def check_player_gift_collision(world_matrix, player_rect, timer=None, oxygen_amount=5):
    """
    Check of speler een gift oppakt (collision in WORLD COORDINATES)
    
    Args:
        world_matrix: De wereld grid
        player_rect: pygame.Rect van de speler (in world coordinates!)
        timer: Timer object met add_oxygen() methode
        oxygen_amount: Hoeveel oxygen toe te voegen
        
    Returns:
        True als een gift is opgepakt, anders False
    """
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
            
            print(f"✓ Pakje opgepakt! Totaal: {packages_collected} | Oxygen +{oxygen_amount}")
            return True
    
    return False


def count_gifts_on_map(world_matrix):
    """Tel hoeveel gifts er nog op de map zijn"""
    count = 0
    for row in world_matrix:
        for cell in row:
            if cell == GIFT1 or cell == GIFT2: 
                count += 1
    return count


def draw_package_counter(font, x=10, y=10):
    """
    Teken de pakjes counter op het scherm
    
    Args:
        font: pygame font object
        x, y: Positie op scherm
    """
    counter_text = f"Pakjes: {packages_collected}"
    text_surface = font.render(counter_text, True, (255, 255, 255))
    
    # Teken achtergrond voor leesbaarheid
    bg_rect = text_surface.get_rect()
    bg_rect.topleft = (x, y)
    bg_rect.inflate_ip(20, 10)
    draw.rect(GAME_DISPLAY, (0, 0, 0, 180), bg_rect)
    
    # Teken tekst
    GAME_DISPLAY.blit(text_surface, (x + 10, y + 5))