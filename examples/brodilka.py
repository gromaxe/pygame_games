import pygame
import sys
import random

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Игра1")
clock = pygame.time.Clock()
FPS = 5

WHITE = (255, 255, 255)

# шрифт
font = pygame.font.Font(None, 36)

# сколько монет собрать для выигрыша
win_condition = 10


# загрузка картинки и изменение размера
def load_image(name, size):
    image = pygame.image.load(name)
    image = pygame.transform.scale(image, size)
    return image


# классы
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size=(50, 50)):
        super().__init__()
        self.image = load_image(image_path, size)
        self.rect = self.image.get_rect(center=position)


class Player(GameObject):
    def __init__(self, image_path, position):
        super().__init__(image_path, position)
        self.hp = 100
        self.speed = 20
        self.coins_collected = 0
        self.last_safe_position = position

    def update(self, coins_group, spikes_group):
        # движение
        self.last_safe_position = (self.rect.x, self.rect.y)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # встроенный метод проверки границ экрана
        self.rect.clamp_ip(screen.get_rect())

        # проверяем столкновения
        coins_hit = pygame.sprite.spritecollide(self, coins_group, True) # последний аргумент - убирать ли то с чем столкнулись
        if coins_hit:
            self.coins_collected += len(coins_hit)

        spikes_hit = pygame.sprite.spritecollide(self, spikes_group, False)
        if spikes_hit:
            self.hp -= 10 * len(spikes_hit)
            player.rect.x, player.rect.y = player.last_safe_position



class Coin(GameObject):
    pass # тут можно будет добавлять движение монетки

class Spike(GameObject):
    pass

class Background(GameObject):
    def __init__(self, image_path, position, size):
        super().__init__(image_path, position, size)


# группы спрайтов чтобы проще проверять столкновения
all_sprites = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
background = Background('bg.jpg', (screen_width // 2, screen_height // 2), (screen_width, screen_height))
win_img = Background('win.jpg', (screen_width // 2, screen_height // 2), (screen_width, screen_height))

# создаём объекты и добавляем в группы спрайтов
player = Player('player.png', (screen_width // 2, screen_height // 2))
all_sprites.add(player)

for _ in range(10):
    coin = Coin('coin.png', (random.randint(0, screen_width), random.randint(0, screen_height)))
    all_sprites.add(coin)
    coins_group.add(coin)

for _ in range(5):
    spike = Spike('spike.png', (random.randint(0, screen_width), random.randint(0, screen_height)))
    all_sprites.add(spike)
    spikes_group.add(spike)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(coins_group, spikes_group)

    screen.blit(background.image, background.rect)
    coins_group.draw(screen)
    spikes_group.draw(screen)
    screen.blit(player.image, player.rect)

    # отрисовываем здоровье и количество собранных монет
    health_text = font.render(f"HP: {player.hp}", True, WHITE)
    screen.blit(health_text, (10, 10))
    coins_text = font.render(f"Coins: {player.coins_collected}", True, WHITE)
    screen.blit(coins_text, (10, 50))

    # Проверем условие победы
    if player.coins_collected >= win_condition:
        background = win_img

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
