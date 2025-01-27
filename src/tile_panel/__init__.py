import pygame
import colors
from controls.label import Label
from game_resources import GameResources


class TilePanel(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, 247, 992)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.font = GameResources.get('small_font')

        self.controls = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        self.turn_label = Label(
            self.controls,
            rect=pygame.Rect(50, 400, 174, 24),
            font=self.font,
            color=colors.BLACK,
        )

    def render(self, turn, players):
        """Обновление панели.

        Args:
            turn (number): текущий тур
            players (List[Player]): список всех игроков
        """

        # Отображение текущего хода
        self.turn_label.text = f"Ход: {turn}"

        # Отображение баланса
        self.players.empty()

        label_rect = pygame.Rect(50, 424, 174, 64)
        for player_data in players:
            label = Label(
                self.players,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.text = f"{player_data.name}: {player_data.balance}"
            label_rect = label_rect.move(0, 32)

        self.image.fill((0, 0, 255, 128))
        self.controls.draw(self.image)
        self.players.draw(self.image)
