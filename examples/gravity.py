import pygame
import sys

pygame.init()

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

x, y = 100, 100
speed = 5
gravity = 0.5
jump_height = -10
velocity_y = 0
on_ground = False


def check_collision(x, y):
    return y + 50 > height


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_height

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_s]:
        y += speed

    velocity_y += gravity
    y += velocity_y

    if check_collision(x, y):
        y = height - 50
        velocity_y = 0
        on_ground = True
    else:
        on_ground = False

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.flip()
    clock.tick(60)
