import json

import os


TITLE = 'Tran Ma Su'

DEFAULT_SETTINGS = {

    'music_volume': 0.4,

    'sfx_volume': 0.7,

    'fullscreen': False,

    'width': 1280,

    'height': 720,

    'mute': False,

}

SETTINGS_FILE = 'settings.json'

FPS = 60

PLAYER_SIZE = 112

ENEMY_SIZE = 96

BOSS_SIZE = 280

ITEM_SIZE = 64

PLAYER_BASE_HP = 300

PLAYER_SPEED = 4.5

PLAYER_MELEE_DAMAGE = 18

PLAYER_TALISMAN_DAMAGE = 28

PLAYER_SWORD_BREAK_DAMAGE = 40

PLAYER_FLURRY_HIT_DAMAGE = 12

HEAL_AMOUNT = 45

MELEE_COOLDOWN = 0.25

Q_COOLDOWN = 3.0

E_COOLDOWN = 2.0

F_COOLDOWN = 4.0

R_COOLDOWN = 5.0

LEVEL_EXP = [100, 180, 260, 360, 480]

BG_COLORS = {

    1: (24, 45, 36),

    2: (84, 74, 58),

    3: (54, 18, 22),

}

STAGE_INFO = {

    1: {

        'name': 'Khu Rung Am',

        'target_kills': 9,

        'spawn_interval': 2.0,

        'enemy_pool': ['ghost', 'zombie'],

    },

    2: {

        'name': 'Mieu Hoang',

        'target_kills': 13,

        'spawn_interval': 1.8,

        'enemy_pool': ['ghost', 'zombie', 'fire_demon', 'yaksha'],

    },

    3: {

        'name': 'Huyet Nguyet Dien',

        'target_kills': 17,

        'spawn_interval': 1.6,

        'enemy_pool': ['fire_demon', 'yaksha', 'dark_fiend', 'armored_zombie'],

    },

}

ENEMY_STATS = {

    'ghost': {'name': 'Oan Hon', 'hp': 40, 'damage': 8, 'speed': 1.8, 'color': (170, 220, 255), 'exp': 20},

    'zombie': {'name': 'Tieu Cuong Thi', 'hp': 55, 'damage': 10, 'speed': 1.5, 'color': (120, 180, 120), 'exp': 28},

    'fire_demon': {'name': 'Quy Lua', 'hp': 80, 'damage': 14, 'speed': 1.7, 'color': (255, 120, 60), 'exp': 36},

    'yaksha': {'name': 'Da Xoa', 'hp': 95, 'damage': 16, 'speed': 2.1, 'color': (180, 90, 180), 'exp': 42},

    'dark_fiend': {'name': 'Hac Yeu', 'hp': 130, 'damage': 20, 'speed': 2.3, 'color': (100, 80, 150), 'exp': 56},

    'armored_zombie': {'name': 'Cuong Thi Giap', 'hp': 160, 'damage': 22, 'speed': 1.2, 'color': (90, 90, 100), 'exp': 70},

}

BOSS_STATS = {

    'name': 'Quy Vuong Huyet Nguyet',

    'hp': 600,

    'damage': 25,

    'speed': 1.7,

    'color': (170, 40, 40),

}


def load_settings():

    data = DEFAULT_SETTINGS.copy()

    if os.path.exists(SETTINGS_FILE):

        try:

            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:

                saved = json.load(f)

            for key in data:

                if key in saved:

                    data[key] = saved[key]

        except (json.JSONDecodeError, OSError):

            pass

    return data


def save_settings(data):

    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:

        json.dump(data, f, ensure_ascii=False, indent=2)

