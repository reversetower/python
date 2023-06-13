# Python 3.7
# stage_components.py
# Ian: ianisablackcat@gmail.com
# 2019.03.07

import pygame, threading, time, random
import widgets as ws
import scripts_data as sp
import program_data as pd
import update as ud
from pygame.sprite import Group
from character_components import *


class OpeningPage:
    def __init__(self, screen, game_status):
        self.screen = screen
        self.game_status = game_status
        self.op_imgs, self.op_rects, self.op_press = pd.opening_page_parameters(self.screen)
        self.op_flash_time = 0
        self.op_flash_ctrl = True

    def play_stage(self):
        while True:
            if not self.game_status.get_current_scenes() == 0: break
            ws.op_key_events(self.game_status)
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()

    def draw(self):
        if not self.op_flash_ctrl and (time.time() - self.op_flash_time > 0.8):
            self.op_flash_ctrl = True
            self.op_flash_time = time.time()
        elif self.op_flash_ctrl and (time.time() - self.op_flash_time > 1.2):
            self.op_flash_ctrl = False
            self.op_flash_time = time.time()

        for img, rect in zip(self.op_imgs, self.op_rects):
            self.screen.blit(img, rect)
        if self.op_flash_ctrl: self.screen.blit(self.op_press[0], self.op_press[1])


class Stage:
    def __init__(self, screen, game_status, stage_enemy_prms, boss_amount):
        self.screen = screen
        self.game_status = game_status
        self.stage_enemy_prms = stage_enemy_prms
        self.boss_amount = boss_amount
        self.enemies = Group()
        self.player_weapons = Group()
        self.bombs = Group()
        self.enemy_weapons = Group()
        self.bonuses = Group()
        self.bosses = Group()
        self.explode = Group()
        self.stars = []
        self.player = Player(self.screen)
        self.stage_scripts = sp.stage_01_scripts()
        self.script_time = 0
        self.script_marker = 0
        self.stage_clear = False
        self.game_status.set_stage_boss_amount(self.boss_amount)
        self.show_info = ShowStatusInfo(screen, game_status)

    def play_stage(self):
        script_control = threading.Thread(target=self.script_line_control)
        script_control.start()
        while True:
            if not self.game_status.get_game_active() or self.stage_clear:
                self.game_status.jump_to_settle_page()
                time.sleep(0.5)
                break
            if not self.game_status.get_current_scenes() == self.stage_enemy_prms['stage']: break
            ws.make_star(self.screen, self.stars, self.stage_enemy_prms['stage'])
            ws.game_key_events(self.screen, self.game_status, self.player, self.player_weapons, self.bombs)
            ud.update_game_screen_event(self.screen, self.game_status, self.player, self.enemies, self.bosses,
                                        self.player_weapons, self.bombs, self.enemy_weapons, self.bonuses, self.show_info,
                                        self.stars, self.explode)
            character_status = self.game_status.get_character_status()
            if character_status['remain_life'] < 0: self.game_status.set_gameover()
            if character_status['remain_boss'] == 0:
                self.stage_clear = True
                if self.game_status.get_current_scenes() == 3: self.game_status.set_gameover()

    def script_line_control(self):
        while True:
            time.sleep(1)
            if self.script_marker == 15:
                for num in range(0, self.boss_amount):
                    new_boss = Boss(self.screen, self.game_status, self.stage_enemy_prms)
                    self.bosses.add(new_boss)
            if self.script_marker >= len(self.stage_scripts):
                now_script = self.stage_scripts[self.script_marker % len(self.stage_scripts)]
                print(now_script)
            else:
                now_script = self.stage_scripts[self.script_marker]
                print(now_script)
            self.performance(now_script)
            self.script_marker += 1
            if not self.game_status.get_game_active(): break
            if self.game_status.get_current_scenes() == 99: break

    def performance(self, script):
        if script == 0:
            return
        if script['qua'] == 1:
            new_enemy = Enemy(self.screen, self.stage_enemy_prms, script)
            self.enemies.add(new_enemy)
        else:
            temp_script = script.copy()
            for num in range(temp_script['qua']):
                temp_script['loc_x'] += 80
                new_enemy = Enemy(self.screen, self.stage_enemy_prms, temp_script)
                self.enemies.add(new_enemy)


class SettlePage:
    def __init__(self, screen, game_status):
        self.screen = screen
        self.game_status = game_status
        self.game_active = self.game_status.get_game_active()
        self.stl_imgs, self.stl_rects, self.graphics_data = pd.settle_page_parameters(self.screen, self.game_active,
                                                                                      self.game_status.get_game_score())
        self.stl_flash_time = 0
        self.stl_flash_ctrl = True

        self.boss_img = pygame.image.load('images/boss_2.png').convert_alpha()
        self.boss_rect = self.boss_img.get_rect()
        self.boss_rect.center = (self.graphics_data['boss_x'], self.graphics_data['boss_y'])

    def play_stage(self):
        time.sleep(1)
        pygame.event.clear()
        while True:
            if not self.game_status.get_current_scenes() == 99: break
            ws.stl_key_events(self.game_status)
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
        time.sleep(0.5)
        pygame.event.clear()

    def draw(self):
        for num in range(0, 6):
            self.screen.blit(self.stl_imgs[num], self.stl_rects[num])
        if self.game_active:
            if not self.stl_flash_ctrl and (time.time() - self.stl_flash_time > 0.8):
                self.stl_flash_ctrl = True
                self.stl_flash_time = time.time()
            elif self.stl_flash_ctrl and (time.time() - self.stl_flash_time > 1.2):
                self.stl_flash_ctrl = False
                self.stl_flash_time = time.time()
            if self.stl_flash_ctrl: self.screen.blit(self.stl_imgs[6], self.stl_rects[6])

        pygame.draw.polygon(self.screen, self.graphics_data['gray_3'],
                            [[self.graphics_data['enemy_x']-24, self.graphics_data['enemy_y']+28],
                             [self.graphics_data['enemy_x']+24, self.graphics_data['enemy_y']+28],
                             [self.graphics_data['enemy_x']+24, self.graphics_data['enemy_y']+23],
                             [self.graphics_data['enemy_x'], self.graphics_data['enemy_y']+18],
                             [self.graphics_data['enemy_x']-24, self.graphics_data['enemy_y']+23]])
        pygame.draw.polygon(self.screen, self.graphics_data['gray_3'],
                            [[self.graphics_data['enemy_x']-11, self.graphics_data['enemy_y']+8],
                             [self.graphics_data['enemy_x']+11, self.graphics_data['enemy_y']+8],
                             [self.graphics_data['enemy_x']+11, self.graphics_data['enemy_y']+6],
                             [self.graphics_data['enemy_x'], self.graphics_data['enemy_y']+3],
                             [self.graphics_data['enemy_x']-11, self.graphics_data['enemy_y']+6]])
        pygame.draw.ellipse(self.screen, self.graphics_data['gray_1'],
                            [self.graphics_data['enemy_x']-5, self.graphics_data['enemy_y'], 11, 45])
        pygame.draw.polygon(self.screen, self.graphics_data['white'],
                            [[self.graphics_data['enemy_x'], self.graphics_data['enemy_y']+35],
                             [self.graphics_data['enemy_x']-1, self.graphics_data['enemy_y']+32],
                             [self.graphics_data['enemy_x']-1, self.graphics_data['enemy_y']+27],
                             [self.graphics_data['enemy_x']+1, self.graphics_data['enemy_y']+27],
                             [self.graphics_data['enemy_x']+1, self.graphics_data['enemy_y']+32]])
        pygame.draw.rect(self.screen, self.graphics_data['gray_3'],
                         [self.graphics_data['enemy_x']-8, self.graphics_data['enemy_y']+40, 16, 2])

        self.screen.blit(self.boss_img, self.boss_rect)


class ShowStatusInfo:
    def __init__(self, screen, game_status):
        self.screen = screen
        self.game_status = game_status
        self.color_prms = pd.show_status_info_parameters()
        self.character_status = self.game_status.get_character_status()
        self.remain_font = pygame.font.Font("font/comic.ttf", 30)
        self.remain_life = str(self.character_status['remain_life'])
        self.remain_bomb = str(self.character_status['remain_bomb'])
        self.remain_life_img = self.remain_font.render(self.remain_life, True, self.color_prms['white'])
        self.remain_bomb_img = self.remain_font.render(self.remain_bomb, True, self.color_prms['white'])
        self.remain_life_rect = self.remain_life_img.get_rect()
        self.remain_life_rect.center = (980, 690)
        self.remain_bomb_rect = self.remain_bomb_img.get_rect()
        self.remain_bomb_rect.center = (30, 690)

    def draw(self):
        pygame.draw.circle(self.screen, self.color_prms['red_1'], (950, 700), 10)
        pygame.draw.circle(self.screen, self.color_prms['red_1'], (960, 700), 10)
        pygame.draw.polygon(self.screen, self.color_prms['red_1'], [(940, 700), (955, 715), (970, 700)])
        pygame.draw.circle(self.screen, self.color_prms['blue_1'], (15, 693), 5)
        pygame.draw.polygon(self.screen, self.color_prms['blue_1'], [(10, 693), (10, 713), (20, 713), (20, 693)])
        self.screen.blit(self.remain_life_img, self.remain_life_rect)
        self.screen.blit(self.remain_bomb_img, self.remain_bomb_rect)

    def update(self):
        self.character_status = self.game_status.get_character_status()
        self.remain_life = str(self.character_status['remain_life'])
        self.remain_bomb = str(self.character_status['remain_bomb'])
        self.remain_life_img = self.remain_font.render(self.remain_life, True, self.color_prms['white'])
        self.remain_bomb_img = self.remain_font.render(self.remain_bomb, True, self.color_prms['white'])
        self.remain_life_rect = self.remain_life_img.get_rect()
        self.remain_life_rect.center = (985, 700)
        self.remain_bomb_rect = self.remain_bomb_img.get_rect()
        self.remain_bomb_rect.center = (40, 700)
