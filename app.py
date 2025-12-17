from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player

def main():
    init()
    mixer.music.load("christmas-jazz-christmas-holiday-347485.mp3")
    mixer.music.play(-1)

    surface = create_main_surface()

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
            time.wait(60)

        state.update()

        clear_surface(surface)
        state.render(surface)

main()

