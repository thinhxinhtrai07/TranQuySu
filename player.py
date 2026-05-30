import pygame

from settings import (

    PLAYER_SIZE, PLAYER_BASE_HP, PLAYER_SPEED, PLAYER_MELEE_DAMAGE,

    PLAYER_TALISMAN_DAMAGE, PLAYER_SWORD_BREAK_DAMAGE, PLAYER_FLURRY_HIT_DAMAGE,

    HEAL_AMOUNT, MELEE_COOLDOWN, Q_COOLDOWN, E_COOLDOWN, F_COOLDOWN, R_COOLDOWN,

    LEVEL_EXP,

)

from skill import Projectile, Effect, normalize

from asset_loader import load_player_pose_set


class Player:

    def __init__(self, x, y):

        self.x = x

        self.y = y

        self.size = PLAYER_SIZE

        self.max_hp = PLAYER_BASE_HP

        self.hp = self.max_hp

        self.speed = PLAYER_SPEED

        self.base_damage = PLAYER_MELEE_DAMAGE

        self.skill_damage_bonus = 0

        self.level = 1

        self.exp = 0

        self.exp_to_next = LEVEL_EXP[0]

        self.facing = (1, 0)

        self.facing_dir = 'right'

        self.hit_flash = 0.0

        self.attack_timer = 0.0

        self.invuln_timer = 0.0

        self.cooldowns = {'melee': 0.0, 'q': 0.0, 'e': 0.0, 'f': 0.0, 'r': 0.0}

        self.flurry_timer = 0.0

        self.flurry_hits_left = 0

        self.flurry_tick = 0.0

        self.kills = 0

        self.is_moving = False

        self.visual_state = 'idle'

        self.action_pose = None

        self.images = self._load_images()


    @property

    def rect(self):

        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)


    def center(self):

        return (self.x + self.size / 2, self.y + self.size / 2)


    def _load_images(self):

        try:

            return load_player_pose_set(size=(self.size, self.size), allow_flip_fallback=True)

        except Exception:

            return {

                'idle': {'right': None, 'left': None},

                'walk': {'right': None, 'left': None},

                'attack': {'right': None, 'left': None},

                'cast': {'right': None, 'left': None},

                'skill': {'right': None, 'left': None},

            }


    def _refresh_visual_state(self):

        if self.attack_timer > 0:

            self.visual_state = self.action_pose or 'attack'

        elif self.flurry_timer > 0:

            self.visual_state = 'skill'

        elif self.is_moving:

            self.visual_state = 'walk'

        else:

            self.visual_state = 'idle'

            self.action_pose = None


    def _current_sprite(self):

        state_images = self.images.get(self.visual_state, {})

        sprite = state_images.get(self.facing_dir)

        if sprite is not None:

            return sprite

        for fallback_state in ('idle', 'walk', 'attack', 'cast', 'skill'):

            sprite = self.images.get(fallback_state, {}).get(self.facing_dir)

            if sprite is not None:

                return sprite

        return None


    def take_damage(self, amount):

        if self.invuln_timer > 0:

            return

        self.hp -= amount

        self.hit_flash = 0.2

        self.invuln_timer = 0.35


    def heal(self, amount):

        self.hp = min(self.max_hp, self.hp + amount)


    def add_exp(self, amount):

        leveled = False

        self.exp += amount

        while self.exp >= self.exp_to_next:

            self.exp -= self.exp_to_next

            self.level += 1

            self.max_hp += 10

            self.hp = min(self.max_hp, self.hp + 10)

            self.base_damage += 3

            self.skill_damage_bonus += 4

            idx = min(self.level - 1, len(LEVEL_EXP) - 1)

            self.exp_to_next = LEVEL_EXP[idx]

            leveled = True

        return leveled


    def update(self, dt, keys, mouse_world, world_rect, enemies, projectiles, effects):

        self.hit_flash = max(0, self.hit_flash - dt)

        self.attack_timer = max(0, self.attack_timer - dt)

        if self.attack_timer <= 0:

            self.action_pose = None

        self.invuln_timer = max(0, self.invuln_timer - dt)

        for key in self.cooldowns:

            self.cooldowns[key] = max(0, self.cooldowns[key] - dt)


        mx, my = mouse_world

        cx, cy = self.center()

        self.facing = normalize(mx - cx, my - cy)

        if mx < cx:

            self.facing_dir = 'left'

        elif mx > cx:

            self.facing_dir = 'right'


        dx = (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0)

        dy = (1 if keys[pygame.K_s] else 0) - (1 if keys[pygame.K_w] else 0)

        self.is_moving = bool(dx or dy)

        if dx or dy:

            ndx, ndy = normalize(dx, dy)

            self.x += ndx * self.speed * 60 * dt

            self.y += ndy * self.speed * 60 * dt

        self.x = max(world_rect.left, min(world_rect.right - self.size, self.x))

        self.y = max(world_rect.top, min(world_rect.bottom - self.size, self.y))


        if self.flurry_timer > 0:

            self.flurry_timer -= dt

            self.flurry_tick -= dt

            if self.flurry_tick <= 0 and self.flurry_hits_left > 0:

                self.flurry_hits_left -= 1

                self.flurry_tick = 0.14

                fx, fy = self.facing

                hit_rect = pygame.Rect(int(self.x + fx * 36 - 24), int(self.y + fy * 36 - 24), 120, 120)

                for enemy in enemies:

                    if enemy.rect.colliderect(hit_rect):

                        enemy.take_damage(PLAYER_FLURRY_HIT_DAMAGE + self.skill_damage_bonus)

                effects.append(Effect(cx + fx * 54, cy + fy * 54, 86, 0.22, (255, 170, 120), 'F'))


        self._refresh_visual_state()


    def melee_attack(self, enemies, effects):

        if self.cooldowns['melee'] > 0:

            return False

        fx, fy = self.facing

        cx, cy = self.center()

        hit_rect = pygame.Rect(int(cx + fx * 34 - 48), int(cy + fy * 34 - 48), 96, 96)

        for enemy in enemies:

            if enemy.rect.colliderect(hit_rect):

                enemy.take_damage(self.base_damage)

        effects.append(Effect(cx + fx * 48, cy + fy * 48, 52, 0.18, (240, 230, 160), 'ATK'))

        self.cooldowns['melee'] = MELEE_COOLDOWN

        self.action_pose = 'attack'

        self.attack_timer = 0.18

        self._refresh_visual_state()

        return True


    def cast_talisman(self, projectiles, effects):

        if self.cooldowns['e'] > 0:

            return False

        cx, cy = self.center()

        damage = PLAYER_TALISMAN_DAMAGE + self.skill_damage_bonus

        projectiles.append(Projectile(cx, cy, self.facing, 440, damage, kind='talisman', burn_time=2.0, color=(50, 220, 255), radius=16))

        effects.append(Effect(cx, cy, 74, 0.45, (60, 230, 255), 'E'))

        self.cooldowns['e'] = E_COOLDOWN

        self.action_pose = 'cast'

        self.attack_timer = 0.22

        self._refresh_visual_state()

        return True


    def sword_break(self, enemies, effects):

        if self.cooldowns['q'] > 0:

            return False

        fx, fy = self.facing

        cx, cy = self.center()

        hit_rect = pygame.Rect(int(cx + fx * 42 - 68), int(cy + fy * 42 - 68), 136, 136)

        for enemy in enemies:

            if enemy.rect.colliderect(hit_rect):

                enemy.take_damage(PLAYER_SWORD_BREAK_DAMAGE + self.skill_damage_bonus)

        effects.append(Effect(cx + fx * 60, cy + fy * 60, 108, 0.32, (255, 80, 60), 'Q'))

        self.cooldowns['q'] = Q_COOLDOWN

        self.action_pose = 'skill'

        self.attack_timer = 0.25

        self._refresh_visual_state()

        return True


    def flurry(self, effects):

        if self.cooldowns['f'] > 0:

            return False

        self.flurry_timer = 0.6

        self.flurry_hits_left = 4

        self.flurry_tick = 0.05

        effects.append(Effect(*self.center(), 118, 0.55, (255, 200, 130), 'Fury'))

        self.cooldowns['f'] = F_COOLDOWN

        self.action_pose = 'skill'

        self.attack_timer = 0.45

        self._refresh_visual_state()

        return True


    def cast_heal(self, effects):

        if self.cooldowns['r'] > 0:

            return False

        self.heal(HEAL_AMOUNT)

        effects.append(Effect(*self.center(), 96, 0.65, (120, 255, 120), 'Heal'))

        self.action_pose = 'cast'

        self.attack_timer = max(self.attack_timer, 0.2)

        self.cooldowns['r'] = R_COOLDOWN

        self._refresh_visual_state()

        return True


    def draw(self, screen, camera=(0, 0)):

        rect = self.rect.move(-camera[0], -camera[1])

        sprite = self._current_sprite()

        if sprite is not None:

            image = sprite.copy()

            if self.hit_flash > 0:

                overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)

                overlay.fill((255, 255, 255, 80))

                image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            screen.blit(image, rect.topleft)

            return


        color = (255, 255, 255) if self.hit_flash > 0 else (225, 210, 120)

        pygame.draw.rect(screen, color, rect, border_radius=10)

        pygame.draw.rect(screen, (50, 30, 20), rect, 2, border_radius=10)

        cx = rect.centerx

        cy = rect.centery

        fx, fy = self.facing

        pygame.draw.line(screen, (90, 40, 10), (cx, cy), (cx + int(fx * 26), cy + int(fy * 26)), 4)

