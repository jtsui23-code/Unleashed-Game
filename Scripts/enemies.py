import pygame
from character import Character, skill

class Enemy(Character):

    def __init__(self, game, pos, size):
        super().__init__(game, 'Enemy', pos, size)

        self.name = ' '

        self.attackstat = 0.8
        self.sp = 100

        # How much the attack 
        self.attackDmg = 10
        self.maxHp = 100
        self.currentHp = self.maxHp
        #self.skillCooldown = []
        self.skills = [skill, skill]

        self.attackFlip = False

    def takeDmg(self, amount):

        # Reduces the current hp of enemy by amount of inflicted attack.
        # Have to use max(0, ...) or the enemy's health 
        # will eventually become negative.
        self.currentHp = max(0, self.currentHp - amount)

        if self.currentHp <= 0:
            print(self.name + " has been defeated.")
       
    def heal(self, amount):

        # Increases the current hp of enemy by amount of healing.
        # Have to use min(eslf.maxHp, ...) or the enemy's health 
        # will eventually overcap.
        self.currentHp = min(self.maxHp, self.currentHp + amount)

    def basicAttack(self):
        self.attackDmg = 10 * self.attackstat
        return self.attackDmg
    
    def TakeTurn(self):
        #if skill 1 of cooldown and has enough sp use it
        if self.skills[0].cooldown == 0 and self.sp > self.skills[0].sp:
            self.sp -= self.skills[0].sp # lose sp based on skill
            return self.skills[0].use

        #if skill 2 on cooldown and skill 2 of cooldown use it
        elif self.skills[1].cooldown == 0 and self.sp > self.skills[1].sp:
            self.sp -= self.skills[1].sp # lose sp based on skill
            return self.skills[1].use

        #if either skill is about to be off cooldown then gaurd
        elif self.skills[0].cooldown == 1 or self.skills[1].cooldown == 1:
            self.gaurd()
            return 0
    
        else:
            return self.basicAttack()
        
#    def skillAttack(self):
#        self.attackDmg = 30 * self.attacksta
#        return self.attackDmg

#    def skillAttack2(self):
#        self.attackDmg = 50 * self.attackstat
#        return self.attackDmg        


    
class RSoldier(Enemy):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)

        self.name = 'Revived Soldier'

        self.attackstat = 0.8
        self.sp = 100

        # How much the attack 
        self.attackDmg = 10
        self.maxHp = 100
        self.currentHp = self.maxHp
        self.skillCooldown = []

        # Skills
        BSlash = skill('Big Slash', 20, 3, 10)
        SBash = skill('Shield Bash', 10, 2, 5)

        self.skills = [BSlash, SBash]
        self.attackFlip = False

