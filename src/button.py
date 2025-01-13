"""Button controls to use in game.

Classes:

    Button
"""

import pygame


class Button:
    """In-game button."""

    # TODO: Fix this lint warnings
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        """
        Инициализация кнопки.

        :param x: Координата X верхнего левого угла кнопки.
        :param y: Координата Y верхнего левого угла кнопки.
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param text: Текст на кнопке.
        :param font: Шрифт текста.
        :param color: Основной цвет кнопки.
        :param hover_color: Цвет кнопки при наведении.
        :param text_color: Цвет текста.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        """
        Отрисовывает кнопку на экране.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Отрисовка текста
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """
        Проверяет, была ли кнопка нажата мышью.

        :param event: Событие Pygame.
        :return: True, если кнопка была нажата, иначе False.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False
