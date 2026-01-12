

class LivingCreature:

    """
    Class methods always include self as the first input of their methods. That is because they always can refer to
    themselves
    """


    def __init__(self, input_name):
        """
        This is a constructor method. Every time you create a LivingCreature, this method runs under the hood.

        Example:
        my_dog = LivingCreature("Fido")
        """

        #when we initialize an object like this, we want to have it store information about itself. Below is how we do this...
        self.name = input_name
        self.age = 0 #this variable is automatically 0, we will need a different method to change it
        #now if we create a variable my_dog = LivingCreature("Fido"), and type my_dog.name, it will return input_name
        #this is important for storing variables later

    def get_name(self):
        """
        It is standard practice to create get methods whenever there is a variable you want to get from a class a lot.
        This helps other people understand what your doing, since my_dog.name is more vague than my_dog.get_name()
        """

        return self.name

    def set_age(self, input_age):
        """
        Here we will use a method to set the current age of our LivingCreature
        """

        self.age = input_age #this method takes in a variable and sets it to whatever we need it to be


    def __str__(self):
        """
        This is how you tell python how to print out your class when you use the print() function
        """

        print(f"This {self.name} is {self.age} years old")

class Plant(LivingCreature):
    """
    This allows us to make a sub-class of LivingCreature that inherits all of the properties of its super class
    """

    def __init__(self, input_name, has_flowers):
        #since we are editing the superclass initialization method, we need to call the superclass init here
        super().__init__(input_name)
        self.has_flowers = has_flowers


