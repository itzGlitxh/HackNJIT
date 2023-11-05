import pygame
import sys
import math
import random

pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Cannon Game")

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

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
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (64, 64))

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
timer = 0

while running:
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

        angle = math.atan2(player_y - enemy_y, player_x - enemy_x)

        enemy_speed = random.uniform(2, 4)

        enemies.append([enemy_x, enemy_y, angle, enemy_speed])

        enemy_spawn_interval = max(100, 1000 - 1.0005**(timer*(5/3)))

        enemy_spawn_timer = current_time

    if not game_over:
        for cannon in cannonballs:
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

            for enemy in enemies:
                enemy_x = enemy[0]
                enemy_y = enemy[1]
                enemy_radius = 32

                distance = math.hypot(heavy_cannon_x - enemy_x, heavy_cannon_y - enemy_y)

                if distance < heavy_cannon_radius + enemy_radius:
                    enemies.remove(enemy)

        for enemy in enemies:
            angle = enemy[2]
            enemy[0] += enemy[3] * math.cos(angle)
            enemy[1] += enemy[3] * math.sin(angle)
            screen.blit(enemy_image, (enemy[0], enemy[1]))

    timer += 1
    timer_text = font.render("Time: " + str(timer // 60), True, (255, 255, 255))
    screen.blit(timer_text, timer_rect)

    rotated_player_image = pygame.transform.rotate(player_image, -player_angle)
    player_rect = rotated_player_image.get_rect(center=(player_x + 32, player_y + 32))
    screen.blit(rotated_player_image, player_rect.topleft)

    pygame.display.flip()

    if not game_over:
        for cannon in cannonballs:
            for enemy in enemies:
                if math.hypot(cannon[0] - enemy[0], cannon[1] - enemy[1]) < 32:
                    cannonballs.remove(cannon)
                    enemies.remove(enemy)

        for enemy in enemies:
            if math.hypot(player_x + 32 - enemy[0], player_y + 32 - enemy[1]) < 32:
                game_over = True
                break

while running:
    if game_over:
        screen.blit(background_image, (0, 0))
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        final_time_text = font.render("Time Survived: " + str(timer // 60) + " seconds", True, (255, 0, 0))
        final_time_rect = final_time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        screen.blit(final_time_text, final_time_rect)
        pygame.display.flip()
        pygame.quit()
        sys.exit()
