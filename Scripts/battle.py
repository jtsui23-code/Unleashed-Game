import pygame
from enemies import Enemy
from character import Player, Character, TakeDown
from Scripts.ui import TextBox



class Battle:
    def __init__(self, player, enemy):
        self.player = player  # Instance of Player
        self.enemy = enemy    # Instance of Enemy
        self.won = False

    def guard(self, entity):
        # Print a message indicating the entity is guarding
        print(f"{entity.name} guarded!")

    def GameOver(self):
        # Handle game over logic
        print("Game Over!")

    def fight(self):
        # Main combat loop
        while not self.won:
            # Player and Enemy take their turns and store choices in variables
            pmov = self.player.TakeTurn()
            emov = self.enemy.TakeTurn()

            # Ensure pmov and emov are valid numbers
            if pmov is None:
                pmov = 0  # Default to 0 if pmov is None
            if emov is None:
                emov = 0  # Default to 0 if emov is None

            # If guarded, TakeTurn will return 0
            if emov == 0:
                self.guard(self.enemy)  # Prints 'name' guarded and restarts loop
                continue

            if pmov == 0:
                self.guard(self.player)
                continue

            # If defender dies, TakeDmg will return 0
            if self.enemy.TakeDmg(pmov) == 0:  # If enemy dies, break loop
                self.won = True
                break
            else:
                if self.player.TakeDmg(emov) == 0:  # If player dies, call game over
                    self.GameOver()
                    break

            # Reduce cooldowns for all skills
            for skill in self.player.skills:
                skill.reduceCD()
            for skill in self.enemy.skills:
                skill.reduceCD()

        return 0