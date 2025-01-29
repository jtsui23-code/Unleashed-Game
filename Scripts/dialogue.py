import pygame
from character import Character
from enemies import Enemy, RSoldier, Orc, Rat, FFaith, Ghoul, Carrion, wiz
from ui import TextBox, Text
import sys
import os
import textwrap

class Dialogue(Character):

    def __init__(self, player, enemy):
        
        self.player = player
        self.enemy = enemy

    def yap(self, text):
        self.text = text
        self.text = TextBox(200, 75, 900, 600, text)
        self.text.print
    


class PlayerDialogue(Dialogue):
    def __init__(self, player, enemy):
        super().__init__(player, enemy)

    def yap(self, text):
        self.text = text
        self.text = TextBox(200, 75, 900, 600, text)
        self.text.print

class EnemyDialogue(Dialogue):
    def __init__(self, player, enemy):
        super().__init__(player, enemy)

    def yap(self, text):
        if self.enemy.currentHp > 0:
            self.text = text
            self.text = TextBox(200, 75, 900, 600, text)
            self.text.print
