import random

import pygame

from settings import ITEM_SIZE

from asset_loader import try_load_item_image


class Item:

    _cache = {}

    _filename_map = {

        'heal_small': 'potion_small.png',

        'heal_big': 'potion_big.png',

        'exp': 'exp_orb.png',

        'damage_boost': 'damage_orb.png',

        'max_hp': 'max_hp_orb.png',

    }


    def __init__(self, x, y, item_type, value):

        self.x = x

        self.y = y

        self.item_type = item_type

        self.value = value

        self.rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)

        self.color = {

            'heal_small': (70, 210, 90),

            'heal_big': (220, 70, 70),

            'exp': (130, 220, 255),

            'damage_boost': (220, 80, 80),

            'max_hp': (235, 210, 80),

        }.get(item_type, (255, 255, 255))

        self.image = self._load_image()


    def _load_image(self):

        filename = self._filename_map.get(self.item_type)

        if not filename:

            return None

        key = (filename, ITEM_SIZE)

        if key not in Item._cache:

            Item._cache[key] = try_load_item_image(filename, size=(ITEM_SIZE, ITEM_SIZE))

        return Item._cache[key]


    def draw(self, screen, camera=(0, 0)):

        rect = self.rect.move(-camera[0], -camera[1])

        if self.image is not None:

            screen.blit(self.image, rect.topleft)

            return

        pygame.draw.rect(screen, self.color, rect, border_radius=6)

        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=6)


def random_drop(x, y):

    roll = random.random()

    if roll < 0.25:

        return Item(x, y, 'exp', random.randint(15, 35))

    if roll < 0.35:

        return Item(x, y, 'heal_small', 25)

    if roll < 0.42:

        return Item(x, y, 'heal_big', 40)

    if roll < 0.48:

        return Item(x, y, 'damage_boost', 1)

    if roll < 0.52:

        return Item(x, y, 'max_hp', 20)

    return None

