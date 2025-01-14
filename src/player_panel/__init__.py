"""Модуль, содержащий панель с информацией об игроке."""

import pygame
import colors
from controls.label import Label


class PlayerPanel(pygame.sprite.Sprite):
    """Панель информации об игроке."""

    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.background = pygame.image.load("res/player-panel.png").convert_alpha()
        # self.rect = rect if rect is not None else self.background.get_rect()
        self.rect = rect if rect is not None else pygame.Rect(0, 0, 277, 992)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.font = pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24)

        self.controls = pygame.sprite.Group()
        self.name_label = Label(
            self.controls,
            rect=pygame.Rect(50, 420, 174, 64),
            font=pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 48),
            color=colors.BLACK,
        )
        self.turn_label = Label(
            self.controls,
            rect=pygame.Rect(50, 484, 174, 64),
            font=self.font,
            color=colors.BLACK,
        )

    def render(self, player, turn, players):
        """Обновление панели.

        Args:
            player (Player): текущий игрок
            turn (number): текущий тур
            players (List[Player]): список всех игроков
        """
        self.name_label.color = player.color
        self.name_label.text = player.name

        # Отображение текущего хода
        self.turn_label.text = f"Ход: {turn}"

        # Отображение баланса
        labels = pygame.sprite.Group()

        label_rect = pygame.Rect(50, 548, 174, 64)
        for player_data in players:
            label = Label(
                labels,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.text = f"{player_data.name}: {player_data.balance}"
            label_rect = label_rect.move(0, 32)

        label_rect = pygame.Rect(50, 676, 174, 64)
        for tile in player.properties:
            label = Label(
                labels,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.text = tile.name
            label_rect = label_rect.move(0, 32)

        self.image.blit(player.avatar, (32, 51))
        self.image.blit(self.background, (0, 0))
        self.controls.draw(self.image)
        labels.draw(self.image)

    def __repr__(self):
        return f"PlayerPanel(rect={self.rect})"
