import pygame
import math
from Scripts.ui import TextBox, Text, Button
from Scripts.util import loadImage

class skill:
    def __init__(self, name, dmg, cooldown, cost):
        self.name = name
        self.damage = dmg
        self.max_cooldown = cooldown  # Store the max cooldown
        self.currentCD = 0  # Current cooldown starts at 0
        self.sp = cost
        self.text = Text(200, 75, 900, 600, name + '!', 
                        pygame.font.Font('Media/Assets/Fonts/fantasy.ttf', 100), 
                        (255, 255, 255))

    def __str__(self):
        return f"{self.name} does {self.damage} damage and has a cooldown of {self.max_cooldown} turns. It costs {self.sp} SP to use."

    def use(self, screen=None):
        """
        Use the skill and return its damage.
        If screen is provided, draw the skill name.
        """
        if not self.is_available():
            return 0
            
        if screen:
            self.text.draw(screen)
            
        self.currentCD = self.max_cooldown  # Start the cooldown
        return self.damage
    
    def is_available(self):
        """Check if the skill is available to use"""
        return self.currentCD == 0
    
    def get_cooldown(self):
        """Get current cooldown value"""
        return self.currentCD

    def reduceCD(self):
        """Reduce cooldown by 1 if it's greater than 0"""
        if self.currentCD > 0:
            self.currentCD -= 1  # Fixed the syntax error here
    
    def get_sp_cost(self):
        """Get the SP cost of the skill"""
        return self.sp


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
    def __init__(self, game, pos, size, surface):
        super().__init__(game, "player", pos, size)

        self.attacking = False
        self.maxSp = 100
        self.sp = self.maxSp
        self.attackstat = 0.8
        self.name = 'You'
        self.gold = 0
        self.surface = surface

        self.sprite = pygame.transform.scale(loadImage('enemies/2.png').convert_alpha(), (100, 100))

        # Skill points will be the unit expensed when using a skill.
        self.currentSp = self.maxSp

        # Need this incase player is fighting from the left or right side.
        self.attackFlip = False
        self.attackDmg = 10
        self.infectRate = 0.5

        self.maxHp = 80
        self.currentHp = self.maxHp
        Pari = skill('Parasitic Rage', 30, 3, 20)

        # Blank skills to be replaced after infection
        BlankSkill1 = skill('', 0, 0, 0)
        BlankSkill2 = skill('', 0, 0, 0)

        self.Skills = [Pari, BlankSkill1, BlankSkill2]
        self.skillCooldowns = []



        # self.bottons = {
        #     # The text box is at the beginning of the map because it will be the first thing to be drawn.
        #     'Text': TextBox(200, 75, 900, 600, text=''),
        #     'Attack': Button(500, 500, 280, 50, 'Attack'),
        #     'Skill1': Button(500, 575, 280, 50, 'Skill 1'),
        #     'Skill2': Button(500, 575, 280, 50, 'Skill 2'),
        #     'Guard': Button(500, 575, 280, 50, 'Guard'),
        #     'Inventory': Button(500, 650, 280, 50, 'Inventory')
        # }

        # self.SkillList = {
        #     'Skill1' : Button(250, 550, 200, 50, self.Skills[0].name),
        #     'Skill2' : Button(250, 450, 200, 50, self.Skills[1].name),
        #     'Skill3' : Button(250, 350, 200, 50, self.Skills[2].name)
        # }

    def TakeDmg(self, amount):

        # Reduces the current hp of player by amount of inflicted attack.
        # Have to use max(0, ...) or the player's health 
        # will eventually become negative.
        self.currentHp = max(0, self.currentHp - int(amount))

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

    def drawMenu(self, menu):
        self.surface.fill((0, 0, 0))
        for option in menu.values():
            option.draw(self.surface)


    def TakeTurn(self):
        
        print(skill)    

        action_selected = False
        
        # Draw the menu
        self.drawMenu(self.bottons)

        while not action_selected:
            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.bottons['Attack'].rect.collidepoint(mousePos):
                            action_selected = True
                            return self.basicAttack
                        
                        if self.bottons['Skill1'].rect.collidepoint(mousePos):
                            action_selected = True
                            return self.Skills[0].use
                        
                        if self.bottons['Skill2'].rect.collidepoint(mousePos):
                            action_selected = True
                            return self.Skills[1].use
                        
                        if self.bottons['Guard'].rect.collidepoint(mousePos):
                            action_selected = True
                            self.guard()
                            return 0

        # Keep the game running while waiting for input
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        
        
        # If skill 1 is off cooldown and has enough SP, use it
        #if self.Skills[0].cooldown == 0 and self.sp >= self.Skills[0].sp:
        #    self.sp -= self.Skills[0].sp  # Lose SP based on skill
        #    return self.Skills[0].use  # Ensure this returns a valid damage value

        # If skill 2 is off cooldown and has enough SP, use it
        #elif self.Skills[1].cooldown == 0 and self.sp >= self.Skills[1].sp:
        #    self.sp -= self.Skills[1].sp  # Lose SP based on skill
        #    return self.Skills[1].use  # Ensure this returns a valid damage value

        # If either skill is about to be off cooldown, then guard
        #elif self.Skills[0].cooldown == 1 or self.Skills[1].cooldown == 1:
        #    return 0  # Guarding returns 0 damage

        # Otherwise, use a basic attack
        #else:
        #    return self.basicAttack()  # Ensure this returns a valid damage value

       
    def infect(self, enemy):
        # Parasite copies enemy stats and skills
        self.Skills[1] = enemy.Skills[0]
        self.Skills[2] = enemy.Skills[1]
        self.attackDmg = enemy.attackDmg
        self.attackstat = enemy.attackstat

    def GetGold(self, enemy):
        self.gold += enemy.gold