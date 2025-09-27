# 필요한 라이브러리 import
import pygame
import cv2
import math
import sys
import random
import speech_recognition as sr
import numpy as np
import time
import threading
import mediapipe as mp
from pygame.locals import *
from weather import *

# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLINK = [(224, 255, 255), (192, 240, 255), (128, 224, 255), (64, 192, 255), (128, 224, 255), (192, 240, 255)]

# 미디어파이프에 필요한 변수 정의
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# 게임 화면을 pygame 내장 함수를 이용해서 880*720크기로 설정하고 screen 변수로 저장
screen = pygame.display.set_mode((880, 720))

# test_map_mask.png를 map_mask 변수에 저장 convert_alpha를 이용해서 알파채널을 지원하도록 설정
#map_mask = pygame.image.load("img/test_map_mask.png").convert_alpha()

# 필요한 이미지 로딩
imgTitle = pygame.image.load("img/title.jpg")
imgBtlBG = pygame.image.load("img/btlbg.png")
imgEnemy = pygame.image.load("img/enemy0.png")
imgEffect = pygame.image.load("img/effect_a.png")
img_end = pygame.image.load('img/ending.png')

# 변수 선언
speed = 1
idx = 0
tmr = 0
pl_str = 0
hand_flag = None
emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0
dmg_eff = 0
COMMAND = ["[O]rder"]
EMY_NAME = ["Rifleman"]


def hand():
    rectangles = []
    for i in range(3):
        for j in range(3):
            x = j * 110 + 100
            y = i * 110 + 100
            rectangles.append(Rectangle(x, y, 100, 100, i + 1, j + 1))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_tip_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
                finger_tip_y = int(hand_landmarks.landmark[8].y * frame.shape[0])

                for rect in rectangles:
                    if rect.x < finger_tip_x < rect.x + rect.w and rect.y < finger_tip_y < rect.y + rect.h:
                        rect.click_action(frame)
                        rect.update_color((0, 0, 255)) 
                    else:
                        rect.update_color((0, 255, 0))
                        rect.alpha = 100 

        for rect in rectangles:
            cv2.rectangle(frame, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), rect.color, 2)

        cv2.imshow('Transparent Rectangles', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
class Rectangle:
    def __init__(self, x, y, w, h, row, column):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.row = row
        self.column = column
        self.color = (0, 255, 0) 
        self.alpha = 100

    def click_action(self, frame):
        global hand_flag
        
        if self.row == 2 and self.column == 3:
            cv2.putText(frame, "Right", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'd'
        elif self.row == 1 and self.column == 2:
            cv2.putText(frame, "up", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'w'
        elif self.row == 3 and self.column == 2:
            cv2.putText(frame, "down", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'x'
        elif self.row == 2 and self.column == 2:
            cv2.putText(frame, "stop", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'stop'
        elif self.row == 2 and self.column == 1:
            cv2.putText(frame, "Left", (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'a'
        elif self.row == 1 and self.column == 1:
            cv2.putText(frame, 'dia135', (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'q'
        elif self.row == 1 and self.column == 3:
            cv2.putText(frame, 'dia45', (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'e'
        elif self.row == 3 and self.column == 1:
            cv2.putText(frame, 'dia225', (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'z'
        elif self.row == 3 and self.column == 3:
            cv2.putText(frame, 'dia315', (self.x + 10, self.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            hand_flag = 'c'
        else:
            hand_flag = '0'
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 255, 255), -2)
        cv2.addWeighted(overlay, self.alpha / 255, frame, 1 - self.alpha / 255, 0, frame)

    def update_color(self, color):
        self.color = color
    
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.up_images = [pygame.image.load(f'img/main_char/char_back{i}.png').convert_alpha() for i in range(1, 4)]
        self.down_images = [pygame.image.load(f'img/main_char/char_front{i}.png').convert_alpha() for i in range(1, 4)]
        self.left_images = [pygame.image.load(f'img/main_char/char_left{i}.png').convert_alpha() for i in range(1, 4)]
        self.right_images = [pygame.image.load(f'img/main_char/char_right{i}.png').convert_alpha() for i in range(1, 4)]
        self.dia45_images = [pygame.image.load(f'img/main_char/char_dia45_{i}.png').convert_alpha() for i in range(1, 4)]
        self.dia135_images = [pygame.image.load(f'img/main_char/char_dia135_{i}.png').convert_alpha() for i in range(1, 4)]
        self.dia225_images = [pygame.image.load(f'img/main_char/char_dia225_{i}.png').convert_alpha() for i in range(1, 4)]
        self.dia315_images = [pygame.image.load(f'img/main_char/char_dia315_{i}.png').convert_alpha() for i in range(1, 4)]
        self.index = 0
        self.image = pygame.image.load('img/main_char/char_front2.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos) # 메인 캐릭터 초기 위치
        self.initial_pos = pos
        self.x, self.y = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
    def input(self):
        global hand_flag
        
        if self.index > 2:
            self.index = 0

        if self.rect.top < 0:
            self.direction.y = 0
            self.rect.top = 0
        if self.rect.bottom > 1600:
            self.direction.y = 0
            self.rect.bottom = 1600
        if self.rect.left < 0:
            self.direction.x = 0
            self.rect.left = 0
        if self.rect.right > 1600:
            self.direction.x = 0
            self.rect.right = 1600

        if hand_flag == 'w':
            self.direction.y = -1
            self.image = self.up_images[self.index]
            self.index += 1
        elif hand_flag == 'x':
            self.direction.y = 1
            self.image = self.down_images[self.index]
            self.index += 1
        elif hand_flag == 'd':
            self.direction.x = 1
            self.image = self.right_images[self.index]
            self.index += 1
        elif hand_flag == 'a':
            self.direction.x = -1
            self.image = self.left_images[self.index]
            self.index += 1  
        elif hand_flag == 'q':
            self.direction.x = -0.5
            self.direction.y = -0.5
            self.image = self.dia135_images[self.index]
            self.index += 1
        elif hand_flag == 'e':
            self.direction.x = 0.5
            self.direction.y = -0.5
            self.image = self.dia45_images[self.index]
            self.index += 1
        elif hand_flag == 'z':
            self.direction.x = -0.5
            self.direction.y = 0.5
            self.image = self.dia225_images[self.index]
            self.index += 1
        elif hand_flag == 'c':
            self.direction.x = 0.5
            self.direction.y = 0.5
            self.image = self.dia315_images[self.index]
            self.index += 1
        elif hand_flag == 'stop':
            self.direction.x = 0
            self.direction.y = 0
            self.image = self.down_images[1]
        elif hand_flag == '0':
            self.direction.x = 0
            self.direction.y = 0
            self.image = self.down_images[1]
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.imag = self.down_images[1]
            
    def update(self):
        self.input()
    
        self.rect.center += self.direction * self.speed

        # Update collision mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def reset_position(self):
        self.rect.center = self.initial_pos
        
    def char_stop(self, poi, x=0, y=0):
        # 충돌이 발생한 지점을 기준으로 보정값을 계산
        correction_x = 0
        correction_y = 0

        if poi[0] < self.rect.centerx:
            correction_x = self.rect.centerx - poi[0]  # 충돌이 왼쪽에서 발생했을 때, 오른쪽으로 보정
            correction_y = self.rect.centery - poi[1]
        elif poi[0] > self.rect.centerx:
            correction_x = self.rect.centerx - poi[0]  # 충돌이 오른쪽에서 발생했을 때, 왼쪽으로 보정
            corrention_y = self.rect.centery - poi[1]
        elif poi[1] < self.rect.centery:
            correction_y = self.rect.centery - poi[1]  # 충돌이 위쪽에서 발생했을 때, 아래쪽으로 보정
            correction_x = self.rect.centerx - poi[0]
        elif poi[1] > self.rect.centery:
            correction_y = self.rect.centery - poi[1]  # 충돌이 아래쪽에서 발생했을 때, 위쪽으로 보정
            correction_x = self.rect.centerx - poi[0]

        # 보정값을 사용하여 캐릭터의 위치를 조정
        self.rect.x += correction_x
        self.rect.y += correction_y

    def collide(self, mask, x=0, y=0):
        self.mask_rect = self.mask.get_rect()
        self.mask_rect.center = self.rect.center
        
        offset = (self.mask_rect.x, self.mask_rect.y)

        # 마스크와 주어진 마스크 사이의 충돌 감지
        poi = mask.overlap(self.mask, (self.mask_rect.x, self.mask_rect.y))
        return poi

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        
        #box setup
        self.camera_borders = {'left':300, 'right':300, 'top':250, 'bottom':200}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)
        
        # ground
        self.ground_surf = pygame.image.load('img/ori_map.png').convert_alpha()
        self.ground_wall1_surf = pygame.image.load('img/ori_map_mask.png').convert_alpha()
        self.ground_wall2_surf = pygame.image.load('img/ori_map_wall_mask.png').convert_alpha()
        self.enemy_surf = pygame.image.load('img/enemy.png').convert_alpha()
        self.next_surf = pygame.image.load('img/end.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
        self.ground_mask = pygame.mask.from_surface(self.ground_wall1_surf)
        self.enemy_mask = pygame.mask.from_surface(self.enemy_surf)
        self.next_mask = pygame.mask.from_surface(self.next_surf)
        
    # 카메라를 플레이어 중심으로 맞춤
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h
    
    # 플레이어가 카메라 박스 영역을 벗어나면 카메라 재조정
    def box_target_camera(self, target):
        # 카메라의 왼쪽 경계가 맵 이미지의 왼쪽 경계에 닿았을 때
        if self.camera_rect.left <= 128:
            self.camera_rect.left = 128
        # 카메라의 오른쪽 경계가 맵 이미지의 오른쪽 경계에 닿았을 때
        if self.camera_rect.right >= 1572:
            self.camera_rect.right = 1572
        # 카메라의 상단 경계가 맵 이미지의 상단 경계에 닿았을 때
        if self.camera_rect.top <= 128:
            self.camera_rect.top = 128
        # 카메라의 하단 경계가 맵 이미지의 하단 경계에 닿았을 때
        if self.camera_rect.bottom >= 1572:
            self.camera_rect.bottom = 1572

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom
            
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
        
    
    # 화면에 배경, 스프라이트 그림
    def custom_draw(self, player):
        self.center_target_camera(player)
        self.box_target_camera(player)
        
        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)
        self.display_surface.blit(self.ground_wall2_surf, ground_offset)
        
        # active elements
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            
        rect_pos = (self.camera_rect.topleft - self.offset)
        rect_size = self.camera_rect.size
        pygame.draw.rect(self.display_surface, 'yellow', pygame.Rect(rect_pos, rect_size), 5)
        player_rect = player.rect.move(-self.offset.x, -self.offset.y)  # 캐릭터의 위치를 카메라 오프셋만큼 이동
        pygame.draw.rect(self.display_surface, (255, 255, 255), player_rect, 2)
        
# 그림자 포함한 문자 표시
def draw_text(bg, txt, x, y, fnt, col): 
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x + 1, y + 2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

# 전투 시작 준비
def init_battle(): 
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y, type_num, emy_type
    
    lev = 1
    typ = 1
    imgEnemy = pygame.image.load("img/enemy0.png")
    emy_name = EMY_NAME[0] + " LV" + str(lev)
    emy_lifemax = 60 * (typ + 1) + (lev - 1) * 10
    emy_life = emy_lifemax
    emy_str = int(emy_lifemax / 8)
    emy_x = 440 - imgEnemy.get_width() / 2
    emy_y = 560 - imgEnemy.get_height()

# 적 체력 표시 게이지
def draw_bar(bg, x, y, w, h, val, ma):
    pygame.draw.rect(bg, WHITE, [x - 2, y - 2, w + 4, h + 4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0, 128, 255), [x, y, w * val / ma, h])

# 전투 화면 표시
def draw_battle(bg, fnt):
    global emy_blink, dmg_eff, type_system
    bx = 0
    by = 0
    X = 30
    Y = 600
    
    if dmg_eff > 0:
        dmg_eff -= 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink % 2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y + emy_step])
    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)

    if emy_blink > 0:
        emy_blink -= 1
    for i in range(10): # 전투 메세지 표시
        draw_text(bg, message[i], 600, 100 + i * 50, fnt, WHITE)

# 커맨드 입력 및 표시
def battle_command(bg, fnt, key):
    global btl_cmd, vToText
    ent = False
    btl_cmd = 0
    if key[K_o]: # O키
        btl_cmd = 1
        ent = True
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    c = WHITE
    if btl_cmd == 0: c = BLINK[tmr % 6]
    draw_text(bg, COMMAND[0], 20, 360 + 0 * 60, fnt, c)
    return ent

#전투 메세지 표시 처리
message = [""] * 10
def init_message():
    for i in range(10):
        message[i] = ""

def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i + 1]
    message[9] = msg

# 음성 인식 처리
def Recognizer():
    try:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            speech = r.listen(source, timeout=3, phrase_time_limit=2)
            vToText = r.recognize_google(speech, language="ko-KR")

            return vToText
    except sr.UnknownValueError:
        set_message("Try Again")
    except sr.RequestError as e:
        set_message("Try Again")
    except sr.WaitTimeoutError as w:
        set_message("Try Again")

# 메인 처리
def main():
    global speed, idx, tmr
    global emy_life, emy_step, emy_blink, dmg_eff, btl_cmd, hand_flag
    dmg = 0
    
    pygame.init()
    pygame.display.set_caption("Dungeon Escape")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)
    weather = proc_weather().split('.')
    Y = [125, 150, 175]
    
    camera_group = CameraGroup()
    player = Player((300,380), camera_group)
    webcam = cv2.VideoCapture(0)
    
    se = [ # 효과음 및 징글
        pygame.mixer.Sound("sound/attack.mp3"),
        pygame.mixer.Sound("sound/attack2.mp3"),
        pygame.mixer.Sound("sound/win.mp3"),
        pygame.mixer.Sound("sound/run.mp3")
    ]
    
    # 메인 루프
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        tmr += 1
        key = pygame.key.get_pressed()
        
        # 타이틀 화면
        if idx == 0:
            if tmr == 1:
                pygame.mixer.music.load("sound/title.mp3")
                pygame.mixer.music.play(-1)
            screen.fill(BLACK)
            screen.blit(imgTitle, [40, 60])
            draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr % 6])
            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                pygame.mixer.music.load("sound/field.mp3")
                pygame.mixer.music.play(-1)

        # 미로 맵, 플레이어 이동
        elif idx == 1:
            screen.fill('#001A30')
            poi = player.collide(camera_group.ground_mask)
            enemy = player.collide(camera_group.enemy_mask)
            end = player.collide(camera_group.next_mask)
            if poi is not None:
                player.char_stop(poi)
                camera_group.update()
                camera_group.custom_draw(player)
            elif enemy is not None:
                idx = 10
                tmr = 0
            elif end is not None:
                pygame.mixer.music.load("sound/ending.mp3")
                pygame.mixer.music.play(-1)
                idx = 24
                tmr = 0
            else:
                camera_group.update()
                camera_group.custom_draw(player)
            weather_filter(screen, 1)
            for i in range(3):
                t = threading.Thread(target=draw_text, args=(screen, "{}".format(weather[i]), 60, Y[i], fontS, WHITE))
                t.start()
            if key[K_t] == 1:
                player.reset_position()
                idx = 23
                tmr = 0
                
        # 전투 시작, 적 등장
        elif idx == 10:
            if tmr == 1:
                pygame.mixer.music.load("sound/battle.mp3")
                pygame.mixer.music.play(-1)
                init_battle()
                init_message()
            elif tmr <= 4:
                bx = (4 - tmr) * 220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr <= 16:
                draw_battle(screen, fontS)
                draw_text(screen, emy_name + " appear!", 300, 200, font, WHITE)
            else:
                idx = 11
                tmr = 0
                
        # 플레이어 턴(입력 대기)
        elif idx == 11:
            draw_battle(screen, fontS)
            if tmr == 1: set_message("Your turn")
            if battle_command(screen, font, key) == True:
                if btl_cmd == 1:
                    vToText = Recognizer()
                    if vToText == '공격':
                        idx = 12
                        tmr = 0
                    elif vToText == '회복':
                        if potion < 0:
                            set_message("No Potion!")
                        idx = 20
                        tmr = 0
                    elif vToText == '마법' and blazegem > 0:
                        idx = 21
                        tmr = 0
                    elif vToText == '도망':
                        idx = 14
                        tmr = 0
                    else:
                        tmr = 2
                        set_message("Try Again")
                        
                    
        # 플레이어 공격
        elif idx == 12:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You attack")
                se[0].play()
                if type_system == 0:
                    dmg = pl_str + random.randint(0, 9)
                elif type_system == 1:
                    dmg = (pl_str + random.randint(0, 9) + 20) # 상성이 유리하면 dmg + 20
                elif type_system == 2:
                    dmg = (pl_str + random.randint(0, 9) - 20) # 상성이 불리하면 dmg - 20
            if 2 <= tmr and tmr <= 4:
                screen.blit(imgEffect[0], [700 - tmr * 120, -100 + tmr * 120])
            if tmr == 5:
                emy_blink = 5
                set_message(str(dmg) + "pts of damage!")
            if tmr == 11:
                emy_life -= dmg
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
            if tmr == 16:
                idx = 13
                tmr = 0
                
        # 적 턴, 적 공격
        elif idx == 13:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Enemy turn")
            if tmr == 5:
                set_message(emy_name + " attack!")
                se[1].play()
                emy_step = 30
            if tmr == 9:
                dmg = emy_str + random.randint(0, 9)
                set_message(str(dmg) + "pts of damage!")
                dmg_eff = 5
                emy_step = 0
            if tmr == 20:
                idx = 11
                tmr = 0
                
        # 후퇴 여부 파악 후 결정
        elif idx == 14:
            draw_battle(screen, fontS)
            if tmr == 1: set_message("...")
            if tmr == 2: set_message(".....")
            if tmr == 3: set_message("........")
            if tmr == 4: set_message("...........")
            if tmr == 5:
                if random.randint(0, 99) < 60:
                    set_message("You succeed to flee!")
                    idx = 22
                else:
                    set_message("You failed to flee")
            if tmr == 10:
                idx = 13
                tmr = 0
                
        # 승리
        elif idx == 16:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You win!")
                pygame.mixer.music.stop()
                se[2].play()
            if tmr == 28:
                idx = 22
                
        # 전투 종료
        elif idx == 22:
            pygame.mixer.music.load("sound/field.mp3")
            pygame.mixer.music.play(-1)
            player.reset_position()
            idx = 1
            tmr = 11
        
        # 타이틀로
        elif idx == 23:
            if 1 <= tmr and tmr <= 10:
                draw_text(screen, "Click T again to return to title", 320, 560, fontS, WHITE)
                if key[K_t] == 1:
                    idx = 0
                    tmr = 0
                    attack_type = 0
            if tmr == 11:
                idx = 1
                tmr = 0
        # 엔딩
        elif idx == 24:
            screen.blit(img_end, [0, 0])
            draw_text(screen, "The End", 600, 140, fontS, WHITE)
            draw_text(screen, "Press R to return to title", 530, 180, fontS, WHITE)
            draw_text(screen, "attack sound-Wood Golf Club Hit Ball", 410, 440, fontS, WHITE)
            draw_text(screen, "attack2 sound-Long Rifle Shots", 410, 470, fontS, WHITE)
            draw_text(screen, "run sound-Sneakers Run Light Grit", 410, 500, fontS, WHITE)
            draw_text(screen, "map sound-Final Girl - Jeremy Blake", 410, 530, fontS, WHITE)
            draw_text(screen, "win sound-1 Person Cheering Sound", 410, 560, fontS, WHITE)
            draw_text(screen, "https://sellbuymusic.com/md/sjircft-uccbcbw", 410, 590, fontS, WHITE)
            draw_text(screen, "ending sound-Gran Sentimiento - Luna Cantina", 410, 620, fontS, WHITE)
            draw_text(screen, "battle sound-Addicted - VYEN", 410, 650, fontS, WHITE)
            draw_text(screen, "title sound-Neither Sweat Nor Tears-Dan Bodan", 410, 680, fontS, WHITE)
            
            if key[K_r] == 1:
                player.reset_position()
                idx = 0
                tmr = 0
        
        clock.tick(16)
        pygame.display.update()
        

if __name__ == '__main__':
    hand_thread = threading.Thread(target = hand)
    hand_thread.daemon = True
    hand_thread.start()
    
    main()