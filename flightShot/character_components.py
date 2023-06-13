# Python 3.7
# character_components.py
# Ian: ianisablackcat@gmail.com
# 2019.03.07

import pygame, time, random, threading
import widgets as ws
import program_data as pd
from pygame.sprite import Sprite
from weapon_components import *


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(0, 0, 35, 35)
        self.rect.centerx, self.rect.top = self.screen_rect.centerx, self.screen_rect.bottom - 55
        self.x, self.y = int(self.rect.centerx), int(self.rect.top)
        self.color_prms, self.player_prms = pd.player_parameters()

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.move_top_right = False
        self.move_bottom_right = False
        self.move_top_left = False
        self.move_bottom_left = False
        self.attack = False
        self.attack_time = time.time()

    def draw(self):
        pygame.draw.polygon(self.screen, self.color_prms['red_1'], [[self.x, self.y - 5],
                                                                     [self.x - 4, self.y + 8],
                                                                     [self.x - 4, self.y + 45],
                                                                     [self.x + 4, self.y + 45],
                                                                     [self.x + 4, self.y + 8]])
        pygame.draw.polygon(self.screen, self.color_prms['red_2'], [[self.x - 5, self.y + 15],
                                                                     [self.x - 20, self.y + 32],
                                                                     [self.x - 20, self.y + 39],
                                                                     [self.x - 5, self.y + 39]])
        pygame.draw.polygon(self.screen, self.color_prms['red_2'], [[self.x + 5, self.y + 15],
                                                                     [self.x + 20, self.y + 32],
                                                                     [self.x + 20, self.y + 41],
                                                                     [self.x + 5, self.y + 41]])
        pygame.draw.polygon(self.screen, self.color_prms['yellow_1'], [[self.x, self.y + 4],
                                                                        [self.x - 2, self.y + 10],
                                                                        [self.x - 2, self.y + 16],
                                                                        [self.x + 2, self.y + 16],
                                                                        [self.x + 2, self.y + 10]])
        pygame.draw.rect(self.screen, self.color_prms['gray_2'], [self.x - 1, self.y + 38, 3, 10])
        pygame.draw.rect(self.screen, self.color_prms['gray_1'], [self.x - 20, self.y + 40, 16, 2])
        pygame.draw.rect(self.screen, self.color_prms['gray_1'], [self.x + 5, self.y + 40, 16, 2])
        pygame.draw.polygon(self.screen, self.color_prms['gray_1'], [[self.x - 17, self.y + 28],
                                                                      [self.x - 16, self.y + 27],
                                                                      [self.x - 16, self.y + 23],
                                                                      [self.x - 17, self.y + 23]])
        pygame.draw.polygon(self.screen, self.color_prms['gray_1'], [[self.x + 17, self.y + 28],
                                                                      [self.x + 16, self.y + 27],
                                                                      [self.x + 16, self.y + 27],
                                                                      [self.x + 17, self.y + 23]])

    def update(self, game_status, player_weapons):
        if self.attack and (time.time()-self.attack_time) > 0.3:
            ws.player_attack(self.screen, game_status, self.x, self.y, player_weapons)
            self.attack_time = time.time()
        if self.move_right and self.x < (self.screen_rect.right - 23):
            self.x += self.player_prms['factor']
            self.rect.centerx = self.x
        elif self.move_left and self.x > 23:
            self.x -= self.player_prms['factor']
            self.rect.centerx = self.x
        elif self.move_up and self.y > 10:
            self.y -= self.player_prms['factor']
            self.rect.y = self.y
        elif self.move_down and self.y < (self.screen_rect.bottom - 50):
            self.y += self.player_prms['factor']
            self.rect.y = self.y
        elif self.move_top_right and self.x < (self.screen_rect.right - 23) and self.y > 10:
            self.x += self.player_prms['factor'] / 2
            self.y -= self.player_prms['factor'] / 2
            self.rect.centerx = self.x
            self.rect.y = self.y
        elif self.move_bottom_right and self.x < (self.screen_rect.right - 24) and self.y < (
                self.screen_rect.bottom - 50):
            self.x += self.player_prms['factor'] / 2
            self.y += self.player_prms['factor'] / 2
            self.rect.centerx = self.x
            self.rect.y = self.y
        elif self.move_top_left and self.x > 23 and self.y > 10:
            self.x -= self.player_prms['factor'] / 2
            self.y -= self.player_prms['factor'] / 2
            self.rect.centerx = self.x
            self.rect.y = self.y
        elif self.move_bottom_left and self.x > 23 and self.y < (self.screen_rect.bottom - 50):
            self.x -= self.player_prms['factor'] / 2
            self.y += self.player_prms['factor'] / 2
            self.rect.centerx = self.x
            self.rect.y = self.y

    def forward_direction(self, direction):
        if direction == 'right':
            self.move_right = True
        elif direction == 'left':
            self.move_left = True
        elif direction == 'up':
            self.move_up = True
        elif direction == 'down':
            self.move_down = True
        elif direction == 'top_right':
            self.move_top_right = True
        elif direction == 'bottom_right':
            self.move_bottom_right = True
        elif direction == 'top_left':
            self.move_top_left = True
        elif direction == 'bottom_left':
            self.move_bottom_left = True

    def stop_direction(self, direction):
        if direction == 'right':
            self.move_right = False
        elif direction == 'left':
            self.move_left = False
        elif direction == 'up':
            self.move_up = False
        elif direction == 'down':
            self.move_down = False
        elif direction == 'top_right':
            self.move_top_right = False
        elif direction == 'bottom_right':
            self.move_bottom_right = False
        elif direction == 'top_left':
            self.move_top_left = False
        elif direction == 'bottom_left':
            self.move_bottom_left = False

    def reset_position(self, game_status):
        self.x = self.screen_rect.centerx
        self.y = self.screen_rect.bottom - 55
        self.rect.centerx = self.x
        self.rect.top = self.y
        game_status.set_bonus(99)


class Enemy(Sprite):
    def __init__(self, screen, stage_enemy_prms, script):
        super(Enemy, self).__init__()
        self.screen = screen
        self.fighter_factor = stage_enemy_prms['enemy_fighter_factor']
        self.bullet_factor = stage_enemy_prms['enemy_bullet_factor']
        self.fire_rate = stage_enemy_prms['enemy_fire_rate']
        self.color_prms, self.bullet_prms = pd.enemy_parameters()
        self.screen_rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, 31, 40)
        self.rect.centerx, self.rect.top = script['loc_x'], script['loc_y']
        self.x, self.y = int(self.rect.centerx), int(self.rect.top)
        self.move_mode = script['move_mode']
        self.attack_mode = script['attack_mode']
        self.bonus = script['bonus']
        self.fire_time_count = time.time()

    def draw(self):
        pygame.draw.polygon(self.screen, self.color_prms['gray_3'], [[self.rect.centerx - 24, self.rect.top + 28],
                                                                     [self.rect.centerx + 24, self.rect.top + 28],
                                                                     [self.rect.centerx + 24, self.rect.top + 23],
                                                                     [self.rect.centerx, self.rect.top + 18],
                                                                     [self.rect.centerx - 24, self.rect.top + 23]])
        pygame.draw.polygon(self.screen, self.color_prms['gray_3'], [[self.rect.centerx - 11, self.rect.top + 8],
                                                                     [self.rect.centerx + 11, self.rect.top + 8],
                                                                     [self.rect.centerx + 11, self.rect.top + 6],
                                                                     [self.rect.centerx, self.rect.top + 3],
                                                                     [self.rect.centerx - 11, self.rect.top + 6]])
        pygame.draw.ellipse(self.screen, self.color_prms['gray_1'], [self.rect.centerx - 5, self.rect.top, 11, 45])
        pygame.draw.polygon(self.screen, self.color_prms['white'], [[self.rect.centerx, self.rect.top + 35],
                                                                    [self.rect.centerx - 1, self.rect.top + 32],
                                                                    [self.rect.centerx - 1, self.rect.top + 27],
                                                                    [self.rect.centerx + 1, self.rect.top + 27],
                                                                    [self.rect.centerx + 1, self.rect.top + 32]])
        pygame.draw.rect(self.screen, self.color_prms['gray_3'], [self.rect.centerx - 8, self.rect.top + 40, 16, 2])

    def update(self, enemy_weapons):
        if self.move_mode == 1:
            self.x -= self.fighter_factor
            self.y += self.fighter_factor
            self.rect.centerx = self.x
            self.rect.top = self.y
        elif self.move_mode == 2:
            self.y += self.fighter_factor
            self.rect.top = self.y
        elif self.move_mode == 3:
            self.x += self.fighter_factor
            self.y += self.fighter_factor
            self.rect.centerx = self.x
            self.rect.top = self.y
        if (time.time() - self.fire_time_count) >= self.fire_rate:
            self.fire_bullet(enemy_weapons, self.x, self.y + 45)
            self.fire_time_count = time.time()

    def fire_bullet(self, enemy_weapons, x, y):
        new_bullet = EnemyBullet(self.screen, self.bullet_prms, self.bullet_factor, x, y)
        enemy_weapons.add(new_bullet)


class Boss(Sprite):
    def __init__(self, screen, game_status, stage_enemy_prms):
        super(Boss, self).__init__()
        self.screen = screen
        self.game_status = game_status
        self.boss_prms, self.bullet_direction = pd.boss_parameters()
        self.x, self.y = random.randint(50, 950), random.randint(50, 400)
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (self.x, self.y)
        self.pic_number = 1
        self.boss_img = pygame.image.load('images/boss_1.png').convert_alpha()
        self.boss_rect = self.boss_img.get_rect()
        self.boss_rect.center = self.rect.center
        self.life_value = self.boss_prms['life_value']
        self.factor = stage_enemy_prms['boss_factor']
        self.bullet_factor = stage_enemy_prms['boss_bullet_factor']
        self.fire_rate = stage_enemy_prms['boss_fire_rate']
        self.fire_time_count = time.time()
        self.fire_type = 1
        self.act_factor_x = 0.2
        self.act_factor_y = 0.2

    def draw(self):
        self.screen.blit(self.boss_img, self.boss_rect)

    def update(self, player, enemy_weapons):
        if self.x < 0: self.act_factor_x = self.factor * 0.2
        elif self.x > 1000: self.act_factor_x = self.factor * -1 * 0.2
        if self.y < 0: self.act_factor_y = self.factor * 0.2
        elif self.y > 500: self.act_factor_y = self.factor * -1 * 0.2
        self.x += self.act_factor_x
        self.y += self.act_factor_y
        self.boss_rect.center = self.rect.center = (self.x, self.y)
        if (time.time() - self.fire_time_count) >= self.fire_rate:
            if self.fire_type == 1:
                another = threading.Thread(target=self.fire_bullets, args=(player, enemy_weapons))
                another.start()
                self.fire_type = 2
                self.fire_time_count = time.time()
            elif self.fire_type == 2:
                self.fire_circle_bullets(enemy_weapons)
                self.fire_type = 1
                self.fire_time_count = time.time()

    def fire_bullets(self, player, enemy_weapons):
        for num in range(0, 5):
            new_bullet = BossBullet(self.screen, self.boss_prms, self.bullet_factor, self.boss_rect.centerx,
                                    self.boss_rect.bottom, player.x, player.y)
            enemy_weapons.add(new_bullet)
            time.sleep(0.3)

    def fire_circle_bullets(self, enemy_weapons):
        if self.x > 500:
            for x, y in zip(self.bullet_direction[0], self.bullet_direction[1]):
                new_circle_bullet = BossCircleBullet(self.screen, self.boss_prms, self.bullet_factor,
                                                     self.boss_rect.centerx, self.boss_rect.bottom, x, y)
                enemy_weapons.add(new_circle_bullet)
        else:
            for x, y in zip(self.bullet_direction[2], self.bullet_direction[3]):
                new_circle_bullet = BossCircleBullet(self.screen, self.boss_prms, self.bullet_factor,
                                                     self.boss_rect.centerx, self.boss_rect.bottom, x, y)
                enemy_weapons.add(new_circle_bullet)

    def hitted(self, num):
        self.life_value -= num

    def is_live(self):
        if self.life_value <= 0:
            return False
        else:
            return True


class Star:
    def __init__(self, screen, factor):
        self.screen = screen
        self.factor = factor
        self.x = random.randint(5, 996)
        self.y = random.randint(10, 720)

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), [self.x, self.y, 2, 2], 1)

    def update(self):
        self.y += (1*self.factor)
