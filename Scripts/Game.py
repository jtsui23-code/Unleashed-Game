import pygame
import sys
from ui import Button, Text


class Game:
    
    def __init__(self):

         # Starts up Pygame
        pygame.init()

        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption("Rogue")

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) )
        self.screen = pygame.display.set_mode((1280 , 720 ))

        self.titleColor = (175, 23, 189)
        self.titleFont = pygame.font.Font(None, 150)
        # Stores the Buttons objects for the main menu.
        self.menuState = "main"
        self.mainMenuOptions = {
            'Title': Text(500, 200, 280, 50, 'Title of the Game', self.titleFont, self.titleColor),
            'Start': Button(500, 375, 280, 50, 'Start'),
            'Shop': Button(500, 450, 280, 50, 'Shop'),
            'Exit': Button(500, 525, 280, 50, 'Exit')
        }

        self.shopOptions = {
            'Title': Text(500, 200, 280, 50, 'Upgrades', self.titleFont, self.titleColor),
            'Upgrade': Button(500, 375, 280, 50, 'Upgrade'),
            'Back': Button(500, 525, 280, 50, 'Back')
        }

        self.gameStates = {
            'main': True, 'shop': False, 
            'battle': False, 'intermission': False, 
            'gameOver': False
        }

        # Stores the selected button by the player.
        self.selectedOption = None

        self.assets = {

        }
    
    def drawMenu(self, menu):
        # Draw the menu options for the main menu.
        for option in menu.values():
            option.draw(self.screen)


    def run(self):
        while True:
            
            
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

                        # Switches to the shop menu when the shop button is clicked.
                        if self.gameStates['main']:
                            if self.mainMenuOptions['Shop'].rect.collidepoint(mousePos):
                                self.gameStates['main'] = False
                                self.gameStates['shop'] = True
                                self.drawMenu(self.shopOptions)

            
            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            if self.gameStates['main']:

                # Get mouse position for hover effect on buttons.
                mousePos = pygame.mouse.get_pos()
                for button in self.mainMenuOptions.values():
                    button.isHovered = button.rect.collidepoint(mousePos)

                # Draws the Main Menu when the game is in the main menu state.
                self.drawMenu(self.mainMenuOptions)

            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()




