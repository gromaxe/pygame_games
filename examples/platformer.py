import pygame
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = -10

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

game_state = "menu"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = PLAYER_SPEED
        self.vel_y = 0

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[pygame.K_SPACE] and self.vel_y == 0:
            self.jump()

        self.vel_y += GRAVITY
        self.rect.move_ip(0, self.vel_y)

        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0

    def jump(self):
        self.vel_y = JUMP_HEIGHT


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        self.rect.move_ip(0, 1)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0


class Button:
    def __init__(self, text, width, height, pos, elevation, action):
        self.text = text
        self.width = width
        self.height = height
        self.position = pos
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_position = pos[1]
        self.top_color = '#475F77'
        self.action = action
        self.text_surf = pygame.font.Font(None, 40).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=(pos[0] + width // 2, pos[1] + height // 2))

    def draw(self, screen):
        self.top_rect = pygame.Rect(self.position, (self.width, self.height))
        self.top_rect.y = self.original_y_position - self.dynamic_elevation
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                if not self.action:
                    self.action = True
            else:
                self.dynamic_elevation = self.elevation
                if self.action:
                    self.action()
                    self.action = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'


def main_menu():
    global game_state
    play_button = Button("Play", 200, 50, (300, 250), 5, lambda: change_game_state("play"))
    exit_button = Button("Exit", 200, 50, (300, 350), 5, sys.exit)

    while game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        play_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def change_game_state(state):
    global game_state
    game_state = state


def game_loop():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player()
    platform_positions = [(i * 1.2, i) for i in range(100, SCREEN_HEIGHT, 80)]
    for pos in platform_positions:
        platform = Platform(pos[0], pos[1], SCREEN_WIDTH // 3, 20)
        all_sprites.add(platform)
        platforms.add(platform)

    all_sprites.add(player)

    while game_state == "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        for platform in platforms:
            platform.update()

        collisions = pygame.sprite.spritecollide(player, platforms, False)
        if collisions:
            player.rect.bottom = collisions[0].rect.top
            player.vel_y = 0

        screen.fill(BLACK)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    while True:
        if game_state == "menu":
            main_menu()
        elif game_state == "play":
            game_loop()
