from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player

def main():
    init()
    game_display = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = time.Clock()

    state = State()
    
    # Create player with map size for boundary checking
    player_position = Vector2(START.x,START.y)
    p = Player(player_position)
    m = Map(p)
    world_matrix = m.generate_world()
    
    running = True
    while running:
        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        # Process input
        p.process_key_input(m.map_size)
        
        # Draw everything
        m.draw(game_display, world_matrix)
        p.draw(game_display, m.map_size)
        state.render(game_display)
        
        display.flip()  
        clock.tick(60)  


main()