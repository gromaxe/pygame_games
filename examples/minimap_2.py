import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Параметры игрока
player_pos = [400, 300]
player_speed = 5

# Загрузка данных карты
map_data = """
####################
#                  #
#    ######        #
#                  #
#        #######   #
#                  #
####################
""".strip().split('\n')

# Размеры тайла и карты
tile_size = 50
map_width = len(map_data[0]) * tile_size
map_height = len(map_data) * tile_size

# Конвертация данных карты в список препятствий
obstacles = []
for y, row in enumerate(map_data):
    for x, char in enumerate(row):
        if char == '#':
            obstacles.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))


def draw_map():
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 255, 255), obstacle)


def draw_minimap():
    minimap_scale = 0.2
    minimap_surface = pygame.Surface((map_width * minimap_scale, map_height * minimap_scale))
    minimap_surface.fill((0, 0, 0))
    for obstacle in obstacles:
        minimap_rect = pygame.Rect(obstacle.x * minimap_scale, obstacle.y * minimap_scale, obstacle.width * minimap_scale, obstacle.height * minimap_scale)
        pygame.draw.rect(minimap_surface, (255, 255, 255), minimap_rect)
    screen.blit(minimap_surface, (0, 0))


def move_map(dx, dy):
    for obstacle in obstacles:
        obstacle.x -= dx
        obstacle.y -= dy


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w]:
        dy = player_speed
    if keys[pygame.K_s]:
        dy = -player_speed
    if keys[pygame.K_a]:
        dx = player_speed
    if keys[pygame.K_d]:
        dx = -player_speed

    move_map(dx, dy)

    screen.fill((0, 0, 0))
    draw_map()
    draw_minimap()
    pygame.display.flip()
    clock.tick(60)
