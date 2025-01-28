import pygame
import colors
from controls.button import Button
from game_resources import GameResources


class HeaderButton(Button):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(0, 0, 134, 34),
            text="Заголовок",
        )
        self.label.font = GameResources.get('header_font')
        self.color = (200, 200, 200, 128)
        self.hover_color = colors.TRANSPARENT_DARK_GRAY


class RollButton(Button):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(48, 0, 134, 34),
            text="Бросить",
        )
        self.label.font = GameResources.get('small_font')
        self.color = (200, 200, 200, 128)
        self.hover_color = colors.TRANSPARENT_DARK_GRAY

        self.on_click = self.do_roll
        self.player = None

    def do_roll(self):
        if self.player is None:
            return

        self.player.do_roll()


class ActionButton(Button):
    def __init__(self, *groups, rect=None, text=""):
        super().__init__(
            *groups,
            rect=rect,
            text=text,
        )
        self.label.font = GameResources.get('small_font')
        self.color = (200, 200, 200, 128)
        self.hover_color = colors.TRANSPARENT_DARK_GRAY


class BuyButton(ActionButton):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(0, 34, 134, 64),  # 116
            text="Купить предприятие",
        )


class PayButton(ActionButton):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(0, 150, 134, 64),  # 116
            text="Оплатить услуги",
        )


class PlayButton(ActionButton):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(0, 267, 134, 64),  # 88
            text="Сыграть в казино",
        )


class ReportButton(ActionButton):
    def __init__(self, *groups):
        super().__init__(
            *groups,
            rect=pygame.Rect(0, 355, 134, 64),  # 77
            text="Отчёт",
        )


class ActionPanelGroup(pygame.sprite.Group):
    width = 137
    height = 589

    def __init__(self, rect=None):
        """Интерактивные элементы.
    
        - Кнопки:
            - "Купить предприятие" (появляется при возможности).
            - "Оплатить услуги" (если попал на чужую клетку).
            - "Сыграть в казино" (если игрок на клетке казино).
            - "Отчёт" (показывает историю действий игрока).
        - Панель также отображает подсказки для текущего действия.

        """
        super().__init__()
        self.rect = rect if rect is not None else pygame.Rect(0, 0, self.width, self.height)

        font = GameResources.get('small_font')
        color = (200, 200, 200, 128)
        hover_color = colors.TRANSPARENT_DARK_GRAY

        self.header = HeaderButton(self)

        self.buttons = pygame.sprite.Group()

        self.roll_button = RollButton(self.buttons)

        self.buy_button = BuyButton(self.buttons)
        self.pay_button = PayButton(self.buttons)
        self.play_button = PlayButton(self.buttons)
        self.report_button = ReportButton(self.buttons)

        self.button5 = ActionButton(
            self.buttons,
            rect=pygame.Rect(self.rect.left, self.rect.top + 432, 134, 76),
            text="Кнопка",
        )
        self.button6 = ActionButton(
            self.buttons,
            rect=pygame.Rect(self.rect.left, self.rect.top + 508, 134, 82),
            text="Кнопка",
        )

    def process_event(self, event):
        """
        Проверяет, была ли кнопка нажата мышью.

        :param event: Событие Pygame.
        :return: True, если кнопка была нажата, иначе False.
        """
        for button in self.buttons:
            button.process_event(event)

    def update_data(self, player):
        self.roll_button.player = player

    def update(self):
        self.empty()

        self.header.rect.topleft = self.rect.topleft
        topleft = self.header.rect.bottomleft

        for button in self.buttons:
            button.rect.topleft = topleft
            topleft = button.rect.bottomleft

            if button.rect.bottom < self.rect.bottom:
                self.add(button)

        self.add(self.header)

        super().update()