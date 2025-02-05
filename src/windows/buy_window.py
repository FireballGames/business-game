"""Окно покупки предприятия."""

import pygame
import colors
from controls.button import Button
from .window import Window


class BuyWindow(Window):
    """Окно покупки предприятия."""

    def __init__(self, screen, font, enterprise, on_yes):
        super().__init__(screen)

        self.font = font
        self.enterprise = enterprise

        # Создание кнопок
        self.yes_button = Button(
            self.controls,
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
            self.controls,
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

    def on_yes_button_click(self):
        self.hide()
        self.on_yes()

    def on_no_button_click(self):
        self.hide()

    def __update_title(self):
        """Текст с названием предприятия и ценой."""
        self.title.image = self.font.render(
            f"Купить {self.enterprise.name} за {self.enterprise.price}?",
            True,
            colors.BLACK,
        )
        self.title.rect = self.title.image.get_rect(center=(self.rect.centerx, self.rect.y + 50))

    def update(self):
        """Отрисовка окна."""
        self.__update_title()
        super().update()
