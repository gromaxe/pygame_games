import pygame
import sys

# Инициализация PyGame
pygame.init()

# Определение размеров экрана
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# Цвета
black = 0, 0, 0
red = 255, 0, 0

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    x, y = pygame.mouse.get_pos()

    screen.fill(black)
    pygame.draw.circle(screen, red, (x, y), 20)
    pygame.display.flip()
