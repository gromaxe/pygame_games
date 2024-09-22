import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 1 - стена, 0 - пол
world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

TILE_SIZE = 100
FOV = math.pi / 2  # поле зрения

class Object:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)

    def move(self, dx, dy):
        """Двигаемся на dx dy."""
        self.x += dx
        self.y += dy
        self.update_rect()

    def update_rect(self):
        """Для обсчёта столкновений."""
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

class Player(Object):
    def __init__(self, x, y, size, speed):
        super().__init__(x, y, size)
        self.speed = speed
        self.angle = 0

    def rotate(self, da):
        """Поворот."""
        self.angle += da

class Target(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.alive = True

    def hit(self):
        """Убиваем цель."""
        self.alive = False

# цели
targets = [
    Target(400, 200, 30),
    Target(600, 400, 30),
    Target(300, 500, 30),
]

def get_wall_rects():
    wall_rects = []
    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            if tile == 1:  # стена
                wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return wall_rects

# Рейкастинг
def cast_rays(player):
    num_rays = 60
    ray_angle_step = FOV / num_rays
    ray_angle = player.angle - FOV / 2

    for ray in range(num_rays):
        for depth in range(1, 800):
            target_x = player.x + depth * math.cos(ray_angle)
            target_y = player.y + depth * math.sin(ray_angle)

            map_x = int(target_x / TILE_SIZE)
            map_y = int(target_y / TILE_SIZE)

            if world_map[map_y][map_x] == 1:
                # попали в стену - считаем расстояние и её высоту
                distance = depth
                wall_height = SCREEN_HEIGHT / (distance * 0.01)

                # считаем яркость
                brightness = max(50, 255 - int(distance * 0.1))

                # рисуем
                color = (brightness, brightness, brightness)
                pygame.draw.rect(screen, color,
                                 (ray * (SCREEN_WIDTH // num_rays), SCREEN_HEIGHT // 2 - wall_height // 2,
                                  SCREEN_WIDTH // num_rays, wall_height))
                break

        ray_angle += ray_angle_step

def draw_minimap():
    minimap_width = 200
    map_width = len(world_map[0])  # ширина карты
    map_height = len(world_map)    # высота

    minimap_height = int(minimap_width * (map_height / map_width))

    minimap_scale_x = minimap_width / map_width
    minimap_scale_y = minimap_height / map_height

    minimap = pygame.Surface((minimap_width, minimap_height))
    minimap.fill((50, 50, 50))

    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            color = (200, 200, 200) if tile == 1 else (0, 0, 0)
            pygame.draw.rect(minimap, color, (x * minimap_scale_x, y * minimap_scale_y, minimap_scale_x, minimap_scale_y))

    player_minimap_x = int(player.x / TILE_SIZE * minimap_scale_x)
    player_minimap_y = int(player.y / TILE_SIZE * minimap_scale_y)
    pygame.draw.circle(minimap, (255, 0, 0), (player_minimap_x, player_minimap_y), 5)

    for target in targets:
        if target.alive:
            target_minimap_x = int(target.x / TILE_SIZE * minimap_scale_x)
            target_minimap_y = int(target.y / TILE_SIZE * minimap_scale_y)
            pygame.draw.circle(minimap, (0, 255, 0), (target_minimap_x, target_minimap_y), 5)

    screen.blit(minimap, (0, 0))

# проверка столкновения
def is_colliding(player, walls):
    for wall in walls:
        if player.rect.colliderect(wall):
            return True
    return False

def check_target_hit(player):
    ray_angle = player.angle
    for depth in range(1, 800):
        target_x = player.x + depth * math.cos(ray_angle)
        target_y = player.y + depth * math.sin(ray_angle)
        for target in targets:
            if target.alive and target.rect.collidepoint(target_x, target_y):
                target.hit()
                return target
    return None

def draw_targets_on_view(player):
    for target in targets:
        if not target.alive:
            continue
        dx = target.x - player.x
        dy = target.y - player.y
        distance = math.sqrt(dx**2 + dy**2)
        angle_to_target = math.atan2(dy, dx) - player.angle

        if -FOV / 2 < angle_to_target < FOV / 2:
            target_size_on_screen = min(5000 / (distance + 0.1), SCREEN_HEIGHT)
            screen_x = (angle_to_target + FOV / 2) * (SCREEN_WIDTH / FOV)

            pygame.draw.rect(screen, (0, 255, 0), (screen_x - target_size_on_screen // 2,
                                                   SCREEN_HEIGHT // 2 - target_size_on_screen // 2,
                                                   target_size_on_screen,
                                                   target_size_on_screen))

def draw_shooting_crosshair(fade_time):
    crosshair_size = 10
    color = (255, 0, 0, fade_time)  # Add alpha for fade effect
    pygame.draw.rect(screen, color, (SCREEN_WIDTH // 2 - crosshair_size // 2,
                                     SCREEN_HEIGHT // 2 - crosshair_size // 2,
                                     crosshair_size, crosshair_size))

player = Player(150, 150, 20, 5)
shooting = False
fade_time = 0

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Сохраняем положение игрока
    old_player_x, old_player_y = player.x, player.y

    # Проверяем нажатия клавиш
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.rotate(-0.05)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.rotate(0.05)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.move(player.speed * math.cos(player.angle), player.speed * math.sin(player.angle))
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.move(-player.speed * math.cos(player.angle), -player.speed * math.sin(player.angle))

    if keys[pygame.K_SPACE]:
        hit_target = check_target_hit(player)
        if hit_target:
            print("Target hit!")
        shooting = True
        fade_time = 255

    wall_rects = get_wall_rects()

    # Проверяем на столкновение
    if is_colliding(player, wall_rects):
        # При столкновении, не двигаемся
        player.x, player.y = old_player_x, old_player_y
        player.update_rect()

    screen.fill((0, 0, 0))
    cast_rays(player)
    draw_targets_on_view(player)  # отрисоввка целей
    draw_minimap()

    if shooting:
        draw_shooting_crosshair(fade_time)
        fade_time -= 10
        if fade_time <= 0:
            shooting = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
