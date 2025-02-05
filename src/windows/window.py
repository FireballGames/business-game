"""Base window."""

import pygame
import colors
from game_resources import GameResources


class Window:
    """Base window."""

    def __init__(self, screen):
        self.font = GameResources.get('small_font')

        # Set window size
        width, height = 400, 200
        self.rect = pygame.Rect(0, 0, width, height)

        # Set window position
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery

        # Create controls
        self.controls = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.window = pygame.sprite.Sprite(self.controls)
        self.title = pygame.sprite.Sprite(self.controls)

        # Set visibility
        self.__visible = True

    @property
    def visible(self):
        return self.__visible

    def show(self):
        self.__visible = True

    def hide(self):
        self.__visible = False

    def process_event(self, event):
        """Обработка событий окна."""
        # Проверка кнопок
        for button in self.buttons:
            button.process_event(event)

    def update_window(self):
        """Отрисовка окна."""
        self.window.rect = self.rect
        self.window.image = pygame.Surface(self.window.rect.size)
        rect = self.window.image.get_rect()
        pygame.draw.rect(self.window.image, colors.WHITE, rect)
        pygame.draw.rect(self.window.image, colors.BLACK, rect, 2)

    def update(self):
        self.update_window()
        self.controls.update()

    def draw(self, screen):
        """Отрисовка окна."""
        self.controls.draw(screen)
