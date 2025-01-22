import pygame
import colors
from controls.button import Button
from game_resources import GameResources


class PropertyPanelGroup(pygame.sprite.Group):
    width = 1250
    height = 172

    def __init__(self, rect=None):
        super().__init__()
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)

        font = GameResources.get('big_font')

        self.buttons = pygame.sprite.Group()
        left = self.rect.left
        top = self.rect.top
        button_rect = pygame.Rect(left + 4 + 1, top + 1, 108, 172)
        for _ in range(10):
            button = Button(
                self,
                self.buttons,
                rect=button_rect,
                text="Кнопка",
            )
            button.label.font = font

            button.color = None
            button.hover_color = colors.TRANSPARENT_DARK_GRAY

            button.background_image = GameResources.get('property-button')

            button.hover = pygame.Surface(button.rect.size, pygame.SRCALPHA)
            pygame.draw.rect(button.hover, colors.TRANSPARENT_DARK_GRAY, button.image.get_rect())

            button_rect = button_rect.move(110, 0)

        portrait = Button(
            self,
            rect=pygame.Rect(left + 1108, top, 142, 172),
            text="Портрет",
        )
        portrait.label.font = font
        # portrait.color = (200, 0, 0, 128)
        portrait.hover_color = colors.TRANSPARENT_DARK_GRAY

        portrait.background_image = GameResources.get('portrait-button')

        portrait.hover = pygame.Surface(portrait.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(portrait.hover, colors.TRANSPARENT_DARK_GRAY, portrait.image.get_rect())

        self.portrait_group = pygame.sprite.GroupSingle(portrait)

    def adapt(self):
        left = self.rect.left
        top = self.rect.top

        button_rect = pygame.Rect(left + 4 + 1, top + 1, 108, 172)
        for button in self.buttons:
            button.rect = button_rect
            button_rect = button_rect.move(110, 0)

        self.portrait_group.sprite.rect = pygame.Rect(left + 1108, top, 142, 172)

