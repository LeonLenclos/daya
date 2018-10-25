import random
from sprite import Sprite
import os


CHANCES_TO_DO_IDDLE_MOVE = 0.08
FATNESS_LIMIT = -500
THINNES_LIMIT = 500
DEATH_POS_LIMIT = 1000
DEATH_NEG_LIMIT = -1000
START_HUNGER = 950
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
        self.hunger = START_HUNGER
        self.load_sprite()
    
    def load_sprite(self):
        self.current_sprite = self.sprites[os.path.join(self.weight, self.state)]


    def update(self):

        self.hunger += 1

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
        
        current_index = self.current_sprite.index
        self.load_sprite()

        if self.state == "eat":
            self.current_sprite.index = current_index

        try:
            self.current_sprite.update()
        except Sprite.EndOfAnimation:
            self.current_sprite.reset()
            if self.alive:
                self.state = "base"
            else:
                self.state = "dead"
           # self.update()

    def draw(self, surface):

        self.current_sprite.draw(surface, (0,0))

    def eat(self):

        if self.state == "eat" and self.current_sprite.index == EAT_FRAME:
            self.hunger -= FOOD_WEIGHT
            return True
        elif self.state == "base":
            self.state = "eat"
        
        return False
        