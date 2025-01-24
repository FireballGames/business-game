import pygame
from .align import horyzontal, vertical
from player_panel import PlayerPanel


class MainGUI(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.inner_rect = self.rect.copy()

        self.player_panel = PlayerPanel(self)
        self.tile_panel = None
        self.main_panel = None

    def update(self):
        rects = list(horyzontal(
            self.rect.copy(),
            left=[self.player_panel.rect],
            right=[self.tile_panel.rect],
        ))
        self.player_panel.rect = rects[0]
        self.inner_rect = rects[1].inflate(-20, -20)
        self.tile_panel.rect = rects[2]

        panels = list(vertical(
            self.inner_rect.copy(),
            top=[pygame.Rect(0, 0, 0, 180)],
            bottom=[pygame.Rect(0, 0, 0, 235)],
        ))

        self.main_panel.resize(self.inner_rect)

        super().update()