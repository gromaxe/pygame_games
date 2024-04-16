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
ground = pygame.transform.scale(ground, (int(screen_width * 1.2), screen_height // 5))

flap_sound = pygame.mixer.Sound("birds/flap.wav")
score_sound = pygame.mixer.Sound("birds/score.wav")
game_over_sound = pygame.mixer.Sound("birds/gameover.wav")


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
        flap_sound.play()


class PipePair(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load(f"birds/pipe.png")
        self.image = pygame.transform.scale(self.image, (50, 800))
        self.top_pipe = pygame.transform.flip(self.image, False, True)
        self.bottom_pipe = self.image.copy()
        self.gap_size = 200
        self.top_height = random.randint(25, screen_height - self.gap_size - 25)
        self.bottom_height = screen_height - (self.top_height + self.gap_size)
        self.top_rect = self.top_pipe.get_rect(midbottom=(x, self.top_height))
        self.bottom_rect = self.bottom_pipe.get_rect(midtop=(x, self.top_height + self.gap_size))
        self.velocity = 5
        self.passed = False

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
score = 0
start_time = pygame.time.get_ticks()

pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 2000)

running = True
while running:
    screen.blit(bg, (0, 0))
    game_time = (pygame.time.get_ticks() - start_time) // 1000

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

        for pipe_pair in pipe_group:
            if bird.rect.colliderect(pipe_pair.top_rect) or bird.rect.colliderect(pipe_pair.bottom_rect):
                game_over = True
                game_over_sound.play()
                print("Game over!")
            if bird.rect.left > pipe_pair.top_rect.right and not pipe_pair.passed:
                pipe_pair.passed = True
                score += 1
                score_sound.play()

    bird_group.draw(screen)
    for pipe_pair in pipe_group:
        screen.blit(pipe_pair.top_pipe, pipe_pair.top_rect)
        screen.blit(pipe_pair.bottom_pipe, pipe_pair.bottom_rect)

    screen.blit(ground, (ground_scroll, screen_height - ground.get_height()))
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f'Score: {score}', True, pygame.Color('white'))
    time_surface = font.render(f'Time: {game_time}s', True, pygame.Color('white'))
    screen.blit(score_surface, (10, 10))
    screen.blit(time_surface, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
