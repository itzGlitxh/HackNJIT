import pygame
import sys
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cannon Game")

PLAYER_SPEED = 5
CANNONBALL_SPEED = 8
HEAVY_CANNONBALL_SPEED = 5
GRAPE_SHOT_RADIUS = 100
GRAPE_SHOT_DELAY = 300
CANNONBALL_COOLDOWN = 1000
HEAVY_CANNONBALL_COOLDOWN = 3000
GRAPE_SHOT_COOLDOWN = 5000

font = pygame.font.Font(None, 36)
timer_text = font.render("Time: 0", True, (255, 255, 255))
timer_rect = timer_text.get_rect()
timer_rect.centerx = 800 // 2
timer_rect.top = 10

GREY = (128, 128, 128)

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (64, 64))
cannonball_image = pygame.image.load("cannonball.png")
heavy_cannonball_image = pygame.image.load("heavy_cannonball.png")

player_x = 400
player_y = 300

cannonballs = []
heavy_cannonballs = []
grapeshot_cooldown = 0
cannonball_cooldown = 0
heavy_cannonball_cooldown = 0

clock = pygame.time.Clock()
running = True
timer = 0

while running:
    screen.fill(GREY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_w]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player_y += PLAYER_SPEED

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] and cannonball_cooldown <= 0:
        cannonball_x = player_x + 32
        cannonball_y = player_y + 32
        angle = math.atan2(mouse_y - cannonball_y, mouse_x - cannonball_x)
        cannonballs.append([cannonball_x, cannonball_y, angle])
        cannonball_cooldown = CANNONBALL_COOLDOWN

    if pygame.mouse.get_pressed()[2] and heavy_cannonball_cooldown <= 0:
        heavy_cannonball_x = player_x + 32
        heavy_cannonball_y = player_y + 32
        angle = math.atan2(mouse_y - heavy_cannonball_y, mouse_x - heavy_cannonball_x)
        heavy_cannonballs.append([heavy_cannonball_x, heavy_cannonball_y, angle])
        heavy_cannonball_cooldown = HEAVY_CANNONBALL_COOLDOWN

    if keys[pygame.K_q] and grapeshot_cooldown <= 0:
        for angle in range(0, 360, 45):
            radian_angle = math.radians(angle)
            cannonball_x = player_x + 32
            cannonball_y = player_y + 32
            angle = radian_angle
            cannonballs.append([cannonball_x, cannonball_y, angle])
        grapeshot_cooldown = GRAPE_SHOT_COOLDOWN

    if cannonball_cooldown > 0:
        cannonball_cooldown -= 16

    if heavy_cannonball_cooldown > 0:
        heavy_cannonball_cooldown -= 16

    if grapeshot_cooldown > 0:
        grapeshot_cooldown -= 16

    player_x = max(0, min(player_x, 800 - 64))
    player_y = max(0, min(player_y, 600 - 64))

    screen.blit(player_image, (player_x, player_y))

    for cannon in cannonballs:
        angle = cannon[2]
        cannon[0] += CANNONBALL_SPEED * math.cos(angle)
        cannon[1] += CANNONBALL_SPEED * math.sin(angle)
        screen.blit(cannonball_image, (cannon[0], cannon[1]))
        if (
            cannon[0] < 0
            or cannon[0] > 800
            or cannon[1] < 0
            or cannon[1] > 600
        ):
            cannonballs.remove(cannon)

    for heavy_cannon in heavy_cannonballs:
        angle = heavy_cannon[2]
        heavy_cannon[0] += HEAVY_CANNONBALL_SPEED * math.cos(angle)
        heavy_cannon[1] += HEAVY_CANNONBALL_SPEED * math.sin(angle)
        screen.blit(heavy_cannonball_image, (heavy_cannon[0], heavy_cannon[1]))
        if (
            heavy_cannon[0] < 0
            or heavy_cannon[0] > 800
            or heavy_cannon[1] < 0
            or heavy_cannon[1] > 600
        ):
            heavy_cannonballs.remove(heavy_cannon)

    timer += 1
    timer_text = font.render("Time: " + str(timer // 60), True, (255, 255, 255))
    screen.blit(timer_text, timer_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
