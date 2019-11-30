import pygame

class ShowRedTri:
    def __init__(self):
        self.surface = pygame.transform.scale(pygame.image.load("./asset/triangle.png"), (64, 64))
        self.rect = self.surface.get_rect()
        self.move = []
    
    def is_clicked(self, event):
        return

    def draw(self, win, pos):
        win.blit(self.surface, (pos[1], pos[0]))