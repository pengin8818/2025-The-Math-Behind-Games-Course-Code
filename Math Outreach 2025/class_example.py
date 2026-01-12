class Animal:

    def __init__(self, name, age, weight):

        self.name = name
        self.age = age
        self.weight = weight

    def rename(self, new_name):
        self.name = new_name

    def grow(self, years, weight):
        self.age = self.age + years
        self.weight = self.weight + weight

    def __str__(self):

        return f"This animal's name is {self.name}, it is {self.age} years old and weighs {self.weight} kilos."


example_animal = Animal("Bonobo", 3, 50)

print(example_animal)
