import random
from sprite import Sprite, EndOfAnimation
import os


CHANCES_TO_DO_IDDLE_MOVE = 0.1 #0.08
FATNESS_LIMIT = -500
THINNES_LIMIT = 500
DEATH_POS_LIMIT = 1000
DEATH_NEG_LIMIT = -1000
START_HUNGER =  -900
FOOD_WEIGHT = 100
EAT_FRAME = 11

class Bird():
    """The bird, main character of the game"""


    def __init__(self):

        self.sprites = {}
        for weight in "thin", "normal", "fat":
            for state in "base", "iddle", "eat", "dead":
                path = os.path.join(weight, state)
                self.sprites[path] = Sprite(path)

        self.weight = "normal"
        self.state = "base"
        self.alive = True
        self.eating = False
        self.hunger = START_HUNGER
        self.current_sprite = self.sprites[self.get_state()]
        
    def get_state(self):
        return os.path.join(self.weight, self.state)        

    def update(self):

        print(self.state)
        if self.alive:
            self.hunger += 1



        try:
            self.current_sprite.update()
        except EndOfAnimation:



            if self.hunger > DEATH_POS_LIMIT or self.hunger < DEATH_NEG_LIMIT:
                self.alive = False
            elif self.hunger > THINNES_LIMIT:
                self.weight = "thin"
            elif self.hunger < FATNESS_LIMIT:
                self.weight = "fat"
            else:
                self.weight = "normal"

            if self.state == "base":
                if random.random() < CHANCES_TO_DO_IDDLE_MOVE:
                    self.state = "iddle"
            else :
                self.state = "base"
            print(self.state)

            if self.eating:
                self.state = "eat"

            if not self.alive:
                self.state = "dead"

            next_sprite = self.sprites[self.get_state()]
            self.current_sprite = next_sprite
            self.current_sprite.reset()
            self.current_sprite.update()

                

            # if self.state == "eat":
                # next_sprite.index = self.current_sprite.index




           # self.update()

    def draw(self, surface):

        self.current_sprite.draw(surface, (0,0))

    def eat(self):
        if self.state == "eat" and self.current_sprite.index == EAT_FRAME:
            self.hunger -= FOOD_WEIGHT
            self.eating = False
            print("!!!")
            return True
        elif not self.eating:
            self.eating = True
        
        return False
        
