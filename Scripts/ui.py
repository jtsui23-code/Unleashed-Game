import pygame
import sys
import os
import textwrap

pygame.init()
#Fonts
TEXT_FONT = pygame.font.Font(None,36)
BUTTON_FONT = pygame.font.Font(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)


class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.animated_text = ''     # Characters that have been drawn
        self.animation_speed = 0.2  # Characters per frame
        self.animation_timer = 0    
        self.current_char = 0
        self.line_height = TEXT_FONT.get_linesize()
        self.max_chars_per_line = (width - 20) // TEXT_FONT.size('A')[0]

        # Wrap text to fit in the box.
        self.lines = self.wrap_text()

        self.isFinished = False

    def wrap_text(self):

        # Split text into words to allow for repositioning them
        # to lower lines if they don't fit in the current line.
        words = self.text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:

            # Check if the word fits in the current line.
            word_width = TEXT_FONT.size(word + ' ')[0]

            # If the word fits, add it to the current line.
            if current_width + word_width <= self.rect.width - 20:
                current_line.append(word)
                current_width += word_width

            # If the word doesn't fit, start a new line.
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        # Add the last line to the list of lines.
        if current_line:
            lines.append(' '.join(current_line))
        return lines


    def update(self, dt): # dt is the amount of time between letters appearing 
        # animated text must be less than the full text to prevent overflow
        if len(self.animated_text) < len(self.text):
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animated_text += self.text[self.current_char]
                self.current_char += 1
                self.animation_timer = 0
        else:
            self.isFinished = True

    def isTyping(self):
        return self.isFinished
    
    def skipTyping(self):
        self.animated_text = self.text
        self.isFinished = True

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        y = self.rect.y + 10
        visible_text = self.animated_text
        
        for line in self.lines:
            if not visible_text:
                break
            if len(visible_text) > len(line):
                text_to_render = line
                visible_text = visible_text[len(line):]
            else:
                text_to_render = visible_text
                visible_text = ''
            
            text_surf = TEXT_FONT.render(text_to_render, True, BLACK)
            surface.blit(text_surf, (self.rect.x + 10, y))
            y += self.line_height
            
            if y + self.line_height > self.rect.bottom - 10:
                break
            
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = GRAY
        self.hoverColor = WHITE
        self.isHovered = False

    def draw(self, surface):

        color = self.hoverColor if self.isHovered else self.color  
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = BUTTON_FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.hoverColor
            else:
                self.color = GRAY
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Text:
    def __init__(self, x, y, width, height, text, font,  color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
    
    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)