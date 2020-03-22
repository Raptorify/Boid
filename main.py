import math
import numpy as np
import random
import pygame
import time


# Initializing
pygame.init()
WIDTH, HEIGHT = 800, 600
CLOCK = pygame.time.Clock()
CLOCK.tick(60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boid Simulation")
boidList = []

# Vector functions
def normalize(x):
    if x.all() > 0:
        return x / np.sqrt(np.sum(x**2))
    else:
        return np.array([0, 0])


class Boid:
    def __init__(self):
        self.position = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.acceleration = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.maxSpeed = 0.3
        self.radius = 6
        self.perceptionRadius = 100
        self.color = (255, 255, 255)

# Draws the boids
    def render(self):
        pygame.draw.circle(screen, self.color, [int(i) for i in self.position], self.radius)

# Limit the maximum velocity
    def limit(self):
        for i in range(len(self.velocity)):
            if self.velocity[i] > 0:
                if abs(self.velocity[i]) > self.maxSpeed:
                    self.velocity[i] = self.maxSpeed
            if self.velocity[i] < 0:
                if abs(self.velocity[i]) > self.maxSpeed:
                    self.velocity[i] = -self.maxSpeed

# Updates velocity and position
    def update(self):
        alignment = self.align()
### Try to set direction without affecting the speed!
        self.acceleration = np.add(self.acceleration, alignment)
        self.velocity = np.add(self.velocity, self.acceleration)
        Boid.limit(self)
        self.position = np.add(self.position, self.velocity)

# Loop boids around the window
    def border(self):
        if self.position[0] >= WIDTH:
            self.position[0] = 0
        elif self.position[0] <= 0:
            self.position[0] = WIDTH
        if self.position[1] >= HEIGHT:
            self.position[1] = 0
        elif self.position[1] <= 0:
            self.position[1] = HEIGHT

# Calculate the distance between 2 boids
    def dist(self, flockmate):
        return math.sqrt((flockmate.position[0] - self.position[0])**2
                       + (flockmate.position[1] - self.position[1])**2)

# Steer towards the average heading of local flockmates
    def align(self):
        steering = np.array([0, 0])
        total = 0

        for flockmate in boidList:
            distance = Boid.dist(self, flockmate)
            if flockmate != self and distance <= self.perceptionRadius:
                total += 1
                steering = np.add(steering, flockmate.velocity)
        if total > 0:
            steering = np.divide(steering, total)
            steering = np.subtract(steering, self.velocity)
        return steering

# Populate the list with boid units
for i in range(20):
    boidList.append(Boid())

# Main loop
def setup():
    running = True
    while running:
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render background and clear old boid position
        screen.fill((0,0,0))
        # Render boids
        for boid in boidList:
            # boid.align()
            boid.border()
            boid.render()
            boid.update()
        # Update display
        pygame.display.update()


setup()
