import pygame
from character import Player
from enemies import Enemy
from ui import TextBox



class Battle:
    def __init__(self, player, enemy):
        
        self.player = player
        self.enemy = enemy
        self.won = False

    def gaurd(self, entity):
        text = TextBox(200, 600, 900, 200, text= entity.name + ' gaurded!')

    def GameOver(self):
        pass

    def fight(self):

        # Main combat loop
        while self.won == False:
                
            # Player and Enemy take their turns and store choices in variables   
            pmov = self.player.TakeTurn
            emov = self.enemy.TakeTurn

            # If guarded TakeTurn will return 0
            if emov == 0: 
                self.gaurd(self.enemy) # Prints 'name' gaurded and restarts
                continue               # loop before damage is done

            if pmov == 0: 
                self.gaurd(self.player)
                continue

            # If defender dies TakeDmg will return 0
            # TakeDmg will change defender's HP based on amount passed in and return 0 if defender dies

            if self.enemy.TakeDmg(pmov) == 0: # If enemy dies break loop
                self.won = True  
                break
            else:
                if self.player.TakeDmg(emov) == 0: # If player dies call game over
                    self.GameOver
                    break
            
            for x in self.player.skills:
                self.player.skills[x].reduceCD
                                                    # Reduce Cooldowns for all skills
            for x in self.enemy.skills:
                self.enemy.skills[x].reduceCD

        return 0