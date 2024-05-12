import math

import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60

pygame.display.set_caption("Защита замка")
clock = pygame.time.Clock()

class Castle:
    def __init__(self, x, y, width=100, height=100):
        self.health = 1000
        self.max_health = self.health
        self.image = pygame.image.load("birds/pipe.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft = (x, y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.rect.left
        y_dist = -(mouse_pos[1] - self.rect.top)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        pygame.draw.line(screen, (1,1,1), (self.rect.left, self.rect.top), (mouse_pos))
        if pygame.mouse.get_pressed()[0] == 1:
            new_arrow = Arrow(self.rect.left, self.rect.top, self.angle)
            arrows_group.add(new_arrow)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("birds/birb1.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = (x, y))

arrows_group = pygame.sprite.Group()

bg = pygame.image.load("birds/back.png")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

castle = Castle(700, 350)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




    screen.blit(bg, (0,0))
    castle.draw()
    castle.shoot()
    arrows_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit