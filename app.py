from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player
from oxygen import Timer

def main():
    init()

    # mixer.music.load("christmas-jazz-christmas-holiday-347485.mp3")
    # mixer.music.play(-1)

    GAME_FONT1 = font.SysFont("New Times Roman", 70, font.Font.bold)
    GAME_FONT2 = font.SysFont("Arial", 30)
    clock = time.Clock()

    state = State()
    running = True
    t = Timer(60)
    
    # Create player with map size for boundary checking
    player_position = Vector2(START.x,START.y)
    p = Player(player_position)
    m = Map(p)
    world_matrix = m.generate_world()
    
    while running:
        dt = clock.tick(60) * .001 * TARGET_FPS
        # Events
        for e in event.get():
            if e.type == QUIT:
                running = False

            if t.time_left == 0 and e.type == KEYDOWN and e.key == K_RETURN:
                time.set_timer(t.TIMER_EVENT, 0)
                state = State()
                p = Player(START)
                m = Map(p)
                world_matrix = m.generate_world()
                t = Timer(10)

            # Only handle timer events if game is running
            if t.time_left > 0:
                t.handle_event(e)

        #blocks
        blocks = m.get_world_rects(world_matrix)

        # Process input only if game is not over
        if t.time_left > 0:
            p.process_key_input(dt, blocks)

        # Draw everything
        m.draw(blocks)
        
        if t.time_left > 0:
            p.draw()
            state.render()
            t.render(GAME_DISPLAY)
        else:
            # Draw game over screen
            text_surface1 = GAME_FONT1.render(
                "Game Over",
                True, (250, 0, 0)
            )
            GAME_DISPLAY.blit(text_surface1, (355, 300))
            text_surface2 = GAME_FONT2.render(
                "Geen zuurstof! Druk ENTER om opnieuw te beginnen.",
                True, (250, 250, 250)
            )
            GAME_DISPLAY.blit(text_surface2, (225, 380))
        
        display.flip()  


main()