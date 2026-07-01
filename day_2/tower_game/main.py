"""
塔防游戏 - Tower Defense Game
基于Pygame实现的塔防游戏
"""
import pygame
import math
import random
import sys

# ============================================================
# 初始化
# ============================================================
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("塔防游戏 - Tower Defense")

# ============================================================
# 常量
# ============================================================
SCREEN_W = 960
SCREEN_H = 640
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN_D = (50, 200, 50)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 0, 255)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK = (40, 40, 40)
LGRAY = (200, 200, 200)

# ============================================================
# 虚拟坐标系 — 0 到 5000
# 现在所有路径和塔区都在 0-5000 虚拟坐标系内定义，再映射到实际屏幕。
# ============================================================
VIRTUAL_W = 5000
VIRTUAL_H = 5000
ROUTE_SHIFT_X = 100


def to_screen(pt):
    return (
        max(0, int((pt[0] - ROUTE_SHIFT_X) * SCREEN_W / VIRTUAL_W)),
        int(pt[1] * SCREEN_H / VIRTUAL_H),
    )


def rect_to_screen(x, y, w, h):
    return pygame.Rect(
        int(x * SCREEN_W / VIRTUAL_W),
        int(y * SCREEN_H / VIRTUAL_H),
        max(1, int(w * SCREEN_W / VIRTUAL_W)),
        max(1, int(h * SCREEN_H / VIRTUAL_H)),
    )

# 箭头标记的关键路线节点，已固定到图像上的格子坐标。
ROUTE_START = (0, 3101)               # 怪物出生点，起始位置
ROUTE_FORK1 = (1250, 3101)            # 第一个分岔点入口，怪物先到达这里
ROUTE_FORK1_UP = (1250, 1900)         # 第一个分岔点向上分支
ROUTE_FORK1_RIGHT = (1723, 3101)      # 第一个分岔点向右分支
ROUTE_FIRST_MERGE = (1723, 1900)      # 第一个分岔后汇合点
ROUTE_AFTER_MERGE_RIGHT = (2400, 1900) # 第一个汇合之后的向右移动节点
ROUTE_AFTER_MERGE_DOWN = (2400, 3050) # 向右后向下的转折点
ROUTE_FORK2 = (3100, 3050)            # 第二个分岔点入口
ROUTE_FORK2_UP = (3100, 1000)         # 第二个分岔点向上分支起点
ROUTE_FORK2_RIGHT = (3850, 3050)      # 第二个分岔点向右分支起点
ROUTE_SECOND_MERGE = (3850, 1000)     # 第二个分岔后汇合点
ROUTE_END = (4522, 1000)              # 终点，怪物到达则失败

VIRTUAL_ROUTES = [
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_UP,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_UP,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_RIGHT,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_UP,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_UP,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_RIGHT,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
    [
        ROUTE_START,
        ROUTE_FORK1,
        ROUTE_FORK1_RIGHT,
        ROUTE_FIRST_MERGE,
        ROUTE_AFTER_MERGE_RIGHT,
        ROUTE_AFTER_MERGE_DOWN,
        ROUTE_FORK2,
        ROUTE_FORK2_RIGHT,
        ROUTE_SECOND_MERGE,
        ROUTE_END,
    ],
]

ROUTES = [[to_screen(pt) for pt in route] for route in VIRTUAL_ROUTES]

ROAD_W = 48

VIRTUAL_TOWER_ZONES = [
    (0, 0, 1375, 1203),
    (3101, 0, 1721, 1203),
    (0, 3800, 4822, 1022),
]

TOWER_ZONES = [rect_to_screen(*zone) for zone in VIRTUAL_TOWER_ZONES]

# ============================================================
# 配置
# ============================================================
TOWERS_CFG = {
    'normal': {'name': '普通炮塔', 'cost': 100, 'range': 160, 'dmg': 25,
                'cd': 28, 'color': YELLOW, 'bullet_speed': 10, 'splash': 0},
    'flame':  {'name': '火焰炮塔', 'cost': 150, 'range': 140, 'dmg': 50,
                'cd': 45, 'color': ORANGE, 'bullet_speed': 7, 'splash': 28},
    'freeze': {'name': '冰冻炮塔', 'cost': 120, 'range': 145, 'dmg': 12,
                'cd': 38, 'color': CYAN, 'bullet_speed': 8, 'splash': 0,
                'slow': 0.35, 'slow_len': 90},
}

ENEMY_CFG = {
    'normal': {'hp': 60, 'spd': 1.6, 'reward': 20, 'color': RED,
               'img': 'normal_enemy.png', 'r': 12},
    'fast':   {'hp': 35, 'spd': 3.0, 'reward': 15, 'color': PURPLE,
               'img': 'fast_enemy.png', 'r': 10},
    'boss':   {'hp': 350, 'spd': 0.9, 'reward': 80, 'color': (180, 20, 20),
               'img': 'boss_enemy.png', 'r': 18},
}

INIT_GOLD = 200
GAME_TIME = 90  # 秒
END_HP = 1


# ============================================================
# 工具函数
# ============================================================
def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def pt_seg_dist(p, a, b):
    """点到线段距离"""
    ax, ay = a; bx, by = b
    dx, dy = bx-ax, by-ay
    if dx == dy == 0:
        return dist(p, a)
    t = max(0, min(1, ((p[0]-ax)*dx+(p[1]-ay)*dy)/(dx*dx+dy*dy)))
    return dist(p, (ax+t*dx, ay+t*dy))

def on_road(pos):
    for route in ROUTES:
        for i in range(len(route)-1):
            if pt_seg_dist(pos, route[i], route[i+1]) < ROAD_W/2:
                return True
    return False

def in_tower_zone(pos):
    return True

def path_len(route):
    ln = 0.0
    for i in range(len(route)-1):
        ln += dist(route[i], route[i+1])
    return ln

def path_pos(progress, route):
    """根据进度返回路径上坐标"""
    total = path_len(route)
    if total == 0: return route[0]
    target = progress * total
    acc = 0.0
    for i in range(len(route)-1):
        seg = dist(route[i], route[i+1])
        if acc + seg >= target:
            t = (target-acc)/seg if seg > 0 else 0
            return (route[i][0]+t*(route[i+1][0]-route[i][0]),
                    route[i][1]+t*(route[i+1][1]-route[i][1]))
        acc += seg
    return route[-1]


# ============================================================
# 敌人
# ============================================================
class Enemy:
    def __init__(self, etype):
        c = ENEMY_CFG[etype]
        self.type = etype
        self.hp = self.max_hp = c['hp']
        self.base_spd = c['spd']
        self.spd = c['spd']
        self.reward = c['reward']
        self.color = c['color']
        self.radius = c['r']
        self.progress = 0.0
        self.alive = True
        self.escaped = False
        self.got_reward = False
        self.slow = 1.0
        self.slow_t = 0
        self.route = random.choice(ROUTES)
        self.route_len = path_len(self.route)
        self.x, self.y = self.route[0]

        self.img = None
        try:
            img = pygame.image.load(f'icon/{c["img"]}')
            s = 0.5
            self.img = pygame.transform.scale(img, (int(img.get_width()*s), int(img.get_height()*s)))
        except:
            pass

    def update(self):
        if not self.alive or self.escaped:
            return
        if self.slow_t > 0:
            self.slow_t -= 1
            if self.slow_t == 0:
                self.slow = 1.0
        self.spd = self.base_spd * self.slow

        inc = self.spd / self.route_len if self.route_len > 0 else 0
        self.progress += inc
        if self.progress >= 1.0:
            self.progress = 1.0
            self.escaped = True
            self.alive = False
            self.got_reward = True
        self.x, self.y = path_pos(self.progress, self.route)

    def hit(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def apply_slow(self, f, dur):
        self.slow = min(self.slow, f)
        self.slow_t = max(self.slow_t, dur)

    def draw(self, surf):
        if not self.alive:
            return
        px, py = int(self.x), int(self.y)

        if self.img:
            r = self.img.get_rect(center=(px, py))
            surf.blit(self.img, r)
        else:
            pygame.draw.circle(surf, self.color, (px, py), self.radius)
            pygame.draw.circle(surf, BLACK, (px, py), self.radius, 2)

        if self.hp < self.max_hp:
            bw, bh = 36, 4
            bx = px - bw//2
            by = py - self.radius - 10
            pygame.draw.rect(surf, RED, (bx, by, bw, bh))
            w = int(bw * max(0, self.hp/self.max_hp))
            pygame.draw.rect(surf, GREEN_D, (bx, by, w, bh))
            pygame.draw.rect(surf, BLACK, (bx, by, bw, bh), 1)


# ============================================================
# 子弹
# ============================================================
class Bullet:
    def __init__(self, x, y, target, dmg, spd, spl=0, slow=1.0, slow_len=0, color=YELLOW, img_path=None):
        self.x, self.y = x, y
        self.target = target
        self.dmg = dmg
        self.spd = spd
        self.splash = spl
        self.slow = slow
        self.slow_len = slow_len
        self.color = color
        self.alive = True
        self.img = None
        if img_path:
            try:
                img = pygame.image.load(img_path)
                self.img = pygame.transform.scale(img, (int(img.get_width()*0.35), int(img.get_height()*0.35)))
            except:
                self.img = None

    def update(self):
        if not self.alive:
            return
        if not self.target or not self.target.alive:
            self.alive = False
            return

        tx, ty = self.target.x, self.target.y
        d = math.hypot(tx-self.x, ty-self.y)
        if d < self.spd:
            self._hit()
            return
        self.x += (tx-self.x)/d * self.spd
        self.y += (ty-self.y)/d * self.spd

    def _hit(self):
        if self.target and self.target.alive:
            self.target.hit(self.dmg)
            if self.slow < 1.0:
                self.target.apply_slow(self.slow, self.slow_len)
        self.alive = False

    def draw(self, surf):
        if not self.alive:
            return
        px, py = int(self.x), int(self.y)
        if self.img:
            r = self.img.get_rect(center=(px, py))
            surf.blit(self.img, r)
        else:
            pygame.draw.circle(surf, self.color, (px, py), 5)
            pygame.draw.circle(surf, BLACK, (px, py), 5, 1)


# ============================================================
# 塔
# ============================================================
class Tower:
    def __init__(self, x, y, ttype):
        c = TOWERS_CFG[ttype]
        self.x, self.y = x, y
        self.type = ttype
        self.cost = c['cost']
        self.range = c['range']
        self.dmg = c['dmg']
        self.cd_max = c['cd']
        self.cd = 0
        self.color = c['color']
        self.bullet_spd = c['bullet_speed']
        self.splash = c['splash']
        self.slow = c.get('slow', 1.0)
        self.slow_len = c.get('slow_len', 0)
        self.angle = 0
        self.size = 30

        self.img = None
        img_map = {'normal': 'normal_tower.png', 'flame': 'flame_tower.png', 'freeze': 'freeze_tower.png'}
        if ttype in img_map:
            try:
                img = pygame.image.load(f'icon/{img_map[ttype]}')
                self.img = pygame.transform.scale(img, (int(img.get_width()*0.45), int(img.get_height()*0.45)))
            except:
                pass

    def update(self, enemies):
        self.cd = max(0, self.cd-1)
        best = None
        best_d = float('inf')
        for e in enemies:
            if e.alive and not e.escaped:
                d = dist((self.x, self.y), (e.x, e.y))
                if d < self.range and d < best_d:
                    best, best_d = e, d

        if best and self.cd == 0:
            self.cd = self.cd_max
            self.angle = math.atan2(best.y-self.y, best.x-self.x)
            bullet_img = f'icon/{self.type}_bullet.png'
            return Bullet(self.x, self.y, best, self.dmg, self.bullet_spd,
                          self.splash, self.slow, self.slow_len, self.color,
                          img_path=bullet_img)
        return None

    def draw(self, surf, show_range=False):
        if show_range:
            s = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, 35), (self.range, self.range), self.range)
            pygame.draw.circle(s, (255, 255, 255, 70), (self.range, self.range), self.range, 2)
            surf.blit(s, (self.x-self.range, self.y-self.range))

        if self.img:
            rot = pygame.transform.rotate(self.img, -math.degrees(self.angle))
            r = rot.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(rot, r)
        else:
            pygame.draw.circle(surf, DARK, (int(self.x), int(self.y)), self.size)
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.size-6)
            ex = self.x + math.cos(self.angle)*self.size
            ey = self.y + math.sin(self.angle)*self.size
            pygame.draw.line(surf, BLACK, (self.x, self.y), (ex, ey), 5)
            pygame.draw.line(surf, self.color, (self.x, self.y), (ex, ey), 3)


# ============================================================
# 粒子
# ============================================================
class Particle:
    def __init__(self, x, y, color, n=1):
        self.pts = []
        for _ in range(n):
            a = random.uniform(0, 6.28)
            s = random.uniform(1, 4)
            self.pts.append([x, y, math.cos(a)*s, math.sin(a)*s, random.uniform(8, 20)])

    def update(self):
        for p in self.pts:
            p[0] += p[2]; p[1] += p[3]
            p[2] *= 0.92; p[3] *= 0.92
            p[4] -= 1
        self.pts = [p for p in self.pts if p[4] > 0]

    @property
    def alive(self):
        return len(self.pts) > 0

    def draw(self, surf):
        for p in self.pts:
            alpha = int(255 * p[4]/20)
            c = (255, 215, 0, alpha)  # 金色
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(s, c, (3, 3), 3)
            surf.blit(s, (int(p[0]-3), int(p[1]-3)))


# ============================================================
# 游戏主类
# ============================================================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("SimHei", 48)
        self.font_mid = pygame.font.SysFont("SimHei", 24)
        self.font_sml = pygame.font.SysFont("SimHei", 18)
        self.font_tmr = pygame.font.SysFont("Arial", 40, bold=True)

        # 背景
        self.bg = None
        try:
            self.bg = pygame.image.load('icon/background.jpg')
        except:
            self.bg = pygame.Surface((SCREEN_W, SCREEN_H))
            self.bg.fill((50, 120, 50))

        # 音效
        self.sfx = {}
        try:
            self.sfx['shoot'] = pygame.mixer.Sound('sound/shoot.ogg')
            self.sfx['shoot'].set_volume(0.2)
            self.sfx['win'] = pygame.mixer.Sound('sound/win.ogg')
            self.sfx['lose'] = pygame.mixer.Sound('sound/game_over.wav')
        except:
            pass

        # 结果图
        self.win_img = None
        self.lose_img = None
        try:
            self.win_img = pygame.image.load('icon/win.png')
            self.lose_img = pygame.image.load('icon/game_over.png')
        except:
            pass

        self.current_music = None
        self.reset()

    def reset(self):
        self.state = 'menu'
        self.gold = INIT_GOLD
        self.timer = GAME_TIME * FPS
        self.result_tmr = 0
        self.end_hp = END_HP
        self.enemies = []
        self.towers = []
        self.bullets = []
        self.particles = []
        self.sel_tower = None
        self.placing = False
        self.spawn_tmr = 0
        self.kills = 0
        self.spawned = 0
        self.hover_tower = None  # 鼠标悬停查看的塔
        self._play_music('sound/main_menu.ogg', volume=0.16)

        # 按钮 - 塔选择
        self.btns = {}
        xs = SCREEN_W - 360
        for i, (k, v) in enumerate(TOWERS_CFG.items()):
            self.btns[k] = {'rect': pygame.Rect(xs+i*110, 6, 100, 38),
                           'label': f'{v["name"]}({v["cost"]})', 'sel': False}

        # 开始按钮
        # 底部横排塔选择按钮
        self.btns = {}
        bottom_y = SCREEN_H - 52
        xs = SCREEN_W//2 - 190
        for i, (k, v) in enumerate(TOWERS_CFG.items()):
            self.btns[k] = {'rect': pygame.Rect(xs + i*160, bottom_y, 140, 42),
                           'label': f'{v["name"]}({v["cost"]})', 'sel': False}

    def _play_music(self, path, volume=0.18):
        try:
            if self.current_music == path:
                return
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume)
            self.current_music = path
        except:
            self.current_music = None

    def _stop_music(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    # ----- 输入处理 -----
    def handle(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False

            if self.state == 'menu':
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.reset()
                    self.state = 'playing'
                    self._play_music('sound/ingame.ogg', volume=0.22)
                continue

            if self.state == 'playing':
                # 快捷键
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_1:
                        self._select_tower('normal')
                    elif ev.key == pygame.K_2:
                        self._select_tower('flame')
                    elif ev.key == pygame.K_3:
                        self._select_tower('freeze')
                    elif ev.key == pygame.K_ESCAPE:
                        if self.placing:
                            self.placing = False
                            self.sel_tower = None
                        else:
                            return False

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    # 检查按钮
                    for k, v in self.btns.items():
                        if v['rect'].collidepoint(ev.pos):
                            self._select_tower(k)
                            break
                    else:
                        if self.placing and self.sel_tower:
                            self._place_tower(ev.pos[0], ev.pos[1])
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
                    self.placing = False
                    self.sel_tower = None

                if ev.type == pygame.MOUSEMOTION:
                    # 看鼠标是否悬停在一个塔上
                    self.hover_tower = None
                    for t in self.towers:
                        if dist((ev.pos[0], ev.pos[1]), (t.x, t.y)) < 25:
                            self.hover_tower = t
                            break

            elif self.state in ('win', 'lose'):
                if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 'menu'
                    self._stop_music()
                    self._play_music('sound/main_menu.ogg', volume=0.16)

        return True

    def _select_tower(self, ttype):
        if self.sel_tower == ttype:
            self.placing = False
            self.sel_tower = None
        else:
            self.sel_tower = ttype
            self.placing = True

    def _place_tower(self, x, y):
        cfg = TOWERS_CFG.get(self.sel_tower)
        if not cfg: return
        if self.gold < cfg['cost']: return
        if y < 50 or x < 15 or x > SCREEN_W-15 or y > SCREEN_H-15: return
        if not in_tower_zone((x, y)): return
        if on_road((x, y)): return
        for t in self.towers:
            if dist((x, y), (t.x, t.y)) < 45: return

        t = Tower(x, y, self.sel_tower)
        self.towers.append(t)
        self.gold -= cfg['cost']
        try: self.sfx['shoot'].play()
        except: pass

    # ----- 更新逻辑 -----
    def update(self):
        if self.state in ('win', 'lose'):
            if self.result_tmr > 0:
                self.result_tmr -= 1
                if self.result_tmr <= 0:
                    self.state = 'menu'
                    self._stop_music()
                    self._play_music('sound/main_menu.ogg', volume=0.16)
            return

        if self.state != 'playing':
            return

        self.timer -= 1
        remaining = self.timer // FPS

        # 检查终点到达 → 只要怪物到达最后一个点位立即判定失败
        for e in self.enemies:
            if e.escaped:
                self.particles.append(Particle(e.x, e.y, RED, 10))
                self.state = 'lose'
                self.result_tmr = FPS * 5
                try:
                    self.sfx['lose'].play()
                    pygame.mixer.music.stop()
                except: pass
                return

        # 时间到，则胜利
        if self.timer <= 0:
            self.state = 'win'
            self.result_tmr = FPS * 5
            try:
                self.sfx['win'].play()
                pygame.mixer.music.stop()
            except: pass
            return

        # 生成敌人
        self.spawn_tmr -= 1
        if self.spawn_tmr <= 0:
            elapsed = GAME_TIME - remaining
            if elapsed < 20:
                pool = ['normal']
            elif elapsed < 45:
                pool = ['normal', 'normal', 'fast']
            elif elapsed < 70:
                pool = ['normal', 'fast', 'fast', 'boss']
            else:
                pool = ['normal', 'fast', 'boss', 'fast', 'boss']

            etype = random.choice(pool)
            e = Enemy(etype)
            # 随时间加难度
            scale = 1.0 + elapsed / 50
            e.max_hp = int(e.max_hp * scale)
            e.hp = e.max_hp
            self.enemies.append(e)
            self.spawned += 1

            interval = max(15, int(FPS * (1.5 - elapsed/120)))
            self.spawn_tmr = interval

        # 更新敌人
        for e in self.enemies:
            e.update()

        # 逃跑判定：有敌人到终点，立即失败
        for e in self.enemies:
            if e.escaped:
                self.particles.append(Particle(e.x, e.y, RED, 10))
                self.state = 'lose'
                self.result_tmr = FPS * 5
                try:
                    self.sfx['lose'].play()
                    pygame.mixer.music.stop()
                except: pass
                return

        # 更新塔（生成新子弹）
        for t in self.towers:
            b = t.update(self.enemies)
            if b:
                self.bullets.append(b)

        # 子弹飞行（子弹击中敌人造成伤害）
        for b in self.bullets:
            b.update()

        # 处理击杀奖励（子弹造成敌人死亡后在此处理）
        for e in self.enemies:
            if e.escaped:
                continue
            if not e.alive and not e.got_reward:
                e.got_reward = True
                self.gold += e.reward
                self.kills += 1
                self.particles.append(Particle(e.x, e.y, GOLD, 8))

        # 粒子更新
        for p in self.particles:
            p.update()

        # 清理
        self.enemies = [e for e in self.enemies if e.alive]
        self.bullets = [b for b in self.bullets if b.alive]
        self.particles = [p for p in self.particles if p.alive]

        # 按钮选中
        for k, v in self.btns.items():
            v['sel'] = (k == self.sel_tower)

    # ----- 绘制 -----
    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        if self.state == 'menu':
            self._draw_menu()
            pygame.display.flip()
            return

        # 绘制放置区域和路径参考线（蓝色区域为可放置塔的位置）
        self._draw_path()

        # 塔
        for t in self.towers:
            show_r = (self.hover_tower == t)
            t.draw(self.screen, show_r)

        # 敌人
        for e in self.enemies:
            e.draw(self.screen)

        # 子弹
        for b in self.bullets:
            b.draw(self.screen)

        # 粒子
        for p in self.particles:
            p.draw(self.screen)

        # 放置预览
        self._draw_preview()

        # HUD
        self._draw_hud()

        # 结果
        if self.state in ('win', 'lose'):
            self._draw_result()

        pygame.display.flip()

    def _draw_path(self):
        """绘制半透明路径引导线"""
        s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for route in ROUTES:
            for i in range(len(route)-1):
                a, b = route[i], route[i+1]
                pygame.draw.line(s, (220, 220, 220, 140), a, b, 24)
        self.screen.blit(s, (0, 0))

        # 起点终点标记
        start = ROUTES[0][0]
        end = ROUTES[0][-1]
        pygame.draw.circle(self.screen, (230, 230, 230, 160), start, 10, 3)
        pygame.draw.circle(self.screen, (230, 230, 230, 160), end, 10, 3)

    def _draw_hud(self):
        # 顶部半透明条
        s = pygame.Surface((SCREEN_W, 48), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))
        pygame.draw.line(self.screen, GOLD, (0, 48), (SCREEN_W, 48), 2)

        # 金币
        t1 = self.font_mid.render(f'💰 {self.gold}', True, GOLD)
        self.screen.blit(t1, (12, 12))

        # 击杀
        t2 = self.font_sml.render(f'击杀:{self.kills}', True, WHITE)
        self.screen.blit(t2, (130, 15))

        # 计时
        left = max(0, self.timer // FPS)
        color = RED if left <= 15 else WHITE
        t3 = self.font_tmr.render(f'{left:02d}', True, color)
        r3 = t3.get_rect(center=(SCREEN_W//2, 24))
        self.screen.blit(t3, r3)

        # 怪物数
        t4 = self.font_sml.render(f'已出:{self.spawned}', True, WHITE)
        self.screen.blit(t4, (SCREEN_W//2 + 60, 15))

        # 城堡生命
        t5 = self.font_sml.render(f'城堡生命:{self.end_hp}', True, ORANGE if self.end_hp <= 3 else WHITE)
        self.screen.blit(t5, (SCREEN_W - 180, 15))

        # 塔按钮
        self._draw_btns()

        # 提示
        if self.placing and self.sel_tower:
            hint = f'点击地图放置{TOWERS_CFG[self.sel_tower]["name"]}(ESC取消)'
            t5 = self.font_sml.render(hint, True, GOLD)
            self.screen.blit(t5, (SCREEN_W//2-t5.get_width()//2, 52))

    def _draw_btns(self):
        for k, v in self.btns.items():
            r = v['rect']
            bg = GOLD if v['sel'] else DARK
            pygame.draw.rect(self.screen, bg, r, border_radius=8)
            if v['sel']:
                pygame.draw.rect(self.screen, WHITE, r, 2, border_radius=8)
            t = self.font_sml.render(v['label'], True, WHITE)
            tr = t.get_rect(center=r.center)
            self.screen.blit(t, tr)

    def _draw_preview(self):
        if not self.placing or not self.sel_tower:
            return
        mx, my = pygame.mouse.get_pos()
        if my < 55:
            return
        cfg = TOWERS_CFG[self.sel_tower]
        ok = True
        if self.gold < cfg['cost']: ok = False
        elif not in_tower_zone((mx, my)): ok = False
        elif on_road((mx, my)): ok = False
        elif my < 50 or mx < 15 or mx > SCREEN_W-15 or my > SCREEN_H-15: ok = False
        else:
            for t in self.towers:
                if dist((mx, my), (t.x, t.y)) < 45:
                    ok = False; break

        color = GREEN_D if ok else RED
        s = pygame.Surface((cfg['range']*2, cfg['range']*2), pygame.SRCALPHA)
        c1 = (100, 255, 100, 40) if ok else (255, 100, 100, 40)
        c2 = (100, 255, 100, 80) if ok else (255, 100, 100, 80)
        pygame.draw.circle(s, c1, (cfg['range'], cfg['range']), cfg['range'])
        pygame.draw.circle(s, c2, (cfg['range'], cfg['range']), cfg['range'], 2)
        self.screen.blit(s, (mx-cfg['range'], my-cfg['range']))
        pygame.draw.circle(self.screen, color, (mx, my), 22, 3)
        pygame.draw.circle(self.screen, color+(80,), (mx, my), 20)

    def _draw_menu(self):
        try:
            bg = pygame.image.load('icon/menu_background.jpg')
            self.screen.blit(bg, (0, 0))
        except:
            self.screen.fill(DARK)

        s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        self.screen.blit(s, (0, 0))

        title = self.font_big.render('塔防大作战', True, GOLD)
        r = title.get_rect(center=(SCREEN_W//2, SCREEN_H//2-90))
        self.screen.blit(title, r)

        tips = [
            '选择炮塔后点击可建造地点放置',
            '击杀怪物获得金币，购买更多炮塔',
            '只有一条命，城堡被攻破即失败',
            '点击任意处开始游戏',
        ]
        for i, line in enumerate(tips):
            t = self.font_mid.render(line, True, WHITE)
            tr = t.get_rect(center=(SCREEN_W//2, SCREEN_H//2-30+i*30))
            self.screen.blit(t, tr)

    def _draw_result(self):
        s = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        self.screen.blit(s, (0, 0))

        if self.state == 'win':
            if self.win_img:
                r = self.win_img.get_rect(center=(SCREEN_W//2, SCREEN_H//2-60))
                self.screen.blit(self.win_img, r)
            t = self.font_big.render('胜利！', True, GOLD)
            tr = t.get_rect(center=(SCREEN_W//2, SCREEN_H//2+80))
            self.screen.blit(t, tr)
            info = f'击杀 {self.kills} 个怪物 | 剩余 {self.gold} 金币'
        else:
            if self.lose_img:
                r = self.lose_img.get_rect(center=(SCREEN_W//2, SCREEN_H//2-60))
                self.screen.blit(self.lose_img, r)
            t = self.font_big.render('失败', True, RED)
            tr = t.get_rect(center=(SCREEN_W//2, SCREEN_H//2+80))
            self.screen.blit(t, tr)
            info = f'坚持了 {GAME_TIME - self.timer//FPS} 秒 | 击杀 {self.kills} 个怪物'

        t2 = self.font_mid.render(info, True, WHITE)
        r2 = t2.get_rect(center=(SCREEN_W//2, SCREEN_H//2+130))
        self.screen.blit(t2, r2)
        if self.result_tmr > 0:
            countdown = max(0, self.result_tmr // FPS)
            if self.state == 'lose':
                tip = f'{countdown}s后退出游戏'
            else:
                tip = f'{countdown}s后返回菜单'
        else:
            tip = '点击任意处返回菜单'
        t3 = self.font_sml.render(tip, True, LGRAY)
        r3 = t3.get_rect(center=(SCREEN_W//2, SCREEN_H//2+170))
        self.screen.blit(t3, r3)

    # ----- 主循环 -----
    def run(self):
        running = True
        while running:
            running = self.handle()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game().run()
