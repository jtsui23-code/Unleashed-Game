import pygame

class DialogueManager:
    def __init__(self):
        self.current_dialogue = None # Will store the current dialogue.
        self.dialogues = {}  # Stores all dialogues
        self.is_active = False  # Checks whether a dialogue is currently active.

    def addDialogue(self, name, textBox):
        # Add a dialogue to the manager.
        self.dialogues[name] = textBox

    # This function is used to reset a specific dialogue so it can be replayed with typing animation.
    # It sets the text of the dialogue to its original text, which will trigger the typing animation when started again.
    def resetDialogue(self, name):
    # Reset a specific dialogue so it replays with typing animation
        if name in self.dialogues:
            text_box = self.dialogues[name]
            text_box.setText(text_box.text)  # Reset to same text to re-init animation


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

