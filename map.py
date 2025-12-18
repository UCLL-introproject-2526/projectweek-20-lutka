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
        return Vector2(x,y)

# zorgt dat de camera de sub volgt
    def draw(self, blocks_list):
        position = Map.tracking_player(self)
        GAME_DISPLAY.blit(self.background_image, (-position.x, -position.y))
        
        Map.draw_world(self, blocks_list)


    def get_world_rects(self, matrix):
        position = Map.tracking_player(self)
        current_cell_origin = Vector2(0,0)
        rect_list = []

        for i in range(ROWS):    
            for j in range(COLS):
                if matrix[i][j] == 1:
                    rock = Rect(current_cell_origin.x-position.x, current_cell_origin.y-position.y, CELL_SIZE, CELL_SIZE)
                    rect_list.append(rock)
                current_cell_origin.x += CELL_SIZE
            current_cell_origin.x = 0
            current_cell_origin.y += CELL_SIZE

        return rect_list        


    def draw_world(self, blocks_list):
    
        for rock in blocks_list:    
            draw.rect(GAME_DISPLAY, GREY, rock)


    def generate_world(self):
        water = 0
        rock = 1
        gift = 7

        #een 0 is water, een 1 is rots, een 7 is pakje
        world_matrix = []

        world_matrix.append([0]*COLS)

        #genereer de matrix met 1/nde kans op water (zodat er al simpele natuurlijke grot structuren kunnen ontstaan)
        for i in range(ROWS-1):
            row = []
            for j in range(COLS):
                chance_rock = r.randint(0,WATER_CHANCE-1)

                #als niet nul dan is er een rotsblok, bij nul is er water
                if chance_rock != 0:
                    row.append(rock)
                else:
                    row.append(water)
            world_matrix.append(row)

        #we graven in de matrix een pad van midden boven tot beneden met kronkels
        digger_row = 0
        digger_col = (COLS+1)//2

        #0 is links, 1 is beneden, 2 is rechts
        left = 0
        down = 1
        right = 2

        while digger_row != ROWS-1:

            #ga niet verder naar links als helemaal links en analoog voor rechts
            if digger_col == 0:
                random_direction = r.randint(1,2)
            elif digger_col == (COLS-1):
                random_direction = r.randint(0,1)
            else:
                random_direction = r.randint(0,2)

            #graaf in de juiste richting
            if random_direction == left and 0 < digger_col:
                digger_col -=1
                world_matrix[digger_row][digger_col] = water
            
            elif random_direction == down:
                digger_row +=1
                world_matrix[digger_row][digger_col] = water

            elif random_direction == right and digger_col < (COLS-1):
                digger_col +=1
                world_matrix[digger_row][digger_col] = water
        
        return world_matrix