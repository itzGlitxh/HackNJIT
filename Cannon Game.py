import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
CANNONBALL_SPEED = 8
HEAVY_CANNONBALL_SPEED = 5
GRAPE_SHOT_RADIUS = 100
GRAPE_SHOT_DELAY = 300

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cannon Game")

player_image = pygame.image.load("player.png")
cannonball_image = pygame.image.load("cannonball.png")
heavy_cannonball_image = pygame.image.load("heavy_cannonball.png")

player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed_x = 0
player_speed_y = 0

primary_cooldown = 0
heavy_cooldown = 0
grapeshot_cooldown = 0

cannonballs = []

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    if pygame.mouse.get_pressed()[0] and primary_cooldown <= 0:
        primary_cooldown = 1000

    if pygame.mouse.get_pressed()[2] and heavy_cooldown <= 0:
        heavy_cooldown = 3000

    if pygame.key.get_pressed()[pygame.K_e] and grapeshot_cooldown <= 0:
        grapeshot_cooldown = GRAPE_SHOT_DELAY

    if primary_cooldown > 0:
        primary_cooldown -= 16
    if heavy_cooldown > 0:
        heavy_cooldown -= 16
    if grapeshot_cooldown > 0:
        grapeshot_cooldown -= 16

    player_x = max(0, min(player_x, WIDTH))
    player_y = max(0, min(player_y, HEIGHT))

    new_cannonballs = []
    for cb in cannonballs:
        if not collision_with_enemy(cb):
            new_cannonballs.append(cb)
    cannonballs = new_cannonballs

    screen.blit(player_image, (player_x, player_y))

    for cb in cannonballs:
        screen.blit(cannonball_image, (cb[0], cb[1]))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
