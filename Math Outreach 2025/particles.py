import numpy as np
import pygame
import random


screen_size = (640, 640)

def normalize(vector_tuple):
    x = vector_tuple[0]
    y = vector_tuple[1]
    magnitude = length(vector_tuple)
    x = x / magnitude
    y = y/ magnitude
    return (x,y)

def length(vector_tuple):
    x = vector_tuple[0]
    y = vector_tuple[1]

    return np.sqrt(x ** 2 + y ** 2)

def distance(vector1, vector2):
    difference_vector = subtract_tuples(vector1, vector2)
    return length(difference_vector)

def add_tuples(tuple1, tuple2):
    tuple1_x = tuple1[0]
    tuple1_y = tuple1[1]
    tuple2_x = tuple2[0]
    tuple2_y = tuple2[1]

    return tuple1_x + tuple2_x, tuple1_y + tuple2_y

def subtract_tuples(tuple1, tuple2):
    tuple1_x = tuple1[0]
    tuple1_y = tuple1[1]
    tuple2_x = tuple2[0]
    tuple2_y = tuple2[1]

    return (tuple1_x - tuple2_x, tuple1_y - tuple2_y)

def multiply_tuples(tuple1, tuple2):
    tuple1_x = tuple1[0]
    tuple1_y = tuple1[1]
    tuple2_x = tuple2[0]
    tuple2_y = tuple2[1]
    return (tuple1_x * tuple2_x, tuple1_y * tuple2_y)

def out_of_bounds(position, corner1, corner2):
    x = position[0]
    y = position[1]
    if corner1[0] <= x <= corner2[0] and corner1[1] <= y <= corner2[1]:
        return False
    else:
        return True

def dot_product(vector1, vector2):
    vector1_x = vector1[0]
    vector1_y = vector1[1]
    vector2_x = vector2[0]
    vector2_y = vector2[1]
    return vector1_x * vector2_x + vector1_y * vector2_y

def reflect(direction, normal):
    direction_dot_normal = dot_product(direction, normal)
    direction_dot_normal_times_normal = multiply_tuples((direction_dot_normal, direction_dot_normal), normal)
    two_times_direction_dot_normal_times_normal = multiply_tuples((2,2), direction_dot_normal_times_normal)
    ttddntn = two_times_direction_dot_normal_times_normal
    return subtract_tuples(direction, ttddntn)


class Particle:

    def __init__(self, position, mass, radius):

        self.position = position
        self.mass = mass
        self.radius = random.uniform(5,30)
        self.velocity = (random.uniform(-1,1),random.uniform(-1,1))
        self.gravity_force = (0, 9.8/60)

    def get_out_of_bounds_normal(self):
        position_x = self.position[0]
        position_y = self.position[1]

        if position_x < 0 and position_y < 0:
            return (1,1)
        elif position_x < 0 and 0 <= position_y <= 640:
            return (1,0)
        elif position_x < 0 and position_y > 640:
            return (1, -1)
        elif 0 <= position_x <= 640 and position_y > 640:
            return (0, -1)
        elif position_x > 640 and position_y > 640:
            return (-1,-1)
        elif position_x > 640 and 0 <= position_y <= 640:
            return (-1, 0)
        elif position_x > 640 and position_y < 0:
            return (-1, 1)
        elif 0 <= position_x <= 640 and position_y < 0:
            return (0, 1)

    def bounce(self, dampening_ratio):
        reflect_vector = reflect(self.velocity, normalize(self.get_out_of_bounds_normal()))
        self.velocity = multiply_tuples(reflect_vector, (dampening_ratio, dampening_ratio))

    def update(self):
        self.velocity = add_tuples(self.velocity, self.gravity_force)
        self.position = add_tuples(self.position, self.velocity)

        if length(self.velocity) < 1:
            if self.position[0] < -1:
                self.position = (0, self.position[1])
            if self.position[0] > 641:
                self.position = (640, self.position[1])
            if self.position[1] < -1:
                self.position = (self.position[0], 640)
            if self.position[1] > 641:
                self.position = (self.position[0], 640)

    def particle_deflect(self, other_particle):
        distance_between = distance(self.position, other_particle.position)
        if distance_between < self.radius + other_particle.radius:
            repulsion = multiply_tuples((1/distance_between, 1/distance_between), subtract_tuples(self.position, other_particle.position))
            self.velocity = add_tuples(self.velocity, repulsion)

pygame.init()

FPS = 60

screen = pygame.display.set_mode((640,640))

clock = pygame.time.Clock()

particles = []
for i in range(50):
    particles.append(Particle((random.uniform(0,640), random.uniform(0,640)), 10, 5))



while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    for particle in particles:
        particle.update()
        if out_of_bounds(particle.position, (0,0), (640,640)):
            particle.bounce(0.9)
        for other_particle in particles:
            if other_particle is not particle:
                particle.particle_deflect(other_particle)

    screen.fill("black")  # Fill the display with a solid color

    for particle in particles:
        pygame.draw.circle(screen, (255, 0, 0), particle.position, particle.radius)

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)