import pygame
import sys

# Инициализация PyGame
pygame.init()

# Определение размеров экрана
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# Цвета
black = 0, 0, 0
white = 255, 255, 255

# Начальное положение объекта
x, y = width // 2, height // 2
speed = 5

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += speed

    screen.fill(black)
    pygame.draw.rect(screen, white, pygame.Rect(x, y, 50, 50))
    pygame.display.flip()
