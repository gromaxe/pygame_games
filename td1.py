import pygame
import random
import math

# Global Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # Frames per second
TOWER_RELOAD_TIME = 60  # Frames to reload
TOWER_HEALTH = 100
ENEMY_HEALTH = 20
ENEMY_SPEED = 2
ENEMY_RADIUS = 10
ENEMY_Y_SPEED_RANGE = (1, 3)  # Min and max Y speed for enemies


class Tower:
    def __init__(self, x, y, radius=200, damage=5, health=TOWER_HEALTH):
        self.x = x
        self.y = y
        self.radius = radius
        self.damage = damage
        self.health = health
        self.can_shoot = True
        self.reload_counter = 0

    def shoot(self, enemies, screen):
        if self.can_shoot:
            for enemy in enemies:
                distance = ((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2) ** 0.5
                if distance <= self.radius:
                    enemy.health -= self.damage
                    pygame.draw.line(screen, (0, 255, 0), (self.x, self.y), (enemy.x, enemy.y))
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        global destroyed_enemies_counter
                        destroyed_enemies_counter += 1
                    self.can_shoot = False
                    break

    def update(self):
        if not self.can_shoot:
            self.reload_counter += 1
            if self.reload_counter >= TOWER_RELOAD_TIME:
                self.can_shoot = True
                self.reload_counter = 0

    def draw(self, screen):
        # Draw shooting range as a transparent circle
        range_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (255, 255, 255, 16), (self.radius, self.radius),
                           self.radius)  # 50 is the alpha value
        screen.blit(range_surface, (self.x - self.radius, self.y - self.radius))
        # Draw reload progress as a circular bar
        reload_percentage = self.reload_counter / TOWER_RELOAD_TIME
        end_angle = reload_percentage * 360
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 22, 2)
        if end_angle != 360:
            rect = (self.x - 22, self.y - 22, 44, 44)
            pygame.draw.arc(screen, (0, 255, 0), rect, -math.pi / 2, -math.pi / 2 + math.radians(end_angle), 2)

        # Draw health bar
        health_percentage = self.health / TOWER_HEALTH
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 20, self.y - 30, 40 * health_percentage, 5))

    def take_damage(self, amount):
        self.health -= amount
        global destroyed_towers_counter
        if self.health <= 0:
            destroyed_towers_counter += 1
        return self.health <= 0


class Enemy:
    def __init__(self, x, y, health=ENEMY_HEALTH, speed=ENEMY_SPEED, y_speed=random.uniform(*ENEMY_Y_SPEED_RANGE),
                 radius=ENEMY_RADIUS):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.y_speed = y_speed
        self.radius = radius

    def move(self):
        self.x += self.speed
        self.y += self.y_speed
        # Bounce off top and bottom
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.y_speed *= -1

    def check_collision_with_tower(self, towers):
        for tower in towers:
            distance = ((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2) ** 0.5
            if distance <= self.radius + 20:  # 20 is the tower's radius
                if tower.take_damage(self.health):
                    towers.remove(tower)
                return True
        return False

    def draw(self, screen):
        # Draw enemy
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
        # Draw health bar
        health_percentage = self.health / ENEMY_HEALTH
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.radius, self.y - self.radius - 5, self.radius * 2, 5))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.x - self.radius, self.y - self.radius - 5, self.radius * 2 * health_percentage, 5))


def create_tower(x, y):
    return Tower(x, y, radius=100, damage=5)


def create_enemy(x, y):
    return Enemy(x, y, health=random.randint(15, 25), speed=random.uniform(1, 3))


def draw_tower(tower, screen):
    pygame.draw.circle(screen, (0, 255, 0), (tower.x, tower.y), 20)
    # Draw health bar
    health_percentage = tower.health / TOWER_HEALTH
    pygame.draw.rect(screen, (255, 0, 0), (tower.x - 20, tower.y - 30, 40, 5))
    pygame.draw.rect(screen, (0, 255, 0), (tower.x - 20, tower.y - 30, 40 * health_percentage, 5))


def draw_enemy(enemy, screen):
    pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), enemy.radius)


def update_towers(towers, enemies, screen):
    for tower in towers:
        tower.shoot(enemies, screen)
        tower.update()


def update_enemies(enemies, towers):
    for enemy in enemies[:]:
        enemy.move()
        if enemy.x > SCREEN_WIDTH or enemy.x < 0:
            enemy.x -= enemy.speed
            enemy.speed *= -1
        if enemy.check_collision_with_tower(towers) or enemy.x > SCREEN_WIDTH or enemy.x < 0:
            enemies.remove(enemy)


def main():
    global destroyed_enemies_counter, destroyed_towers_counter
    destroyed_enemies_counter = 0
    destroyed_towers_counter = 0
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tower Defense')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 24)

    towers = []
    enemies = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    # Check for collision with existing towers
                    can_place_tower = True
                    for tower in towers:
                        distance = math.sqrt((tower.x - x) ** 2 + (tower.y - y) ** 2)
                        if distance < 40:  # Assuming the tower radius is 20
                            can_place_tower = False
                            break

                    if can_place_tower:
                        towers.append(create_tower(x, y))
                elif event.button == 3:
                    enemies.append(create_enemy(x, y))

        screen.fill((0, 0, 0))

        for tower in towers:
            tower.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        update_towers(towers, enemies, screen)
        update_enemies(enemies, towers)

        # Display counters
        enemies_text = font.render(f'Destroyed Enemies: {destroyed_enemies_counter}', True, (255, 255, 255))
        screen.blit(enemies_text, (10, 10))
        towers_text = font.render(f'Destroyed Towers: {destroyed_towers_counter}', True, (255, 255, 255))
        screen.blit(towers_text, (SCREEN_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
