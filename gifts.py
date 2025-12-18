from pygame import *
import random as r
from constants import *

water = 0
rock = 1
gift1 = 7
gift2 = 8 

package_image1 = transform.scale(
    image.load('assets/images/pakje1.png'), 
    (CELL_SIZE - 30, CELL_SIZE - 30)
)
package_image2 = transform.scale(
    image.load('assets/images/pakje2.png'), 
    (CELL_SIZE - 30, CELL_SIZE - 30)
)

def spawn_gift_in_matrix(world_matrix):
    water_positions = []
    for row in range(ROWS):
        for col in range(COLS):
            if world_matrix[row][col] == water:
                water_positions.append((row, col))
    
    if water_positions:
        row, col = r.choice(water_positions)
        # Random kiezen tussen gift1 en gift2
        world_matrix[row][col] = r.choice([gift1, gift2])
        return True
    return False


def spawn_multiple_gifts(world_matrix, amount=5):
    spawned = 0
    for _ in range(amount):
        if spawn_gift_in_matrix(world_matrix):
            spawned += 1
    return spawned


def draw_all_gifts(screen, world_matrix, player_pos):
    window_width, window_height = screen.get_size()
    cam_x = max(0, min(player_pos.x - window_width // 2, MAP_SIZE[0] - window_width))
    cam_y = max(0, min(player_pos.y - window_height // 2, MAP_SIZE[1] - window_height))
    
    for row in range(ROWS):
        for col in range(COLS):
            cell = world_matrix[row][col]
            if cell == gift1 or cell == gift2:
                x = col * CELL_SIZE + 5 - cam_x
                y = row * CELL_SIZE + 5 - cam_y
                # Teken de juiste afbeelding
                if cell == gift1:
                    screen.blit(package_image1, (x, y))
                else:
                    screen.blit(package_image2, (x, y))


def check_player_gift_collision(world_matrix, player_pos, timer=None, oxygen_amount=3):
    player_col = int(player_pos.x // CELL_SIZE)
    player_row = int(player_pos.y // CELL_SIZE)
    
    if 0 <= player_row < ROWS and 0 <= player_col < COLS:
        cell = world_matrix[player_row][player_col]
        if cell == gift1 or cell == gift2:
            world_matrix[player_row][player_col] = water
            
            if timer:
                timer.add_oxygen(oxygen_amount)
            
            return True
    return False

def count_gifts_on_map(world_matrix):
    count = 0
    for row in world_matrix:
        for cell in row:
            if cell == gift1 or cell == gift2: 
                count += 1
    return count