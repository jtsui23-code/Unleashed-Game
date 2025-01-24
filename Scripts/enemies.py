import pygame
from character import Character

class Enemy(Character):

    def __init__(self, game, pos, size):
        super().__init__(game, 'Enemy', pos, size)

        self.attackDmg = 10
        self.maxHp = 100
        self.currentHp = self.maxHp
        self.skillCooldown = []
        
        self.attackFlip = False