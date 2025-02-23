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

        # Stores the Button objects for the battle menu.
        self.battle = {
            # The text box is at the beginning of the map because it will be the first thing to be drawn.
            'Text': TextBox(200, 75, 900, 600, text=''),
            'Attack': Button(500, 400, 280, 50, 'Attack'),
            'Skill': Button(500, 475, 280, 50, 'Skills'),
            'Guard': Button(500, 550, 280, 50, 'Guard'),
            'Inventory': Button(500, 725, 280, 50, 'Inventory'),
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
            'orc': Orc(self, (0, 0), (100, 100)),           # Create an instance of Orc
            'rat': Rat(self, (0, 0), (100, 100)),           # Create an instance of Rat
            'priest': FFaith(self, (0, 0), (100, 100)),     # Create an instance of FFaith
            'ghoul': Ghoul(self, (0, 0), (100, 100)),       # Create an instance of Ghoul
            'carrion': Carrion(self, (0, 0), (100, 100)),   # Create an instance of Carrion
            'boss': wiz(self, (0, 0), (100, 100))           # Create an instance of wiz
        }
        
        # Stores the Button objects for the shop menu.
        self.shopOptions = {
            'Box': TextBox(200, 75, 900, 600, '', (43, 44, 58, 160)),
            'Title': Text(500, 120, 280, 50, 'Upgrades', self.fonts['fanta'], self.titleColor),
            'Attack':Button(275, 500, 140,50, 'Attack'),
            'Infection': Button(575, 500, 140, 50, 'Infect'),
            'SP': Button(875, 500, 140, 50, 'SP'),
            'Back': Button(20, 620, 140, 50, 'Back')
        }

        # Manages the upgrades the players have
        self.upgrades = {
           'attack': 0,
           'infection': 0,
           'sp': 0
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
            'itemReward': False
            
        }

        # Stores the selected button by the player.
        self.selectedOption = None

        # Stores battle music
        self.assets = {
            'titleBackground':pygame.transform.scale(loadImage('/background/otherTitle.png').convert_alpha(), (1280, 720)),
            'intermission': pygame.transform.scale(loadImage('/background/intermission.png').convert_alpha(), (1280, 720)),
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

        # Stores the current battle instance
    def drawMenu(self, menu):
        # Draw the menu options for the main menu.
        for option in menu.values():
            option.draw(self.screen)


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

            #elif (self.gameStates['midBoss']) and not self.titleMusicPlaying and not self.battleMusicPlaying:
            #    self.assets['intermissionSong'].stop()
            #    self.assets['titleSong'].stop()
            #    self.assets['battleSong'].stop()
            #    self.assets['midBossSong'].play(-1)
            #    self.midBossMusicPlaying = True
            #    self.battleMusicPlaying = False
            #    self.titleMusicPlaying = False
            #    self.intermissionMusicPlaying = False
            #    self.finalBossMusicPlaying = False

            #elif (self.gameStates['finalBoss']) and not self.titleMusicPlaying and not self.battleMusicPlaying:
            #    self.assets['intermissionSong'].stop()
            #    self.assets['titleSong'].stop()
            #    self.assets['battleSong'].stop()
            #    self.assets['midBossSong'].play(-1)
            #    self.finalBossMusicPlaying = True
            #    self.battleMusicPlaying = False
            #    self.titleMusicPlaying = False
            #    self.intermissionMusicPlaying = False
            #    self.midBossMusicPlaying = False



            
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

                        # Handles the player's choice to fight or infect the enemies.
                        if self.gameStates['prebattle']:
                            if self.preBattle['fight'].rect.collidepoint(mousePos):
                                print("Fight button clicked")  # Debug print
                                self.gameStates['prebattle'] = False
                                self.gameStates['battle'] = True
                                self.currentBattle = Battle(self.player, self.enemies['soldier'])

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
                            # additional click which will exist the 
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

            if self.gameStates['itemReward']:
                # Changes the background when the item reward screen starts.

                # Need for creating the typing animation for the text box.
                dt = clock.tick(60) / 1  

                # Picks the reward dialogue and starts the typing animation.
                self.dialogue.startDialogue('reward')

                 # Adds next character from text.
                self.dialogue.update(dt)
                self.drawMenu(self.intermission)

                # Draw the text box.
                self.dialogue.draw(self.screen)

                # Checks for mouse clicks to skip the typing animation or progress the dialogue.
                if self.dialogue.is_active and self.dialogue.current_dialogue.isTyping():
                                self.dialogue.handleEvent(event)
                else:
                    self.gameStates['itemReward'] = False
                    self.gameStates['prebattle'] = True  


            if self.gameStates['prebattle']:
                self.screen.fill((0, 0, 0))

                # Draw the enemies on the screen
                self.screen.blit(self.assets['enemy1'], (200, 200))
                self.screen.blit(self.assets['enemy2'], (500, 200))

                # Draw the menu to prompt the user to fight or infect the enemies
                self.drawMenu(self.preBattle)

                # Handle hover effect on the buttons
                mousePos = pygame.mouse.get_pos()

                for button in self.preBattle.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

                


                                



            if self.gameStates['battle']:
                # Background for battle
                action_selected = False
                move = 0
                current_menu = 'battle'  # Track which menu we're showing

                self.screen.fill((0, 0, 0))
                
                # Initially draw battle UI elements
                self.drawMenu(self.battle)

                while not action_selected:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        mousePos = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            
                            if current_menu == 'battle':
                                if self.battle['Attack'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.basicAttack()
                                
                                elif self.battle['Skill'].rect.collidepoint(mousePos):
                                    current_menu = 'skills'
                                    self.screen.fill((0, 0, 0))
                                    self.drawMenu(self.moves)
                                
                                elif self.battle['Inventory'].rect.collidepoint(mousePos):
                                    continue
                                
                                elif self.battle['Guard'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = 0

                            elif current_menu == 'skills':
                                if self.moves['Back'].rect.collidepoint(mousePos):
                                    current_menu = 'battle'
                                    self.screen.fill((0, 0, 0))
                                    self.drawMenu(self.battle)
                                
                                elif self.moves['Skill0'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[0]
                                
                                elif self.moves['Skill1'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[1]
                                
                                elif self.moves['Skill2'].rect.collidepoint(mousePos):
                                    action_selected = True
                                    move = self.player.Skills[2]

                    # Update display
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)

                # Handle the battle once an action is selected
                result = self.currentBattle.fight(move)
                
                # Check battle result
                if result == 0:  # Battle is finished
                    self.gameStates['battle'] = False
                    self.gameStates['intermission'] = True


            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()