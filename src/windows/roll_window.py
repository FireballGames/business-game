"""Roll result window."""

import pygame
import colors
from game_resources import GameResources
from controls.button import Button
from .window import Window


class RollWindow(Window):
    """Roll result window."""

    def __init__(self, screen, roll, on_close=None):
        super().__init__(screen)

        self.ok_button = Button(
            self.controls,
            self.buttons,
            rect=pygame.Rect(
                0,
                self.rect.y + 130,
                100,
                40,
            ),
            text="Ок",
        )
        self.ok_button.rect.centerx = self.rect.centerx
        self.ok_button.label.font = self.font
        self.ok_button.on_click = self.on_ok_button_click

        self.roll = roll

        self.on_close = on_close

    def on_ok_button_click(self):
        self.hide()

        if self.on_close is not None:
            self.on_close()

    def __update_title(self):
        """Set roll value text."""
        self.title.image = self.font.render(
            f"Бросок: {self.roll}",
            True,
            colors.BLACK,
        )
        self.title.rect = self.title.image.get_rect(center=(self.rect.centerx, self.rect.y + 50))

    def update(self):
        self.__update_title()
        super().update()
