import pygame
pygame.init()

class Slab:
    def __init__(self, x, y, width, height, max_upgrades):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_upgrades = max_upgrades
        self.current_upgrades = 0
        self.background_color = (0, 0, 0)  # Black
        self.fill_color = (255, 0, 0)       # Red

    def set_upgrades(self, count):
        self.current_upgrades = count

    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        # Calculate filled width based on current upgrades
        fill_width = (self.current_upgrades / self.max_upgrades) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.fill_color, fill_rect)