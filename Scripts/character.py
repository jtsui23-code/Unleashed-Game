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
        self.maxSp = 100
        self.attackstat = 0.8

        # Skill points will be the unit expensed when using a skill.
        self.currentSp = self.maxSp

        # Need this incase player is fighting from the left or right side.
        self.attackFlip = False
        self.attackDmg = 10
        self.infectRate = 0.5

        self.maxHp = 80
        self.currentHp = self.maxHp
        self.skillCooldowns = []

    def takeDmg(self, amount):

        # Reduces the current hp of player by amount of inflicted attack.
        # Have to use max(0, ...) or the player's health 
        # will eventually become negative.
        self.currentHp = max(0, self.currentHp - amount)

        if self.currentHp <= 0:
            print("Player has been defeated.")
       
    def heal(self, amount):

        # Increases the current hp of player by amount of healing.
        # Have to use min(eslf.maxHp, ...) or the player's health 
        # will eventually overcap.
        self.currentHp = min(self.maxHp, self.currentHp + amount)


    

        