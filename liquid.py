import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and other constants
WIDTH, HEIGHT = 800, 600
PARTICLE_RADIUS = 20
GRAVITY = np.array([0, 0.1])  # Gravity effect
INTERACTION_RADIUS = 40
MAX_VELOCITY = 5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid Simulation")

class Particle:
    def __init__(self, position, velocity, volume, density, salinity, temperature):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.volume = volume
        self.density = density
        self.salinity = salinity
        self.temperature = temperature
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.position.astype(int), PARTICLE_RADIUS)

    def update(self, particles):
        # Apply gravity and limit velocity
        self.velocity += GRAVITY
        self.velocity *= 0.99
        self.velocity = np.clip(self.velocity, -MAX_VELOCITY, MAX_VELOCITY)
        self.position += self.velocity

        # Boundary collision
        self.check_boundary_collision()

        # Check for interactions with nearby particles
        self.apply_repulsion(particles)

    def check_boundary_collision(self):
        if self.position[0] - PARTICLE_RADIUS <= 0 or self.position[0] + PARTICLE_RADIUS >= WIDTH:
            self.velocity[0] *= -1
            self.position[0] = np.clip(self.position[0], PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        if self.position[1] - PARTICLE_RADIUS <= 0 or self.position[1] + PARTICLE_RADIUS >= HEIGHT:
            self.velocity[1] *= -1
            self.position[1] = np.clip(self.position[1], PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)

    def apply_repulsion(self, particles):
        for particle in particles:
            if particle != self:
                vector_to_other = particle.position - self.position
                distance = np.linalg.norm(vector_to_other)
                if 0 < distance < INTERACTION_RADIUS:
                    # Normalized direction vector from self to other particle
                    direction = vector_to_other / distance
                    repulsion_force = direction*200/distance #* min(0.9, 60 / distance)
                    self.position -= repulsion_force  # Move away from the other particle

# Create a list of particles
particles = [Particle((random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS),
                       random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)),
                      [0, 0], 1, 1, 1, 1) for _ in range(150)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Clear screen

    # Update and draw particles
    for particle in particles:
        particle.update(particles)
        particle.render(screen)

    pygame.display.flip()  # Update screen

pygame.quit()
