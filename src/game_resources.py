"""Load resources.

Classes:

    GameResources
"""

import logging
import pygame
from sprite_loader import load_logos, load_portraits


class GameResources:
    """Resource loader."""

    __instance = None
    """Resources instance."""
    __is_loaded = False
    """Resource list is loaded."""
    resources = {}
    """Resources dictionary."""

    def __init__(self):
        logging.debug("Создание реестра ресурсов")
        GameResources.__instance = self
        self.load()

    @classmethod
    def instance(cls):
        """Get resouces instance.

        Returns:
            GameResources: Resources instance.
        """
        if cls.__instance is None:
            cls()

        return cls.__instance

    @classmethod
    def get(cls, resource_id):
        """Get resource by id.

        Args:
            resource_id (string): Id of resource.

        Returns:
            any: Resource.
        """
        return cls.instance().resources.get(resource_id)

    @classmethod
    def load(cls):
        """Load resources list."""
        if cls.__is_loaded:
            return

        logging.debug("Загрузка ресурсов")
        cls.resources = {
            # Images
            'main-screen': pygame.image.load("res/main-screen.png").convert_alpha(),
            # Spritesheets
            'logos': load_logos(),
            'portraits': load_portraits(),
            # Fonts
            'big_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 36),
            'small_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24),
            # Controls
            'property-button': pygame.image.load("res/property-button.png").convert_alpha(),
            'portrait-button': pygame.image.load("res/portrait.png").convert_alpha(),
        }

        logging.debug("Ресурсы загружены")
        cls.__is_loaded = True
