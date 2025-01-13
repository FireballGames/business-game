"""Окно покупки предприятия."""

import pygame
import colors
from controls.button import Button


class BuyWindow:
    """Окно покупки предприятия."""

    def __init__(self, screen, font, enterprise, on_yes):
        self.font = font
        self.enterprise = enterprise

        # Размеры окна
        window_width, window_height = 400, 200
        screen_width, screen_height = screen.get_size()
        self.rect = pygame.Rect(
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2,
            window_width,
            window_height,
        )

        # Создание кнопок
        self.buttons = pygame.sprite.Group()
        self.yes_button = Button(
            self.buttons,
            rect=pygame.Rect(
                self.rect.x + 50,
                self.rect.y + 130,
                100,
                40,
            ),
            text="Купить",
        )
        self.yes_button.label.font = font
        self.yes_button.on_click = self.on_yes_button_click

        self.no_button = Button(
            self.buttons,
            rect=pygame.Rect(
                self.rect.x + 250,
                self.rect.y + 130,
                100,
                40,
            ),
            text="Отказаться",
        )
        self.no_button.label.font = font
        self.no_button.on_click = self.on_no_button_click

        self.on_yes = on_yes
        self.visible = True

    def on_yes_button_click(self):
        self.visible = False
        self.on_yes()

    def on_no_button_click(self):
        self.visible = False

    def update(self, event):
        """Обработка событий окна."""
        # Проверка кнопок
        for button in self.buttons:
            button.process_event(event)

    def draw(self, screen):
        """Отрисовка окна."""
        # Рисуем окно
        pygame.draw.rect(screen, colors.WHITE, self.rect)
        pygame.draw.rect(screen, colors.BLACK, self.rect, 2)

        # Текст с названием предприятия и ценой
        title_text = self.font.render(
            f"Купить {self.enterprise.name} за {self.enterprise.price}?",
            True,
            colors.BLACK,
        )
        title_rect = title_text.get_rect(center=(self.rect.centerx, self.rect.y + 50))
        screen.blit(title_text, title_rect)

        # Рисуем кнопки
        for button in self.buttons:
            button.update()
        self.buttons.draw(screen)
