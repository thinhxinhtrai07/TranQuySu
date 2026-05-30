import math

import random

import pygame

from settings import ENEMY_SIZE, ENEMY_STATS

from skill import Projectile, normalize

from asset_loader import try_load_enemy_image


class Enemy:

    _image_cache = {}


    def __init__(self, x, y, enemy_type):

        stats = ENEMY_STATS[enemy_type]

        self.enemy_type = enemy_type

        self.name = stats['name']

        self.x = x

        self.y = y

        self.size = ENEMY_SIZE

        self.hp = stats['hp']

        self.max_hp = stats['hp']

        self.damage = stats['damage']

        self.speed = stats['speed']

        self.color = stats['color']

        self.exp_reward = stats['exp']

        self.attack_cd = 1.1

        self.hit_flash = 0.0

        self.burn_timer = 0.0

        self.burn_tick = 0.0

        self.projectile_cd = random.uniform(1.5, 2.8)

        self.teleport_cd = random.uniform(2.8, 4.5)

        self.image = self._load_image()


    def _load_image(self):

        key = (self.enemy_type, self.size)

        if key not in Enemy._image_cache:

            Enemy._image_cache[key] = try_load_enemy_image(f'{self.enemy_type}.png', size=(self.size, self.size))

        return Enemy._image_cache[key]


    @property

    def rect(self):

        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)


    def center(self):

        return (self.x + self.size / 2, self.y + self.size / 2)


    def take_damage(self, amount, burn_time=0.0):

        self.hp -= amount

        self.hit_flash = 0.15

        if burn_time > 0:

            self.burn_timer = max(self.burn_timer, burn_time)

            self.burn_tick = 0.25


    def alive(self):

        return self.hp > 0


    def update(self, dt, player, enemy_projectiles, world_rect):

        self.attack_cd = max(0, self.attack_cd - dt)

        self.hit_flash = max(0, self.hit_flash - dt)


        px, py = player.center()

        ex, ey = self.center()

        dx, dy = normalize(px - ex, py - ey)

        distance = math.hypot(px - ex, py - ey)


        if self.burn_timer > 0:

            self.burn_timer -= dt

            self.burn_tick -= dt

            if self.burn_tick <= 0:

                self.hp -= 2

                self.burn_tick = 0.4


        if self.enemy_type == 'dark_fiend' and self.teleport_cd <= 0 and distance > 140:

            self.x += dx * 80

            self.y += dy * 80

            self.teleport_cd = random.uniform(2.8, 4.5)

        else:

            self.teleport_cd -= dt


        if self.enemy_type in ('ghost', 'zombie', 'yaksha', 'dark_fiend', 'armored_zombie'):

            self.x += dx * self.speed * 60 * dt

            self.y += dy * self.speed * 60 * dt

        elif self.enemy_type == 'fire_demon':

            if distance > 150:

                self.x += dx * self.speed * 50 * dt

                self.y += dy * self.speed * 50 * dt

            self.projectile_cd -= dt

            if self.projectile_cd <= 0 and distance < 420:

                enemy_projectiles.append(Projectile(ex, ey, (dx, dy), 260, self.damage, kind='enemy_fire', color=(255, 90, 40), radius=12))

                self.projectile_cd = random.uniform(1.7, 2.8)


        self.x = max(world_rect.left, min(world_rect.right - self.size, self.x))

        self.y = max(world_rect.top, min(world_rect.bottom - self.size, self.y))


        if self.rect.colliderect(player.rect) and self.attack_cd <= 0:

            player.take_damage(self.damage)

            self.attack_cd = 1.15


    def draw(self, screen, camera=(0, 0)):

        rect = self.rect.move(-camera[0], -camera[1])

        if self.image is not None:

            image = self.image.copy()

            if self.hit_flash > 0:

                overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)

                overlay.fill((255, 255, 255, 80))

                image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            screen.blit(image, rect.topleft)

        else:

            color = (255, 255, 255) if self.hit_flash > 0 else self.color

            pygame.draw.rect(screen, color, rect, border_radius=8)

            pygame.draw.rect(screen, (20, 20, 20), rect, 2, border_radius=8)

        hp_ratio = max(0, self.hp / self.max_hp)

        pygame.draw.rect(screen, (30, 30, 30), (rect.x, rect.y - 10, rect.w, 6))

        pygame.draw.rect(screen, (220, 40, 40), (rect.x, rect.y - 10, int(rect.w * hp_ratio), 6))

