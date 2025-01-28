"""Модуль, содержащий панель с информацией об игроке."""

import pygame
import colors
from controls.button import Button
from controls.label import Label
from game_resources import GameResources


class PlayerPanel(pygame.sprite.Sprite):
    """Панель информации об игроке.
    
    - Показ текущего состояния игрока:
        - Баланс (рубли).
        - Список предприятий.
        - Статус (в тюрьме, свободен).
        - Возможность открыть подробную статистику.

    """

    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.background = pygame.image.load("res/player-panel.png").convert_alpha()
        # self.rect = rect if rect is not None else self.background.get_rect()
        self.rect = rect if rect is not None else pygame.Rect(0, 0, 277, 992)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.font = GameResources.get('small_font')

        self.controls = pygame.sprite.Group()

        self.name_label = Label(
            self.controls,
            rect=pygame.Rect(50, 352, 174, 48),
            font=GameResources.get('header_font'),
            color=colors.BLACK,
        )

        self.turn_label = Label(
            self.controls,
            rect=pygame.Rect(50, 400, 174, 24),
            font=self.font,
            color=colors.BLACK,
        )

        self.balance_label = Label(
            self.controls,
            rect=pygame.Rect(50, 436, 174, 36),
            font=self.font,
            color=colors.BLACK,
        )

        self.status_label = Label(
            self.controls,
            rect=pygame.Rect(50, 472, 174, 36),
            font=self.font,
            color=colors.BLACK,
        )

        # Возможность открыть подробную статистику.
        self.stats_button = Button(
            self.controls,
            rect=pygame.Rect(50, 508, 174, 36),
            text="Статистика",
        )
        self.stats_button.label.font = self.font

        self.enterprise_label = Label(
            self.controls,
            rect=pygame.Rect(50, 544, 174, 36),
            font=self.font,
            color=colors.BLACK,
        )
        self.enterprise_label.text = "Список предприятий"

    def render(self, player):
        """Обновление панели.

        Args:
            player (Player): текущий игрок
            turn (number): текущий тур
        """
        self.name_label.color = player.color
        self.name_label.text = player.name

        # Отображение текущего хода
        self.turn_label.text = f"Ход: {player.turn}"

        # Show balance
        self.balance_label.text = f"Баланс: {player.balance}"

        # Show status
        status = "свободен"
        self.status_label.text = f"Статус: {status}"

        # Show properties
        labels = pygame.sprite.Group()

        label_rect = pygame.Rect(50, 620, 174, 24)
        for tile in player.properties:
            label = Label(
                labels,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.text = tile.name
            label_rect = label_rect.move(0, 32)

        self.controls.update()

        self.image.blit(player.avatar, (32, 51))
        self.image.blit(self.background, (0, 0))

        self.controls.draw(self.image)
        labels.draw(self.image)

    def __repr__(self):
        return f"PlayerPanel(rect={self.rect})"
