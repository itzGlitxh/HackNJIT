import pygame
import sys
import math

pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Cannon Game")

PLAYER_SPEED = 5
CANNONBALL_SPEED = 8
HEAVY_CANNONBALL_SPEED = 5
GRAPE_SHOT_RADIUS = 100
GRAPE_SHOT_COOLDOWN = 5000
CANNONBALL_COOLDOWN = 1000
HEAVY_CANNONBALL_COOLDOWN = 3000

font = pygame.font.Font(None, 36)
timer_text = font.render("Time: 0", True, (255, 255, 255))
timer_rect = timer_text.get_rect()
timer_rect.centerx = screen.get_width() // 2
timer_rect.top = 10

GREY = (128, 128, 128)

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (64, 64))
player_angle = 0
cannonball_image = pygame.image.load("cannonball.png")
heavy_cannonball_image = pygame.image.load("heavy_cannonball.png")

player_x = screen.get_width() // 2 - 16
player_y = screen.get_height() // 2 - 16

cannonballs = []
heavy_cannonballs = []
grapeshot_cooldown = 0
cannonball_cooldown = 0
heavy_cannonball_cooldown = 0
grapeshot_image = pygame.image.load("grapeshot.png")
grapeshot_image = pygame.transform.scale(grapeshot_image, (32, 32))

cooldown_images = {
    "cannonball": (cannonball_image, CANNONBALL_COOLDOWN),
    "heavy_cannonball": (heavy_cannonball_image, HEAVY_CANNONBALL_COOLDOWN),
    "grapeshot": (grapeshot_image, GRAPE_SHOT_COOLDOWN),
}

cooldown_timers = {key: 0 for key in cooldown_images}

def draw_cooldown_images():
    x = screen.get_width() - 200
    y = screen.get_height() - 100
    for key, (image, cooldown) in cooldown_images.items():
        screen.blit(image, (x, y))
        cooldown_text = font.render(f"{key.capitalize()} Cooldown: {cooldown_timers[key] // 1000}", True, (255, 255, 255))
        screen.blit(cooldown_text, (x, y + 32))
        x -= 100

clock = pygame.time.Clock()
running = True
timer = 0

while running:
    screen.fill(GREY)

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

    for key in cooldown_timers:
        if cooldown_timers[key] > 0:
            cooldown_timers[key] -= 16

    player_x = max(0, min(player_x, screen.get_width() - 64))
    player_y = max(0, min(player_y, screen.get_height() - 64))

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

    for heavy_cannon in heavy_cannonballs:
        angle = heavy_cannon[2]
        heavy_cannon[0] += HEAVY_CANNONBALL_SPEED * math.cos(angle)
        heavy_cannon[1] += HEAVY_CANNONBALL_SPEED * math.sin(angle)
        screen.blit(heavy_cannonball_image, (heavy_cannon[0], heavy_cannon[1]))

    timer += 1
    timer_text = font.render("Time: " + str(timer // 60), True, (255, 255, 255))
    screen.blit(timer_text, timer_rect)

    draw_cooldown_images()

    rotated_player_image = pygame.transform.rotate(player_image, -player_angle)
    player_rect = rotated_player_image.get_rect(center=(player_x + 32, player_y + 32))
    screen.blit(rotated_player_image, player_rect.topleft)

    draw_cooldown_images()

    pygame.display.flip()

pygame.quit()
sys.exit()
