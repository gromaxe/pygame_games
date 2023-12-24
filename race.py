import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load car image
car_image = pygame.image.load('car.png')  # Replace 'car.png' with the path to your car image
car_image = pygame.transform.scale(car_image, (64, 64))  # Scale to appropriate size

# Car Class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Direction car is facing
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.turn_speed = 0.03
        self.handbrake_on = False
        self.movement_angle = 0  # Actual movement direction
        self.movement_speed = 0
        self.width = car_image.get_width()
        self.height = car_image.get_height()
        self.trails = [[], [], [], []]  # Trails for each wheel

    def update(self, keys, dt):
        # Check handbrake
        self.handbrake_on = keys[pygame.K_SPACE]

        # Acceleration and Deceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.max_speed, self.speed + self.acceleration)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(0, self.speed - self.deceleration)

        # Turning
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.turn_speed

        # Update movement angle and speed
        if self.handbrake_on:
            # Drifting logic
            self.movement_angle = self.angle
            self.movement_speed *= 0.98
        else:
            self.movement_angle = self.angle
            self.movement_speed = self.speed

        # Calculate new position
        self.x += math.sin(self.movement_angle) * self.movement_speed
        self.y -= math.cos(self.movement_angle) * self.movement_speed

        # Keep car within screen boundaries
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

        # Update trails (wheel traces)
        wheel_offsets = [(15, 30), (-15, 30), (15, -30), (-15, -30)]  # Front and rear wheel positions
        if self.handbrake_on:
            for i, offset in enumerate(wheel_offsets):
                offset_x, offset_y = offset
                wheel_x = self.x + offset_x * math.cos(math.radians(self.angle)) - offset_y * math.sin(math.radians(self.angle))
                wheel_y = self.y + offset_x * math.sin(math.radians(self.angle)) + offset_y * math.cos(math.radians(self.angle))
                self.trails[i].append((int(wheel_x), int(wheel_y)))
                if len(self.trails[i]) > 50:  # Limit trail length
                    self.trails[i].pop(0)

    def draw(self, screen):
        # Draw wheel traces
        for trail in self.trails:
            for pos in trail:
                pygame.draw.circle(screen, (255, 255, 255), pos, 2)

        # Draw car
        rotated_image = pygame.transform.rotate(car_image, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)

# Main game loop
running = True
car = Car(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen
    screen.fill((0, 0, 0))

    # Update and draw car
    keys = pygame.key.get_pressed()
    car.update(keys, dt)
    car.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
