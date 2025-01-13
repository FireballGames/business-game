import pygame
import colors


class Label(pygame.sprite.Sprite):
    """Текстовая информация как спрайт."""

    def __init__(self, *groups, color=colors.BLACK, font=None, rect=None):
        super().__init__(*groups)
        self.rect = pygame.Rect(rect)
        self.image = None

        self.font = font
        self.color = color
        self.__text = ""

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.render()

    def render(self):
        """Создаёт изображение из текста.

        Args:
            text (string): Текст, из которого предстоит сделать изображение.
        """
        if self.font is None:
            return

        self.image = self.font.render(self.__text, True, self.color)
        self.rect = self.image.get_rect(center=self.rect.center)

    def __repr__(self):
        return f"Label(rect={self.rect}, text={self.__text})"
