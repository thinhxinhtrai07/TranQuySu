import os

import pygame


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

MUSIC_DIR = os.path.join(ASSETS_DIR, 'music')


PLAYER_DIR = os.path.join(IMAGES_DIR, 'player')

ENEMIES_DIR = os.path.join(IMAGES_DIR, 'enemies')

BOSS_DIR = os.path.join(IMAGES_DIR, 'boss')

ITEMS_DIR = os.path.join(IMAGES_DIR, 'items')

SKILLS_DIR = os.path.join(IMAGES_DIR, 'skills')

UI_DIR = os.path.join(IMAGES_DIR, 'ui')

MAPS_DIR = os.path.join(IMAGES_DIR, 'maps')


def get_asset_path(*parts):

    return os.path.join(ASSETS_DIR, *parts)


def get_image_path(folder, filename):

    return os.path.join(IMAGES_DIR, folder, filename)


def get_sound_path(filename):

    return os.path.join(SOUNDS_DIR, filename)


def get_music_path(filename):

    return os.path.join(MUSIC_DIR, filename)


def get_player_path(filename):

    return os.path.join(PLAYER_DIR, filename)


def get_enemy_path(filename):

    return os.path.join(ENEMIES_DIR, filename)


def get_boss_path(filename):

    return os.path.join(BOSS_DIR, filename)


def get_item_path(filename):

    return os.path.join(ITEMS_DIR, filename)


def get_skill_path(filename):

    return os.path.join(SKILLS_DIR, filename)


def get_ui_path(filename):

    return os.path.join(UI_DIR, filename)


def get_map_path(filename):

    return os.path.join(MAPS_DIR, filename)


def get_player_pose_path(pose, direction):

    return get_player_path(f'player_{pose}_{direction}.png')


def get_player_idle_path(direction='right'):

    return get_player_pose_path('idle', direction)


def get_player_walk_path(direction='right'):

    return get_player_pose_path('walk', direction)


def get_player_attack_path(direction='right'):

    return get_player_pose_path('attack', direction)


def get_player_cast_path(direction='right'):

    return get_player_pose_path('cast', direction)


def get_player_skill_path(direction='right'):

    return get_player_pose_path('skill', direction)


def file_exists(path):

    return os.path.exists(path)


def require_file(path):

    if not os.path.exists(path):

        raise FileNotFoundError(f'Khong tim thay file asset: {path}')

    return path


def ensure_asset_folders():

    for folder in [ASSETS_DIR, IMAGES_DIR, SOUNDS_DIR, MUSIC_DIR, PLAYER_DIR, ENEMIES_DIR, BOSS_DIR, ITEMS_DIR, SKILLS_DIR, UI_DIR, MAPS_DIR]:

        os.makedirs(folder, exist_ok=True)


def _trim_transparent(image):

    try:

        rect = image.get_bounding_rect(min_alpha=1)

    except TypeError:

        rect = image.get_bounding_rect()

    if rect.width > 0 and rect.height > 0:

        image = image.subsurface(rect).copy()

    return image


def scale_keep_ratio(image, target_size):

    tw, th = target_size

    iw, ih = image.get_size()

    if iw <= 0 or ih <= 0:

        return image

    scale = min(tw / iw, th / ih)

    nw = max(1, int(iw * scale))

    nh = max(1, int(ih * scale))

    image = pygame.transform.smoothscale(image, (nw, nh))

    canvas = pygame.Surface((tw, th), pygame.SRCALPHA)

    canvas.blit(image, ((tw - nw) // 2, (th - nh) // 2))

    return canvas


def load_image(path, size=None, convert_alpha=True, trim=True):

    require_file(path)

    image = pygame.image.load(path)

    image = image.convert_alpha() if convert_alpha else image.convert()

    if trim and convert_alpha:

        image = _trim_transparent(image)

    if size is not None:

        image = scale_keep_ratio(image, size)

    return image


def try_load_image(path, size=None, convert_alpha=True, trim=True):

    if not file_exists(path):

        return None

    return load_image(path, size=size, convert_alpha=convert_alpha, trim=trim)


def load_player_image(filename, size=None):

    return load_image(get_player_path(filename), size=size, convert_alpha=True)


def try_load_player_image(filename, size=None):

    return try_load_image(get_player_path(filename), size=size, convert_alpha=True)


def load_enemy_image(filename, size=None):

    return load_image(get_enemy_path(filename), size=size, convert_alpha=True)


def try_load_enemy_image(filename, size=None):

    return try_load_image(get_enemy_path(filename), size=size, convert_alpha=True)


def load_boss_image(filename, size=None):

    return load_image(get_boss_path(filename), size=size, convert_alpha=True)


def try_load_boss_image(filename, size=None):

    return try_load_image(get_boss_path(filename), size=size, convert_alpha=True)


def load_item_image(filename, size=None):

    return load_image(get_item_path(filename), size=size, convert_alpha=True)


def try_load_item_image(filename, size=None):

    return try_load_image(get_item_path(filename), size=size, convert_alpha=True)


def load_skill_image(filename, size=None):

    return load_image(get_skill_path(filename), size=size, convert_alpha=True)


def try_load_skill_image(filename, size=None):

    return try_load_image(get_skill_path(filename), size=size, convert_alpha=True)


def load_ui_image(filename, size=None):

    return load_image(get_ui_path(filename), size=size, convert_alpha=True)


def try_load_ui_image(filename, size=None):

    return try_load_image(get_ui_path(filename), size=size, convert_alpha=True)


def load_map_image(filename, size=None):

    return load_image(get_map_path(filename), size=size, convert_alpha=False, trim=False)


def try_load_map_image(filename, size=None):

    return try_load_image(get_map_path(filename), size=size, convert_alpha=False, trim=False)


def load_player_pose(pose, direction, size=None):

    return load_image(get_player_pose_path(pose, direction), size=size, convert_alpha=True)


def try_load_player_pose(pose, direction, size=None):

    return try_load_image(get_player_pose_path(pose, direction), size=size, convert_alpha=True)


def load_player_pose_set(size=None, allow_flip_fallback=True):

    poses = {pose: {'right': None, 'left': None} for pose in ('idle', 'walk', 'attack', 'cast', 'skill')}

    for pose in poses:

        poses[pose]['right'] = try_load_player_pose(pose, 'right', size=size)

        poses[pose]['left'] = try_load_player_pose(pose, 'left', size=size)

        if allow_flip_fallback:

            if poses[pose]['left'] is None and poses[pose]['right'] is not None:

                poses[pose]['left'] = pygame.transform.flip(poses[pose]['right'], True, False)

            if poses[pose]['right'] is None and poses[pose]['left'] is not None:

                poses[pose]['right'] = pygame.transform.flip(poses[pose]['left'], True, False)

    return poses


def get_default_asset_manifest():

    return {

        'player': {

            'idle_right': get_player_idle_path('right'),

            'idle_left': get_player_idle_path('left'),

            'walk_right': get_player_walk_path('right'),

            'walk_left': get_player_walk_path('left'),

            'attack_right': get_player_attack_path('right'),

            'attack_left': get_player_attack_path('left'),

            'cast_right': get_player_cast_path('right'),

            'cast_left': get_player_cast_path('left'),

            'skill_right': get_player_skill_path('right'),

            'skill_left': get_player_skill_path('left'),

        },

        'enemies': {

            'ghost': get_enemy_path('ghost.png'),

            'zombie': get_enemy_path('zombie.png'),

            'fire_demon': get_enemy_path('fire_demon.png'),

            'yaksha': get_enemy_path('yaksha.png'),

            'dark_fiend': get_enemy_path('dark_fiend.png'),

            'armored_zombie': get_enemy_path('armored_zombie.png'),

        },

        'boss': {'blood_moon_king': get_boss_path('blood_moon_king.png')},

        'items': {

            'potion_small': get_item_path('potion_small.png'),

            'potion_big': get_item_path('potion_big.png'),

            'exp_orb': get_item_path('exp_orb.png'),

            'damage_orb': get_item_path('damage_orb.png'),

            'max_hp_orb': get_item_path('max_hp_orb.png'),

        },

        'skills': {

            'talisman_fire': get_skill_path('talisman_fire.png'),

            'sword_break': get_skill_path('sword_break.png'),

            'flurry': get_skill_path('flurry.png'),

            'heal': get_skill_path('heal.png'),

        },

        'ui': {

            'icon_q': get_ui_path('icon_q.png'),

            'icon_e': get_ui_path('icon_e.png'),

            'icon_f': get_ui_path('icon_f.png'),

            'icon_r': get_ui_path('icon_r.png'),

            'button': get_ui_path('button.png'),

            'panel': get_ui_path('panel.png'),

            'logo': get_ui_path('logo.png'),

            'cursor': get_ui_path('cursor.png'),

        },

        'maps': {

            'forest': get_map_path('forest_bg.png'),

            'temple': get_map_path('temple_bg.png'),

            'blood_moon_palace': get_map_path('blood_moon_palace_bg.png'),

            'menu': get_map_path('menu_bg.png'),

            'game_over': get_map_path('game_over_bg.png'),

            'victory': get_map_path('victory_bg.png'),

        },

    }


ensure_asset_folders()

