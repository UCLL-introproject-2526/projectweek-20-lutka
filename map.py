import random as r
from constants import *
from pygame import *

class Map():
    def __init__(self, player):
        bg_image = image.load("achtergrond gradient.png").convert()
        self.background_image = transform.scale(bg_image, MAP_SIZE)
        self.player = player

    def tracking_player(self):
        x = max(0, min(MAP_SIZE[0] - DISPLAY_WIDTH, self.player.pos.x - DISPLAY_WIDTH // 2))
        y = max(0, min(MAP_SIZE[1] - DISPLAY_HEIGHT, self.player.pos.y - DISPLAY_HEIGHT // 2))
        return Vector2(x, y)

    def draw(self, blocks_list):
        position = self.tracking_player()
        GAME_DISPLAY.blit(self.background_image, (-position.x, -position.y))
        # camera positie doorgeven
        self.draw_world(blocks_list, position)

    def get_world_rects(self, matrix):
        # geen camera offset - pure world coordinates
        current_cell_origin = Vector2(0, 0)
        rect_list = []

        for i in range(ROWS):    
            for j in range(COLS):
                if matrix[i][j] == 1:
                    # maak rects in world coordinates (zonder camera offset)
                    rock = Rect(current_cell_origin.x, current_cell_origin.y, CELL_SIZE, CELL_SIZE)
                    rect_list.append(rock)
                current_cell_origin.x += CELL_SIZE
            current_cell_origin.x = 0
            current_cell_origin.y += CELL_SIZE

        return rect_list

    def draw_world(self, blocks_list, camera_pos):
        # teken blokken met camera offset
        for rock in blocks_list:
            # converteer world coordinates naar screen coordinates
            screen_rect = Rect(
                rock.x - camera_pos.x,
                rock.y - camera_pos.y,
                rock.width,
                rock.height
            )
            # teken alleen als op scherm zichtbaar
            if screen_rect.right > 0 and screen_rect.left < DISPLAY_WIDTH and \
               screen_rect.bottom > 0 and screen_rect.top < DISPLAY_HEIGHT:
                draw.rect(GAME_DISPLAY, GREY, screen_rect)

    def generate_world(self):
        water = 0
        rock = 1
        gift = 7

        # Een 0 is water, een 1 is rots, een 7 is pakje
        world_matrix = []

        world_matrix.append([0]*COLS)

        # Genereer de matrix met 1/nde kans op water
        for i in range(ROWS-1):
            row = []
            for j in range(COLS):
                chance_rock = r.randint(0, WATER_CHANCE-1)

                if chance_rock != 0:
                    row.append(rock)
                else:
                    row.append(water)
            world_matrix.append(row)

        # Graaf een pad van midden boven tot beneden met kronkels
        digger_row = 0
        digger_col = (COLS+1)//2

        left = 0
        down = 1
        right = 2

        while digger_row != ROWS-1:
            if digger_col == 0:
                random_direction = r.randint(1, 2)
            elif digger_col == (COLS-1):
                random_direction = r.randint(0, 1)
            else:
                random_direction = r.randint(0, 2)

            if random_direction == left and 0 < digger_col:
                digger_col -= 1
                world_matrix[digger_row][digger_col] = water
            
            elif random_direction == down:
                digger_row += 1
                world_matrix[digger_row][digger_col] = water

            elif random_direction == right and digger_col < (COLS-1):
                digger_col += 1
                world_matrix[digger_row][digger_col] = water
        
        return world_matrix