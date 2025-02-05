"""Load resources.

Classes:

    GameResources
"""

import logging
import pygame
from sprite_loader import load_logos, load_portraits


logger = logging.getLogger('resource')


class GameResources:
    """Resource loader."""

    __instance = None
    """Resources instance."""
    __is_loaded = False
    """Resource list is loaded."""
    resources = {}
    """Resources dictionary."""

    def __init__(self):
        logger.debug("Создание реестра ресурсов")
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
    def __load_resource(cls, resource_id, data):
        cls.resources[resource_id] = data
        logger.debug(f"Ресурс \"{resource_id}\" загружен")


    @classmethod
    def load(cls):
        """Load resources list."""
        if cls.__is_loaded:
            return

        logger.debug("Загрузка ресурсов")
        cls.resources = {}

        # Images
        logger.debug("Загрузка изображений")
        cls.__load_resource('main-screen', pygame.image.load("res/main-screen.png").convert_alpha())

        # Spritesheets
        logger.debug("Загрузка спрайтлистов")
        cls.__load_resource('logos', load_logos())
        cls.__load_resource('portraits', load_portraits())

        # Fonts
        logger.debug("Загрузка шрифтов")
        cls.__load_resource('header_font', pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 48))
        cls.__load_resource('big_font', pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 36))
        cls.__load_resource('small_font', pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24))

        # Controls
        logger.debug("Загрузка элементов управления")
        cls.__load_resource('property-button', pygame.image.load("res/property-button.png").convert_alpha())
        cls.__load_resource('portrait-button', pygame.image.load("res/portrait.png").convert_alpha())

        logger.debug("Ресурсы загружены")
        cls.__is_loaded = True
