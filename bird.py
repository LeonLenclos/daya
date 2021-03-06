import random
from sprite import Sprite, EndOfAnimation
import requests

import os


CHANCES_TO_DO_IDDLE_MOVE = 0.03
FATNESS_LIMIT = -6*60*10
THINNES_LIMIT = 1000
DEATH_POS_LIMIT = 8*60*10
DEATH_NEG_LIMIT = -10000
START_HUNGER =  0
FOOD_WEIGHT = 1600
EAT_FRAME = 11

class Bird():
    """The bird, main character of the game"""
    def __init__(self):

        self.sprites = {}
        for weight in "thin", "normal", "fat":
            for state in "base", "iddle", "eat", "dead":
                path = os.path.join(weight, state)
                self.sprites[path] = Sprite(path)
        self.init()


    def init(self):
        self.weight = "normal"
        self.state = "base"
        self.alive = True
        self.eating = False
        self.hunger = START_HUNGER
        self.current_sprite = self.sprites[self.get_state()]
        self.must_dance = False
        self.dancing = False

    def get_state(self):
        return os.path.join(self.weight, self.state)        

    def dance(self):
        self.must_dance = True
        self.dancing = True


    def update(self):

        if self.alive:
            self.hunger += 1



        try:
            self.current_sprite.update()
        except EndOfAnimation:
            if self.hunger > DEATH_POS_LIMIT or self.hunger < DEATH_NEG_LIMIT:
                if self.alive:
                    try:
                        r = requests.post("http://10.0.0.10:8000/talk", json={'msg': 'dis Lucy est morte.', 'conversation_id':-1})
                    except Exception: #Ugly again !!!!!!!!!!!!!!!!!!!!!!!!! (beurk)
                        pass
                    print(r.status_code, r.reason)
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

            if self.eating:
                self.state = "eat"

            if not self.alive:
                self.state = "dead"



            # overide if dancing
            variation_index = None
            if self.dancing :
                self.weight = "normal"
                if self.must_dance:
                    self.state = "iddle"
                    variation_index = 0
                    self.must_dance = False
                elif self.state == 'iddle':
                    self.state = 'base'
                
            next_sprite = self.sprites[self.get_state()]

            self.current_sprite = next_sprite
            self.current_sprite.reset(variation_index)

            self.current_sprite.update()


            # if self.state == "eat":
                # next_sprite.index = self.current_sprite.index




           # self.update()

    def draw(self, surface, pos=(0,0)):

        self.current_sprite.draw(surface, pos)

    def eat(self):
        if self.state == "eat" and self.current_sprite.index == EAT_FRAME:
            self.hunger -= FOOD_WEIGHT
            self.eating = False
            return True
        elif not self.eating:
            self.eating = True
        
        return False
        
