import unittest

#A tuple is a data type in Python that is similar to a vector
my_tuple = ("hello", "world", 5, 3.14159, (0,1,2,3)) #they can store any data type
#unlike Lists, you cannot modify the values of a tuple after it is created
#Lists use up more memory because of this, so tuples can be more efficient to use in complex processes

printing_tuple = ("first", "second", "third")

print(printing_tuple[0]) #this prints "first", tuples use the same indexing as lists, they start at 0

print(printing_tuple[-1]) #this prints "third", since negative indices go to the end of the tuple

for value in printing_tuple: #you can iterate over tuples too!
    print(value)

"""
Classwork

Fill out the following functions based on each of their descriptions, they all perform different vector math operations
"""

def dot_product(vector1: tuple, vector2: tuple) -> float:
    """
    This function takes in two tuples, and outputs their dot product as if they were vectors.

    First I will break up the first vector into it's x and y components
    Then I will break up the 2nd vector into it's x and y components

    Then I will multiply the first components
    Then I will multiply the second components

    Then I will add them all together, and return a float (real number)
    """
    v1_x = vector1[0]
    v1_y = vector1[1]

    v2_x = vector2[0]
    v2_y = vector2[1]

    return v1_x * v2_y + v1_x * v2_y

def add_vectors(vector1: tuple, vector2: tuple) -> tuple:
    """
    This function takes in two tuples, and outputs their sum as if they were vectors
    """
    # fill in your code here! be sure to return the correct type!


def scale_vector(scalar: float, vector: tuple) -> tuple:
    """
    This function takes in a float value and a tuple. It then returns a tuple that has each of its components scaled
    by the scalar amount (multiplied)

    scale_vector(3, (1,1)) -> (3,3)
    """
    # fill in your code here! be sure to return the correct type!

def length(vector: tuple) -> float:
    """
    This function takes in tuple, and returns the length of the corresponding vector.
    Be sure to use Pythagoras formula!

    length((1,1)) = sqrt(2)
    length((1,0)) = 1
    """
    # fill in your code here! be sure to return the correct type!

def normalize(vector: tuple) -> tuple:
    """
    This function takes a tuple, finds its length, and scales it by 1/its length

    Hint: Use the length function and the scale_vector function here!
    """


#Below is some testing code, which will run every time you run your code.
#If any of your functions are incorrectly implemented, some of the tests will fail
#If you are having trouble figuring out why a test is failing, let me know and I can help you!
class TestVectorMath(unittest.TestCase):

    def test_dot_product(self):

        v1 = (0,1)
        v2 = (1,0)
        v3 = (1,1)
        v4 = (4,4)
        self.assertEqual(dot_product(v1, v2), 0)

    def test_dot_product_non_orthogonal(self):
        v1 = (0, 1)
        v2 = (1, 0)
        v3 = (1, 1)
        v4 = (4, 4)
        self.assertEqual(dot_product(v3, v4), 8)

    def test_add_vectors(self):
        v3 = (1, 1)
        v4 = (4, 4)
        self.assertEqual(add_vectors(v3, v4), (5,5))

    def test_scale_vector(self):
        v = -0.5
        v4 = (4, 4)
        self.assertEqual(scale_vector(v, v4), (-2,-2))

    def test_length(self):
        self.assertEqual(length((3,4)), 5)

    def test_length_negative(self):
        self.assertEqual(length((3,-4)), 5)

    def test_normalize(self):
        self.assertEqual(normalize((1000,0)), (1,0))

    def test_normalize2(self):
        self.assertEqual(normalize((-(2 ** 0.5)/2, -(2 ** 0.5)/2)), (-(2 ** 0.5)/2, -(2 ** 0.5)/2))

if __name__ == '__main__':
    unittest.main()