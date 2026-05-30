import random

import sys

import pygame


from settings import TITLE, FPS, load_settings, save_settings, BG_COLORS, STAGE_INFO

from player import Player

from enemy import Enemy

from boss import Boss

from item import random_drop

from sound import SoundManager

from ui import draw_button, draw_hud, draw_text

from skill import Effect

from asset_loader import try_load_map_image, try_load_ui_image


WORLD_W = 2200

WORLD_H = 1400

WORLD_RECT = pygame.Rect(0, 0, WORLD_W, WORLD_H)


class Game:

    def __init__(self):

        pygame.init()

        pygame.font.init()

        self.settings = load_settings()

        self.sound = SoundManager(self.settings)

        self.screen = self.create_screen()

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()


        font_family = ['segoeui', 'verdana', 'calibri', 'arial']

        self.fonts = {

            'tiny': pygame.font.SysFont(font_family, 15, bold=True),

            'small': pygame.font.SysFont(font_family, 22),

            'medium': pygame.font.SysFont(font_family, 30),

            'large': pygame.font.SysFont(font_family, 52, bold=True),

        }

        self.state = 'menu'

        self.running = True

        self.selected_menu = 0

        self.selected_settings = 0

        self.stage = 1

        self.player = None

        self.enemies = []

        self.enemy_projectiles = []

        self.player_projectiles = []

        self.items = []

        self.effects = []

        self.boss = None

        self.stage_kills = 0

        self.spawn_timer = 0

        self.total_time = 0.0

        self.message = ''

        self.summary = {}

        self.backgrounds = {}

        self.ui_logo = None

        self.load_visual_assets()

        self.sound.play_background_music('menu')


    def create_screen(self):

        flags = pygame.FULLSCREEN if self.settings['fullscreen'] else 0

        return pygame.display.set_mode((self.settings['width'], self.settings['height']), flags)


    def load_visual_assets(self):

        screen_size = (self.settings['width'], self.settings['height'])

        self.backgrounds = {

            'menu': try_load_map_image('menu_bg.png', size=screen_size),

            'game_over': try_load_map_image('game_over_bg.png', size=screen_size),

            'victory': try_load_map_image('victory_bg.png', size=screen_size),

            1: try_load_map_image('forest_bg.png', size=(WORLD_W, WORLD_H)),

            2: try_load_map_image('temple_bg.png', size=(WORLD_W, WORLD_H)),

            3: try_load_map_image('blood_moon_palace_bg.png', size=(WORLD_W, WORLD_H)),

        }

        self.ui_logo = try_load_ui_image('logo.png', size=(96, 72))


    def reset_game(self):

        self.player = Player(WORLD_W // 2, WORLD_H // 2)

        self.enemies = []

        self.enemy_projectiles = []

        self.player_projectiles = []

        self.items = []

        self.effects = []

        self.boss = None

        self.stage = 1

        self.stage_kills = 0

        self.spawn_timer = 0

        self.total_time = 0.0

        self.message = ''

        self.load_stage(1)


    def load_stage(self, number):

        self.stage = number

        self.stage_kills = 0

        self.spawn_timer = STAGE_INFO[number]['spawn_interval']

        self.enemies.clear()

        self.enemy_projectiles.clear()

        self.player_projectiles.clear()

        self.items.clear()

        self.effects.clear()

        self.boss = None

        self.player.x = WORLD_W // 2

        self.player.y = WORLD_H // 2

        self.message = ''

        self.sound.play_background_music('stage1')


    def spawn_enemy(self, enemy_type=None):

        info = STAGE_INFO[self.stage]

        if enemy_type is None:

            enemy_type = random.choice(info['enemy_pool'])

        side = random.choice(['top', 'bottom', 'left', 'right'])

        margin = 120

        if side == 'top':

            x = random.randint(0, WORLD_W - 60)

            y = margin

        elif side == 'bottom':

            x = random.randint(0, WORLD_W - 60)

            y = WORLD_H - margin

        elif side == 'left':

            x = margin

            y = random.randint(0, WORLD_H - 60)

        else:

            x = WORLD_W - margin

            y = random.randint(0, WORLD_H - 60)

        self.enemies.append(Enemy(x, y, enemy_type))


    def start_game(self):

        self.reset_game()

        self.state = 'playing'


    def handle_event(self, event):

        if event.type == pygame.QUIT:

            self.running = False

        elif self.state == 'menu':

            self.handle_menu_event(event)

        elif self.state == 'settings':

            self.handle_settings_event(event)

        elif self.state == 'playing':

            self.handle_play_event(event)

        elif self.state in ('game_over', 'victory'):

            self.handle_end_event(event)


    def handle_menu_event(self, event):

        options = ['Start Game', 'Settings', 'Exit']

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, pygame.K_w):

                self.selected_menu = (self.selected_menu - 1) % len(options)

            elif event.key in (pygame.K_DOWN, pygame.K_s):

                self.selected_menu = (self.selected_menu + 1) % len(options)

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):

                self.activate_menu()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.activate_menu(mouse_pos=event.pos)


    def activate_menu(self, mouse_pos=None):

        btns = self.menu_buttons()

        if mouse_pos is not None:

            for idx, rect in enumerate(btns):

                if rect.collidepoint(mouse_pos):

                    self.selected_menu = idx

        choice = self.selected_menu

        if choice == 0:

            self.start_game()

        elif choice == 1:

            self.state = 'settings'

        elif choice == 2:

            self.running = False


    def handle_settings_event(self, event):

        options = self.settings_options()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.state = 'menu'

            elif event.key in (pygame.K_UP, pygame.K_w):

                self.selected_settings = (self.selected_settings - 1) % len(options)

            elif event.key in (pygame.K_DOWN, pygame.K_s):

                self.selected_settings = (self.selected_settings + 1) % len(options)

            elif event.key in (pygame.K_LEFT, pygame.K_a):

                self.adjust_setting(-1)

            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_RETURN, pygame.K_SPACE):

                self.adjust_setting(1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.click_settings(event.pos)


    def click_settings(self, pos):

        rects = self.settings_buttons()

        for idx, rect in enumerate(rects):

            if rect.collidepoint(pos):

                self.selected_settings = idx

                self.adjust_setting(1)

                break


    def adjust_setting(self, direction):

        options = self.settings_options()

        self.selected_settings = max(0, min(self.selected_settings, len(options) - 1))

        option = options[self.selected_settings]

        if option == 'fullscreen':

            self.settings[option] = not self.settings[option]

        elif option == 'resolution':

            resolutions = [(1280, 720), (1366, 768), (1600, 900)]

            current = (self.settings['width'], self.settings['height'])

            idx = resolutions.index(current) if current in resolutions else 0

            idx = (idx + direction) % len(resolutions)

            self.settings['width'], self.settings['height'] = resolutions[idx]

            self.screen = self.create_screen()

            self.load_visual_assets()

        elif option == 'back':

            save_settings(self.settings)

            self.screen = self.create_screen()

            self.load_visual_assets()

            self.state = 'menu'

            return

        save_settings(self.settings)


    def handle_play_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.state = 'menu'

                self.sound.play_background_music('menu')

            elif event.key == pygame.K_q:

                if self.player.sword_break(self.enemies_with_boss(), self.effects):

                    self.sound.play_skill_sound('q')

            elif event.key == pygame.K_e:

                if self.player.cast_talisman(self.player_projectiles, self.effects):

                    self.sound.play_skill_sound('e')

            elif event.key == pygame.K_f:

                if self.player.flurry(self.effects):

                    self.sound.play_skill_sound('f')

            elif event.key == pygame.K_r:

                if self.player.cast_heal(self.effects):

                    self.sound.play_heal_sound()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            if self.player.melee_attack(self.enemies_with_boss(), self.effects):

                self.sound.play_attack_sound()


    def handle_end_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):

                self.start_game()

            elif event.key == pygame.K_ESCAPE:

                self.state = 'menu'

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            buttons = self.end_buttons()

            if buttons[0].collidepoint(event.pos):

                self.start_game()

            elif buttons[1].collidepoint(event.pos):

                self.running = False


    def enemies_with_boss(self):

        result = list(self.enemies)

        if self.boss and self.boss.hp > 0:

            result.append(self.boss)

        return result


    def update(self, dt):

        if self.state != 'playing':

            return

        self.total_time += dt

        self.spawn_logic(dt)


        mouse_screen = pygame.mouse.get_pos()

        camera = self.get_camera()

        mouse_world = (mouse_screen[0] + camera[0], mouse_screen[1] + camera[1])

        keys = pygame.key.get_pressed()

        self.player.update(dt, keys, mouse_world, WORLD_RECT, self.enemies_with_boss(), self.player_projectiles, self.effects)


        for enemy in list(self.enemies):

            enemy.update(dt, self.player, self.enemy_projectiles, WORLD_RECT)

            if not enemy.alive():

                self.kill_enemy(enemy)

        if self.boss and self.boss.alive():

            self.boss.update(dt, self.player, self.enemy_projectiles, WORLD_RECT, self.enemies, self.spawn_enemy)

        elif self.boss and not self.boss.alive():

            self.win_game()


        self.update_projectiles(dt)

        self.update_items()

        self.update_effects(dt)


        if self.player.hp <= 0:

            self.lose_game()


        if self.stage != 3 and self.stage_kills >= STAGE_INFO[self.stage]['target_kills']:

            self.load_stage(self.stage + 1)

        elif self.stage == 3 and self.stage_kills >= STAGE_INFO[3]['target_kills'] and self.boss is None:

            self.boss = Boss(WORLD_W // 2 - 100, 160)

            self.message = 'Boss xuat hien: Quy Vuong Huyet Nguyet!'


    def spawn_logic(self, dt):

        if self.stage == 3 and self.boss is not None:

            return

        info = STAGE_INFO[self.stage]

        if self.stage_kills + len(self.enemies) >= info['target_kills']:

            return

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:

            self.spawn_enemy()

            self.spawn_timer = info['spawn_interval']


    def update_projectiles(self, dt):

        for proj in list(self.player_projectiles):

            proj.update(dt, WORLD_RECT)

            for enemy in self.enemies_with_boss():

                if proj.alive and enemy.rect.colliderect(proj.rect):

                    enemy.take_damage(proj.damage, burn_time=proj.burn_time)

                    proj.alive = False

                    self.effects.append(Effect(enemy.center()[0], enemy.center()[1], 50, 0.35, (255, 120, 60), 'Burn'))

            if not proj.alive and proj in self.player_projectiles:

                self.player_projectiles.remove(proj)


        for proj in list(self.enemy_projectiles):

            proj.update(dt, WORLD_RECT)

            if proj.alive and self.player.rect.colliderect(proj.rect):

                self.player.take_damage(proj.damage)

                proj.alive = False

            if not proj.alive and proj in self.enemy_projectiles:

                self.enemy_projectiles.remove(proj)


    def update_items(self):

        for item in list(self.items):

            if self.player.rect.colliderect(item.rect):

                if item.item_type == 'exp':

                    self.player.add_exp(item.value)

                elif item.item_type in ('heal_small', 'heal_big'):

                    self.player.heal(item.value)

                elif item.item_type == 'damage_boost':

                    self.player.base_damage += 3

                    self.player.skill_damage_bonus += 5

                elif item.item_type == 'max_hp':

                    self.player.max_hp += item.value

                    self.player.hp += item.value

                self.items.remove(item)


    def update_effects(self, dt):

        for effect in list(self.effects):

            effect.update(dt)

            if not effect.alive():

                self.effects.remove(effect)


    def kill_enemy(self, enemy):

        if enemy in self.enemies:

            self.enemies.remove(enemy)

        self.stage_kills += 1

        self.player.kills += 1

        self.player.add_exp(enemy.exp_reward)

        drop = random_drop(int(enemy.x), int(enemy.y))

        if drop:

            self.items.append(drop)


    def lose_game(self):

        self.sound.play_death_sound()

        self.summary = {'kills': self.player.kills, 'time': self.total_time, 'level': self.player.level, 'stage': self.stage}

        self.state = 'game_over'

        self.sound.play_background_music('menu')


    def win_game(self):

        self.summary = {'kills': self.player.kills, 'time': self.total_time, 'level': self.player.level, 'stage': self.stage}

        self.state = 'victory'

        self.sound.play_background_music('menu')


    def get_camera(self):

        if not self.player:

            return (0, 0)

        sx, sy = self.screen.get_size()

        x = int(self.player.x - sx // 2)

        y = int(self.player.y - sy // 2)

        x = max(0, min(WORLD_W - sx, x))

        y = max(0, min(WORLD_H - sy, y))

        return (x, y)


    def draw_world(self):

        bg = BG_COLORS[self.stage if self.state == 'playing' else 1]

        self.screen.fill(bg)

        camera = self.get_camera() if self.player else (0, 0)

        bg_img = self.backgrounds.get(self.stage)

        if bg_img is not None:

            self.screen.blit(bg_img, (-camera[0], -camera[1]))

        for item in self.items:

            item.draw(self.screen, camera)

        for proj in self.player_projectiles:

            proj.draw(self.screen, camera)

        for proj in self.enemy_projectiles:

            proj.draw(self.screen, camera)

        for enemy in self.enemies:

            enemy.draw(self.screen, camera)

        if self.boss:

            self.boss.draw(self.screen, camera)

        if self.player:

            self.player.draw(self.screen, camera)

        for effect in self.effects:

            effect.draw(self.screen, camera, self.fonts['tiny'])

        if self.player:

            info = STAGE_INFO[self.stage]

            remaining = max(0, info['target_kills'] - self.stage_kills if not (self.stage == 3 and self.boss) else len(self.enemies))

            draw_hud(self.screen, self.fonts, self.player, self.stage, info['name'], remaining, self.total_time, self.boss)


    def draw_menu(self):

        if self.backgrounds.get('menu') is not None:

            self.screen.blit(self.backgrounds['menu'], (0, 0))

        else:

            self.screen.fill((15, 16, 22))

        if self.ui_logo is not None:

            margin = 24

            rect = self.ui_logo.get_rect(bottomright=(self.screen.get_width() - margin, self.screen.get_height() - margin))

            self.screen.blit(self.ui_logo, rect.topleft)

        else:

            draw_text(self.screen, 'TRAN MA SU', self.fonts['large'], (240, 215, 150), self.screen.get_width() // 2, 110, center=True)

        for idx, rect in enumerate(self.menu_buttons()):

            draw_button(self.screen, rect, ['Start Game', 'Settings', 'Exit'][idx], self.fonts['medium'], hovered=(idx == self.selected_menu or rect.collidepoint(pygame.mouse.get_pos())))

        draw_text(self.screen, 'Dieu khien: WASD | Chuot phai | Q E F R', self.fonts['small'], (210, 210, 210), self.screen.get_width() // 2, self.screen.get_height() - 50, center=True)


    def draw_settings(self):

        self.screen.fill((20, 20, 28))

        draw_text(self.screen, 'SETTINGS', self.fonts['large'], (240, 215, 150), self.screen.get_width() // 2, 90, center=True)

        labels = [

            f"Fullscreen: {'On' if self.settings['fullscreen'] else 'Off'}",

            f"Resolution: {self.settings['width']}x{self.settings['height']}",

            'Back'

        ]

        self.selected_settings = max(0, min(self.selected_settings, len(labels) - 1))

        for idx, rect in enumerate(self.settings_buttons()):

            draw_button(self.screen, rect, labels[idx], self.fonts['small'], hovered=(idx == self.selected_settings or rect.collidepoint(pygame.mouse.get_pos())))

        draw_text(self.screen, 'Mui ten trai/phai de dieu chinh. Enter hoac click de doi.', self.fonts['small'], (220, 220, 220), self.screen.get_width() // 2, self.screen.get_height() - 50, center=True)


    def draw_end_screen(self, victory=False):

        key = 'victory' if victory else 'game_over'

        if self.backgrounds.get(key) is not None:

            self.screen.blit(self.backgrounds[key], (0, 0))

        else:

            self.screen.fill((18, 12, 12) if not victory else (12, 24, 16))


        for idx, rect in enumerate(self.end_buttons()):

            draw_button(self.screen, rect, ['Choi lai', 'Thoat'][idx], self.fonts['medium'], hovered=rect.collidepoint(pygame.mouse.get_pos()))


    def menu_buttons(self):

        cx = self.screen.get_width() // 2 - 160

        return [pygame.Rect(cx, 275 + i * 96, 320, 68) for i in range(3)]


    def settings_options(self):

        return ['fullscreen', 'resolution', 'back']


    def settings_buttons(self):


        cx = self.screen.get_width() // 2 - 160

        start_y = 260

        return [pygame.Rect(cx, start_y + i * 88, 320, 60) for i in range(len(self.settings_options()))]


    def end_buttons(self):

        cx = self.screen.get_width() // 2 - 185

        y = self.screen.get_height() - 175

        return [pygame.Rect(cx, y, 170, 60), pygame.Rect(cx + 200, y, 170, 60)]


    def draw(self):

        if self.state == 'menu':

            self.draw_menu()

        elif self.state == 'settings':

            self.draw_settings()

        elif self.state == 'playing':

            self.draw_world()

        elif self.state == 'game_over':

            self.draw_end_screen(victory=False)

        elif self.state == 'victory':

            self.draw_end_screen(victory=True)

        pygame.display.flip()


    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():

                self.handle_event(event)

            self.update(dt)

            self.draw()

        pygame.quit()

        sys.exit()


if __name__ == '__main__':

    Game().run()

