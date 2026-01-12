import numpy as np
import pygame
import random

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

def add_tuples(tuple1, tuple2):
    tuple1_x = tuple1[0]
    tuple1_y = tuple1[1]
    tuple2_x = tuple2[0]
    tuple2_y = tuple2[1]

    return (tuple1_x + tuple2_x, tuple1_y + tuple2_y)

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


class Boid:

    def __init__(self, position):
        self.position = position
        self.velocity = (random.uniform(-1,1),random.uniform(-1,1))
        self.angle = 0
        self.max_speed = 10
        self.min_distance = 5
        self.align_distance = 10
        self.collision_distance = 40
        self.flock_distance = 40

    def get_distance(self, other_position):
        x_diff = self.position[0] - other_position[0]
        y_diff = self.position[1] - other_position[1]

        return length((x_diff, y_diff))

    def separate(self, flock):
        sepr_v_x = 0
        sepr_v_y = 0
        for bird in flock:
            if bird is not self:
                distance = self.get_distance(bird.position)
                if distance < self.min_distance:
                    sepr_v_x += 1 / distance * (self.position[0] - bird.position[0])
                    sepr_v_y += 1 / distance * (self.position[0] - bird.position[0])
                    print("bird is separating")
        self.velocity = add_tuples(self.velocity, (sepr_v_x, sepr_v_y))

    def align(self, flock):
        flock_v_x = 0
        flock_v_y = 0
        birds_in_range = 1
        for bird in flock:
            if bird.position is not self.position:
                distance = self.get_distance(bird.position)
                if distance < self.align_distance:
                    birds_in_range += 1
                    flock_v_x += bird.velocity[0]
                    flock_v_y += bird.velocity[1]
                    print(self, bird)

        self.velocity = add_tuples(multiply_tuples(self.velocity, (0.5, 0.5)), (0.5 * flock_v_x / birds_in_range, 0.5 * flock_v_y / birds_in_range))


    def join_flock(self, flock):
        average_flock_position = (0,0)
        birds_in_range = 1
        for bird in flock:
            if bird is not self:
                distance = self.get_distance(bird.position)
                if distance < self.flock_distance:
                    birds_in_range += 1
                    average_flock_position = add_tuples(average_flock_position, bird.position)
                    print("bird is flocking")
        average_flock_position = multiply_tuples(average_flock_position, (1/birds_in_range, 1/birds_in_range))

        self.velocity = add_tuples(self.velocity, multiply_tuples((-1,-1), average_flock_position))

    def avoid_obstacle(self):
        future_offset = multiply_tuples(self.velocity, (1,1))
        if out_of_bounds(add_tuples(future_offset, self.position), (0,0), (640,640)):
            print("bird is leaving map")
            self.velocity = add_tuples(multiply_tuples(self.velocity, (-0.1,-0.1)), self.velocity)

    def update_position(self):
        self.position = add_tuples(self.position, self.velocity)

    def normalize_velocity(self):
        self.velocity = normalize(self.velocity)

    def multiply_velocity(self, amount):
        self.velocity = multiply_tuples(self.velocity, (amount,amount))



pygame.init()

screen = pygame.display.set_mode((640,640))

clock = pygame.time.Clock()
boid_flock = []
for i in range(40):
    boid_flock.append(Boid((random.uniform(0,640), random.uniform(0,640))))

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    for boid in boid_flock:
        boid.align(boid_flock)
        boid.join_flock(boid_flock)
        boid.separate(boid_flock)
        boid.avoid_obstacle()
        boid.multiply_velocity(0.1)

        boid.update_position()


    screen.fill("black")  # Fill the display with a solid color

    for boid in boid_flock:
        pygame.draw.circle(screen, (255,0,0), boid.position, 5)

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
