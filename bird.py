import random
from sprite import Sprite

class Bird():
    """The bird, main character of the game"""


    def __init__(self):

        self.sprites = {}
        self.sprites["base"] = Sprite("base")
        self.sprites["iddle"] = Sprite("iddle")
        self.sprites["eat"] = Sprite("eat")

        self.state = "base"

    def update(self):

        if self.state == "base":
            if random.random() > .95:
                self.state = "iddle"

        self.current_sprite = self.sprites[self.state]

        try:
            self.current_sprite.update()
        except Sprite.EndOfAnimation:
            self.current_sprite.reset()
            self.state = "base"
            self.update()

    def draw(self, surface):

        self.current_sprite.draw(surface, (0,0))

    def eat(self):

        if self.state == "eat" and self.current_sprite.index == 11:
            return True
        elif self.state == "base":
            self.state = "eat"
        
        return False
        