import pygame
import sys
import math
import random

def render_text(surface, text, font, color, position):
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = position
    surface.blit(text_render, text_rect)

def title_screen(screen):
    title_font = pygame.font.Font("Kotra-w17WP.ttf", 144)
    button_font = pygame.font.Font("EmotionalBaggage-ZVdXK.ttf", 72)
    title_text = title_font.render("Sailor's Odyssey", True, (164, 87, 41))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))

    play_button_text = button_font.render("Play", True, (255, 255, 255))
    play_button_rect = play_button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_button_text, play_button_rect)

        game_rules_font = pygame.font.Font(None, 42)
        rules_text = [
            "Rules",
            "",
            "1. The objective of the game is to survive for as long as possible by controlling a player character",
            "   and using various cannonballs to defeat incoming enemies.",
            "",
            "2. The player has the ability to move the character with the WASD keys, fire cannonballs with the left",
            "   mouse button, and launch heavy cannonballs with the right mouse button. Additionally, they can use",
            "   a grape shot attack by pressing the Q key. Enemies will spawn from various directions and must be",
            "   defeated to continue surviving.",
            "",
            "3. Have fun playing 'Sailor's Odyssey' and test your skills in this action-packed cannon shooting game!"
        ]
        text_position = (screen.get_width() // 2, int(screen.get_height() * 5 / 8))
        for line in rules_text:
            render_text(screen, line, game_rules_font, (255, 255, 255), text_position)
            text_position = (text_position[0], text_position[1] + 36)

        pygame.display.flip()

def initialize_game():
    pygame.init()
    pygame.mixer.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Cannon Game")

    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    PLAYER_SPEED = 5
    CANNONBALL_SPEED = 12
    HEAVY_CANNONBALL_SPEED = 9
    GRAPE_SHOT_RADIUS = 100
    GRAPE_SHOT_COOLDOWN = 2500
    CANNONBALL_COOLDOWN = 500
    HEAVY_CANNONBALL_COOLDOWN = 1500
    ENEMY_SPEED = 3

    font = pygame.font.Font(None, 36)
    timer_text = font.render("Time: 0", True, (255, 255, 255))
    timer_rect = timer_text.get_rect()
    timer_rect.centerx = screen.get_width() // 2
    timer_rect.top = 10

    player_image = pygame.image.load("player.png")
    player_image = pygame.transform.scale(player_image, (64, 64))
    player_angle = 0
    cannonball_image = pygame.image.load("cannonball.png")
    heavy_cannonball_image = pygame.image.load("heavy_cannonball.png")

    enemy_images = [
        pygame.image.load("enemy1.png"),
        pygame.image.load("enemy2.png"),
        pygame.image.load("enemy3.png")
    ]

    for i in range(len(enemy_images)):
        enemy_images[i] = pygame.transform.scale(enemy_images[i], (64, 64))

    player_x = screen.get_width() // 2 - 16
    player_y = screen.get_height() // 2 - 16

    cannonballs = []
    heavy_cannonballs = []
    heavy_cannonball_timers = []
    enemies = []
    grapeshot_cooldown = 0
    cannonball_cooldown = 0
    heavy_cannonball_cooldown = 0

    enemy_spawn_interval = 1000
    enemy_spawn_timer = 0

    game_over = False
    clock = pygame.time.Clock()
    running = True
    elapsed_time = 0
    start_time = pygame.time.get_ticks()
    try_again_button_rect = None

    def game_over_screen():
        nonlocal try_again_button_rect
        nonlocal elapsed_time

        game_over_font = pygame.font.Font(None, 72)
        timer_font = pygame.font.Font(None, 48)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if try_again_button_rect.collidepoint(event.pos):
                        return initialize_game()

            screen.fill((0, 0, 0))
            screen.blit(background_image, (0, 0))
            game_over_font = pygame.font.Font("Kotra-w17WP.ttf", 144)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            screen.blit(game_over_text, game_over_rect)
            final_time_font = pygame.font.Font("Kotra-w17WP.ttf", 72)
            final_time_text = final_time_font.render("Time Survived: " + str(elapsed_time) + " seconds", True, (164, 87, 41))
            final_time_rect = final_time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
            screen.blit(final_time_text, final_time_rect)
            try_again_button_font = pygame.font.Font("EmotionalBaggage-ZVdXK.ttf", 72)
            try_again_text = try_again_button_font.render("Try Again", True, (255, 255, 255))
            try_again_button_rect = try_again_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 150))
            screen.blit(try_again_text, try_again_button_rect)
            pygame.display.flip()

    while running:
        if game_over:
            game_over_screen()

        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_x, move_y = 0, 0
        clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            move_x += PLAYER_SPEED
        if keys[pygame.K_w]:
            move_y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            move_y += PLAYER_SPEED

        if move_x != 0 or move_y != 0:
            player_angle = math.degrees(math.atan2(move_y, move_x) + math.pi/2)

        player_x += move_x
        player_y += move_y

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and cannonball_cooldown <= 0:
            cannonball_x = player_x + 16
            cannonball_y = player_y + 16
            angle = math.atan2(mouse_y - cannonball_y, mouse_x - cannonball_x)
            cannonballs.append([cannonball_x, cannonball_y, angle])
            cannonball_cooldown = CANNONBALL_COOLDOWN

        if pygame.mouse.get_pressed()[2] and heavy_cannonball_cooldown <= 0:
            heavy_cannonball_x = player_x + 16
            heavy_cannonball_y = player_y + 16
            angle = math.atan2(mouse_y - heavy_cannonball_y, mouse_x - heavy_cannonball_x)
            heavy_cannonballs.append([heavy_cannonball_x, heavy_cannonball_y, angle])
            heavy_cannonball_timers.append(pygame.time.get_ticks())
            heavy_cannonball_cooldown = HEAVY_CANNONBALL_COOLDOWN

        if keys[pygame.K_q] and grapeshot_cooldown <= 0:
            for angle in range(0, 360, 45):
                radian_angle = math.radians(angle)
                cannonball_x = player_x + 16
                cannonball_y = player_y + 16
                angle = radian_angle
                cannonballs.append([cannonball_x, cannonball_y, angle])
            grapeshot_cooldown = GRAPE_SHOT_COOLDOWN

        if cannonball_cooldown > 0:
            cannonball_cooldown -= 16
        if heavy_cannonball_cooldown > 0:
            heavy_cannonball_cooldown -= 16
        if grapeshot_cooldown > 0:
            grapeshot_cooldown -= 16

        player_x = max(0, min(player_x, screen.get_width() - 64))
        player_y = max(0, min(player_y, screen.get_height() - 64))

        current_time = pygame.time.get_ticks()

        if current_time - enemy_spawn_timer >= enemy_spawn_interval:
            spawn_side = random.choice(["top", "bottom", "left", "right"])
            if spawn_side == "top":
                enemy_x = random.randint(0, screen.get_width() - 64)
                enemy_y = -64
            elif spawn_side == "bottom":
                enemy_x = random.randint(0, screen.get_width() - 64)
                enemy_y = screen.get_height()
            elif spawn_side == "left":
                enemy_x = -64
                enemy_y = random.randint(0, screen.get_height() - 64)
            elif spawn_side == "right":
                enemy_x = screen.get_width()
                enemy_y = random.randint(0, screen.get_height() - 64)

            enemy_image = random.choice(enemy_images)
            angle = math.atan2(player_y - enemy_y, player_x - enemy_x)
            if spawn_side == "top" or spawn_side == "left":
                enemy_image = pygame.transform.rotate(enemy_image, -math.degrees(angle))
            else:
                enemy_image = pygame.transform.rotate(enemy_image, math.degrees(angle))
                enemy_image = pygame.transform.flip(enemy_image, True, False)
                enemy_image = pygame.transform.flip(enemy_image, False, True)
                enemy_image = pygame.transform.flip(enemy_image, True, False)
            enemy_speed = random.uniform(2, 4)

            enemies.append([enemy_x, enemy_y, angle, enemy_speed, enemy_image])

            enemy_spawn_interval = max(100, 1000 - 1.05 ** (elapsed_time * (5/3)))
            enemy_spawn_timer = current_time

        if not game_over:
            for cannon in cannonballs[:]:
                angle = cannon[2]
                cannon[0] += CANNONBALL_SPEED * math.cos(angle)
                cannon[1] += CANNONBALL_SPEED * math.sin(angle)
                screen.blit(cannonball_image, (cannon[0], cannon[1]))
                if (
                    cannon[0] < 0
                    or cannon[0] > screen.get_width()
                    or cannon[1] < 0
                    or cannon[1] > screen.get_height()
                ):
                    cannonballs.remove(cannon)

            for i, heavy_cannon in enumerate(heavy_cannonballs):
                angle = heavy_cannon[2]
                heavy_cannon_x = heavy_cannon[0]
                heavy_cannon_y = heavy_cannon[1]
                heavy_cannon_radius = 80

                heavy_cannon[0] += HEAVY_CANNONBALL_SPEED * math.cos(angle)
                heavy_cannon[1] += HEAVY_CANNONBALL_SPEED * math.sin(angle)
                screen.blit(heavy_cannonball_image, (heavy_cannon[0], heavy_cannon[1]))

                for enemy in enemies[:]:
                    enemy_x = enemy[0]
                    enemy_y = enemy[1]
                    enemy_radius = 48

                    distance = math.hypot(heavy_cannon_x - enemy_x, heavy_cannon_y - enemy_y)

                    if distance < heavy_cannon_radius + enemy_radius:
                        enemies.remove(enemy)

            for enemy in enemies[:]:
                angle = enemy[2]
                enemy[0] += enemy[3] * math.cos(angle)
                enemy[1] += enemy[3] * math.sin(angle)
                screen.blit(enemy[4], (enemy[0], enemy[1]))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = font.render("Time: " + str(elapsed_time), True, (255, 255, 255))
        screen.blit(timer_text, timer_rect)

        rotated_player_image = pygame.transform.rotate(player_image, -player_angle)
        player_rect = rotated_player_image.get_rect(center=(player_x + 32, player_y + 32))
        screen.blit(rotated_player_image, player_rect.topleft)

        pygame.display.flip()

        if not game_over:
            for cannon in cannonballs[:]:
                for enemy in enemies[:]:
                    if math.hypot(cannon[0] - enemy[0], cannon[1] - enemy[1]) < 48:
                        cannonballs.remove(cannon)
                        enemies.remove(enemy)

            for enemy in enemies[:]:
                player_rect = pygame.Rect(player_x, player_y, 48, 48)
                enemy_rect = pygame.Rect(enemy[0], enemy[1], 48, 48)
                if player_rect.colliderect(enemy_rect):
                    game_over = True
                    pygame.mixer.music.stop()
                    break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Cannon Game")

    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    title_screen(screen)

    initialize_game()
