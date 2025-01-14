import pygame


class TilePanel(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, 247, 992)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def update(self):
        self.image.fill((0, 0, 255, 128))
