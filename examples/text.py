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

# Создание шрифта
font = pygame.font.Font(None, 36)

# Текст для вывода
text = font.render('Привет, PyGame!', True, white)

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    screen.blit(text, (50, 50))
    pygame.display.flip()
