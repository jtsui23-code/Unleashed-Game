import pygame
import sys
import random
from Scripts.ui import Button, Text, TextBox
from Scripts.upgrade import Slab
from Scripts.util import loadImage
from Scripts.dialogue import DialogueManager
from Scripts.allDialogues import dialogues
from Scripts.battle import Battle
from Scripts.character import Player
from Scripts.enemies import RSoldier, Orc, Rat, FFaith, Ghoul, Carrion, wiz

class Game:
    
    def __init__(self):

         # Starts up Pygame
        pygame.init()

        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption("Unleeched")

        self.screenWidth = 1280
        self.screenHeight = 720

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) ).
        self.screen = pygame.display.set_mode((self.screenWidth , self.screenHeight ))

        self.goldColor = (255, 223, 0)
        self.titleColor = (200, 50, 50)
        self.black = (0, 0, 0)

        # Tracks which enemy is being hovered over
        # 0 - firsts enemy 
        # 1 - second enemy
        self.hoveredEnemy = None

        self.turnNum = 1
        
        # Stores all of the enemies on each floor and replaces with the old ones.
        self.currentEnemy = []
        # Tracks which of the enemy the player is fighting.
        self.currentEnemyIndex = 0

        self.enemyDefeated = False

        # Tracks number of potions the player has.
        self.item = 0

        # Stores sprites of the enemies on the current floor.
        self.currentEnemyAsset = []

        # Checks if the player or enemy has guraded for defense logic.
        self.playerGuarded = False
        self.enemyGuarded = False

        # Checks if it is the enemies turn to start the enemy battle AI.
        self.isEnemeyTurn = True

        self.haveAppliedUpgrades = False

        # Tracks the current floor that the player is on for 
        # calculating coins player has earned and for swapping the self.currentEnemy
        # with the new enemies.
        self.currentFloor = 1

        # The coins the player has accumulated on their current round.
        self.currentCoin = 0

        # Stores the total of all of the coins the player has.
        self.totalCoin = 10000
        
        # Checks if either the player or enemy has used a skill
        # needed for battle dialouge.
        self.hasUsedSkill = False

        # Storing the skill's damage to display on the battle UI.
        self.skillDamage = 0

        # Storing the name of the skill to indicate what skill
        # was used on the battle UI.
        self.skillUsed = "None"
        
        # Need the duplicate for when the enemy guards since the enemy and player both
        # share self.skillUsed.
        self.skillPlayerUsed = "None"
        self.skillDialogueSet = False

        # Stores the selected button by the player.
        self.selectedOption = None

        # Flags to track if certain music are playing.
        self.intermissionMusicPlaying = False
        self.titleMusicPlaying = False
        self.battleMusicPlaying = False
        self.midBossMusicPlaying = False
        self.finalBossMusicPlaying = False

        # Stores the enemy rects to apply blinking effect onto them.
        self.enemyRect = []
        
        # Needed for the blinking effect when hovering over an enemy in the
        # infect screen.
        self.blinkTimer = 0
        self.blinkInterval = 500

        # Storing the player's and enemy's position to 
        # properly align them on the correct side of the screen no matter 
        # which enemy the player decides to infect.
        self.playerPos = (200, 100)
        self.enemyPos = (700, 100)
        self.flipSprites = False

        # Invisiblity is for the blinking effect.
        self.blinkState = True # True for visible, False for invisible

        # Create an instance of the Player class
        self.player = Player(self, (0, 0), (100, 100), self.screen)

        # Proportions for the text box used in the battle screen and game over 
        # menu. This is useful because the text box scales with any window 
        # dimensions.
        self.textX = int(self.screenWidth * (150/1280))    # 11.72% of screen width
        self.textY = int(self.screenHeight * (600/720))    # 83.33% of screen height
        self.textWidth = int(self.screenWidth * (1000/1280)) # 78.13% of screen width
        self.textHeight = int(self.screenHeight * (100/720))# 13.89% of screen height


        # stores the fonts used in the text and text box.
        self.fonts = {
            'fanta': pygame.font.Font('Media/Assets/Fonts/fantasy.ttf', 100),
            'arial': pygame.font.Font('Media/Assets/Fonts/Ariall.ttf', 50),
        }
        
        # Creating DialougeManager obect to control all of the dialouge in the game.
        self.dialogue = DialogueManager()
        
        # Loading all of the dialouages into the dialouge object.
        for key, params in dialogues.items():
            x, y, width, height, text = params
            self.dialogue.addDialogue(key, TextBox(x, y, width, height, text=text))
               
        # Stores the Buttons objects for the main menu
        self.menuState = "main"

        # Stores the Button objects for the main menu.
        self.mainMenuOptions = {
            'Title': Text(500, 200, 280, 50, 'Unleeched', self.fonts['fanta'], self.titleColor),
            'Start': Button(500, 375, 280, 50, 'Start'),
            'Shop': Button(500, 450, 280, 50, 'Shop'),
            'Exit': Button(500, 525, 280, 50, 'Exit')
        }

        # Provides preBattle options
        self.preBattle = {
            'fight': Button(500, 375, 280, 50, 'Fight'),
            'infect': Button(500, 460, 280, 50, 'Infect')
        }


        # Stores the Button objects for the battle menu.
        self.battle = {
            # The text box is at the beginning of the map because it will be the first thing to be drawn.
            'Text': TextBox(200, 100, 900, 600, text=''),
            'Attack': Button(500, 375, 280, 50, 'Attack'),
            'Skill': Button(500, 450, 280, 50, 'Skills'),
            'Guard': Button(500, 525, 280, 50, 'Guard'),
            'Inventory': Button(500, 600, 280, 50, 'Inventory'),
        }

        # Stores the Button objects for the battle menu.
        self.moves = {
            'Text': TextBox(200, 75, 900, 600, text=''),
            'Skill0' : Button(500, 400, 280, 50, self.player.Skills[0].name),
            'Skill1' : Button(500, 475, 280, 50, self.player.Skills[1].name),
            'Skill2' : Button(500, 550, 280, 50, self.player.Skills[2].name),
            'Back': Button(20, 620, 140, 50, 'Back')      
        }

        # Store instances of enemies, not class references
        self.enemies = {
            'soldier': RSoldier(self, (0, 0), (100, 100)),  # Create an instance of RSoldier
            'ghoul': Ghoul(self, (0, 0), (100, 100)),       # Create an instance of Ghoul
            'orc': Orc(self, (0, 0), (100, 100)),           # Create an instance of Orc
            'rat': Rat(self, (0, 0), (100, 100)),           # Create an instance of Rat
            'priest': FFaith(self, (0, 0), (100, 100)),     # Create an instance of FFaith
            'carrion': Carrion(self, (0, 0), (100, 100)),   # Create an instance of Carrion
            'boss': wiz(self, (0, 0), (100, 100))           # Create an instance of wiz
        }

        # Maintains and increments the numbers of upgrades purchased in
        # the shop.
        self.upgrades = {
            'Attack':0,
            'SP': 0, 
            'Infection': 0,
            'FullHeal': 0
        }
        
        # Maintains the cost of upgrade prices.
        self.cost = {
            'Attack':50,
            'SP':90,
            'Infect': 135,
            'Heal': 200
        }
        
        # Inside __init__ method of Game class:
        self.shopSlabs = {
            'Attack': Slab(275, 360, 190, 10, 5),      # Positioned above Attack button
            'Infection': Slab(675, 360, 190, 10, 3),   # Above Infection button
            'SP': Slab(475, 360, 190, 10, 5),          # Above SP button
            'FullHeal': Slab(875, 360, 190, 10, 2)      # Above Heal button
        }
        # Stores the Button objects for the shop menu.
        self.shopOptions = {
            'Box': TextBox(200, 75, 900, 600, '', (43, 44, 58, 160)),
            'Title': Text(500, 120, 280, 50, 'Upgrades', self.fonts['fanta'], self.titleColor),
            'Attack':Button(275, 380, 190,50, 'Attack'),
            'Infection': Button(675, 380, 190, 50, 'Infect Rate'),
            'SP': Button(475, 380, 190, 50, 'SP'),
            'FullHeal': Button(875, 380, 190, 50, 'Free Heal'),
            'Back': Button(20, 620, 140, 50, 'Back'),
            'AttackCost': Text(300, 435, 140, 50, str(self.cost['Attack']), self.fonts['arial'], self.goldColor),
            'SPCost': Text(500, 435, 140, 50, str(self.cost['SP']), self.fonts['arial'], self.goldColor),
            'InfectCost': Text(700, 435, 140, 50, str(self.cost['Infect']), self.fonts['arial'], self.goldColor),
            'HealCost': Text(900, 435, 140, 50, str(self.cost['Heal']), self.fonts['arial'], self.goldColor),
            'Coin': Text(530, 600, 200, 50, ('Coins: ' + str(self.totalCoin)), self.fonts['arial'], self.goldColor),

        }

        # Contains the game over menu components.
        self.gameOverMenu = {
            'GameOver': Text(500, 120, 280, 50, 'Game Over', self.fonts['fanta'], self.titleColor),
            'Coin': TextBox(self.textX , self.textY, self.textWidth, self.textHeight, text='')

        }

        # Contains the inventory menu components.
        self.inventoryMenu = {
            'Text': TextBox(200, 75, 900, 600, text=''),
            'Potion' : Button(250, 100, 200, 50, "", borderColor=self.black),
            'Back': Button(20, 620, 140, 50, 'Back'),     
        }

        
        # Maintains the game state to determine which menu to display.
        self.gameStates = {
            'main': True, 
            'shop': False, 
            'startGame':False,
            'battle': False,
            'prebattle': False,
            'intermission': False, 
            'gameOver': False,
            'itemReward': False,
            'infectMode': False,
            'displayBattle': False,
            'enemyTurn': False,
            'inventory': False,
            'gameOver': False
            
        }
        

        # Stores the text boxed used in the battle screen which indicates moves of 
        # both player and the enemy.
        self.displayBattleButtons = {
        'attack': TextBox(self.textX , self.textY, self.textWidth, self.textHeight, text=''),
        'result': TextBox(self.textX , self.textY, self.textWidth, self.textHeight, text='')


        }

        # Item reward screen buttons - now has only a Continue button
        self.itemRewardOptions = {
            'Title': Text(500, 200, 280, 50, 'You found a potion!', self.fonts['fanta'], self.titleColor),
            'Continue': Button(500, 450, 280, 50, 'Continue')
        }

        # Stores battle music
        self.assets = {
            'titleBackground':pygame.transform.scale(loadImage('/background/otherTitle.png').convert_alpha(), (1280, 720)),
            'intermission': pygame.transform.scale(loadImage('/background/intermission.png').convert_alpha(), (1280, 720)),
            'itemRewardBackground':pygame.transform.scale(loadImage('/background/Arena.png').convert_alpha(), (1280, 720)),
            'intermissionSong': pygame.mixer.Sound('Media/Music/intermission.wav'),
            'titleSong': pygame.mixer.Sound('Media/Music/title.wav'),
            'battleSong': pygame.mixer.Sound('Media/Music/battle.wav'),
            'midBossSong': pygame.mixer.Sound('Media/Music/carrion.wav'),
            'finalBossSong': pygame.mixer.Sound('Media/Music/harbinger.wav'),
            'shopBackground': pygame.transform.scale(loadImage('/background/shop.png'), (1280, 720)),
            'enemy1': pygame.transform.scale(loadImage('/enemies/Knight.png').convert_alpha(), (400, 500)),
            'enemy2': pygame.transform.scale(loadImage('/enemies/Ghost.png').convert_alpha(), (400, 300)),
            'arena': pygame.transform.scale(loadImage('/background/Arena.png').convert_alpha(), (1280, 720))
        }

        # Stores the buttons for the intermission screen.
        self.intermission = {
            'left': Button(100, 300, 200, 100, 'Left'),
            'right': Button(1000, 300, 200, 100, 'Right')
        }
        
        

    # Stores the current battle instance
    def drawMenu(self, menu):
        # Draw the menu options for the main menu.
        for option in menu.values():
            option.draw(self.screen)

    def clearFloorCoin(self):
        clearReward = 1.25 * (self.currentFloor - 1) * 10
        return clearReward

    def coinDialogue(self):
        self.gameOverMenu['Coin'].setText(f"You earned {self.currentCoin} coins!")
        self.currentCoin = 0

    def winDialogue(self):
        self.displayBattleButtons['result'].setText(f"You have defeated {self.currentEnemy[self.currentEnemyIndex].name}!")


    # Displays the dialogue for the skills menu.
    def skillDialogue(self, skill):

        # Updates the textbox of the display battle screen to show the skill used.
        # Displays dialogue for when enemy guards as well.

        if self.enemyGuarded:
            self.displayBattleButtons['attack'].setText(f"{self.currentEnemy[self.currentEnemyIndex].name} guarded!")
            
            print(f"self.skillUsed is {self.skillUsed}")
            print(f"self.skillPlayerUsed is {self.skillPlayerUsed}")
            # Needs to set back self.skillUsed to the name of the player's skill used.
            # Otherwise, self.skillUsed will contain the string "Guard" from the enemy's guard.
            self.skillUsed = self.skillPlayerUsed
            
        # Displays the dialogue for the player's skill used.
        elif not self.enemyGuarded and not self.playerGuarded and self.skillUsed != 'Potion':
                
                # Indicates in the battle UI text box who is performing the skill.
                # Has to be enemy turn as true because the player's skill is used.
                if self.isEnemeyTurn:
                    # Indicates that the player is attacking or using a skill in the dialouge.
                    self.displayBattleButtons['attack'].setText(f"Player used {self.skillUsed} which infliced {self.skillDamage} damage!")
                else:
                    # Indicates the enemy is attacking or using a skill in the dialouge.
                    self.displayBattleButtons['attack'].setText(f"{self.currentEnemy[self.currentEnemyIndex].name} used {self.skillUsed} which infliced {self.skillDamage} damage!")

        # Displays dialogue for when the player guards.
        elif self.playerGuarded:
            self.displayBattleButtons['attack'].setText(f"Player guarded!")
        
        # Displays dialogue for when the player uses potion.
        elif self.skillUsed == 'Potion' or self.skillUsed == "Potion":
            print("Potion was used probably.")
            self.displayBattleButtons['attack'].setText("Player used potion!")
        

    # Uses the potion if avaible to heal player's healt.
    def usePotion(self):

        if self.item > 0:
            self.item -= 1

            # Only add HP to player if their health has been lower and do not 
            # overflow the player's health over their max health.
            if self.player.currentHp == self.player.maxHp:
                pass
            elif (self.player.maxHp - self.player.currentHp) < 50:
                self.player.currentHp += (self.player.maxHp - self.player.currentHp)
            else:
                self.player.currentHp += 50
                
            self.hasUsedSkill = True
            self.skillUsed = 'Potion'
        else:
            pass
            


    # Returns a copy of the enemy sprite with different shade of color 
    # to create a blinking effect.
    def colorize(self, image, new_color):

        colored = image.copy()

        # Adds the color given to the rgb value of the enemy sprite.
        colored.fill(new_color, special_flags=pygame.BLEND_ADD)
        return colored


    def blinkEnemySprite(self, enemyIndex):

        # Creates a blinking effect for the hovered enemy sprite.

        # Gets the current time in Pygame.
        currentTime = pygame.time.get_ticks()

        # Makes the blinking effect every 500 milliseconds.
        if currentTime - self.blinkTimer > self.blinkInterval:
            self.blinkTimer = currentTime
            self.blinkState = not self.blinkState

        # Get the enemy images to apply the blinking effect.
        enemy1Image = self.assets['enemy1']
        enemy2Image = self.assets['enemy2']
    
        if self.blinkState:
            # highlightRect = self.currentEnemy[enemyIndex].rect
            # pygame.draw.rect(self.screen, (255, 0, 0), highlightRect, 5)

            if enemyIndex == 0:
                newImage = self.colorize(enemy1Image, (30, 30, 30))
                self.screen.blit(newImage, (200, 100))
            
            elif enemyIndex == 1:
                newImage = self.colorize(enemy2Image, (30, 30, 30))
                self.screen.blit(newImage, (700, 100))

    def setEnemyPair(self, firstEnemyKey, secondEnemyKey):
        """
        Set the current enemy pair based on specific enemy keys
        """
        # Clear current enemy list and add the specified pair
        self.currentEnemy = [
            self.enemies[firstEnemyKey],
            self.enemies[secondEnemyKey]
        ]

    # Checks if the enemy will guard or not.
    # If so, guard ahead of time to initiate the guard for the
    # player's current attack. Otherwise, the enemy will always be guarding 
    # against the player's next attack.
    def enemyWillGuard(self):
        # Stores the all of the enemy skills to check for their cooldowns.
        move = self.currentEnemy[self.currentEnemyIndex].Skills
        
        # If the enemy will be using a skill on its next turn, then the 
        # enemy will not be guarding.
        if move[1].is_available() and self.currentEnemy[self.currentEnemyIndex].sp >= move[1].get_sp_cost():
            return False
        elif move[0].is_available() and self.currentEnemy[self.currentEnemyIndex].sp >= move[0].get_sp_cost():
            return False

        # If the enemy will guard next turn, then the enemy will guard ahead of time.
        # Before the player's current attack starts.
        elif self.currentEnemy[self.currentEnemyIndex].currentHp < self.currentEnemy[self.currentEnemyIndex].maxHp//2 and random.random() < .5:
            return True

        # If the enemy will do its basic attack, then the enemy will not guard.
        else:
            return False
            
    
    def enemyTurn(self):
        
        # Stores the all of the enemy skills to check for their cooldowns.
        move = self.currentEnemy[self.currentEnemyIndex].Skills
        
        # Checks if the enemy has been defeated.
        if self.currentEnemy[self.currentEnemyIndex].currentHp <= 0:
            print(f"{self.currentEnemy[self.currentEnemyIndex].name} has been defeated.")
            return 0

        # Prioties the use of the highr skills becasue they are probably stronger.
        elif move[1].is_available() and self.currentEnemy[self.currentEnemyIndex].sp >= move[1].get_sp_cost():
            
            # Gets the name of the skill used to display on dialogue box.
            self.skillUsed = move[1].name
            

            # Gets the damage of the skill used for dialogue box and to subtract from player's health.
            self.skillDamage = move[1].use()
            self.currentEnemy[self.currentEnemyIndex].sp -= move[1].get_sp_cost()

            # If the player is guarding, the damage is halved.
            if self.playerGuarded:
                self.skillDamage = self.skillDamage // 2
            self.player.currentHp -= self.skillDamage

            # Sets player health to 0 if player's health becomes negative.
            if self.player.currentHp <= 0:
                self.player.currentHp = 0

            # Have to toggle player guard off or player guarding will display for 
            # the display battle screen for the enemy's attack.
            self.playerGuarded = False

        elif move[0].is_available() and self.currentEnemy[self.currentEnemyIndex].sp >= move[0].get_sp_cost():
            
            # Gets the name of the skill used to display on dialogue box.
            self.skillUsed = move[0].name

            
            # Gets the damage of the skill used for dialogue box and to subtract from player's health.
            self.skillDamage = move[0].use()
            self.currentEnemy[self.currentEnemyIndex].sp -= move[0].get_sp_cost()

            # If the player is guarding, the damage is halved.
            if self.playerGuarded:
                self.skillDamage = self.skillDamage // 2
            self.player.currentHp -= self.skillDamage

            # Sets player health to 0 if player's health becomes negative.
            if self.player.currentHp <= 0:
                self.player.currentHp = 0

            # Have to toggle player guard off or player guarding will display for 
            # the display battle screen for the enemy's attack.
            self.playerGuarded = False


        
        # Enemey guards if their health is below 50% half of the time to prevent spamming of guard.
        # enemyGuarded was set ahead of time to initiate the guard for the player's current attack.
        # Otherwise the enemy will always be guarding against the player's next attack.
        # enemyGuarded is determined by the enemyWillGuard function which accounts for the 
        # enemy's current health, skill cooldowns, and 50% guard change.
        elif self.currentEnemy[self.currentEnemyIndex].currentHp < self.currentEnemy[self.currentEnemyIndex].maxHp//2 and self.enemyGuarded:
            self.enemyGuarded = False

        else:

            # Gets the name of the basic attack to display on dialogue box.
            self.skillUsed = "Strike"

            # Gets the damage of the basic attack for dialogue box and to subtract from player's health.
            self.skillDamage = int(self.currentEnemy[self.currentEnemyIndex].basicAttack())
            
            # If the player is guarding, the damage is halved.
            if self.playerGuarded:
                self.skillDamage = self.skillDamage // 2
            self.player.currentHp -= self.skillDamage

            # Sets player health to 0 if player's health becomes negative.
            if self.player.currentHp <= 0:
                self.player.currentHp = 0
            
            # Have to toggle player guard off or player guarding will display for 
            # the display battle screen for the enemy's attack.
            self.playerGuarded = False


    def drawBars(self):
        # PLAYER'S HEALTH AND SP BARS (at top left)
        
        # Player HP bar calculation
        playerHpPercent = self.player.currentHp / self.player.maxHp
        playerHpWidth = 300 * playerHpPercent
        
        # Player SP bar calculation
        playerSpPercent = self.player.sp / self.player.maxSp
        playerSpWidth = 300 * playerSpPercent
        
        # Draw player's HP bar (top left)
        # HP bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 20, 300, 30))
        # HP bar fill
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, playerHpWidth, 30))
        # HP bar outline
        pygame.draw.rect(self.screen, (0, 0, 0), (20, 20, 300, 30), 2)
        # HP text - explicitly labeled as "Player HP"
        hpText = pygame.font.Font(None, 24).render(f"Player HP: {self.player.currentHp}/{self.player.maxHp}", True, (255, 255, 255))
        self.screen.blit(hpText, (25, 30))
        
        # Draw player's SP bar (below player's HP)
        # SP bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 50, 300, 30))
        # SP bar fill
        pygame.draw.rect(self.screen, (0, 0, 255), (20, 50, playerSpWidth, 30))
        # SP bar outline
        pygame.draw.rect(self.screen, (0, 0, 0), (20, 50, 300, 30), 2)
        # SP text
        spText = pygame.font.Font(None, 24).render(f"Player SP: {self.player.sp}/{self.player.maxSp}", True, (255, 255, 255))
        self.screen.blit(spText, (25, 60))
        
        # ENEMY HEALTH BAR (only for non-infected enemy at top right)
        # Only draw when in battle-related states
        if self.gameStates['battle'] or self.gameStates['displayBattle'] or self.gameStates['infectMode']:
            # In the infection scenario, we only want to show the health bar for the non-infected enemy
            # Assuming currentEnemy[0] is the one the player didn't infect 
            enemy = self.currentEnemy[self.currentEnemyIndex]  # The non-infected enemy
            
            if enemy.currentHp > 0:  # Only draw HP for living enemy
                # Position the bar in the top right
                hpX = 960  # 1280 - 300 - 20 (screen width - bar width - margin)
                hpY = 20  # 20px from top
                
                # Calculate HP percentage
                enemyHpPercent = enemy.currentHp / enemy.maxHp
                enemyHpWidth = 300 * enemyHpPercent
                
                # HP bar background
                pygame.draw.rect(self.screen, (100, 100, 100), (hpX, hpY, 300, 30))
                # HP bar fill
                pygame.draw.rect(self.screen, (255, 0, 0), (hpX, hpY, enemyHpWidth, 30))
                # HP bar outline
                pygame.draw.rect(self.screen, (0, 0, 0), (hpX, hpY, 300, 30), 2)
                # HP text
                hpText = pygame.font.Font(None, 24).render(f"{enemy.name}", True, (255, 255, 255))
                self.screen.blit(hpText, (hpX + 5, hpY + 10))

        # The running loop
    def run(self):
        while True:
            clock = pygame.time.Clock() # Initiates clock
            
            # Plays the intermission song after the intro exposition.
            if self.gameStates['intermission'] and not self.intermissionMusicPlaying:
                self.assets['titleSong'].stop()
                self.assets['battleSong'].stop()
                self.assets['intermissionSong'].play(-1)
                self.intermissionMusicPlaying = True
                self.titleMusicPlaying = False
                self.battleMusicPlaying = False
                self.midBossMusicPlaying = False
                self.finalBossMusicPlaying = False

            # Same music for itemReward as intermission
            elif self.gameStates['itemReward'] and not self.intermissionMusicPlaying:
                self.assets['titleSong'].stop()
                self.assets['battleSong'].stop()
                self.assets['intermissionSong'].play(-1)
                self.intermissionMusicPlaying = True
                self.titleMusicPlaying = False
                self.battleMusicPlaying = False
                self.midBossMusicPlaying = False
                self.finalBossMusicPlaying = False

            elif self.gameStates['shop'] and not self.intermissionMusicPlaying:
                self.assets['titleSong'].stop()
                self.assets['battleSong'].stop()
                self.assets['intermissionSong'].play(-1)
                self.intermissionMusicPlaying = True
                self.titleMusicPlaying = False
                self.battleMusicPlaying = False
                self.midBossMusicPlaying = False
                self.finalBossMusicPlaying = False
        
            # Plays the title song when in the main menu and the exposition state.
            elif (self.gameStates['main'] or self.gameStates['startGame']) and not self.titleMusicPlaying:
                self.assets['intermissionSong'].stop()
                self.assets['battleSong'].stop()
                self.assets['titleSong'].play(-1)
                self.titleMusicPlaying = True
                self.intermissionMusicPlaying = False
                self.battleMusicPlaying = False
                self.midBossMusicPlaying = False
                self.finalBossMusicPlaying = False

            # Plays the battle song when in the battle state.
            elif (self.gameStates['battle'] or self.gameStates['prebattle']) and not self.battleMusicPlaying:
                self.assets['intermissionSong'].stop()
                self.assets['titleSong'].stop()
                self.assets['battleSong'].play(-1)
                self.battleMusicPlaying = True
                self.titleMusicPlaying = False
                self.intermissionMusicPlaying = False
                self.midBossMusicPlaying = False
                self.finalBossMusicPlaying = False

            # Event loop
            for event in pygame.event.get():
                # Exit the game when pressing the close button on window.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check if the mouse button is pressed.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Checks if the left mouse button is pressed.
                    if event.button == 1:
                        mousePos = pygame.mouse.get_pos()

                        # Handle itemReward state mouse click - simplified to just check for Continue button
                        if self.gameStates['itemReward']:
                            if self.itemRewardOptions['Continue'].rect.collidepoint(mousePos):
                                self.item += 1
                                print(F" Have {self.item} number of items.")
                                self.gameStates['itemReward'] = False
                                self.gameStates['prebattle'] = True
                        
                        elif self.gameStates['infectMode']:
                            # Contains which enemy the player clicks on to infect.
                                enemyIndex = None
                                for i, rect in enumerate(self.enemyRect):
                                    if rect.collidepoint(mousePos):
                                        enemyIndex = i
                                        break

                                if enemyIndex is not None:

                                    # Infects the enemy that the player clicked on.
                                    self.player.infect(self.currentEnemy[enemyIndex])

                                    # The remaining enemy because the opponent of the 
                                    # player in battle. Also repositions the 
                                    # player to the left side along with flipping the 
                                    # sprites of the player and enemy if needed.
                                    if enemyIndex == 0:
                                        self.currentEnemyIndex = 1
                                        self.playerPos = (200, 100)
                                        self.enemyPos = (700, 100)
                                        self.flipSprites = False
                                    else:
                                        self.currentEnemyIndex = 0
                                        self.playerPos = (700, 100)
                                        self.enemyPos = (200, 100)
                                        self.flipSprites = True

                                    # Move to battle state
                                    self.gameStates['infectMode'] = False
                                    self.gameStates['battle'] = True
                                    self.currentBattle = Battle(self.player, self.currentEnemy[0])

                        # Handles the player's choice to fight or infect the enemies.
                        elif self.gameStates['prebattle']:
                            

                            # Checks if the fight button was clicked on the prebattle screen.
                            if self.preBattle['fight'].rect.collidepoint(mousePos):
                                print("Fight button clicked")  # Debug print
                                self.gameStates['prebattle'] = False
                                self.gameStates['battle'] = True
                                self.currentBattle = Battle(self.player, self.currentEnemy[0])


                            # Checks if the infect button was clicked ont the prebattle screen.
                            elif self.preBattle['infect'].rect.collidepoint(mousePos):

                                # if enemyIndex is not None:
                                #     self.player.infect(self.currentEnemy[enemyIndex])
                                #     print(f"Player infects {self.currentEnemy[enemyIndex].name}")
                                # else:
                                #     print("No enemy selected to infect")
                                #     return
                                
                                # The player will inherit the skills and states of the enemy they infect.
                                # self.player.infect(self.currentEnemy[1])

                                # print(f"Player infects {self.currentEnemy[enemyIndex].name}")
                                # print(f"New skills: {self.player.Skills[1].name}, {self.player.Skills[2].name}")

                                self.gameStates['prebattle'] = False
                                self.gameStates['infectMode'] = True
                                self.currentBattle = Battle(self.player, self.currentEnemy[0])


                        # After pressing left or right button, create a 50% chance for a battle and a 50% chance for a bonus intermission
                        elif self.gameStates['intermission']:

                            # If the player clicks on the right button,
                            # there is a 50% chance to go to the prebattle state or to get
                            # an item.
                            if self.intermission['right'].rect.collidepoint(mousePos):
                                if random.random() < .5:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['prebattle'] = True
                                else:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['itemReward'] = True
                            
                            # If the player clicks on the left button, 
                            # there is a 50% chance to go to the prebattle state or to get
                            # an item.
                            elif self.intermission['left'].rect.collidepoint(mousePos):
                                if random.random() < .5:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['prebattle'] = True
                                else:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['itemReward'] = True

                        elif self.gameStates['inventory']:

                            # Uses potion if player has any.
                            if self.item > 0 and self.inventoryMenu['Potion'].rect.collidepoint(mousePos):
                                self.usePotion()
                                self.gameStates['inventory'] = False
                                self.gameStates['displayBattle'] = True
                                print("Clicked on Potion")
                            
                            # Goes back to the skills menu.
                            elif self.inventoryMenu['Back'].rect.collidepoint(mousePos):
                                print("Clicked on back button")
                                self.gameStates['inventory'] = False
                                self.gameStates['battle'] = True


                                  
                        # Switches to the shop menu when the shop button is clicked.
                        elif self.gameStates['main']:

                            if self.mainMenuOptions['Shop'].rect.collidepoint(mousePos):
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = True

                                self.titleMusicPlaying = False

                            # Exits the game when the exit button is clicked.
                            if self.mainMenuOptions['Exit'].rect.collidepoint(mousePos):
                                pygame.quit()
                                sys.exit()

                            # Starts game when start button is hit.
                            if self.mainMenuOptions['Start'].rect.collidepoint(mousePos):
                                self.gameStates['startGame'] = True
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = False

                        # Switches back to the main menu when the back button is clicked.
                        elif self.gameStates['shop']:
                            
                            # Changes color of shop buttons if hovering over them.
                            for option in self.shopOptions.values():
                                if isinstance(option, Button):  # Only process Buttons
                                    option.isHovered = option.rect.collidepoint(mousePos)

                            # Checks if the player clicks on the back button in the shop menu.
                            # If so, return back to the title screen.
                            if self.shopOptions['Back'].rect.collidepoint(mousePos):
                                self.gameStates['shop'] = False
                                self.gameStates['main'] = True
                                self.intermissionMusicPlaying = False
                                self.assets['intermissionSong'].stop()

                            # Checks if the player has clicked on the attack upgrade button.
                            # If so, upgrade the player's attack and updates cost.
                            elif self.shopOptions['Attack'].rect.collidepoint(mousePos):
                                if self.upgrades['Attack'] < 5 and self.totalCoin >= self.cost['Attack']:
                                    self.upgrades['Attack']+= 1

                                    # Spends the player's coin on the upgrade.
                                    self.totalCoin -= self.cost['Attack']
                                    # Updates the value of the player's coins on display.
                                    self.shopOptions['Coin'].text = f'Coins: {self.totalCoin}'

                                    self.cost['Attack'] = int(self.cost['Attack'] * 1.25)

                                    # Updates the display of the attack price upgrades.
                                    self.shopOptions['AttackCost'].text = f'{self.cost['Attack']}'


                            # Checks if the player has clicked on the infection upgrade button.
                            # If so, upgrade the player's infection rate and updates cost.
                            elif self.shopOptions['Infection'].rect.collidepoint(mousePos):
                                if self.upgrades['Infection'] < 3 and self.totalCoin >= self.cost['Infect']:
                                    self.upgrades['Infection'] += 1

                                    # Spends the player's coin on the upgrade.
                                    self.totalCoin -= self.cost['Infect']
                                    # Updates the value of the player's coins on display.
                                    self.shopOptions['Coin'].text = f'Coins: {self.totalCoin}'

                                    self.cost['Infect'] = int(self.cost['Infect'] * 1.40)
                                    # Updates the display of the Infect price upgrades.
                                    self.shopOptions['InfectCost'].text = f'{self.cost['Infect']}'


                            # Checks if the player has clicked on the SP upgrade button.
                            # If so, upgrade the player's SP and updates cost.
                            elif self.shopOptions['SP'].rect.collidepoint(mousePos):
                                if self.upgrades['SP'] < 5 and self.totalCoin >= self.cost['SP']:
                                    self.upgrades['SP']+= 1

                                    # Spends the player's coin on the upgrade.
                                    self.totalCoin -= self.cost['SP']
                                    # Updates the value of the player's coins on display.
                                    self.shopOptions['Coin'].text = f'Coins: {self.totalCoin}'

                                    self.cost['SP'] = int(self.cost['SP'] * 1.25)

                                    # Updates the display of the SP price upgrades.
                                    self.shopOptions['SPCost'].text = f'{self.cost['SP']}'

                            # Checks if the player has clicked on the heal upgrade button.
                            # If so, gives player free heal and updates cost.
                            elif self.shopOptions['FullHeal'].rect.collidepoint(mousePos):
                                if self.upgrades['FullHeal'] < 2 and self.totalCoin >= self.cost['Heal']:
                                    self.upgrades['FullHeal'] += 1

                                    # Spends the player's coin on the upgrade.
                                    self.totalCoin -= self.cost['Heal']
                                    # Updates the value of the player's coins on display.
                                    self.shopOptions['Coin'].text = f'Coins: {self.totalCoin}'

                                    self.cost['Heal'] *= 2
                                    
                                    # Updates the display of the Heal price upgrades.
                                    self.shopOptions['HealCost'].text = f'{self.cost['Heal']}'

            # main state    
            if self.gameStates['main']:
                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.mainMenuOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

                self.screen.blit((self.assets['titleBackground']), (0,0))
                # Draws the Main Menu when the game is in the main menu state.
                self.drawMenu(self.mainMenuOptions)
            
            elif self.gameStates['startGame']:
                # Changes the background when the intro exposition starts.
                self.screen.fill((0,0,0))

                dt = clock.tick(60) / 1  # Time in seconds since last frame.

                # Picks the intro dialogue and starts the typing animation.
                self.dialogue.startDialogue('intro')

                # Adds next character from text
                self.dialogue.update(dt) 

                # Draw the text box
                self.dialogue.draw(self.screen)  

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If the text has finished typing, 
                            # and the user clicks the screen, the game will
                            # move to the intermission state.
                            if not self.dialogue.current_dialogue.isTyping():
                                self.gameStates['startGame'] = False
                                self.gameStates['intermission'] = True
                            # If the text is typing, the user can skip the typing animation 
                            # by clicking on the screen.
                            else:
                                self.dialogue.current_dialogue.skipTyping()

                                
            
            # Needed for creating hover effect on the buttons in the shop menu
            # and for adding functionality to the upgrade buttons.
            elif self.gameStates['shop']:
                self.screen.blit(self.assets['shopBackground'], (0, 0))

                # Udaptes the display of the player's coins.
                self.shopOptions['Coin'].text = f'Coins: {self.totalCoin}'

                self.drawMenu(self.shopOptions)

                # Syncs the values in the upgrade dictionary with the shopSlab dictionary. 
                # This makes it so the shopSlab will share the same functionality with the 
                # upgrade dictionary when the upgrade buttons are clicked in the shop.
                for upgrade_key, slab in self.shopSlabs.items():
                    slab.set_upgrades(self.upgrades[upgrade_key])
                    slab.draw(self.screen)
                
                mousePos = pygame.mouse.get_pos()
                for button in self.shopOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

            # Renders the infect 
            elif self.gameStates['infectMode']:
                self.screen.fill((0, 0, 0))

                # # Makes a rect object of the enemies on the screen so can apply blinking effect.
                # enemyRect1 = self.currentEnemy[0].rect()
                # enemyRect2 = self.currentEnemy[1].rect()

                # self.enemyRect = [enemyRect1, enemyRect2]

                # Getting the enemy images to apply the blinking effect to enemy sprites.
                enemy1_image = self.assets['enemy1']
                enemy2_image = self.assets['enemy2']

                # Create rects based on where the images are drawn and their size
                enemy_rect1 = pygame.Rect(200, 100, enemy1_image.get_width(), enemy1_image.get_height())
                enemy_rect2 = pygame.Rect(700, 100, enemy2_image.get_width(), enemy2_image.get_height())
                self.enemyRect = [enemy_rect1, enemy_rect2]
                
                # Handle hover effect on the buttons
                mousePos = pygame.mouse.get_pos()

                # Have to reset to prevent infinite blinking effect despite 
                # the mouse not being on the enemy.
                self.hoveredEnemy = None

                # Checks if the mouse is hovering over an enemy to apply the blinking effect.
                if enemy_rect1.collidepoint(mousePos):
                    self.hoveredEnemy = 0
                elif enemy_rect2.collidepoint(mousePos):
                    self.hoveredEnemy = 1
                
                # Flip the enemy on the left side or the enemy will be facing the wrong
                # direction.

                self.screen.blit(self.assets['enemy1'], (200, 100))
                self.screen.blit(self.assets['enemy2'], (700, 100))

                if self.hoveredEnemy is not None:
                    self.blinkEnemySprite(self.hoveredEnemy)


            # intermission state
            elif self.gameStates['intermission']:
                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.intermission.values():
                    button.isHovered = button.rect.collidepoint(mousePos)
                
                # Draws the intermission background and the buttons within the 
                # intermission screen.
                self.screen.blit(self.assets['intermission'], (0, 0))
                self.drawMenu(self.intermission)

            # SIMPLIFIED itemReward state handling - just display background and continue button
            elif self.gameStates['itemReward']:
                # Display the background
                self.screen.blit(self.assets['itemRewardBackground'], (0, 0))
                
                # Draw the continue button with hover effect
                mousePos = pygame.mouse.get_pos()
                for button in self.itemRewardOptions.values():
                    if isinstance(button, Button):
                        button.isHovered = button.rect.collidepoint(mousePos)
                
                # Draw all components of the itemReward screen
                self.drawMenu(self.itemRewardOptions)

            elif self.gameStates['prebattle']:
                self.screen.fill((0, 0, 0))

                if self.currentFloor == 1:
                    self.setEnemyPair('soldier', 'ghoul')
                elif self.currentFloor == 2:
                    self.setEnemyPair('orc', 'rat')
                elif self.currentFloor == 3:
                    self.setEnemyPair('priest', 'carrion')

                
                # Handle hover effect on the buttons
                mousePos = pygame.mouse.get_pos()


               # Draw the enemies on the screen without blinking effect.
                self.screen.blit(self.assets['enemy1'], (200, 100))
                self.screen.blit(self.assets['enemy2'], (700, 100))

                
                # Draw the menu to prompt the user to fight or infect the enemies
                self.drawMenu(self.preBattle)

                for button in self.preBattle.values():
                    button.isHovered = button.rect.collidepoint(mousePos)


            elif self.gameStates['displayBattle']:
                self.screen.fill((0,0,0))

                self.hasUsedSkill = False
                
                # Display the battle screen background.
                self.screen.blit(self.assets['arena'], (0, 0))
                self.isFirstTurn = False
                enemy1 = pygame.transform.flip(self.assets['enemy1'], self.flipSprites, False)
                enemy2 = pygame.transform.flip(self.assets['enemy2'], self.flipSprites, False)


                # Display enemy sprites on the display battle screen.
                self.screen.blit(enemy1, self.playerPos)
                self.screen.blit(enemy2, self.enemyPos)

                # Health Bar and SP bar for the player and enemies.
                self.drawBars()

                # Render textbox for the skill used in the display battle screen.

                dt = clock.tick(60) / 1  # Time in seconds since last frame.

                # Continue to display the battle dialouge with the skills being used 
                # by the player and the enemy when the enemy's health is above zero.
                if not self.enemyDefeated:
                    # Sets the recently used skill by the player or the 
                    # enemy to the dialouge so it can be displayed.
                    if self.skillDialogueSet == False:
                        self.skillDialogue(self.skillUsed)
                        self.skillDialogueSet = True

                    self.displayBattleButtons['attack'].update(dt)
                    self.displayBattleButtons['attack'].draw(self.screen)
                
                # If the enemy's health is zero, display the winning dialogue.
                else:
                    self.displayBattleButtons['result'].update(dt)
                    self.displayBattleButtons['result'].draw(self.screen)
                
                # Waits for the user to click the screen to exit the display battle screen.
                # Also returns to the battle screen with all of the skills available.
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If the text has finsihed typing, 
                            # and the user clicks the screen, switch the battle screen
                            # with all of the skills.
                            if not self.dialogue.current_dialogue.isTyping():
                                self.gameStates['displayBattle'] = False
                                if self.isEnemeyTurn:
                                    self.gameStates['enemyTurn'] = True
                                else:
                                    # Transitions to the game over screen if
                                    # the player health hits zero.
                                    if self.player.currentHp <= 0:

                                        # Calculates the coins earned on this round based on number of enemies defeated and the 
                                        # current enemy's remaining health.
                                        self.currentCoin = int(0.5 * self.currentFloor + self.currentEnemy[self.currentEnemyIndex].maxHp - self.currentEnemy[self.currentEnemyIndex].currentHp + 2 + self.clearFloorCoin()) // 2
                                        self.totalCoin += self.currentCoin
                                        
                                        self.coinDialogue()
                                        self.gameStates['enemyTurn'] = False
                                        self.gameStates['gameOver'] = True
                                    else:
                                        self.gameStates['battle'] = True
                                # self.skillUsed = "None"
                                self.skillDialogueSet = False

                            # If the text is still typing, the user can skip the typing animation
                            # by clicking on the screen.
                            else:
                                self.dialogue.current_dialogue.skipTyping()
                                
            elif self.gameStates['enemyTurn']:
                self.isEnemeyTurn = False   
                self.enemyTurn()
                
                self.gameStates['enemyTurn'] = False
                self.gameStates['displayBattle'] = True


            # Displays the inventory of the player.
            elif self.gameStates['inventory']:
                # Displays the inventory menu to the player.
                self.screen.fill((0,0,0))

                # Drawing the individual components of the inventory 
                # menu because the potions button will not be rendered 
                # if the player has zero potions.
                self.inventoryMenu['Text'].draw(self.screen)
                self.inventoryMenu['Back'].draw(self.screen)

                if self.item > 0:
                    self.inventoryMenu['Potion'].draw(self.screen)
                
                # Updates the display of number of potions the users has.
                self.inventoryMenu['Potion'].text = f"Potion: {self.item}"

                mousePos = pygame.mouse.get_pos()
                # Applies hovering in the inventory menu.
                for item in self.inventoryMenu.values():
                    if isinstance(item, Button):
                        item.isHovered = item.rect.collidepoint(mousePos)


            elif self.gameStates['battle']:
                # Background for battle

                # Checks if the player has defeated the enemy and displays the winning dialouge if so.
                if self.currentEnemy[self.currentEnemyIndex].currentHp <= 0:
                    self.winDialogue()
                    self.enemyDefeated = True


                # Needs to check the upgrades have been applied to the player's stats.
                # Otherwise the player buffs will be continuously applied.
                if not self.haveAppliedUpgrades:
                    # Increasese the player's max sp by 5 for 
                    # each sp upgrade they have.
                    self.player.maxSp += self.upgrades['SP'] * 5
                    self.player.sp = self.player.maxSp
                    self. haveAppliedUpgrades = True

                # Switches to the game over screen if the player loses all of their
                # health.
                if self.player.currentHp < 1:
                    print("Player is defeated!")
                    self.gameStates['battle'] = False
                    self.gameStates['gameOver'] = True


                action_selected = False
                move = 0
                current_menu = 'battle'  # Track which menu we're showing

                self.turnNum += 1
                
                
                # Allows the enemy to attack after the player's turn needed or the enemy will
                # attack indefinitely.
                self.isEnemeyTurn = True

                self.enemyGuarded = self.enemyWillGuard()

                while not action_selected:
                    # Clear screen EVERY FRAME
                    self.screen.fill((0, 0, 0))

                    # Update mouse position and hover states FIRST
                    mousePos = pygame.mouse.get_pos()

                    # Update hover states for current menu
                    if current_menu == 'battle':
                        for item in self.battle.values():
                            if isinstance(item, Button):
                                item.isHovered = item.rect.collidepoint(mousePos)

                        self.drawMenu(self.battle)  # Redraw battle menu

                    elif current_menu == 'skills':
                        for item in self.moves.values():
                            if isinstance(item, Button):
                                item.isHovered = item.rect.collidepoint(mousePos)
                                
                        self.drawMenu(self.moves)  # Redraw skills menu

                    # Handle events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if current_menu == 'battle':


                                if self.battle['Attack'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    self.hasUsedSkill = True

                                    # Deals the default amount of damage to the enemy.
                                    
                                    # Apply attack upgrade to player's attack.
                                    if self.upgrades['Attack'] > 0:
                                        damage = int(self.player.basicAttack() * (1.05 + self.upgrades['Attack'] * 0.05))
                                    else:
                                        damage = int(self.player.basicAttack())
                                    self.skillDamage = damage
                                    
                                    # If the enemy is guarding, the damage dealt is halved.
                                    if self.enemyGuarded:
                                        self.skillDamage = damage // 2

                                    self.currentEnemy[self.currentEnemyIndex].currentHp -= self.skillDamage

                                    # Stores the string of the attack used to display in the 
                                    # display battle screen.
                                    self.skillUsed = "Strike"

                                    # Needed for when the enemy guards since the 
                                    # enemy and player both share self.skillUsed.
                                    self.skillPlayerUsed = "Strike"

                                    self.gameStates['battle'] = False
                                    self.gameStates['displayBattle'] = True

                                # If the skill button is clicked, switch to the skills menu.
                                elif self.battle['Skill'].rect.collidepoint(mousePos):

                                    for i in range(3):  # Assuming 3 skills
                                        if self.player.Skills[i].currentCD > 0:
                                            self.moves[f'Skill{i}'].text = str(self.player.Skills[i].currentCD)

                                        else:
                                            self.moves[f'Skill{i}'].text = self.player.Skills[i].name

                                    current_menu = 'skills'
                                
                                # If the guard button is clicked, set the action to guard.
                                elif self.battle['Inventory'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    self.skillUsed = 'Potion'
                                    self.gameStates['inventory'] = True
                                    self.gameStates['battle'] = False


                                
                                # If the guard button is clicked, set the action to guard.
                                elif self.battle['Guard'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = 0

                                    # Need to toggle used skill or the cooldowns of 
                                    # skills will not reduce when guarding.
                                    self.hasUsedSkill = True

                                    # Sets the player's guard state to True.
                                    self.playerGuarded = True
                                    self.skillUsed = "Guard"

                                    # Needed for when the enemy guards since the 
                                    # enemy and player both share self.skillUsed.
                                    self.skillPlayerUsed = "Guard"

                                    # Transitions to the display battle screen.
                                    self.gameStates['battle'] = False
                                    self.gameStates['displayBattle'] = True

                            elif current_menu == 'skills':
                                # If the back button is clicked, return to the battle menu.
                                if self.moves['Back'].rect.collidepoint(mousePos):
                                    current_menu = 'battle'
                                
                                # If a skill button is clicked, use the skill.
                                elif self.moves['Skill0'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[0]

                                    if move.is_available() and self.player.sp >= move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True

                                        # Apply attack upgrade to player's attack.
                                        if self.upgrades['Attack'] > 0:
                                            damage = int(move.use() * (1.05 + self.upgrades['Attack'] * 0.05))
                                        else:
                                            damage = int(move.use())


                                        # If the enemy is guarding, the damage dealt is halved.
                                        if self.enemyGuarded:
                                            damage = damage // 2

                                        self.skillDamage = damage

                                        self.currentEnemy[self.currentEnemyIndex].currentHp -= damage
                                        
                                        
                                        self.hasUsedSkill = True

                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[0].name

                                        # Needed for when the enemy guards since the 
                                        self.skillPlayerUsed = self.player.Skills[0].name

                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True

                                # If a skill button is clicked, use the skill.
                                elif self.moves['Skill1'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[1]

                                    # Checks if the 2nd skill is available and the
                                    # player has enough SP to use it.
                                    if move.is_available() and self.player.sp >= move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True
                                        
                                        # Apply attack upgrade to player's attack.
                                        if self.upgrades['Attack'] > 0:
                                            damage = int(move.use() * (1.05 + self.upgrades['Attack'] * 0.05))
                                        else:
                                            damage = int(move.use())

                                        # If the enemy is guarding, the damage dealt is halved.
                                        if self.enemyGuarded:
                                            damage = damage // 2

                                        self.skillDamage = damage

                                        self.hasUsedSkill = True

                                        self.currentEnemy[self.currentEnemyIndex].currentHp -= damage
                                        

                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[1].name

                                        # Needed for when the enemy guards since the 
                                        # enemy and player both share self.skillUsed.
                                        self.skillPlayerUsed = self.player.Skills[1].name

                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True

                                # If a skill button is clicked, use the skill.
                                elif self.moves['Skill2'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[2]

                                    # Checks if the 3rd skill is available and the 
                                    # player has enough SP to use it.
                                    if move.is_available() and self.player.sp >= move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True

                                        # Apply attack upgrade to player's attack.
                                        if self.upgrades['Attack'] > 0:
                                            damage = int(move.use() * (1.05 + self.upgrades['Attack'] * 0.05))
                                        else:
                                            damage = int(move.use())
                                        
                                        # If the enemy is guarding, the damage dealt is halved.
                                        if self.enemyGuarded:
                                            damage = damage // 2

                                        self.skillDamage = damage

                                        self.hasUsedSkill = True

                                        self.currentEnemy[self.currentEnemyIndex].currentHp -= damage
                                        
                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[2].name

                                        # Needed for when the enemy guards since the 
                                        # enemy and player both share self.skillUsed.
                                        self.skillPlayerUsed = self.player.Skills[2].name

                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True


                        # Update display EVERY FRAME
                        pygame.display.flip()
                        pygame.time.Clock().tick(60)    
                
                # Checks if the player has taken an action before reducing the cooldowns of skills.
                # Otherwise the cooldowns will be reduced by toggling back and forth between the
                # Skills menu.
                if self.hasUsedSkill:
                    # Reduces the cooldown of skills only after the player has 
                    # selected a viable action. Otherwise the cooldown for 
                    # skills will be reduced every frame.
                    # Reduce cooldowns for all skills.
                    for i in range(3):
                        self.player.Skills[i].reduceCD()
            
            elif self.gameStates['gameOver']:
                self.screen.fill((0,0,0))
                

                # Needed for the animated typing
                dt = clock.tick(60) / 1 # Time in seconds since last frame.

                # Updates the coin dialouge.
                self.gameOverMenu['Coin'].update(dt)

                # Have to render the game over menu after the typing
                # animation of dialouge or the animation will not work.
                self.drawMenu(self.gameOverMenu)
                self.gameOverMenu['Coin'].draw(self.screen)
                
                # Waits for the user to click the screen to exit the game over screen.
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If the text has finsihed typing, 
                            # and the user clicks the screen, switch the main menu screen
                            if not self.dialogue.current_dialogue.isTyping():
                                self.gameStates['gameOver'] = False
                                self.gameStates['main'] = True

                            else:
                                self.dialogue.current_dialogue.skipTyping()
                

                # # Handle post-battle logic
                # result = self.currentBattle.fight(move)
                # if result == 0:
                #     self.gameStates['battle'] = False
                #     self.gameStates['intermission'] = True

            
            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
