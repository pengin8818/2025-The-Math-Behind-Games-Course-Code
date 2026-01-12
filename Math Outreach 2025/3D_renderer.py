import pygame
import math
from obj_to_list import parse_obj_from_file
pygame.init()
"""
Below are just some parameters that effect the visuals of the 3D rendering program. You don't need to touch these
unless you want to tinker with things after the rest of the code is complete!
"""
width, height = 640, 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Rendering")
my_font = pygame.font.SysFont('Comic Sans MS', 24)
black = (0, 0, 0)
white = (255, 255, 255)
rotation_speed = 0.1
focal_length = 300
translation_vector = [[0],[0],[0]]
running = True
filename = "low_poly_stanford_bunny"
points, connections = parse_obj_from_file(filename)


"""
Below are some functions you must complete in order for the 3D renderer to work properly!
"""
def column(matrix: list, index: int) -> list:
    """
    This function takes in the index of a column of a matrix, and returns a list containing all the elements of that
    column. For example, if you wanted the first column of your matrix, you would use this function like so:

    column(my_matrix, 0), and that would return the first column.

    Matrices in python can be represented as lists of lists, so if I wanted to use the identity matrix here in Python
    (the matrix with 1s on the diagonal and 0s everywhere else), I would create a variable like so:

    identity_matrix = [
                        [1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]
                        ]

    This ^ is just a list of lists. This can be confusing, but if you think about it more, a matrix is really just a
    big list of rows or columns in order, and a row/column is just a list of numbers in order.

    using our function on the identity matrix, column(identity_matrix, 1) should return the list [0, 1, 0] since that
    is the second column of the matrix!
    """
    output_column = []
    for row in matrix:
        output_column.append(row[index])
    return output_column

def dot_product(vector1: list, vector2: list) -> float:
    """
    This function takes in two vector lists of ANY LENGTH, and returns their dot product

    Be sure to use for loops and lists to make this flexible for any length inputs!

    vector1 and vector2 will always be the same length

    assume vector1 and vector2 are of the form [x, y, z], where x,y,z are float values
    """
    output_value = 0
    for index in range(len(vector1)):
        output_value += vector1[index] * vector2[index]
    return output_value

def add_vectors(vector1: list, vector2: list) -> list:
    """
    This function is similar to the previous add vectors function, however, since we are working with 3D transformation
    matrices in python, we are going to have to treat vector1 and vector2 as 1x3 matrices instead of just ordinary
    vectors. That means vector1 and vector2 will be of form: [[x], [y], [z]]. This means that if you want to grab the
    second value of vector1, you would write: vector1[1][0] since the 2nd value is a list containing your desired number

    print(vector1)
    > [[0.14], [-1], [50]]

    """
    output_vector = []
    if type(vector1[0]) == list:
        for i in range(len(vector1)):
            output_vector.append([vector1[i][0] + vector2[i][0]])
        return output_vector

def matrix_multiply(matrix_a: list, matrix_b: list) -> list:
    """
    This function takes in two matrices, and returns their composition.

    Remember that to find the value of the resulting matrix at row x and column y, you must take the dot product
    between row x on MatrixA with column y on MatrixB

    I've started you out below with an empty matrix

    to add an amount to an entry in the matrix, such as the value at the 2nd row and 3rd column, write the following:

    result[1][2] += whatever_your_new_value_is_here

    hint: you will need two for loops, as well as your dot product and column functions written above!
    """
    # Create a result matrix filled with zeros
    result = [[0,0,0],
              [0,0,0],
              [0,0,0]]


    for row in range(len(matrix_a)):
        for col in range(len(matrix_b[0])):
            result[row][col] += dot_product(matrix_a[row], column(matrix_b, col))
    return result

"""
If you completed all the above functions correctly, you should be able to see and move the cube in 3D!

Complete the following functions to enable rotation of the cube too!
"""

def x_rotation(angle) -> list:
    """
    This function takes in an angle, and returns the 3D rotation matrix along the X axis

    Below is an empty matrix, fill it in so that each entry corresponds to the correct value for a rotation
    matrix along this axis of rotation!
    """
    rad_degree = angle * math.pi/180 # Convert angle to radians
    return [
    [1, 0, 0],
    [0, math.cos(rad_degree), -math.sin(rad_degree)],
    [0, math.sin(rad_degree), math.cos(rad_degree)]
    ]

def y_rotation(angle):
    """
    This function takes in an angle, and returns the 3D rotation matrix along the X axis

    Below is an empty matrix, fill it in so that each entry corresponds to the correct value for a rotation
    matrix along this axis of rotation!
    """
    radDegree = angle * math.pi/180 # Convert angle to radians
    return [
    [math.cos(radDegree), 0, math.sin(radDegree)],
    [0,1, 0],
    [-math.sin(radDegree), 0, math.cos(radDegree)]
    ]

def z_rotation(angle):
    """
    This function takes in an angle, and returns the 3D rotation matrix along the X axis

    Below is an empty matrix, fill it in so that each entry corresponds to the correct value for a rotation
    matrix along this axis of rotation!
    """
    radDegree = angle * math.pi/180 # Convert angle to radians
    return [
    [math.cos(radDegree), -math.sin(radDegree), 0],
    [math.sin(radDegree), math.cos(radDegree), 0],
    [0, 0, 1]
    ]



"""
The following is code that determines the positions of the cube's vertices in space. No need to touch this.
"""
# Size of the cube
size = 100
# Define the cube's vertices
points = [
  [[-size / 2], [size / 2], [size / 2]],
  [[size / 2], [size / 2], [size / 2]],
  [[size / 2], [-size / 2], [size / 2]],
  [[-size / 2], [-size / 2], [size / 2]],

  [[-size / 2], [size / 2], [-size / 2]],
  [[size / 2], [size / 2], [-size / 2]],
  [[size / 2], [-size / 2], [-size / 2]],
  [[-size / 2], [-size / 2], [-size / 2]],
  ]

# Define the connections (edges) between vertices
connections = [
  (0, 1), (1, 2), (2, 3), (3, 0), # Front face
  (4, 5), (5, 6), (6, 7), (7, 4), # Back face
  (0, 4), (1, 5), (2, 6), (3, 7), # Edges connecting front and back
]

# Define the cube's orientation as an identity matrix
orientation = [[1,0,0],
               [0,1,0],
               [0,0,1]]

identity = [[1,0,0],
            [0,1,0],
            [0,0,1]]


points, connections = parse_obj_from_file(filename)


while running:

    x_rot = x_rotation(0)
    y_rot = y_rotation(0)
    z_rot = z_rotation(0)

    # Process player inputs.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        x_rot = x_rotation(rotation_speed)

    elif keys[pygame.K_DOWN]:
        x_rot = x_rotation(-rotation_speed)
    if keys[pygame.K_RIGHT]:
        y_rot = y_rotation(rotation_speed)

    elif keys[pygame.K_LEFT]:
        y_rot = y_rotation(-rotation_speed)

    if keys[pygame.K_w]:
        focal_length += 0.1
    elif keys[pygame.K_s]:
        focal_length += -0.1
    shift_on = False
    if keys[pygame.K_LSHIFT]:
        shift_on = True
        print("shift")

    if keys[pygame.K_r]:
        translation_vector = [[0], [0], [0]]
        orientation = identity

    move_speed = 0.1
    if keys[pygame.K_z]:
        translation_vector = add_vectors(translation_vector, matrix_multiply(orientation, [[0], [0], [move_speed]]))


    if keys[pygame.K_y]:
        translation_vector = add_vectors(translation_vector, matrix_multiply(orientation, [[0], [move_speed], [0]]))

    if keys[pygame.K_x]:
        translation_vector = add_vectors(translation_vector, matrix_multiply(orientation, [[move_speed], [0], [0]]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit



    screen.fill(black)

    # Create rotations around the X, Y, and Z axis
    rotationStep = matrix_multiply(x_rot, y_rot)
    rotationStep = matrix_multiply(rotationStep, z_rot)

    # Update the cube's orientation to apply the rotation steps
    orientation = matrix_multiply(rotationStep, orientation)

    # List to store the rotated and projected points
    rotatedPoints = []
    points_translated = []
    for point in points:
        points_translated.append(add_vectors(point, translation_vector))

    # Rotate and project each point (vertex) in 3D space
    for point in points:
        # Apply X, Y, and Z rotations
        rotated = matrix_multiply(orientation, point)
        rotated = add_vectors(rotated, translation_vector)
        # Calculate perspective projection
        z = focal_length / (focal_length - rotated[2][0] + 0.0001)
        perspective = [
          [z, 0, 0],
          [0, z, 0],
        ]
        projected = matrix_multiply(perspective, rotated) # Apply perspective projection
        rotatedPoints.append(projected) # Save the projected point

        # Displace points to be in the middle of the screen
        pointX = int(projected[0][0] + width//2)
        pointY = int(projected[1][0] + height//2)

        # Draw the point (vertex) as a small circle
        pygame.draw.circle(screen, white, (pointX, pointY), 1)

    # Draw edges between the points
    for start, end in connections:
        startPoint = rotatedPoints[start] # Start vertex
        endPoint = rotatedPoints[end] # End vertex

        # Displace points to be in the middle of the screen
        startX = int(startPoint[0][0] + width//2)
        startY = int(startPoint[1][0] + height//2)
        endX = int(endPoint[0][0] + width//2)
        endY = int(endPoint[1][0] + height//2)

        # Draw the edge as a line
        pygame.draw.line(screen, white, (startX, startY), (endX, endY), 1)

    position_text = "position: "
    for value in translation_vector:
        position_text = position_text + str(round(value[0], 0)) + ", "
    position_surface = my_font.render(position_text,False, (255, 255, 255))
    screen.blit(position_surface, (200, 32))

    controls_text = "W: +focal length, S: -focal length"
    current_focal_length = "focal length: " + str(round(focal_length, 0))
    move_text = "XYZ: move, Arrow Keys: rotate, R: reset transformations"

    focal_length_surface = my_font.render(current_focal_length, False, (255, 255, 255))
    screen.blit(focal_length_surface, (200, 64))

    controls_surface = my_font.render(controls_text, False, (255, 255, 255))
    move_surface = my_font.render(move_text, False, (255, 255, 255))
    screen.blit(controls_surface, (20, 500))
    screen.blit(move_surface, (20, 540))



    pygame.display.flip()

pygame.quit()