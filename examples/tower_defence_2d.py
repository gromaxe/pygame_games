import math

import pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60

pygame.display.set_caption("Защита замка")
clock = pygame.time.Clock()

# Таймер для спавна врагов
ENEMY_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SPAWN, 3000)  # начинаем с интервала в 3 секунды

SHOOT_COOLDOWN = 500


class Castle:
    def __init__(self, x, y, width=100, height=100):
        self.health = 1000
        self.max_health = self.health
        self.image = pygame.image.load("birds/pipe.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.last_shot_time = pygame.time.get_ticks()

    def draw_health_bar(self):
        # Полоса здоровья
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y - 10, 100, 10))
        current_health_width = (self.health / self.max_health) * 100
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y - 10, current_health_width, 10))

    def draw(self):
        screen.blit(self.image, self.rect)
        self.draw_health_bar()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= SHOOT_COOLDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x_dist = 1.0*mouse_pos[0] - self.rect.left
            y_dist = 1.0*(mouse_pos[1] - self.rect.top)
            self.angle = math.degrees(math.atan2(y_dist, x_dist))
            # print(self.angle)
            pygame.draw.line(screen, (1,1,1), (self.rect.left, self.rect.top), (mouse_pos))
            if pygame.mouse.get_pressed()[0] == 1:
                new_arrow = Arrow(self.rect.left, self.rect.top, self.angle)
                arrows_group.add(new_arrow)
                self.last_shot_time = current_time


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("birds/birb1.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = (x, y))
        self.dx = 5*math.cos(math.radians(angle))
        self.dy = 5*math.sin(math.radians(angle))

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        self.rect.y += self.dy


arrows_group = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health = 100, *groups):
        super().__init__(*groups)
        self.health = health
        self.image = pygame.image.load("birds/pipe.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        self.rect.x += 1
        for arrow in arrows_group:
            if self.rect.colliderect(arrow.rect):
                arrow.kill()
                self.health -= 25
                self.rect.scale_by_ip(0.8)
                self.image = pygame.transform.smoothscale_by(self.image, 0.8)
                if self.health <=0:
                    self.kill()
        if self.rect.colliderect(castle.rect):
            castle.health -= self.health
            self.kill()

enemies_group = pygame.sprite.Group()

bg = pygame.image.load("birds/back.png")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

castle = Castle(700, 350)
enemy_count = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == ENEMY_SPAWN:
            new_enemy = Enemy(0, 350)
            enemies_group.add(new_enemy)
            enemy_count += 1
            if enemy_count == 15:
                pygame.time.set_timer(ENEMY_SPAWN, 2000)  # Переключение на более частый интервал




    screen.blit(bg, (0,0))
    castle.draw()
    castle.shoot()
    # castle.spawn()
    arrows_group.update()
    arrows_group.draw(screen)

    enemies_group.update()
    enemies_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit
