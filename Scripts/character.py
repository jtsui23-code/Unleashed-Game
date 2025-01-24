import pygame
import math

class Character:

    def __init__(self, game, characterType, pos, size):
        self.game = game
        self.characterType = characterType
        self.pos = list(pos)
        self.size = size

        self.flip = False

    def rect(self):
        # Creates a pygame Rect for collision detection because collision cannot 
        # be detected for images
        # Separated into method to ensure rect always matches current position.
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
class Player(Character):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)

        self.attacking = False
        
       

    

        