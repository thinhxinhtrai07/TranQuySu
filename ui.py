import pygame

from asset_loader import try_load_ui_image


_UI_CACHE = {}


def _get_ui_image(filename, size):

    key = (filename, size)

    if key not in _UI_CACHE:

        _UI_CACHE[key] = try_load_ui_image(filename, size=size)

    return _UI_CACHE[key]


def _get_ui_image_stretched(filename, size):

    """Load UI image and stretch it exactly to size.

    Used for button.png because the button needs to be wider horizontally.
    The normal asset loader keeps image ratio, so increasing width alone
    would not make the button visibly longer.
    """

    key = (filename, size, 'stretch')

    if key not in _UI_CACHE:

        img = try_load_ui_image(filename, size=None)

        if img is not None:

            img = pygame.transform.smoothscale(img, size)

        _UI_CACHE[key] = img

    return _UI_CACHE[key]


def draw_bar(screen, x, y, w, h, ratio, color, bg=(40, 40, 40), border=(255, 255, 255)):

    pygame.draw.rect(screen, bg, (x, y, w, h), border_radius=6)

    pygame.draw.rect(screen, color, (x, y, int(w * max(0, min(1, ratio))), h), border_radius=6)

    pygame.draw.rect(screen, border, (x, y, w, h), 2, border_radius=6)


def draw_text(screen, text, font, color, x, y, center=False):

    surf = font.render(text, True, color)

    rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))

    screen.blit(surf, rect)

    return rect


def draw_button(screen, rect, text, font, hovered=False):

    draw_rect = pygame.Rect(rect.x, rect.y, int(rect.w * 1.20), rect.h)

    draw_rect.center = rect.center

    button_img = _get_ui_image_stretched('button.png', (draw_rect.w, draw_rect.h))

    if button_img is not None:


        screen.blit(button_img, draw_rect.topleft)

    else:


        pygame.draw.rect(screen, (70, 50, 34), draw_rect, border_radius=14)

    draw_text(screen, text, font, (245, 240, 220), draw_rect.centerx, draw_rect.centery, center=True)


def draw_hud(screen, fonts, player, stage_no, stage_name, enemies_left, time_elapsed, boss=None):


    panel_rect = pygame.Rect(12, 8, 370, 175)

    panel = _get_ui_image_stretched('panel.png', (panel_rect.w, panel_rect.h))

    if panel is not None:

        screen.blit(panel, panel_rect.topleft)

    else:

        pygame.draw.rect(screen, (0, 0, 0, 120), panel_rect, border_radius=16)


    left = 68

    bar_w = 250


    hp_y = 34

    exp_y = 63


    draw_bar(screen, left, hp_y, bar_w, 20, player.hp / player.max_hp, (200, 40, 40))

    draw_text(screen, f'HP: {int(player.hp)} / {player.max_hp}', fonts['tiny'], (255, 245, 235), left + 8, hp_y + 2)


    draw_bar(screen, left, exp_y, bar_w, 16, player.exp / player.exp_to_next, (70, 160, 240))

    draw_text(screen, f'EXP: {player.exp} / {player.exp_to_next}   Lv {player.level}', fonts['tiny'], (235, 245, 255), left + 8, exp_y - 1)


    info_x = left

    draw_text(screen, f'Enemies left: {enemies_left}', fonts['tiny'], (255, 245, 205), info_x, 106)


    x = 24

    y = screen.get_height() - 78

    icon_map = {'q': 'icon_q.png', 'e': 'icon_e.png', 'f': 'icon_f.png', 'r': 'icon_r.png'}

    for skill, label in [('q', 'Q'), ('e', 'E'), ('f', 'F'), ('r', 'R')]:

        rect = pygame.Rect(x, y, 72, 60)

        ready = player.cooldowns[skill] <= 0

        pygame.draw.rect(screen, (40, 90, 40) if ready else (80, 40, 40), rect, border_radius=10)

        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)

        icon = _get_ui_image(icon_map[skill], (36, 36))

        if icon is not None:

            screen.blit(icon, (rect.x + 6, rect.y + 12))

        cd_text = label if ready else f'{player.cooldowns[skill]:.1f}'

        draw_text(screen, cd_text, fonts['tiny'], (255, 255, 255), rect.x + 52, rect.centery, center=True)

        x += 82


    if boss:

        draw_bar(screen, screen.get_width() // 2 - 240, 18, 480, 24, boss.hp / boss.max_hp, (160, 30, 30), bg=(30, 15, 15), border=(220, 180, 180))

        draw_text(screen, boss.name + f' - Phase {boss.phase}', fonts['small'], (255, 210, 210), screen.get_width() // 2, 48, center=True)

