import pygame

class ShowRedTri:
    def __init__(self):
        self.surface = pygame.transform.scale(pygame.image.load("./asset/triangle.png"), (64, 64))
        self.rect = self.surface.get_rect()
        self.move_index = []
    
    def is_clicked(self, event):
        if event.button == 1: # is left button clicked
            if self.rect.collidepoint(event.pos): # is mouse over button
                return True
        return

    def draw(self, win, pos):
        # index move
        self.move_index = pos

        # coord loc
        self.rect = pygame.Rect((pos[1] * 90, pos[0] * 90), (64, 64))

        win.blit(self.surface, self.rect)