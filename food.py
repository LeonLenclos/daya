from sprite import Sprite, EndOfAnimation

class Food():
    """The food that the bird eats"""

    def __init__(self):

        self.sprite = Sprite("food")

    def update(self):

        try:
            self.sprite.update()
        except EndOfAnimation:
            pass

    def draw(self, surface, pos=(0,0)):
        self.sprite.draw(surface, pos)
