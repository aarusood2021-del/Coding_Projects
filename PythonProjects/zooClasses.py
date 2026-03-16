import functools
from functools import reduce
import re
class zoo():
    def __init__(self):
        global list_of_animals
        list_of_animals = []
        global list_of_birds 
        list_of_birds = []
    def add(self,creature):
        if not isinstance(creature,Animal) and not isinstance(creature,Bird):
            raise TypeError("The argument is not an animal or bird")
        try:
            if isinstance(creature,Bird):
                if len(list_of_birds) < 1:
                    list_of_birds.append(creature)
                else:
                    print("Zoo full for birds")
            else:
                if len(list_of_animals) < 2:
                    list_of_animals.append(creature)
                else:
                    print("Zoo full for animals")
        except NameError:
            print(" That is not an animal or bird")
        else:
            print("Added successfully")
        Tiger = ['Tiger']
        y = list(filter(lambda x: (x in Tiger), list_of_animals))
    def find_tiger(self):
        x = re.search('^[a-zA-Z]+ $',str(list_of_animals))
        search_for_tiger = lambda t: re.search('Tiger', t)
        lst = list(filter(search_for_tiger, str(list_of_animals)))
        print("\n"+'''Number of hands: 0, Number of legs: 4
Felines belong to the cat family
Tigers can roar and are lethal predators''')
    def find_canine(self):
        find_canine = list(filter(lambda a: isinstance(a,Canine), list_of_animals))
        print("\n"+'''Number of hands: 0, Number of legs: 4
Canines belong to the dog family
Wolves hunt in packs and have a leader''')
    @staticmethod
    def looking():
        creature_list = list(list_of_animals+list_of_birds)
        prod = functools.reduce(lambda acc, ele: "\n"+acc+"\n"+"\n"+ele, list(map(lambda a:a.look(),creature_list)))
        print(prod)
        
class Animal(): 
    def __init__(self):
        self.__number_of_hands = 0
        self.__number_of_legs = 4
    def look(self):
        return "Number of hands: {hands}, Number of legs: {legs}".format(hands = self.__number_of_hands, legs = self.__number_of_legs)
   
class Feline(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.__characteristic = "Felines belong to the cat family" 
    def get_characteristic(self):
        return self.__characteristic
    def look(self):
        return super().look() + "\n" + self.get_characteristic()
    
class Tiger(Feline):
    def __init__(self):
        Animal.__init__(self)
        self.__characteristic1 = "Felines belong to the cat family"
        self.__characteristic2 = "Tigers can roar and are lethal predators"
    def get_characteristic(self):
        return self.__characteristic1 + "\n" + self.__characteristic2
    def look(self):
        return super().look() 
    
class Wildcat(Feline):
    def __init__(self):
        Animal.__init__(self)
        self.__characteristic1 = "Felines belong to the cat family"
        self.__characteristic2 = 'Wild cats can climb trees'
    def get_characteristic(self):
        return self.__characteristic1 + "\n" + self.__characteristic2
    def look(self):
        return super().look() 
    
class Canine(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.__characteristic = 'Canines belong to the dog family'
    def get_characteristic(self):
        return self.__characteristic
    def look(self):
        return super().look() + "\n" +  self.get_characteristic()
    
class Wolf(Canine):
    def __init__(self):
        Animal.__init__(self)
        self.__characteristic1 = 'Canines belong to the dog family'
        self.__characteristic2 = 'Wolves hunt in packs and have a leader' 
    def get_characteristic(self):
        return self.__characteristic1 + "\n" + self.__characteristic2
    def look(self):
        return super().look() 

class Bird():
    def __init__(self):
        self.__number_of_wings = 2
        self.__number_of_legs = 2
    def look(self):
       return "Number of wings: {wings}, Number of legs: {legs}".format(wings = self.__number_of_wings, legs = self.__number_of_legs)

class Flightbird(Bird):
    def __init__(self):
        Bird.__init__(self)
        self.__characteristic = 'Flight birds fly and hunt for food'
    def get_characteristic(self):
        return self.__characteristic
    def look(self):
        return super().look() + "\n" +  self.get_characteristic()

class Eagle(Flightbird):
    def __init__(self):
        Bird.__init__(self)
        self.__characteristic1 = "Flight birds fly and hunt for food"
        self.__characteristic2 = 'Eagles fly extremely high and can see their prey from high up in the sky' 
    def get_characteristic(self):
        return self.__characteristic1 + "\n" + self.__characteristic2
    def look(self):
        return super().look()
