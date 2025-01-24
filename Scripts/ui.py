import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()

TextFount = pygame.font.Font()


class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.animated_text = ''
        self.animation_speed = 0.2  # Characters per frame
        self.animation_timer = 0
        self.current_char = 0

    def update(self, dt):
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
