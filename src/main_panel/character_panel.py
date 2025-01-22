import pygame
import colors
from controls.button import Button
from game_resources import GameResources


class CharacterPanelGroup(pygame.sprite.Group):
    width = 137
    height = 589

    def __init__(self, rect=None):
        super().__init__()
        # self.__temp_image = pygame.sprite.Sprite(self)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)

        font = GameResources.get('big_font')
        color = (200, 200, 200, 128)
        hover_color = colors.TRANSPARENT_DARK_GRAY

        self.header = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top, 134, 34),
            text="Заголовок",
        )
        self.header.label.font = font
        self.header.color = color
        self.header.hover_color = hover_color

        self.button1 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 34, 134, 116),
            text="Кнопка",
        )
        self.button1.label.font = font
        self.button1.color = color
        self.button1.hover_color = hover_color

        self.button2 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 150, 134, 116),
            text="Кнопка",
        )
        self.button2.label.font = font
        self.button2.color = color
        self.button2.hover_color = hover_color

        self.button3 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 267, 134, 88),
            text="Кнопка",
        )
        self.button3.label.font = font
        self.button3.color = color
        self.button3.hover_color = hover_color

        self.button4 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 355, 134, 77),
            text="Кнопка",
        )
        self.button4.label.font = font
        self.button4.color = color
        self.button4.hover_color = hover_color

        self.button5 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 432, 134, 76),
            text="Кнопка",
        )
        self.button5.label.font = font
        self.button5.color = color
        self.button5.hover_color = hover_color

        self.button6 = Button(
            self,
            rect=pygame.Rect(self.rect.left, self.rect.top + 508, 134, 82),
            text="Кнопка",
        )
        self.button6.label.font = font
        self.button6.color = color
        self.button6.hover_color = hover_color

        self.buttons = [
            self.button1,
            self.button2,
            self.button3,
            self.button4,
            self.button5,
            self.button6,
        ]

        self.resize(self.rect)

    def resize(self, rect):
        self.rect = pygame.Rect(rect)

        # self.__temp_image.rect = self.rect
        # self.__temp_image.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # self.__temp_image.image.fill((0, 255, 0, 32))

        self.header.rect.topleft = self.rect.topleft
        topleft = self.header.rect.bottomleft
        for button in self.buttons:
            button.rect.topleft = topleft
            topleft = button.rect.bottomleft
