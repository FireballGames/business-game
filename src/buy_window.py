"""Окно покупки предприятия."""

import pygame
import colors
from button import Button


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
        self.yes_button = Button(
            x=self.rect.x + 50,
            y=self.rect.y + 130,
            width=100,
            height=40,
            text="Купить",
            font=font,
            color=colors.GRAY,
            hover_color=colors.DARK_GRAY,
            text_color=colors.BLACK
        )
        self.no_button = Button(
            x=self.rect.x + 250,
            y=self.rect.y + 130,
            width=100,
            height=40,
            text="Отказаться",
            font=font,
            color=colors.GRAY,
            hover_color=colors.DARK_GRAY,
            text_color=colors.BLACK
        )
        self.on_yes = on_yes
        self.visible = True

    def update(self, event):
        """Обработка событий окна."""
        # Проверка кнопок
        if self.yes_button.is_clicked(event):
            self.visible = False
            self.on_yes()
            return
        if self.no_button.is_clicked(event):
            self.visible = False

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
        self.yes_button.draw(screen)
        self.no_button.draw(screen)
