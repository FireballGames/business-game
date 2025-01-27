"""Button controls to use in game.

Classes:

    Button
"""

import pygame
import colors
from .label import Label


class Button(pygame.sprite.Sprite):
    """In-game button."""

    # TODO: Fix this lint warnings
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, *groups, rect=None, text=""):
        """
        Инициализация кнопки.

        :param rect: Button rect.
        :param text: Текст на кнопке.
        :param font: Шрифт текста.
        :param color: Основной цвет кнопки.
        :param hover_color: Цвет кнопки при наведении.
        :param text_color: Цвет текста.
        """
        super().__init__(groups)
        self.rect = rect
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)

        self.label = Label(rect=self.image.get_rect())
        self.label.text = text

        self.background_image = None
        self.color = colors.GRAY

        self.hover_color = colors.DARK_GRAY
        self.hover = pygame.Surface(rect.size, pygame.SRCALPHA)
        # pygame.draw.rect(self.hover, hover_color, rect)

        self.on_click = None

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, value):
        self.label.text = value

    @property
    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def update(self):
        """
        Отрисовывает кнопку на экране.
        """
        rect = self.image.get_rect()

        if self.background_image is not None:
            self.image.blit(self.background_image, (0, 0))

        if self.is_hovered:
            if self.hover is not None:
                hover = pygame.Surface(rect.size, pygame.SRCALPHA)
                # pygame.draw.rect(hover, self.hover_color, rect)
                hover.fill(self.hover_color)
                self.image.blit(hover, rect)
                # pygame.draw.rect(self.image, self.hover_color, rect)
        else:
            if self.color is not None:
                # pygame.draw.rect(self.image, self.color, rect)
                self.image.fill(self.color)

        # Отрисовка текста
        self.label.render()
        if self.label.image is not None:
            self.image.blit(self.label.image, self.label.rect)

    def process_event(self, event):
        """
        Проверяет, была ли кнопка нажата мышью.

        :param event: Событие Pygame.
        :return: True, если кнопка была нажата, иначе False.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.on_click is not None:
                self.on_click()
