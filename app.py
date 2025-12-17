from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player

def main():
    init()

    # mixer.music.load("christmas-jazz-christmas-holiday-347485.mp3")
    # mixer.music.play(-1)

    game_display = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #maak hier ooit een constante van...
    clock = time.Clock()

    state = State()
    
    # Create player with map size for boundary checking
    player_position = Vector2(START.x,START.y)
    p = Player(player_position)
    m = Map(p, game_display)
    world_matrix = m.generate_world()
    
    running = True
    while running:
        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        # Process input
        p.process_key_input(m.map_size)

        #blocks
        blocks = m.get_world_rects(world_matrix)
        
        # Draw everything
        m.draw(game_display, blocks)
        p.draw(game_display, m.map_size)
        state.render(game_display)
        
        display.flip()  
        clock.tick(60)  


main()