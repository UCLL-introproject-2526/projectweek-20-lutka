from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player
from oxygen import Timer

def main():
    init()

    GAME_FONT1 = font.SysFont("New Times Roman", 70, font.Font.bold)
    GAME_FONT2 = font.SysFont("Arial", 30)
    clock = time.Clock()

    state = State()
    running = True
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

            if t.time_left > 0:
                t.handle_event(e)

        # update
        if t.time_left > 0:
            p.process_key_input(world_blocks)

        # draw
        m.draw(world_blocks)

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
                True, (250, 250, 250)
            )
            GAME_DISPLAY.blit(text_surface2, (225, 380))

        display.flip()
        clock.tick(60)

    quit()

main()