import pygame
from controls.button import Button
from controls.panel import Panel
from game_resources import GameResources


class PropertyPanel(Panel):
    width = 1250
    height = 172

    def __init__(self, *groups, rect=None):
        super().__init__(*groups, rect=rect)
        self.image.fill((0, 0, 0, 128))

        font = GameResources.get('big_font')

        button_rect = pygame.Rect(1 + 4, 1, 108, 172)
        for _ in range(10):
            button = Button(
                self.controls,
                rect=button_rect,
                text="Кнопка",
            )
            button.label.font = font
            button.color = (200, 200, 200, 128)
            button_rect = button_rect.move(110, 0)
            print(button_rect)

        portrait = Button(
            self.controls,
            rect=pygame.Rect(1108, 0, 142, 172),
            text="Портрет",
        )
        portrait.label.font = font
        portrait.color = (200, 0, 0, 128)

    def update(self):
        print("DRAW", self.controls)
        # for control in self.controls:
        #     control.update()

        # self.image.fill((0, 0, 255, 32))
        self.controls.update()
        self.controls.draw(self.image)
        # super().update()
