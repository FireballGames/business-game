import pygame
import colors
from controls.button import Button
from controls.label import Label
from game_resources import GameResources

class TurnPanelGroup(pygame.sprite.Group):
    width = 1250
    height = 227

    def __init__(self, rect=None):
        """Нижняя панель — ходы и события

        - **Текущий ход:** отображает, чей сейчас ход и сколько времени осталось для принятия решения (таймер).
        - **События:** список недавних событий (например, "Игрок X купил предприятие Y").
        - Кнопка "Закончить ход."

        """
        super().__init__()
        self.__temp_image = pygame.sprite.Sprite(self)
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)

        self.font = GameResources.get('small_font')

        self.players = pygame.sprite.Group()
        self.events = pygame.sprite.Group()

        self.turn_label = Label(
            self,
            rect=pygame.Rect(0, 0, 174, 24),
            font=self.font,
            color=colors.BLACK,
        )

        self.next_turn_button = Button(
            self,
            rect=pygame.Rect(0, 36, 200, 50),
            text="Закончить ход",
        )
        self.next_turn_button.label.font = self.font
        self.next_turn_button.label.render()

    def render(self, turn, players):
        """Обновление панели.

        Args:
            turn (number): текущий тур
            players (List[Player]): список всех игроков
        """

        # Отображение текущего хода
        self.turn_label.text = f"Ход: {turn}"

        # Отображение баланса
        self.empty()

        self.add(self.__temp_image)
        self.add(self.turn_label)
        self.add(self.next_turn_button)

        self.players.empty()
        label_rect = pygame.Rect(self.rect.left + 200, self.rect.top, 174, 64)
        for player_data in players:
            label = Label(
                self,
                self.players,
                rect=label_rect,
                font=self.font,
                color=colors.BLACK,
            )
            label.text = f"{player_data.name}: {player_data.balance}"
            label_rect = label_rect.move(0, 32)

    def update(self):
        self.__temp_image.rect = self.rect
        self.__temp_image.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.__temp_image.image.fill((255, 0, 0, 32))

        inner_rect = self.rect.inflate(-8, -8)

        self.turn_label.rect.topleft = inner_rect.topleft

        self.next_turn_button.rect.top = inner_rect.top + 48
        self.next_turn_button.rect.left = inner_rect.left

        player_rect = pygame.Rect(inner_rect.left + 200, inner_rect.top, 174, 64)
        for player in self.players:
            player.rect = player_rect
            player_rect = player_rect.move(0, 32)


        event_rect = pygame.Rect(inner_rect.left + 400, inner_rect.top, 174, 64)
        for event in self.events:
            event.rect = event_rect
            event_rect = event_rect.move(0, 32)

        super().update()
