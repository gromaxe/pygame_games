import pygame
import sys
# Генерация миникарты в текстовом файле
map_data = [
    "##############",
    "#            #",
    "#            #",
    "#    ####    #",
    "#     ##     #",
    "#            #",
    "##############",
]

with open("minimap.txt", "w") as file:
    for line in map_data:
        file.write(f"{line}\n")

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

with open("minimap.txt", "r") as file:
    minimap = file.readlines()
    minimap = [line.strip() for line in minimap]

player_x, player_y = 100, 100
speed = 5


def check_collision(x, y):
    map_x = x // 50
    map_y = y // 50
    if minimap[map_y][map_x] == "#":
        return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and not check_collision(player_x, player_y - speed):
        player_y -= speed
    if keys[pygame.K_s] and not check_collision(player_x, player_y + speed):
        player_y += speed
    if keys[pygame.K_a] and not check_collision(player_x - speed, player_y):
        player_x -= speed
    if keys[pygame.K_d] and not check_collision(player_x + speed, player_y):
        player_x += speed

    screen.fill((0, 0, 0))
    # Отрисовка миникарты
    for y, line in enumerate(minimap):
        for x, char in enumerate(line):
            if char == "#":
                pygame.draw.rect(screen, (255, 255, 255), (x * 50, y * 50, 50, 50))

    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))
    pygame.display.flip()
    clock.tick(60)
