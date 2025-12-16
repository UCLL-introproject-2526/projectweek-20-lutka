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

    # Create map
    bg_image = image.load('hi.png')
    map_size = bg_image.get_size()
    
    # Create player with map size for boundary checking
    p = Player(50, 50, map_size)
    m = Map(p)
    
    running = True
    while running:
        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

        # Process input
        p.process_key_input()
        
        # Draw everything
        m.draw(game_display)
        p.draw(game_display, m.Image.get_size())
        state.render(game_display)
        
        display.flip()  
        clock.tick(60)  

main()