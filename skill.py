import math

import pygame

from asset_loader import try_load_skill_image


class Projectile:

    _cache = {}


    def __init__(self, x, y, direction, speed, damage, kind='talisman', burn_time=0.0, color=(255, 180, 40), radius=10):

        self.x = x

        self.y = y

        self.dx = direction[0]

        self.dy = direction[1]

        self.speed = speed

        self.damage = damage

        self.kind = kind

        self.radius = radius

        self.color = color

        self.burn_time = burn_time

        self.alive = True

        self.image = self._load_image()


    def _load_image(self):

        mapping = {

            'talisman': ('talisman_fire.png', self.radius * 6),

            'boss_orb': ('flurry.png', self.radius * 4),

            'enemy_fire': ('talisman_fire.png', self.radius * 4),

        }

        if self.kind not in mapping:

            return None

        filename, size = mapping[self.kind]

        key = (self.kind, size)

        if key not in Projectile._cache:

            Projectile._cache[key] = try_load_skill_image(filename, size=(size, size))

        return Projectile._cache[key]


    @property

    def rect(self):

        if self.image is not None:

            rect = self.image.get_rect(center=(int(self.x), int(self.y)))

            return rect

        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)


    def update(self, dt, world_rect):

        self.x += self.dx * self.speed * dt

        self.y += self.dy * self.speed * dt

        if not world_rect.collidepoint(self.x, self.y):

            self.alive = False


    def draw(self, screen, camera=(0, 0)):

        sx = int(self.x - camera[0])

        sy = int(self.y - camera[1])

        if self.image is not None:

            angle = -math.degrees(math.atan2(self.dy, self.dx))

            rotated = pygame.transform.rotate(self.image, angle)

            rect = rotated.get_rect(center=(sx, sy))

            screen.blit(rotated, rect.topleft)

            return

        pygame.draw.circle(screen, self.color, (sx, sy), self.radius)


class Effect:

    _cache = {}


    def __init__(self, x, y, radius, duration, color, label=''):

        self.x = x

        self.y = y

        self.radius = radius

        self.duration = duration

        self.max_duration = duration

        self.color = color

        self.label = label

        self.image = self._resolve_image()


    def _resolve_image(self):

        mapping = {

            'E': 'talisman_fire.png',

            'Q': 'sword_break.png',

            'F': 'flurry.png',

            'Fury': 'flurry.png',

            'Heal': 'heal.png',

            'Burn': 'talisman_fire.png',

        }

        filename = mapping.get(self.label)

        if not filename:

            return None

        size = max(32, int(self.radius * 2.8))

        key = (filename, size)

        if key not in Effect._cache:

            Effect._cache[key] = try_load_skill_image(filename, size=(size, size))

        return Effect._cache[key]


    def update(self, dt):

        self.duration -= dt


    def alive(self):

        return self.duration > 0


    def draw(self, screen, camera=(0, 0), font=None):

        alpha_ratio = max(0.1, self.duration / self.max_duration)

        sx = int(self.x - camera[0])

        sy = int(self.y - camera[1])

        if self.image is not None:

            img = self.image.copy()

            img.set_alpha(int(255 * alpha_ratio))

            rect = img.get_rect(center=(sx, sy))

            screen.blit(img, rect.topleft)

        else:

            pygame.draw.circle(screen, self.color, (sx, sy), int(self.radius * alpha_ratio), 2)


def normalize(dx, dy):

    length = math.hypot(dx, dy)

    if length == 0:

        return (1, 0)

    return (dx / length, dy / length)

