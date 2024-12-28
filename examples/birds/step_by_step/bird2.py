import pygame
import sys
import random

pygame.init()
size = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
FPS = 60

bg = pygame.image.load('../back.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

ground = pygame.image.load('../ground.png')
ground = pygame.transform.scale(ground,
                                (SCREEN_WIDTH + 200, 100))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../birb0.png")
        self.rect = self.image.get_rect(centerx=300)
        self.speed = 0

    def update(self):
        if not self.rect.colliderect(ground.get_rect(topleft=(ground_left, 500))):
            self.speed += 1
        else:
            self.speed = min(0, self.speed)
        self.rect.centery += self.speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.speed = -15


bird = Bird()
birds = pygame.sprite.Group()
birds.add(bird)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x=SCREEN_WIDTH, y=SCREEN_HEIGHT//2, flip=False):
        super().__init__()
        self.image = pygame.image.load("../pipe.png")
        if flip:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(topleft=(x,y))  # это контур трубы

    def update(self):
        if self.rect.right < 0:
            self.rect.right=SCREEN_WIDTH
        else:
            self.rect.left -= ground_speed


pipes = pygame.sprite.Group()
pipes.add(Pipe(x = 600, y = 400))
pipes.add(Pipe(x = 600, y =-700, flip=True))
pipes.add(Pipe(x = 200, y= 350))
pipes.add(Pipe(x = 200, y=-750, flip=True))

ground_left = 0
ground_speed = 5
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    screen.blit(bg, (0, 0))

    ground_left -= ground_speed
    if ground_left < -65:
        ground_left = 0
    screen.blit(ground, (ground_left, 500))

    birds.update()
    birds.draw(screen)

    pipes.update()
    pipes.draw(screen)

    if pygame.sprite.spritecollideany(bird, pipes):
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)