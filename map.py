import random as r
from constants import *
from pygame import *

class Map():
    def __init__(self, player, game_display):
        bg_image = image.load("assets/Images/achtergrond gradient.png").convert()
        self.background_image = transform.scale(bg_image, (CELL_SIZE*COLS, CELL_SIZE*ROWS))
        self.map_size = self.background_image.get_size()
        self.player = player
        self.water = 0
        self.rock = 1
        self.gift = 7

        self.window_size = game_display.get_size()

    def tracking_player(self):
        x = max(0, min(self.map_size[0] - self.window_size[0], self.player.pos.x - self.window_size[0] // 2))
        y = max(0, min(self.map_size[1] - self.window_size[1], self.player.pos.y - self.window_size[1] // 2))
        return Vector2(x,y)

# zorgt dat de camera de sub volgt
    def draw(self, game_display, blocks_list):
        position = Map.tracking_player(self)
        game_display.blit(self.background_image, (-position.x, -position.y))
        
        Map.draw_world(self, game_display, blocks_list)

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


    def draw_world(self, game_display, blocks_list):
    
        for rock in blocks_list:    
            draw.rect(game_display, GREY, rock)


    def generate_world(self):
        #een 0 is water, een 1 is rots, een 7 is pakje
        world_matrix = []

        #genereer de matrix met 1/nde kans op water (zodat er al simpele natuurlijke grot structuren kunnen ontstaan)
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                chance_rock = r.randint(0,WATER_CHANCE-1)

                #als niet nul dan is er een rotsblok, bij nul is er water
                if chance_rock != 0:
                    row.append(self.rock)
                else:
                    row.append(self.water)
            world_matrix.append(row)

        #we graven in de matrix een pad van midden boven tot beneden met kronkels
        digger_row = 0
        digger_col = (COLS+1)//2

        #startpunt is water
        world_matrix[digger_row][digger_col] = self.water

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
                world_matrix[digger_row][digger_col] = self.water
            
            elif random_direction == down:
                digger_row +=1
                world_matrix[digger_row][digger_col] = self.water

            elif random_direction == right and digger_col < (COLS-1):
                digger_col +=1
                world_matrix[digger_row][digger_col] = self.water
        
        return world_matrix