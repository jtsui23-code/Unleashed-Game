import pygame

class DialogueManager:
    def __init__(self):
        self.current_dialogue = None # Will store the current dialogue.
        self.dialogues = {}  # Stores all dialogues
        self.is_active = False  # Checks whether a dialogue is currently active.

    def addDialogue(self, name, textBox):
        # Add a dialogue to the manager.
        self.dialogues[name] = textBox

    def startDialogue(self, name):
        
        # Start a specific dialogue by name.
        if name in self.dialogues:
            self.current_dialogue = self.dialogues[name]
            self.is_active = True
        else:
            print(f"Dialogue '{name}' not found.")

    def update(self, dt):
        # Update the current dialogue.
        if self.is_active and self.current_dialogue:
            self.current_dialogue.update(dt)

    def draw(self, surface):
        # Draw the current dialogue.
        if self.is_active and self.current_dialogue:
            self.current_dialogue.draw(surface)

    def handleEvent(self, event):
        # Handle events like mouse clicks to skip typing or progress dialogue.
        if self.is_active and self.current_dialogue:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.current_dialogue.isTyping():
                        self.current_dialogue.skipTyping()
                    else:
                        self.is_active = False  # End the current dialogue

    # Returns whether a dialogue is currently active.
    def isActive(self):
        return self.is_active

