import pygame
import sys

pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FPS = 60

bg = pygame.image.load("birds/back.png")
ground = pygame.image.load("birds/ground.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))
ground = pygame.transform.scale(ground, (int(screen_width*1.2), screen_height//5))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.gravity = 0.5

    def load_images(self):
        for num in range(4):
            img = pygame.image.load(f"birds/birb{num}.png")
            self.images.append(img)

    def update(self):
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)
        if self.rect.bottom >= screen_height - ground.get_height():
            self.rect.bottom = screen_height - ground.get_height()
            self.velocity = 0
        self.index = (self.index+1) % len(self.images)
        self.image = self.images[self.index]

    def jump(self):
        self.velocity = -10

bird = Bird(screen_width // 2, screen_height // 2)
ground_scroll = 0
scroll_speed = 1
game_over = False

running = True
while running:
    screen.blit(bg, (0, 0))
    screen.blit(ground, (ground_scroll, screen_height-ground.get_height()))
    if ground_scroll <= 110:
        ground_scroll = 0
    ground_scroll -= scroll_speed

    bird.update()
    screen.blit(bird.image, bird.rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
