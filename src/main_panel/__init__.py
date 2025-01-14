import pygame
from controls.panel import Panel
from .action_panel import ActionPanel
from .character_panel import CharacterPanel
from .field_panel import FieldPanel
from .property_panel import PropertyPanel


class MainPanel(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=None, field=None):
        super().__init__(*groups)
        self.rect = rect if rect is not None else pygame.Rect(287, 0, 1250, 989)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.panels = pygame.sprite.Group()
        self.no_panels = pygame.sprite.Group()
        self.field_panel = FieldPanel(self.panels, field=field)
        self.property_panel = PropertyPanel(self.panels)
        self.action_panel = ActionPanel(self.panels)
        self.character_panel = CharacterPanel(self.panels)

        print("Update panel")
        self.property_panel.update()

    def adapt_panels(self):
        rect = self.image.get_rect()

        self.property_panel.rect.centerx = rect.width // 2

        self.action_panel.rect.centerx = rect.width // 2
        self.action_panel.rect.bottom = rect.height

        space = (rect.width - self.property_panel.rect.width) // 2
        is_sticky = space < self.character_panel.rect.width
        if is_sticky:
            self.character_panel.rect.top = self.property_panel.rect.bottom
        else:
            self.character_panel.rect.centery = rect.centery
        self.character_panel.rect.right = rect.right

        self.field_panel.resize(rect.size)

    def resize(self, size):
        self.rect.size = size
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.adapt_panels()

    def process_event(self, event):
        self.field_panel.process_event(event)

    def update_data(self, players):
        self.field_panel.players = players

    def update(self):
        self.image.fill((0, 0, 255, 0))
        self.field_panel.update()
        self.panels.draw(self.image)
