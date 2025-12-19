from constants import *
from pygame import *
from gamestate import State
from map import Map
from player import Player
from oxygen import Timer
from gifts import *
from arrow import *

def main():
    init()
    # Background muziek met volume (0.0 == geen geluid) (1.0 == volledige geluid)
    mixer.music.load("assets/Sounds/background_music.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    SPAWN_PACKAGE_EVENT = USEREVENT + 1
    time.set_timer(SPAWN_PACKAGE_EVENT, 2000)

    elf_image = image.load("assets/Images/elf.png")
    elf_image = transform.scale(elf_image, (64, 64))
    elf_picked_up = False
    has_won = False
    
    game_display = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    start_bg = image.load("assets/Images/startscherm.png").convert()
    start_bg = transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    GAME_FONT1 = font.SysFont("New Times Roman", 70, font.Font.bold)
    GAME_FONT2 = font.SysFont("Arial", 30)
    clock = time.Clock()

    state = State()
    running = True
    game_over = False
    t = Timer(25)
    game_started = False
    start_screen_timer = 0  # Timer voor startscherm
    win_screen_timer = 0  # Timer voor win scherm
    elf_just_picked_up = False  # Flag om te tracken of elf net is opgepakt

    # Player
    player_position = Vector2(START.x, START.y)
    p = Player(player_position)

    # Map generate before checking collisions
    m = Map(p)
    world_matrix = m.generate_world()
    world_blocks = m.get_world_rects(world_matrix)
    arrow = ArrowIndicator()
    
    # Spawn initial gifts
    spawn_multiple_gifts(world_matrix, amount=25)

    while running:
        dt = clock.tick(60) / 1000

        for e in event.get():
            if e.type == QUIT:
                running = False
            if not game_started and e.type == KEYDOWN and e.key == K_RETURN:
                game_started = True

            if t.time_left <= 0 and e.type == KEYDOWN and e.key == K_RETURN:
                game_over = False
                game_started = False
                state = State()

                # reset counter
                reset_package_counter()

                player_position = Vector2(START.x, START.y)
                p = Player(player_position)

                m = Map(p)
                world_matrix = m.generate_world()
                world_blocks = m.get_world_rects(world_matrix)

                # Spawn gifts again
                spawn_multiple_gifts(world_matrix, amount=5)

                elf_picked_up = False
                has_won = False

                t = Timer(25)
                
                # Reset start screen timer
                start_screen_timer = 0
                win_screen_timer = 0

                # Herstart timers
                time.set_timer(SPAWN_PACKAGE_EVENT, 5000)

                # Herstart background muziek
                mixer.music.stop()
                mixer.music.load("assets/Sounds/background_music.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(-1)

            # Only handle timer events if game is running
            if e.type == SPAWN_PACKAGE_EVENT:
                if t.time_left > 0 and not elf_picked_up:  # Stop spawning als elf is opgepakt
                    # Spawn 1 nieuw pakje elke 5 seconden
                    spawn_gift_in_matrix(world_matrix)
        
        # Update start screen timer BUITEN event loop - ALLEEN voor win scherm
        # Startscherm start NIET automatisch, alleen met ENTER
        
        # Update win screen timer - ALLEEN als je daadwerkelijk hebt gewonnen
        if has_won and game_started:
            win_screen_timer += dt
            if win_screen_timer >= 5.0:
                # Reset naar startscherm
                game_started = False
                has_won = False
                game_over = False
                state = State()
                reset_package_counter()
                
                player_position = Vector2(START.x, START.y)
                p = Player(player_position)
                
                m = Map(p)
                world_matrix = m.generate_world()
                world_blocks = m.get_world_rects(world_matrix)
                
                spawn_multiple_gifts(world_matrix, amount=25)
                
                elf_picked_up = False
                t = Timer(25)
                start_screen_timer = 0
                win_screen_timer = 0
                
                time.set_timer(SPAWN_PACKAGE_EVENT, 2000)
                
                mixer.music.stop()
                mixer.music.load("assets/Sounds/background_music.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(-1)
        
        # update
        if game_started and not has_won and t.time_left > 0:
            p.process_key_input(world_blocks)
            
            # Alleen auto-refill als de elf nog NIET is opgepakt
            if p.pos.y <= CELL_SIZE and t.time_left < t.max_time and not elf_picked_up:
                t.refill()
            
            # Update arrow timer - ALLEEN als elf nog niet is opgepakt
            if not elf_picked_up:
                arrow.update(dt)
            
            # collision check met pakjes - VOOR oxygen update
            update_game_with_gifts(world_matrix, p, t, state)
            
            # Update oxygen ALTIJD NA gift collision (ook als elf is opgepakt)
            t.update(dt)

        # draw - WIS HET SCHERM EERST!
        game_display.fill((0, 0, 0))
        if not game_started:
            game_display.blit(start_bg, (0, 0))

            text = GAME_FONT2.render("Druk ENTER om te starten", True, (255, 255, 255))
            game_display.blit(text, (SCREEN_WIDTH // 2 - 150, 500))

            display.flip()
            continue
        m.draw(world_blocks, world_matrix)

        # GEBRUIK CAMERA POSITIE!
        camera_pos = m.tracking_player()
        draw_all_gifts(world_matrix, camera_pos)

        elf_picked_up, has_won = p.elf_system(elf_picked_up, elf_image, m)

        # Activeer pijl EENMALIG zodra elf wordt opgepakt EN vul oxygen volledig aan
        if elf_picked_up and not has_won and not arrow.active:
            arrow.activate()
            t.time_left = t.max_time  # Vul oxygen volledig aan wanneer elf wordt opgepakt
            elf_just_picked_up = True

        if has_won:
            text_surface1 = GAME_FONT1.render("You saved the elf!", True, (0, 250, 0))
            GAME_DISPLAY.blit(text_surface1, (300, 300))
            arrow.deactivate()
        elif t.time_left > 0:
            p.draw()
            
            # Teken pijl als elf is opgepakt maar nog niet gewonnen
            if elf_picked_up:
                arrow.draw(GAME_DISPLAY, p.draw_pos.x, p.draw_pos.y)
            
            t.render(GAME_DISPLAY)
            pakjes_teller = GAME_FONT2.render(
                f"Pakjes: {state.score}",
                True, (0, 0, 0)
            )
            GAME_DISPLAY.blit(pakjes_teller, (10, 10))
        else:
            text_surface2 = GAME_FONT1.render(
                "Game Over", True, (250, 0, 0)
            )
            GAME_DISPLAY.blit(text_surface2, (355, 300))

            text_surface3 = GAME_FONT2.render(
                "No oxygen left! Press enter to start again.",
                True, (0, 0, 0)
            )
            GAME_DISPLAY.blit(text_surface3, (225, 380))
            
            text_surface4 = GAME_FONT2.render(
                f"Aantal pakjes verzameld: {state.score}",
                True, (0, 0, 0)
            )
            game_display.blit(text_surface4, (380, 430))

            arrow.deactivate()
            
            # Start gameover muziek
            if not game_over:
                mixer.music.stop()
                mixer.music.load("assets/Sounds/gameover.mp3")
                mixer.music.set_volume(1)
                mixer.music.play(0)
                game_over = True

        display.flip()


main()