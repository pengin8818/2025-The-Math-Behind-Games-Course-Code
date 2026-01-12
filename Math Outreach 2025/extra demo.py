class Fish:

    def __init__(self, species_input):

        self.species = species_input
        self.position_vertical = 0

    def swim_down(self, distance):
        self.position_vertical = self.position_vertical - distance

    def swim_up(self, distance):
        self.position_vertical = self.position_vertical + distance




tuna = Fish("Tuna")

print(tuna.position_vertical)

tuna.swim_up(100)

print(tuna.position_vertical)