import functools
import re

class Animal(): 
    def __init__(self):
        self._number_of_hands = 0
        self._number_of_legs = 4
    def look(self):
        return f"Number of hands: {self._number_of_hands}, Number of legs: {self._legs}"

class Feline(Animal):
    def get_characteristic(self):
        return "Felines belong to the cat family"
    def look(self):
        return super().look() + "\n" + self.get_characteristic()

class Tiger(Feline):
    def get_characteristic(self):
        return "Felines belong to the cat family\nTigers can roar and are lethal predators"

class Canine(Animal):
    def get_characteristic(self):
        return "Canines belong to the dog family"
    def look(self):
        return super().look() + "\n" + self.get_characteristic()

class Wolf(Canine):
    def get_characteristic(self):
        return "Canines belong to the dog family\nWolves hunt in packs and have a leader"

class Bird():
    def __init__(self):
        self._number_of_wings = 2
        self._number_of_legs = 2
    def look(self):
       return f"Number of wings: {self._number_of_wings}, Number of legs: {self._number_of_legs}"

class zoo():
    def __init__(self):
        self.list_of_animals = []
        self.list_of_birds = []

    def add(self, creature):
        if isinstance(creature, Bird):
            if len(self.list_of_birds) < 1:
                self.list_of_birds.append(creature)
                print("Added bird successfully")
            else:
                print("Zoo full for birds")
        elif isinstance(creature, Animal):
            if len(self.list_of_animals) < 2:
                self.list_of_animals.append(creature)
                print("Added animal successfully")
            else:
                print("Zoo full for animals")
        else:
            raise TypeError("Not an animal or bird")

    def find_tiger(self):
        for a in self.list_of_animals:
            if isinstance(a, Tiger):
                print("\n" + a.look())
                return
        print("No Tiger found")

    def looking(self):
        creature_list = self.list_of_animals + self.list_of_birds
        if not creature_list: return
        prod = functools.reduce(lambda acc, ele: acc + "\n\n" + ele.look(), creature_list, "")
        print(prod.strip())

# --- Testing the code ---
my_zoo = zoo()
my_zoo.add(Tiger())
my_zoo.add(Wolf())
my_zoo.looking()
