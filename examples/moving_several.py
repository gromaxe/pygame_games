import pygame
import sys
import os

# Инициализация PyGame
pygame.init()

# Определение размеров экрана
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# Проверка наличия файлов изображений и загрузка, если они существуют
background_image_path = "background.jpg"
object_image_path = "object.png"
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path)
else:
    background_image = None

if os.path.exists(object_image_path):
    object_image = pygame.image.load(object_image_path)
else:
    object_image = None


class MovingObject:
    def __init__(self, image, position, control_keys):
        self.image = image
        self.position = position
        self.speed = 5
        self.control_keys = control_keys  # [влево, вправо, вверх, вниз]

    def move(self, keys):
        if keys[self.control_keys[0]]:
            self.position[0] -= self.speed
        if keys[self.control_keys[1]]:
            self.position[0] += self.speed
        if keys[self.control_keys[2]]:
            self.position[1] -= self.speed
        if keys[self.control_keys[3]]:
            self.position[1] += self.speed

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.position)
        else:
            pygame.draw.circle(surface, (255, 255, 255), self.position, 20)  # Рисуем белый круг


# Создание объектов
player1 = MovingObject(object_image, [width // 4, height // 2], [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s])
player2 = MovingObject(object_image, [3 * width // 4, height // 2], [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    player1.move(keys)
    player2.move(keys)

    # Отрисовка фона
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))  # Заливаем экран чёрным, если нет изображения фона

    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()
