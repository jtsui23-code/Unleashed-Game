import pygame
import sys
import os

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

    def update(self, dt): # dt is the amount of time between letters appearing 
        # animated text must be less than the full text to prevent overflow
        if len(self.animated_text) < len(self.text):
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animated_text += self.text[self.current_char]
                self.current_char += 1
                self.animation_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = TEXT_FONT.render(self.animated_text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

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