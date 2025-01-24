import pygame
from character import Character

class Enemy(Character):

    def __init__(self, game, pos, size):
        super().__init__(game, 'Enemy', pos, size)


        self.attackstat = 0.8

        # How much the attack 
        self.attackDmg = 10
        self.maxHp = 100
        self.currentHp = self.maxHp
        self.skillCooldown = []

        self.attackFlip = False

    def takeDmg(self, amount):

        # Reduces the current hp of enemy by amount of inflicted attack.
        # Have to use max(0, ...) or the enemy's health 
        # will eventually become negative.
        self.currentHp = max(0, self.currentHp - amount)

        if self.currentHp <= 0:
            print("Enemy has been defeated.")
       
    def heal(self, amount):

        # Increases the current hp of enemy by amount of healing.
        # Have to use min(eslf.maxHp, ...) or the enemy's health 
        # will eventually overcap.
        self.currentHp = min(self.maxHp, self.currentHp + amount)

    def basicAttack(self):
        self.attackDmg = 10 * self.attackstat
        return self.attackDmg
    
    def skillAttack(self):
        self.attackDmg = 30 * self.attackstat
        return self.attackDmg

    def skillAttack2(self):
        self.attackDmg = 50 * self.attackstat
        return self.attackDmg        


    
