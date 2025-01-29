import pygame
from character import Player
from enemies import Enemy



class Battle:
    def __init__(self, player, enemy):
        
        self.player = player
        self.enemy = enemy
        self.won = False

    def gaurd(self, entity):
        pass

    def GameOver(self):
        pass

    def fight(self):

        # Main combat loop
        while self.won == False:
                
            # Player and Enemy take their turns and store choices in variables   
            pmov = self.player.TakeTurn
            emov = self.enemy.TakeTurn
            
            if emov == 0: # If guarded TakeTurn will return 0
                self.gaurd(self.enemy)
                # print "enemy gaurded"

            if pmov == 0: 
                self.gaurd(self.player)
                # print "you gaurded"

            # If defender dies TakeDmg will return 0
            # TakeDmg will change defender's HP based on amount passed in and return 0 if defender dies

            if self.enemy.TakeDmg(pmov) == 0: # If enemy dies break loop
                self.won = True  
                break
            else:
                if self.player.TakeDmg(emov) == 0: # If player dies call game over
                    self.GameOver
                        
