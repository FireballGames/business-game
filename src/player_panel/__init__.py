import pygame
import colors


class Label(pygame.sprite.Sprite):
    def __init__(self, *groups, color=colors.BLACK, font=None, rect=None):
        super().__init__(*groups)
        self.rect = rect
        self.image = None

        self.font = font
        self.color = color

    def render(self, text):
        self.image = self.font.render(text, True, self.color)


class PlayerPanel(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=None):
        super().__init__(*groups)
        self.background = pygame.image.load("res/player-panel.png").convert_alpha()
        self.rect = rect if rect is not None else self.background.get_rect()
        self.image = pygame.Surface(self.rect.size)

        self.font = pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24)

        self.controls = pygame.sprite.Group()
        self.name_label = Label(
            self.controls,
            rect=(50, 420, 174, 64),
            font=pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 48),
            color=colors.BLACK,
        )
        self.turn_label = Label(
            self.controls,
            rect=(50, 484, 174, 64),
            font=self.font,
            color=colors.BLACK,
        )

    def render(self, player, turn, players):
        self.name_label.color = player.color
        self.name_label.render(player.name)

        # Отображение текущего хода
        self.turn_label.render(f"Ход: {turn}")

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
            label.render(f"{player_data.name}: {player_data.balance}")
            label_rect = label_rect.move(0, 32)

        label_rect = pygame.Rect(50, 676, 174, 64)
        for tile in player.properties:
            label = Label(
                labels,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.render(tile.name)
            label_rect = label_rect.move(0, 32)

        self.image.fill(colors.WHITE)
        self.image.blit(player.avatar, (32, 51))
        self.image.blit(self.background, (0, 0))
        # self.image.blit(self.name_label.image, self.name_label.rect)
        # self.image.blit(self.turn_label.image, self.turn_label.rect)
        self.controls.draw(self.image)
        labels.draw(self.image)
