import logging
import pygame
from sprite_loader import load_logos, load_portraits


class GameResources:
    __instance = None
    __is_loaded = False
    __resources = {}

    def __init__(self):
        logging.debug("Создание реестра ресурсов")
        GameResources.__instance = self
        self.load()

    def __load(self):
        if self.__is_loaded:
            return

        logging.debug("Загрузка ресурсов")
        self.__resources = {
            # Images
            'main-screen': pygame.image.load("res/main-screen.png").convert_alpha(),
            # Spritesheets
            'logos': load_logos(),
            'portraits': load_portraits(),
            # Fonts
            'big_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 36),
            'small_font': pygame.font.Font("res/fonts/OldStandardTT-Regular.ttf", 24),
        }

        logging.debug("Ресурсы загружены")
        self.__is_loaded = True

    def __get(self, resource_id):
        return self.__resources.get(resource_id)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls()

        return cls.__instance

    @classmethod
    def load(cls):
        cls.instance().__load()

    @classmethod
    def get(cls, resource_id):
        return cls.instance().__get(resource_id)

