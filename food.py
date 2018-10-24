from sprite import Sprite

class Food():
    """The food that the bird eats"""

    def __init__(self):

        self.sprite = Sprite("food")

    def update(self):

        try:
            self.sprite.update()
        except Sprite.EndOfAnimation:
            pass

    def draw(self, surface):
        self.sprite.draw(surface, (0,0))
