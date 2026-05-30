import random

import pygame

from enemy import Enemy

from settings import BOSS_SIZE, BOSS_STATS

from skill import Projectile, normalize

from asset_loader import try_load_boss_image


class Boss(Enemy):

    _boss_cache = {}


    def __init__(self, x, y):

        self.enemy_type = 'boss'

        self.name = BOSS_STATS['name']

        self.x = x

        self.y = y

        self.size = BOSS_SIZE

        self.hp = BOSS_STATS['hp']

        self.max_hp = BOSS_STATS['hp']

        self.damage = BOSS_STATS['damage']

        self.speed = BOSS_STATS['speed']

        self.color = BOSS_STATS['color']

        self.exp_reward = 200

        self.attack_cd = 1.2

        self.hit_flash = 0.0

        self.burn_timer = 0.0

        self.burn_tick = 0.0

        self.projectile_cd = 2.2

        self.summon_cd = 6.0

        self.slam_cd = 4.0

        self.phase = 1

        key = ('blood_moon_king', self.size)

        if key not in Boss._boss_cache:

            Boss._boss_cache[key] = try_load_boss_image('blood_moon_king.png', size=(self.size, self.size))

        self.image = Boss._boss_cache[key]


    def update(self, dt, player, enemy_projectiles, world_rect, enemies, spawn_enemy_cb):

        self.attack_cd = max(0, self.attack_cd - dt)

        self.hit_flash = max(0, self.hit_flash - dt)

        self.projectile_cd -= dt

        self.summon_cd -= dt

        self.slam_cd -= dt

        if self.hp <= self.max_hp * 0.5:

            self.phase = 2


        px, py = player.center()

        ex, ey = self.center()

        dx, dy = normalize(px - ex, py - ey)

        self.x += dx * self.speed * (65 if self.phase == 2 else 48) * dt

        self.y += dy * self.speed * (65 if self.phase == 2 else 48) * dt

        self.x = max(world_rect.left, min(world_rect.right - self.size, self.x))

        self.y = max(world_rect.top, min(world_rect.bottom - self.size, self.y))


        if self.rect.colliderect(player.rect) and self.attack_cd <= 0:

            player.take_damage(self.damage + (6 if self.phase == 2 else 0))

            self.attack_cd = 1.3


        if self.projectile_cd <= 0:

            for angle_shift in (-0.18, 0, 0.18):

                vx = dx * (1 - abs(angle_shift)) - dy * angle_shift

                vy = dy * (1 - abs(angle_shift)) + dx * angle_shift

                enemy_projectiles.append(Projectile(ex, ey, normalize(vx, vy), 300 if self.phase == 2 else 250, 18 if self.phase == 1 else 24, kind='boss_orb', color=(80, 20, 20), radius=18))

            self.projectile_cd = 2.0 if self.phase == 1 else 1.4


        if self.summon_cd <= 0:

            for _ in range(2 if self.phase == 1 else 3):

                spawn_enemy_cb(random.choice(['ghost', 'fire_demon', 'yaksha']))

            self.summon_cd = 7.0 if self.phase == 1 else 5.0


        if self.slam_cd <= 0:

            if pygame.Vector2(ex - px, ey - py).length() < 220:

                player.take_damage(30 if self.phase == 1 else 40)

            self.slam_cd = 5.0 if self.phase == 1 else 3.5

