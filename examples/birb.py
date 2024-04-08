import pygame
import sys
import random

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
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]

    def jump(self):
        self.velocity = -10


class PipePair(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load(f"birds/pipe.png")
        self.image = pygame.transform.scale(self.image, (50,800))
        self.top_pipe = pygame.transform.flip(self.image, False, True)
        self.bottom_pipe = self.image.copy()
        self.gap_size = 200
        self.top_height = random.randint(25, screen_height - self.gap_size - 25)
        self.bottom_height = screen_height - (self.top_height + self.gap_size)
        self.top_rect = self.top_pipe.get_rect(midbottom=(x, self.top_height))
        self.bottom_rect = self.bottom_pipe.get_rect(midtop=(x, self.top_height + self.gap_size))
        self.velocity = 5

    def update(self):
        self.top_rect.x -= int(self.velocity)
        self.bottom_rect.x -= int(self.velocity)
        if self.top_rect.right < 0:
            self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

bird = Bird(screen_width // 2, screen_height // 2)
bird_group.add(bird)

ground_scroll = 0
scroll_speed = 4
game_over = False

pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 2000)

running = True
while running:
    screen.blit(bg, (0, 0))

    if not game_over:
        ground_scroll -= scroll_speed
        if ground_scroll <= -110:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()
        if event.type == pipe_timer:
            pipe_pair = PipePair(screen_width)
            pipe_group.add(pipe_pair)

    if not game_over:
        bird_group.update()
        pipe_group.update()

        # проверяем на столкновения
        for pipe_pair in pipe_group:
            if pipe_pair.top_rect.colliderect(bird.rect) or pipe_pair.bottom_rect.colliderect(bird.rect):
                print("game_over = True")
                bird.image = pygame.transform.flip(bird.image, False, True)

    # отрисовка
    if random.random() > 0.8:
        bird_group.draw(screen)
        for pipe_pair in pipe_group:
            screen.blit(pipe_pair.top_pipe, pipe_pair.top_rect)
            screen.blit(pipe_pair.bottom_pipe, pipe_pair.bottom_rect)
    else:
        for pipe_pair in pipe_group:
            screen.blit(pipe_pair.top_pipe, pipe_pair.top_rect)
            screen.blit(pipe_pair.bottom_pipe, pipe_pair.bottom_rect)
        bird_group.draw(screen)

    screen.blit(ground, (ground_scroll, screen_height - ground.get_height()))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
