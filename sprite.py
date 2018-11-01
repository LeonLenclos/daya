import pygame
import os
import random

class EndOfAnimation(Exception):
    pass

class Sprite(pygame.sprite.Sprite):
    
    
    def __init__(self, name):
        """Init the Sprite
        Load all images for all variations of the animation.
        The images are loaded from the sprite/ directory.
        `name` is the path of the sprite/ subdirectory where to look up.
        this directoy must contain a directory for each variation.
        """
        super(Sprite, self).__init__()
        
        self.name = name
        
        # list of list containing all variations of the animation
        self.frames = []

        # loop threw variation directories
        sprite_path = os.path.join('sprite', name)
        for variation in sorted(os.listdir(sprite_path)):
            variation_path = os.path.join(sprite_path, variation)
            # loop threw image files
            images = []
            for img in sorted(os.listdir(variation_path)):
                image_path = os.path.join(variation_path, img)
                images.append(pygame.image.load(image_path))
            self.frames.append(images)

        self.reset()

    def reset(self):
        """choose a random variation index and rst the index to 0"""
        self.variation_index = random.randint(0, len(self.frames)-1)
        self.index = 0
        self.load_frm()


    def load_frm(self):
        """Load the current frame in self.frm
        If index is greater than the animation length, raise EndOfAnimation"""
        if self.index >= len(self.frames[self.variation_index]):
            raise EndOfAnimation()
        self.frm = self.frames[self.variation_index][self.index]

    def update(self):
        """Load the frm and increment the index"""
        self.load_frm()
        self.index += 1


    def draw(self, surface, pos=(0, 0)):
        """blit the frm on a surface"""
        surface.blit(self.frm, pos)
