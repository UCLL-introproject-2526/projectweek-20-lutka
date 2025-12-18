from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player
from oxygen import Timer
from gifts import *

def main():
    init()
    
    # Background muziek met volume (0.0 == geen geluid) (1.0 == volledige geluid)
    mixer.music.load("assets/Sounds/background_music.mp3")
    mixer.music.set_volume(0.5) 
    mixer.music.play(-1)

    SPAWN_PACKAGE_EVENT = USEREVENT + 1
    time.set_timer(SPAWN_PACKAGE_EVENT, 5000)
    
    game_display = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    GAME_FONT1 = font.SysFont("New Times Roman", 70, font.Font.bold)
    GAME_FONT2 = font.SysFont("Arial", 30)
    clock = time.Clock()
    
    state = State()
    running = True
    game_over = False
    t = Timer(25)

    # Player
    player_position = Vector2(START.x, START.y)
    p = Player(player_position)
    
    # Map generate before chaecking collisions
    m = Map(p)
    world_matrix = m.generate_world()
    world_blocks = m.get_world_rects(world_matrix)
    
    # check collisions with the blocks that exist
    while any(p.get_world_hitbox().colliderect(b) for b in world_blocks):
        p.pos.y -= 1

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False

            if t.time_left == 0 and e.type == KEYDOWN and e.key == K_RETURN:
                game_over = False
                time.set_timer(t.TIMER_EVENT, 0)
                state = State()

                player_position = Vector2(START.x, START.y)
                p = Player(player_position)

                m = Map(p)
                world_matrix = m.generate_world()
                world_blocks = m.get_world_rects(world_matrix)
                
                # Check collisions after regenerating blocks
                while any(p.get_world_hitbox().colliderect(b) for b in world_blocks):
                    p.pos.y -= 1

                t = Timer(25)

                # Herstart timers
                time.set_timer(SPAWN_PACKAGE_EVENT, 5000)
                time.set_timer(t.TIMER_EVENT, 1000)
                
                # Herstart background muziek
                mixer.music.stop()
                mixer.music.load("assets/Sounds/background_music.mp3")
                mixer.music.set_volume(0.5) 
                mixer.music.play(-1)
            
            # Only handle timer events if game is running
            if e.type == SPAWN_PACKAGE_EVENT:
                if t.time_left > 0:
                    t.handle_event(e)
                    spawn_multiple_gifts(world_matrix)

        # update
        if t.time_left > 0:
            p.process_key_input(world_blocks)

        # draw
        m.draw(world_blocks)
        
        draw_all_gifts(game_display, world_matrix, p.pos)

        if t.time_left > 0:
            p.draw()
            state.render()
            t.render(GAME_DISPLAY)
        else:
            text_surface1 = GAME_FONT1.render(
                "Game Over", True, (250, 0, 0)
            )
            GAME_DISPLAY.blit(text_surface1, (355, 300))

            text_surface2 = GAME_FONT2.render(
                "Geen zuurstof! Druk ENTER om opnieuw te beginnen.",
                True, (0, 0, 0)
            )
            GAME_DISPLAY.blit(text_surface2, (225, 380))
            gift_count = count_gifts_on_map(world_matrix)
            text_surface3 = GAME_FONT2.render(
                f"Aantal pakjes verzameld: {state.score}",
                True, (0, 0, 0)
            )
            game_display.blit(text_surface3, (380, 430))
            
            # Start gameover muziek
            if not game_over:
                mixer.music.stop()
                mixer.music.load('assets/Sounds/gameover.mp3')
                mixer.music.set_volume(1)
                mixer.music.play(0)
                game_over = True
        
        display.flip()  
        clock.tick(60)  

    # quit()

main()