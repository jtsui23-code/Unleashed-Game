import pygame
import sys
import random
from Scripts.ui import Button, Text, TextBox
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

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) ).
        self.screen = pygame.display.set_mode((1280 , 720 ))

        self.titleColor = (200, 50, 50)

        # Tracks which enemy is being hovered over
        # 0 - firsts enemy 
        # 1 - second enemy
        self.hoveredEnemy = None
        
        # Stores the enemy rects to apply blinking effect onto them.
        self.enemyRect = []

        self.blinkTimer = 0
        self.blinkInterval = 500

        # Invisiblity is for the blinking effect.
        self.blinkState = True # True for visible, False for invisible

        self.fonts = {
            'fanta': pygame.font.Font('Media/Assets/Fonts/fantasy.ttf', 100),
        }
        
        self.dialogue = DialogueManager()
        
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

        # Create an instance of the Player class
        self.player = Player(self, (0, 0), (100, 100), self.screen)

        self.item = 0

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
        
        self.currentEnemy = []
        self.currentFloor = 1
        
        # Stores the Button objects for the shop menu.
        self.shopOptions = {
            'Box': TextBox(200, 75, 900, 600, '', (43, 44, 58, 160)),
            'Title': Text(500, 120, 280, 50, 'Upgrades', self.fonts['fanta'], self.titleColor),
            'Attack':Button(275, 500, 140,50, 'Attack'),
            'Infection': Button(575, 500, 140, 50, 'Infect'),
            'SP': Button(875, 500, 140, 50, 'SP'),
            'Back': Button(20, 620, 140, 50, 'Back')
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
            
        }

        self.skillUsed = "None"
        self.skillDialogueSet = False

        self.displayBattleButtons = {
        'attack': TextBox(340, 600, 600, 100, text='')
        }

        # Item reward screen buttons - now has only a Continue button
        self.itemRewardOptions = {
            'Title': Text(500, 200, 280, 50, 'You found an item!', self.fonts['fanta'], self.titleColor),
            'Continue': Button(500, 450, 280, 50, 'Continue')
        }

        # Stores the selected button by the player.
        self.selectedOption = None

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
        }

        # Stores the buttons for the intermission screen.
        self.intermission = {
            'left': Button(100, 300, 200, 100, 'Left'),
            'right': Button(1000, 300, 200, 100, 'Right')
        }
        
        # Maintains and increments the numbers of upgrades purchased in
        # the shop.
        self.upgrades = {
            'Attack':0,
            'SP': 0, 
            'Infection': 0
        }


        # Flags to track if certain music are playing.
        self.intermissionMusicPlaying = False
        self.titleMusicPlaying = False
        self.battleMusicPlaying = False
        self.midBossMusicPlaying = False
        self.finalBossMusicPlaying = False

        # Stores the current battle instance
    def drawMenu(self, menu):
        # Draw the menu options for the main menu.
        for option in menu.values():
            option.draw(self.screen)

    # Displays the dialogue for the skills menu.
    def skillDialogue(self, skill):

        # Updates the textbox of the display battle screen to show the skill used.
        self.displayBattleButtons['attack'].setText(f"{self.skillUsed} was used!")

    # Returns a copy of the enemy sprite with different shade of color 
    # to create a blinking effect.
    def colorize(self, image, new_color):

        print("Colorize")
        colored = image.copy()

        # Adds the color given to the rgb value of the enemy sprite.
        colored.fill(new_color, special_flags=pygame.BLEND_ADD)
        return colored


    def blinkEnemySprite(self, enemyIndex):

        print("Blinking")
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
                self.screen.blit(newImage, (200, 200))
            
            elif enemyIndex == 1:
                newImage = self.colorize(enemy2Image, (30, 30, 30))
                self.screen.blit(newImage, (500, 200))

    def setEnemyPair(self, firstEnemyKey, secondEnemyKey):
        """
        Set the current enemy pair based on specific enemy keys
        """
        # Clear current enemy list and add the specified pair
        self.currentEnemy = [
            self.enemies[firstEnemyKey],
            self.enemies[secondEnemyKey]
        ]

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
                                    print(f"Enemy {enemyIndex + 1} clicked")  # Debug print
                                    self.player.infect(self.currentEnemy[enemyIndex])
                                    print(f"Player infects {self.currentEnemy[enemyIndex].name}")

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
                                print("Infect button clicked")  # Debug print

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
                            if self.intermission['right'].rect.collidepoint(mousePos):
                                if random.random() < .5:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['prebattle'] = True
                                else:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['itemReward'] = True
                            
                            elif self.intermission['left'].rect.collidepoint(mousePos):
                                if random.random() < .5:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['prebattle'] = True
                                else:
                                    self.gameStates['intermission'] = False
                                    self.gameStates['itemReward'] = True
                                                                                   
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
                                self.gameStates['Start'] = True
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = False

                        # Switches back to the main menu when the back button is clicked.
                        elif self.gameStates['shop']:
                            # Changes color of shop buttons if hovering over them.
                            for button in self.shopOptions.values():
                                button.isHovered = button.rect.collidepoint(mousePos)

                            if self.shopOptions['Back'].rect.collidepoint(mousePos):
                                self.gameStates['shop'] = False
                                self.gameStates['main'] = True
                                self.intermissionMusicPlaying = False
                                self.assets['intermissionSong'].stop()

                            elif self.shopOptions['Attack'].rect.collidepoint(mousePos):
                                if self.upgrades['Attack'] < 4:
                                    self.upgrades['Attack']+= 1

                            elif self.shopOptions['Infection'].rect.collidepoint(mousePos):
                                if self.upgrades['Infection'] < 4:
                                    self.upgrades['Infection'] += 1

                            elif self.shopOptions['SP'].rect.collidepoint(mousePos):
                                if self.upgrades['SP'] < 4:
                                    self.upgrades['SP']+= 1
                        
            # main state    
            if self.gameStates['main']:
                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.mainMenuOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

                self.screen.blit((self.assets['titleBackground']), (0,0))
                # Draws the Main Menu when the game is in the main menu state.
                self.drawMenu(self.mainMenuOptions)

            # Draws the Shop Menu when the game is in the shop state.
            elif self.gameStates['shop']:
                self.screen.blit(self.assets['shopBackground'], (0, 0))
                self.drawMenu(self.shopOptions)
            
            elif self.gameStates['Start']:
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
                            # If the text is not finsihed typing, 
                            # and the user clicks the screen, skip the typing animation.
                            if self.dialogue.is_active and self.dialogue.current_dialogue.isTyping():
                                self.dialogue.handleEvent(event)
                            # If the text is finished typing, performs an
                            # additional click which will exit the 
                            # exposition.
                            else:
                                self.gameStates['Start'] = False
                                self.gameStates['intermission'] = True
            
            # Needed for creating hover effect on the buttons in the shop menu
            # and for adding functionality to the upgrade buttons.
            if self.gameStates['shop']:
                mousePos = pygame.mouse.get_pos()
                for button in self.shopOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

            # Renders the infect 
            if self.gameStates['infectMode']:
                self.screen.fill((0, 0, 0))

                # # Makes a rect object of the enemies on the screen so can apply blinking effect.
                # enemyRect1 = self.currentEnemy[0].rect()
                # enemyRect2 = self.currentEnemy[1].rect()

                # self.enemyRect = [enemyRect1, enemyRect2]

                # Getting the enemy images to apply the blinking effect to enemy sprites.
                enemy1_image = self.assets['enemy1']
                enemy2_image = self.assets['enemy2']

                # Create rects based on where the images are drawn and their size
                enemy_rect1 = pygame.Rect(200, 200, enemy1_image.get_width(), enemy1_image.get_height())
                enemy_rect2 = pygame.Rect(500, 200, enemy2_image.get_width(), enemy2_image.get_height())
                self.enemyRect = [enemy_rect1, enemy_rect2]
                
                # Handle hover effect on the buttons
                mousePos = pygame.mouse.get_pos()

                # Have to reset to prevent infinite blinking effect despite 
                # the mouse not being on the enemy.
                self.hoveredEnemy = None

                # Checks if the mouse is hovering over an enemy to apply the blinking effect.
                if enemy_rect1.collidepoint(mousePos):
                    print("Hovering over enemy 1")
                    self.hoveredEnemy = 0
                elif enemy_rect2.collidepoint(mousePos):
                    print("Hovering over enemy 2")
                    self.hoveredEnemy = 1
                

                self.screen.blit(self.assets['enemy1'], (200, 200))
                self.screen.blit(self.assets['enemy2'], (500, 200))

                if self.hoveredEnemy is not None:
                    self.blinkEnemySprite(self.hoveredEnemy)


            # intermission state
            if self.gameStates['intermission']:
                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.intermission.values():
                    button.isHovered = button.rect.collidepoint(mousePos)
                
                # Draws the intermission background and the buttons within the 
                # intermission screen.
                self.screen.blit(self.assets['intermission'], (0, 0))
                self.drawMenu(self.intermission)

            # SIMPLIFIED itemReward state handling - just display background and continue button
            if self.gameStates['itemReward']:
                # Display the background
                self.screen.blit(self.assets['itemRewardBackground'], (0, 0))
                
                # Draw the continue button with hover effect
                mousePos = pygame.mouse.get_pos()
                for button in self.itemRewardOptions.values():
                    if isinstance(button, Button):
                        button.isHovered = button.rect.collidepoint(mousePos)
                
                # Draw all components of the itemReward screen
                self.drawMenu(self.itemRewardOptions)

            if self.gameStates['prebattle']:
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
                self.screen.blit(self.assets['enemy1'], (200, 200))
                self.screen.blit(self.assets['enemy2'], (500, 200))

                
                # Draw the menu to prompt the user to fight or infect the enemies
                self.drawMenu(self.preBattle)

                for button in self.preBattle.values():
                    button.isHovered = button.rect.collidepoint(mousePos)


            if self.gameStates['displayBattle']:
                self.screen.fill((0,0,0))

                # Display enemy sprites on the display battle screen.
                self.screen.blit(self.assets['enemy1'], (200, 100))
                self.screen.blit(self.assets['enemy2'], (500, 100))

                # Render textbox for the skill used in the display battle screen.

                dt = clock.tick(60) / 1  # Time in seconds since last frame.

                if self.skillDialogueSet == False:
                    self.skillDialogue(self.skillUsed)
                    self.skillDialogueSet = True

                self.displayBattleButtons['attack'].update(dt)
                self.displayBattleButtons['attack'].draw(self.screen)
                
                # Waits for the user to click the screen to exit the display battle screen.
                # Also returns to the battle screen with all of the skills available.
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            # If the text is not finsihed typing, 
                            # and the user clicks the screen, skip the typing animation.
                            if self.dialogue.is_active and self.dialogue.current_dialogue.isTyping():
                                self.dialogue.handleEvent(event)

                            # If the text is finished typing, performs an
                            # additional click which will exit the 
                            # display battle.
                            else:
                                self.gameStates['displayBattle'] = False
                                self.gameStates['battle'] = True
                                self.skillUsed = "None"
                                self.skillDialogueSet = False



            if self.gameStates['battle']:
                # Background for battle
                
                action_selected = False
                move = 0
                current_menu = 'battle'  # Track which menu we're showing

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
                                    move = self.player.basicAttack()
                                
                                # If the skill button is clicked, switch to the skills menu.
                                elif self.battle['Skill'].rect.collidepoint(mousePos):
                                    
                                    # Updates the text for the skills menu.
                                    self.moves['Skill1'].text = self.player.Skills[1].name
                                    self.moves['Skill2'].text = self.player.Skills[2].name
                                    current_menu = 'skills'
                                
                                # If the guard button is clicked, set the action to guard.
                                elif self.battle['Inventory'].rect.collidepoint(mousePos):
                                    pass  # Add inventory logic here
                                
                                # If the guard button is clicked, set the action to guard.
                                elif self.battle['Guard'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = 0

                            elif current_menu == 'skills':
                                if self.moves['Back'].rect.collidepoint(mousePos):
                                    current_menu = 'battle'
                                
                                elif self.moves['Skill0'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[0]

                                    if move.is_available() and self.player.sp > move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True

                                        damage = move.use()
                                        self.currentEnemy[1].currentHp -= damage
                                        print(f"Skill: {self.player.Skills[0].name} does  {damage} DMG")
                                        print(f"Player sp {self.player.sp}")
                                        print(f"Enenmys '{self.currentEnemy[1].currentHp}'.")

                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[0].name
                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True

                                
                                elif self.moves['Skill1'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[1]

                                    if move.is_available() and self.player.sp > move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True
                                        
                                        damage = move.use()
                                        self.currentEnemy[1].currentHp -= damage
                                        print(f"Skill: {self.player.Skills[1].name} does  {damage} DMG")
                                        print(f"Player sp {self.player.sp}")
                                        print(f"Enenmys '{self.currentEnemy[1].currentHp}'.")

                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[1].name
                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True

                                
                                elif self.moves['Skill2'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[2]

                                    if move.is_available() and self.player.sp > move.get_sp_cost():
                                        self.player.sp -= move.get_sp_cost()
                                        action_selected = True
                                        
                                        damage = move.use()
                                        self.currentEnemy[1].currentHp -= damage
                                        print(f"Skill: {self.player.Skills[2].name} does  {damage} DMG")
                                        print(f"Player sp {self.player.sp}")
                                        print(f"Enenmys '{self.currentEnemy[1].currentHp}'.")

                                        # Saves the skill used as a string to display in the display battle screen.
                                        self.skillUsed = self.player.Skills[2].name
                                        self.gameStates['battle'] = False
                                        self.gameStates['displayBattle'] = True


                    # Update display EVERY FRAME
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)

                # Handle post-battle logic
                result = self.currentBattle.fight(move)
                if result == 0:
                    self.gameStates['battle'] = False
                    self.gameStates['intermission'] = True
            print(self.gameStates['infectMode'])

            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()