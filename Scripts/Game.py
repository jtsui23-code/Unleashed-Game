import pygame
import sys
from Scripts.ui import TextBox, Button


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

        # Stores the Buttons objects for the main menu.
        self.menuState = "main"
        self.menuOptions = {
            'Start': Button(500, 300, 280, 50, 'Start'),
            'Exit': Button(500, 400, 280, 50, 'Exit')
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
    
    def drawMenu(self):
        # Draw the menu options for the main menu.
        for option in self.menuOptions.values():
            option.draw(self.screen)


    def run(self):
        while True:
            
            if self.gameStates['main']:
                # Draws the Main Menu when the game is in the main menu state.
                self.drawMenu()
            

            
            # Event loop
            for event in pygame.event.get():

                # Exit the game when pressing the close button on window.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Display the screen
            pygame.display.flip()

            # Limit the frame rate to 60 FPS
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()




