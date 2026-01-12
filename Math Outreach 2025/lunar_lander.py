import pygame
import numpy as np
from pygame import Surface
import random as rand

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((640,640))

clock = pygame.time.Clock()
fps = 60

#the maximum speed you can land at
max_speed = 90
#the image of the lunar lander
lander_image = pygame.image.load("lunar_lander.png").convert_alpha()
#the width and height of the original image
lander_w = lander_image.get_width()
lander_h = lander_image.get_height()
#the lunar lander image scaled down
lander_image_small = pygame.transform.scale(lander_image, (lander_w * 0.1, lander_h * 0.1))

#the number of points acquired by the player at the start of the game
points = 0



class LunarLander:
    """This is the class for our lunar lander"""

    def __init__(self, fuel, start_position_x, start_position_y):

        self.fuel = fuel #fuel is used up as you fly
        self.start_position_x = start_position_x
        self.start_position_y = start_position_y
        self.position_x = start_position_x
        self.position_y = start_position_y
        self.angle = -90 #the direction the lander is pointing on the cartesian plane relative to origin
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity_x = 0
        self.gravity_y = 3
        self.thrust_velocity = 5
        self.rotation_speed = 1

        self.direction = (0,1) #the direction vector for the lander

    def thrust(self):
        thrust_x = np.cos(np.radians(self.angle)) * self.thrust_velocity #converting angle to radians
        thrust_y = np.sin(np.radians(self.angle)) * self.thrust_velocity #converting angle to radians
        if self.fuel > 0:
            self.velocity_x += thrust_x
            self.velocity_y += thrust_y
            self.fuel = self.fuel - 1
        else:
            return None


    def force(self):
        self.velocity_x += self.gravity_x
        self.velocity_y += self.gravity_y

    def move(self):
        self.position_x += self.velocity_x/fps
        self.position_y += self.velocity_y/fps

        if 0 > self.position_x:
            self.position_x = 639
        if 640 < self.position_x:
            self.position_x = 1



    def rotate(self, amount):
        self.angle += amount
        self.direction = (
            np.cos(np.radians(self.angle)),
            np.sin(np.radians(self.angle))
        )

    def get_velocity(self):
        return np.sqrt(self.velocity_x ** 2 + self.velocity_y ** 2)

class LandingPad:

    def __init__(self, position, size):
        self.position = position
        self.size = size

    def collide(self, other_position):
        if self.position[0] < other_position[0] < self.position[0] + self.size[0]:
            if self.position[1] < other_position[1] < self.position[1] + self.size[1]:
                return True
        else:
            return False

    def move_goal(self, other_position):
        self.position = other_position

lander_surface = Surface((10,10))
lander_surface.fill((244,244,244))
lander = LunarLander(1000, 320, 20)
goal_position_x = rand.uniform(10,630)
goal_position_y = rand.uniform(320,630)
goal = LandingPad((goal_position_x, goal_position_y), (30, 10))
goal_surface = Surface((goal.size[0], goal.size[1]))
goal_surface.fill((0,255,0))
run = True





while run:
    # Process player inputs.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        lander.thrust()
    if keys[pygame.K_RIGHT]:
        lander.rotate(lander.rotation_speed)


    if keys[pygame.K_LEFT]:
        lander.rotate(-lander.rotation_speed)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    lander.force()
    lander.move()
    if goal.collide((lander.position_x, lander.position_y)):
        if np.sqrt(lander.velocity_x ** 2 + lander.velocity_y ** 2) < max_speed:
            goal.move_goal((rand.uniform(10,630), rand.uniform(320,630)))
            points += 1
        else:
            run = False
            print("YOU LOSE, you landed too hard!" + "You earned " + str(points) + " points")

    if lander.position_y > 640:
        print("YOU LOSE, you landed too hard!" + "You earned " + str(points) + " points")
        run = False

    screen.fill("black")  # Fill the display with a solid color
    if lander.get_velocity() < max_speed:
        speed_surface = my_font.render(str(round(lander.get_velocity() / 10, 1)) + " m/s", False, (255, 255, 255))
    else:
        speed_surface = my_font.render("TOO FAST!", False, (255, 0, 0))

    lander_image_small_rotated = pygame.transform.rotate(lander_image_small, -lander.angle - 90)
    screen.blit(lander_image_small_rotated, (lander.position_x - lander_w/20, lander.position_y - lander_h/20))

    pygame.draw.line(screen, (0,255,0), (lander.position_x, lander.position_y), (lander.position_x + 10 * lander.direction[0], lander.position_y + 10 * lander.direction[1]))

    screen.blit(goal_surface, goal.position)
    screen.blit(speed_surface, (32, 32))

    fuel_surface = my_font.render(str(lander.fuel) + " Fuel Remaining", False, (255, 255, 255))
    screen.blit(fuel_surface, (32, 64))

    points_surface = my_font.render(str(points) + " Points", False, (255, 255, 255))
    screen.blit(points_surface, (500, 32))

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(fps)         # wait until next frame (at 60 FPS)