import os
import pygame

# Store the base asset path as a constant to avoid repetition and make path updates easier
# This also makes the code more maintainable as you only need to change the path in one place
BasePath = 'Media/Assets/'

def loadImage(path):
    # Load a single image and prepare it for game use
    # Convert the image for faster rendering - critical for performance in pygame
    img = pygame.image.load(BasePath + path).convert_alpha()
    
    # Set black as the transparent color (0,0,0)
    # This ensures sprites with black backgrounds display correctly in the game
    img.set_colorkey((0, 0, 0))
    return img

def loadImages(path):
    # Load multiple images from a directory into a list
    # Useful for animations or sprite collections that need to be loaded together
    images = []
    
    # os.listdir returns files in arbitrary order, so we sort them
    # This ensures animations or sprite sequences load in the correct order
    # particularly important for numbered sprite sequences (e.g., walk1.png, walk2.png)
    for imgName in sorted(os.listdir(BasePath + path)):
        # Construct the full path and load each image
        # The '/' joining is used to maintain proper path format across different operating systems
        images.append(loadImage(path + '/' + imgName))
    return images


class Animation:
    def __init__(self, images, imgDuration=5, loop=True):
        # A list of every image that pretains to a specific animation.
        self.images = images
        # The number of frames between each image in an animation.
        self.imgDuration = imgDuration

        # Checks if looping through the animation is needed.
        self.loop = loop
        self.false = False
        # Frame of the game not the individual animation.
        self.frame = 0

    # This method returns a copy of the Animation object. 
    # However, the list of images is a shallow copy meaning that 
    # there is only one single list of images. If the list is changed for one 
    # instance of the Animation then all of the other instances of the Animation object's list will
    # be altered. In the context of animation, this is useful because it prevents duplicate images
    # that will take up unnecessary storage. 
    def copy(self):
        return Animation(self.images, self.imgDuration, self.loop)
    
    def update(self):
        if self.loop:

            # Creates a looping counter for animating through images.
            # Each image shows for imgDuration frames before moving to next image.
            # When reaching the end (imgDuration * total images), loops back to 0.
            # Example: With 3 images and imgDuration of 5:
            # Frames 0-4: first image, 5-9: second image, 10-14: third image, 15: loops to 0
            # because 15 % (self.imgDuration * len(self.images)) =>
            # 15 % (5 * 3) => 15 % 15 = 0
            self.frame = (self.frame + 1) % (self.imgDuration * len(self.images))

        else:
            # Example: With 3 images and imgDuration of 5:
            # Frames 0-4: first image, 5-9: second image, 10-14: third image
            # If did not do (self.imgDuration * len(self.images) - 1, 
            # the frame would eventually be set to 15 which does not have a 
            # corresponding image.
            self.frame = min(self.frame + 1, (self.imgDuration * len(self.images) - 1))

            # If aniamation has gone through the last frame of the images,
            # set the animation cycle to done.
            if self.frame >= self.imgDuration * len(self.images):
                self.done = True    

    # This method returns the a specific frame of the animation based off of 
    # the frame of the game. 
    def getFrame(self):
        return self.images[int(self.frame / self.imgDuration)]