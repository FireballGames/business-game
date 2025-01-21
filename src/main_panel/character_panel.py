import pygame


class CharacterPanelGroup(pygame.sprite.Group):
    width = 137
    height = 589

    def __init__(self, rect=None):
        super().__init__()
        self.__temp_image = pygame.sprite.Sprite(self)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)
        self.resize(self.rect)

    def resize(self, rect):
        self.rect = pygame.Rect(rect)

        self.__temp_image.rect = self.rect
        self.__temp_image.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.__temp_image.image.fill((0, 255, 0, 32))
