from typing import Tuple


import pygame
import numpy as np
from pygame import Surface
import random as rand


from pygame.examples.music_drop_fade import starting_pos


"""
Ignore this stuff here, it's just defining properties of the game such as window size and framerate, skip to the next
part for the code you have to figure out
"""
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((640,640))
clock = pygame.time.Clock()
fps = 60


#the maximum speed you can land at
max_speed = 5
#the image of the lunar lander
lander_image = pygame.image.load("lunar_lander.png").convert_alpha()
fuel_image = pygame.image.load("fuel_tank.png").convert_alpha()
#the width and height of the original image
lander_w = lander_image.get_width()
lander_h = lander_image.get_height()
fuel_w = fuel_image.get_width()
fuel_h = fuel_image.get_height()
#the lunar lander image scaled down
lander_image_small = pygame.transform.scale(lander_image, (lander_w * 0.1, lander_h * 0.1))
fuel_image_small = pygame.transform.scale(fuel_image, (fuel_w * 0.1, fuel_h * 0.1))
#the number of points acquired by the player at the start of the game
points = 0
"""
Fill out the functions, class, and methods below! If you do it correctly, your game will function perfectly!
If you finish early, feel free to add new mechanics to your game by tweaking your code(such as limited lives,
more in-depth controls, etc.)


Be sure to ask for help if you need it!


Also, you may get an error when running this that numpy or pygame is not installed. It's a module that is helpful for computing
sine and cosine functions (important for this project). Scroll up to the top of this code and look for the red underlined
text 'import numpy as np' and hover your mouse over it. It will then open a little popup asking if you want to install
it. Click yes and it should run fine after! :)
"""


def add_vectors(vector1: tuple, vector2: tuple) -> tuple:
   """
   This function takes in two tuples, and outputs their sum as if they were vectors
   """
   output_list = []
   for i in range(len(vector1)):
       output_list.append(vector1[i] + vector2[i])


   return tuple(output_list)


def scale_vector(scalar: float, vector: tuple) -> tuple:
   """
   This function takes in a float value and a tuple. It then returns a tuple that has each of its components scaled
   by the scalar amount (multiplied)


   scale_vector(3, (1,1)) -> (3,3)
   """
   x = vector[0]
   y = vector[1]


   return x * scalar, y * scalar


def length(vector: tuple) -> float:
   """
   This function takes in tuple, and returns the length of the corresponding vector.
   Be sure to use Pythagoras formula!


   length((1,1)) = sqrt(2)
   length((1,0)) = 1
   """
   return (vector[0] ** 2 + vector[1] ** 2) ** 0.5


def generate_vector_from_angle(angle: float) -> tuple:
   """
   This function takes in an angle (30, 360, -20.5, etc.) and outputs a vector with length 1 that points in the same
   direction as that angle.


   For those of you who aren't that familiar with sine and cosine functions, here are some steps to follow
   1. convert the angle to radians using this formula: radians = np.pi * (angle/180)
   2. your x component of your tuple is cosine(radians), where your y component is sine(radians)
   3. to use the cosine and sine functions in numpy, use the method np.cos(radians), and np.sin(radians)
   4. don't forget to return a tuple of your combined x and y elements
   """


   radians = np.pi * angle / 180
   return np.cos(radians), np.sin(radians)


class LunarLander:
   """This is the class for our lunar lander
   it requires the following local variables:
   fuel: a float value
   starting_position: a tuple referring to the x,y coordinates that the lander starts from
   position: a tuple referring to the current position of the lander, this will change over time
   angle: the angle the lander is facing in degrees, set this to -90 by default since pygame's y-axis is actually down
   velocity: a tuple representing the velocity vector that the lander has, starts as (0,0)
   gravity: the gravity force vector, you are going to need to add this to your velocity vector every frame
   ^ this will require some fine-tuning
   thrust_power: a float representing the length of the force vector applied to the lander's velocity when using the engine
   rotation_speed: a float representing how many degrees per frame the lander rotates while pressing < or >
   """


   def __init__(self, fuel, start_position_x, start_position_y):
       self.fuel = fuel
       self.position = (start_position_x, start_position_y)
       self.angle = -90
       self.velocity = (0,0)
       self.gravity = (0, 1/60)
       self.thrust_power = 10/60
       self.rotation_speed = 1




   def thrust(self):
       """
       First check if the lander has fuel, if fuel < 0, return None
       This method must create a vector in the direction of the lander's angle, with length = thrust_power
       Then it will add that vector to the lander's velocity vector, and set the new velocity vector to that


       """
       if self.fuel > 0:
           self.fuel -= 1
           thrust_direction = generate_vector_from_angle(self.angle)
           thrust_vector = scale_vector(self.thrust_power, thrust_direction)
           self.velocity = add_vectors(self.velocity, thrust_vector)






   def gravity_force(self):
       """
       This method adds the lander's gravity force to the lander's velocity
       """
       self.velocity = add_vectors(self.velocity, self.gravity)


   def move(self):
       """
       This method takes the lander's velocity vector and adds that to the lander's position vector


       OPTIONAL: You can implement pacman style edge teleporting by setting the lander's x position to 1 whenever it
       goes beyond 640, or to 639 whenever the position goes below 0
       """
       self.position = add_vectors(self.position, self.velocity)


       if 0 > self.position[0]:
           self.position = (639, self.position[1])
       if 640 < self.position[0]:
           self.position = (1, self.position[1])






   def rotate(self, amount):
       """
       This is just a simple function that adds an angle to the lander's current angle
       """
       self.angle += amount




   def get_speed(self) -> float:
       """
       This method returns the current speed of the lander by checking the LENGTH of the velocity vector
       """
       return length(self.velocity)


class LandingPad1:
   """
   I've filled out the details of the LandingPad class for you, no need to do anything here
   """
   def __init__(self, position, size):
       self.position = position
       self.size = size


   def collide(self, other_position):
       if self.position[0] - self.size[0] < other_position[0] < self.position[0] + self.size[0]:
           if self.position[1] - self.size[1] < other_position[1] < self.position[1] + self.size[1]:
               return True
       else:
           return False


   def move_goal(self, other_position):
       self.position = other_position




class FuelPickup(LandingPad1):


   def __init__(self, position, size, fuel_amount):
       super().__init__(position, size)
       self.fuel_amount = fuel_amount




class LandingPad2:


   def __init__(self, position, size):
       self.position = position
       self.size = size


   def collide(self, other_position):
       if self.position[0] - self.size[0] < other_position[0] < self.position[0] + self.size[0]:
           if self.position[1] - self.size[1] < other_position[1] < self.position[1] + self.size[1]:
               return True
       else:
           return False


   def move_goal2(self, other_position):
       self.position = other_position


class LandingPad3:
   def __init__(self, position, size,):
       self.position = position
       self.size = size


   def collide(self, other_position):
       if self.position[0] - self.size[0] < other_position[0] < self.position[0] + self.size[0]:
           if self.position[1] - self.size[1] < other_position[1] < self.position[1] + self.size[1]:
               return True
       else:
           return False


   def move_goal3(self, other_position):
       self.position = other_position






"""
This is some logic that figures out the positioning of the goal and the lunar lander sprite, ignore this
"""
lander_surface = Surface((10,10))
lander_surface.fill((244,244,244))
lander = LunarLander(1000, 320, 20)
goal1_position_x = rand.uniform(10,630)
goal1_position_y = rand.uniform(320,630)
goal1 = LandingPad1((goal1_position_x, goal1_position_y), (30, 10))
goal1_surface = Surface((goal1.size[0], goal1.size[1]))
goal1_surface.fill((255,255,255))


run = True


fuel_position_x = rand.uniform(10,600)
fuel_position_y = rand.uniform(320,600)
fuel_jug = FuelPickup((fuel_position_x, fuel_position_y), (fuel_w/10, fuel_h/10), 100)


goal2_position_x = rand.uniform(10,630)
goal2_position_y = rand.uniform(320,630)
goal2 = LandingPad2((goal2_position_x, goal2_position_y), (30, 10))
goal2_surface = Surface((goal2.size[0], goal2.size[1]))
goal2_surface.fill((0,0,255))


goal3_position_x = rand.uniform(10,630)
goal3_position_y = rand.uniform(320,630)
goal3 = LandingPad3((goal3_position_x, goal3_position_y), (30, 10))
goal3_surface = Surface((goal3.size[0], goal3.size[1]))
goal3_surface.fill((255,255,0))




"""
This is where all the player inputs are processed, you can tweak this if you want but only after making the game run
normally
"""
while run:
   # Process player inputs.
   keys = pygame.key.get_pressed()
   if keys[pygame.K_UP]:
       lander.thrust()




   if keys[pygame.K_RIGHT]:
       lander.rotate(lander.rotation_speed)




   if keys[pygame.K_LEFT]:
       lander.rotate(-lander.rotation_speed)




   if keys[pygame.K_SPACE]:
       lander.position = ((320, 150))




   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           raise SystemExit






   """
   Here's where the game updates the lunar lander, a lot of your errors will seem to come from here. Try to read through
   the error messages you get to see which methods are causing errors!
   """
   lander.gravity_force()
   lander.move()


   if goal1.collide((lander.position[0], lander.position[1])):
       if lander.get_speed() < max_speed:
           screen.fill((0, 255, 0))
           pygame.display.flip()
           pygame.time.delay(100)
           goal1.move_goal((rand.uniform(10,600), rand.uniform(320,600)))
           goal1_surface.fill((255, 255, 255))
           pygame.display.flip()
           points += 100
       else:
           run = False
           screen.fill((255, 0, 0))
           pygame.display.flip()
           pygame.time.delay(100)
           print("YOU LOSE, you landed too hard!" + "You earned " + str(points) + " points")


   if fuel_jug.collide((lander.position[0], lander.position[1])):
       screen.fill((0, 255, 0))
       pygame.display.flip()
       pygame.time.delay(100)
       lander.fuel += fuel_jug.fuel_amount
       fuel_jug.move_goal((rand.uniform(10,600), rand.uniform(320,600)))
       points += 25


   if goal2.collide((lander.position[0], lander.position[1])):
       screen.fill((0, 255, 0))
       pygame.display.flip()
       pygame.time.delay(100)
       goal2.move_goal2((rand.uniform(10,600), rand.uniform(320,600)))
       goal2_surface.fill((0, 0, 255))
       pygame.display.flip()
       points += 50


   if goal3.collide((lander.position[0], lander.position[1])):
       if lander.get_speed() < max_speed:
           screen.fill((0, 255, 0))
           pygame.display.flip()
           pygame.time.delay(100)
           goal3.move_goal3((rand.uniform(10,600), rand.uniform(320,600)))
           goal3_surface.fill((255, 255, 0))
           pygame.display.flip()
           points += 5
       else:
           run = False
           screen.fill((255, 0, 0))
           pygame.display.flip()
           pygame.time.delay(100)
           print("YOU LOSE, you landed too hard!" + "You earned " + str(points) + " points")








   if lander.position[1] > 640:
       screen.fill((255, 0, 0))
       pygame.display.flip()
       pygame.time.delay(100)
       print("YOU LOSE, you landed too hard!" + "You earned " + str(points) + " points")
       run = False


   if lander.position[1] < -100000:
       screen.fill((255, 0, 255))
       pygame.display.flip()
       pygame.time.delay(100)
       screen.fill((0, 0, 0))
       pygame.display.flip()
       pygame.time.delay(100)
       screen.fill((255, 0, 255))
       pygame.display.flip()
       pygame.time.delay(100)
       screen.fill((0, 0, 0))
       pygame.display.flip()
       pygame.time.delay(100)
       screen.fill((255, 0, 255))
       pygame.display.flip()
       pygame.time.delay(100),
       print("YOU WIN! " "you crashed into pluto!!!!!!!!!!!!!!!!!" + "You earned " + str(points * 10) + (" points"))
       run = False


   screen.fill("black")  # Fill the display with a solid color
   if lander.get_speed() < max_speed:
       speed_surface = my_font.render(str(round(lander.get_speed(), 1)) + " m/s", False, (255, 255, 255))
   else:
       speed_surface = my_font.render("TOO FAST!", False, (255, 0, 0))


   lander_image_small_rotated = pygame.transform.rotate(lander_image_small, -lander.angle - 90)
   screen.blit(lander_image_small_rotated, (lander.position[0] - lander_w/20, lander.position[1] - lander_h/20))
   screen.blit(fuel_image_small, (fuel_jug.position[0] - fuel_w/20, fuel_jug.position[1] - fuel_h/20))
   screen.blit(fuel_image_small, (0-fuel_h/20,0-fuel_w/20))
   screen.blit(speed_surface, (32, 32))
   screen.blit(goal2_surface, (goal2.position[0] - goal2.size[0]/2, goal2.position[1] - goal2.size[1]/2))
   screen.blit(goal3_surface, (goal3.position[0] - goal3.size[0]/2, goal3.position[1] - goal3.size[1]/2))
   screen.blit(goal1_surface, (goal1.position[0] - goal1.size[0]/2, goal1.position[1] - goal1.size[1]/2))


   fuel_surface = my_font.render(str(lander.fuel) + " Fuel Remaining", False, (255, 255, 255))
   screen.blit(fuel_surface, (32, 64))


   points_surface = my_font.render(str(points) + " Points", False, (255, 255, 255))
   screen.blit(points_surface, (500, 32))


   pygame.display.flip()  # Refresh on-screen display
   clock.tick(fps)         # wait until next frame (at 60 FPS)
