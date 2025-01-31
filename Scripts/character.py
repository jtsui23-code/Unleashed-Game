import pygame
import math
from Scripts.ui import TextBox, Text, Button
from Scripts.util import loadImage

class skill:
    def __init__(self, name, dmg, cooldown, cost):
        self.name = name
        self.damage = dmg
        self.cooldown = cooldown
        self.currentCD = 0
        self.sp = cost
        self.text = Text(200, 75, 900, 600, name + '!')

    def use(self):
        self.text.print # Prints message declaring skill
        self.currentCD = self.cooldown
        return self.damage
    
    def cooldown(self):
        return self.currentCD

    def reduceCD(self):
        # If Cooldown is more than 0 it is reduced,
        #  if it is 0 the function does nothing
        if self.currentCD > 0:
            self.currentCD - 1


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
        self.name = 'You'
        self.gold = 0

        self.sprite = pygame.transform.scale(loadImage('/enemies/2.jpg').convert_alpha(), (100, 100))

        # Skill points will be the unit expensed when using a skill.
        self.currentSp = self.maxSp

        # Need this incase player is fighting from the left or right side.
        self.attackFlip = False
        self.attackDmg = 10
        self.infectRate = 0.5

        self.maxHp = 80
        self.currentHp = self.maxHp
        Pari = skill('Parasidic Rage', 30, 3, 20)
        BlankSkill1 = skill('', 0, 0, 0)
        BlankSkill2 = skill('', 0, 0, 0)

        self.Skills = [Pari, BlankSkill1, BlankSkill2]
        self.skillCooldowns = []



        self.Buttons = {
            'Box' : TextBox (200, 600, 900, 200, ''),
            'Attack' : Button(250, 550, 200, 50, 'Attack'),
            'Skills' : Button(250, 450, 200, 50, 'Skills'),
            'Gaurd' : Button(250, 350, 200, 50, 'Gaurd')
        }

        self.SkillList = {
            'Skill1' : Button(250, 550, 200, 50, self.Skills[0].name),
            'Skill2' : Button(250, 450, 200, 50, self.Skills[1].name),
            'Skill3' : Button(250, 350, 200, 50, self.Skills[2].name)
        }

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

    def basicAttack(self):
        self.attackDmg = 10 * self.attackstat
        return self.attackDmg


    # Upgrades the states of the player based on number of purchased 
    # upgrades in the shop.
    def stateUpgrade(self, state=''):
        
        if state == 'Attack':
            self.attackstat += 0.2

        if state == 'SP':
            self.maxSP += 10

        if state == 'Infection':
            self.infectRate += 0.5

    def TakeTurn(self):

        inSkills = False

        if inSkills == True:
            for event in pygame.event.get():

                # Check if the mouse button is pressed.
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Changes color of shop buttons if hovering over them.
                    for button in self.shopOptions.values():
                        button.isHovered = button.rect.collidepoint(mousePos)

                    # Checks if the left mouse button is pressed.
                    if event.button == 1:
                        mousePos = pygame.mouse.get_pos()


                        if self.Buttons['Attack'].rect.collidepoint(mousePos):
                            return self.basicAttack

                        elif self.Buttons['Skills'].rect.collidepoint(mousePos):
                            inSkills = True

                            if self.Skills[1].name == '': # If player only has 1 skill only show that button
                                if self.SkillList['Skill1'].rect.collidepoint(mousePos):
                                    return self.Skills[0].use
                                
                            else:
                                if self.SkillList['Skill1'].rect.collidepoint(mousePos):
                                    return self.Skills[0].use
                                
                                if self.SkillList['Skill2'].rect.collidepoint(mousePos):
                                    return self.Skills[1].use
                                
                                if self.SkillList['Skill3'].rect.collidepoint(mousePos):
                                    return self.Skills[2].use
                                

                        elif self.Buttons['Gaurd'].rect.collidepoint(mousePos):
                            return 0

       
    def infect(self, enemy):
        # Parasite copies enemy stats and skills
        self.Skills[1] = enemy.Skills[0]
        self.Skills[2] = enemy.Skills[1]
        self.attackDmg = enemy.attackDmg
        self.attackstat = enemy.attackstat

    def GetGold(self, enemy):
        self.gold += enemy.gold