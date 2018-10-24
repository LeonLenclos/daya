import pygame
import os
import random

class Sprite(pygame.sprite.Sprite):
    
    class EndOfAnimation(Exception):
        pass
    
    def __init__(self, name):

        super(Sprite, self).__init__()
        
        def load_image(name):
            image = pygame.image.load(name)
            return image

        self.variations = []

        for images_set in sorted(os.listdir(os.path.join('sprite', name))):
            self.variations.append([])
            for image in sorted(os.listdir(os.path.join('sprite', name, images_set))):
                file_name = os.path.join('sprite', name, images_set, image)
                self.variations[int(images_set)].append(load_image(file_name))

        self.reset()

    def reset(self):


        self.frames = random.choice(self.variations)
        self.index = 0

    def update(self):
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''

        try:
            self.frm = self.frames[self.index]
        except IndexError:
            raise self.EndOfAnimation()

        self.index += 1


    def draw(self, surface, pos=(0, 0)):
        surface.blit(self.frm, pos)
