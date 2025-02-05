"""Save events.

Classes:

    GameEvents
"""

import logging
import uuid
import pygame
from sprite_loader import load_logos, load_portraits


logger = logging.getLogger('event')


class Event:
    def __init__(self, event_id, event_code, player_id=None, payload=None):
        self.event_id = event_id
        self.event_code = event_code
        self.player_id = player_id
        self.payload = payload

    def __str__(self):
        return f"<Event {self.event_code}[{self.event_id}] ({self.payload})>"


class GameEvent:
    """Events storage."""

    __instance = None
    """Events instance."""
    events = []
    """Events list."""
    __event_by_id = {}
    """Events indices by outer id."""
    __last_event_id = 0
    """Last event id."""

    def __init__(self, event_code, player_id=None, payload=None):
        event_id = uuid.uuid4()
        self.inner_event_id = None
        self.event = Event(event_id, event_code, player_id, payload)

    @property
    def event_id(self):
        return self.event.event_id

    def __str__(self):
        return f"GameEvent #{self.inner_event_id}[{self.event_id}]"

    def save(self):
        event_id = self.event_id
        inner_event_id = len(self.events)

        self.inner_event_id = inner_event_id
        GameEvent.events.append(self)
        GameEvent.__event_by_id[event_id] = inner_event_id
        logger.debug(f"Добавлено событие {self}")

        return event_id

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
    def send(cls, event_code, player_id=None, payload=None):
        """Send event."""
        event = cls(event_code, player_id, payload)
        return event.save()

    @classmethod
    def load(cls, event_id=None):
        """Load new events."""
        if event_id is None:
            logger.debug("Получение событий начиная c первого")
            inner_event_id = 0
        else:
            inner_event_id = cls.__event_by_id.get(event_id) + 1

        if inner_event_id is None:
            return

        for event_data in cls.events[inner_event_id:]:
            event = event_data.event
            logger.debug(f"Получено событие {event_data}")
            yield event
