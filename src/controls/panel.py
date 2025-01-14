import pygame


class Panel(pygame.sprite.Sprite):
    width = 800
    height = 600

    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.controls = pygame.sprite.Group()

    def resize(self, size):
        self.rect.size = size
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def update(self):
        # self.controls.update()
        self.controls.draw(self)
