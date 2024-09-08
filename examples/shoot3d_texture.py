import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

texture = pygame.image.load('menu_bg.png')
texture = pygame.transform.scale(texture, (64, 64))

world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

def auto_pad_map(world_map):
    max_length = max(len(row) for row in world_map)
    padded_map = [row + [1] * (max_length - len(row)) for row in world_map]
    return padded_map

world_map = auto_pad_map(world_map)

TILE_SIZE = 100
FOV = math.pi / 2

class Object:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size, size)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.update_rect()

    def update_rect(self):
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

class Player(Object):
    def __init__(self, x, y, size, speed):
        super().__init__(x, y, size)
        self.speed = speed
        self.angle = 0

    def rotate(self, da):
        self.angle += da

def get_wall_rects():
    wall_rects = []
    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            if tile == 1:
                wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return wall_rects

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
                distance = depth
                wall_height = SCREEN_HEIGHT / (distance * 0.01)

                # какую часть текстуры брать
                hit_x = target_x % TILE_SIZE
                texture_x = int((hit_x / TILE_SIZE) * texture.get_width())
                texture_slice = texture.subsurface(texture_x, 0, 1, texture.get_height())

                texture_slice = pygame.transform.scale(texture_slice, (SCREEN_WIDTH // num_rays, int(wall_height)))

                screen.blit(texture_slice, (ray * (SCREEN_WIDTH // num_rays), SCREEN_HEIGHT // 2 - wall_height // 2))
                break

        ray_angle += ray_angle_step

def is_colliding(player, walls):
    for wall in walls:
        if player.rect.colliderect(wall):
            return True
    return False

player = Player(150, 150, 20, 5)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    old_player_x, old_player_y = player.x, player.y

    if keys[pygame.K_LEFT]:
        player.rotate(-0.05)
    if keys[pygame.K_RIGHT]:
        player.rotate(0.05)
    if keys[pygame.K_UP]:
        player.move(player.speed * math.cos(player.angle), player.speed * math.sin(player.angle))
    if keys[pygame.K_DOWN]:
        player.move(-player.speed * math.cos(player.angle), -player.speed * math.sin(player.angle))

    wall_rects = get_wall_rects()
    if is_colliding(player, wall_rects):
        player.x, player.y = old_player_x, old_player_y
        player.update_rect()

    screen.fill((0, 0, 0))
    cast_rays(player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
