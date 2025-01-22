import pygame
from controls.panel import Panel
from .action_panel import ActionPanelGroup
from .character_panel import CharacterPanelGroup
from .field_panel import FieldPanel
from .property_panel import PropertyPanelGroup


class MainPanel(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=None, field=None):
        super().__init__(*groups)
        self.rect = rect if rect is not None else pygame.Rect(287, 0, 1250, 989)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.panels = pygame.sprite.Group()

        self.field_panel = FieldPanel(self.panels, field=field)

        self.property_panel_group = PropertyPanelGroup()
        self.action_panel_group = ActionPanelGroup()
        self.character_panel_group = CharacterPanelGroup()

    def resize(self, rect):
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        inner_rect = self.image.get_rect()

        self.property_panel_group.rect.centerx = self.rect.centerx
        self.property_panel_group.rect.top = self.rect.top
        self.property_panel_group.adapt()

        self.action_panel_group.rect.centerx = self.rect.centerx
        self.action_panel_group.rect.bottom = self.rect.bottom

        space = (inner_rect.width - self.property_panel_group.rect.width) // 2
        is_sticky = space < self.character_panel_group.rect.width
        if is_sticky:
            self.character_panel_group.rect.top = self.property_panel_group.rect.bottom
        else:
            self.character_panel_group.rect.centery = self.rect.centery
        self.character_panel_group.rect.right = self.rect.right
        self.character_panel_group.resize(self.character_panel_group.rect)

        self.field_panel.resize(rect.size)

    def process_event(self, event):
        self.field_panel.process_event(event)

    def update_data(self, players):
        self.field_panel.players = players

    def update(self):
        self.image.fill((0, 0, 255, 0))
        self.field_panel.update()
        self.panels.draw(self.image)
