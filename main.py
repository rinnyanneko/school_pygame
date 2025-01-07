# Dark Deception ─ The beginning of darkness
# Copyright © 2025 rinnyanneko. All rights reserved.

import os
import keyboard
import pygame
import random
import sys
import time
import cv2

print("Dark Deception ─ The beginning of darkness")
print("Copyright © 2025 rinnyanneko and Keeoka. All rights reserved.")
print("This game is a fan-made game based on the game Dark Deception by Glowstick Entertainment.")
print("This game is not affiliated with Glowstick Entertainment.")
print("Make sure to read the LICENSE file before using this game.")
running = True

monster_timeout_video = os.path.join("assets","monster_timeout.mp4")
monster_timeout_audio = os.path.join("assets","monster_timeout.mp3")

WIDTH = 1280
HEIGHT = 720

# 初始化 Pygame
pygame.init()
# 設置遊戲窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dark Deception ─ The beginning of darkness")

# 加載圖片
background = pygame.image.load(os.path.join("assets", "background.webp")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

scorePlusItem_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Plus.png")), (100, 318))
scoreMinusItem_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "minus.png")), (100, 318))
monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster.webp")), (100, 159))

#取得現在時間(ms)
def current_milli_time():
    return int(time.time() * 1000)

# set monster spawn time
def set_monster_spawn_time():
    if score < 25:
        return random.randint(7000, 25000)
    elif 25 <= score < 50:
        return random.randint(5000, 20000)
    elif 50 <= score < 75:
        return random.randint(3000, 15000)
    elif 75 <= score < 100:
        return random.randint(2000, 10000)

#play video
def play_video(video_path, audio_path):
    global running
    cap = cv2.VideoCapture(video_path)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(audio_path))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        if keyboard.is_pressed("q"):
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.mixer.Channel(1).stop()
                running = False
                break
        pygame.time.delay(5)
    cap.release()
    pygame.mixer.Channel(1).stop()




# main function
def main():
    # initialize game variables
    global running
    # 設置字體
    font = pygame.font.Font(None, 36)
    score = 5
    scorePlusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
    scoreMinusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
    timer: int = current_milli_time()
    scorePlusItem_interval = 1000  # 毫秒
    scoreMinusItem_interval = 1000
    scorePlusItem_update_time = timer + scorePlusItem_interval
    scoreMinusItem_update_time = timer + scoreMinusItem_interval
    game_time = 181000  # 180秒
    remaining_time: int = int(timer + game_time)
    start_time = timer
    monster_appear = False
    monster_life = 0
    life = 3
    monster_pos = (0, 0)
    monster_spawn_time = set_monster_spawn_time() + timer
    show_plus_item = True

    # play opening video
    play_video(os.path.join("assets", "opening.mp4"), os.path.join("assets", "opening.mp3"))

    # play bgm
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join("assets", "bgm.MP3")))
    # 遊戲主循環
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if scorePlusItem_position[0] <= mouse_pos[0] <= scorePlusItem_position[0] + 100 and \
                        scorePlusItem_position[1] <= mouse_pos[1] <= scorePlusItem_position[1] + 318:
                    score += 1
                    scorePlusItem_position = (random.randint(0, 750), random.randint(0, 550))
                    show_plus_item = False
                elif scoreMinusItem_position[0] <= mouse_pos[0] <= scoreMinusItem_position[0] + 100 and \
                        scoreMinusItem_position[1] <= mouse_pos[1] <= scoreMinusItem_position[1] + 318:
                    score -= 10
                    scoreMinusItem_position = (random.randint(0, 750), random.randint(0, 550))
                    scoreMinusItem_update_time = timer + scoreMinusItem_interval
                    if score < 0: score = 0
                elif monster_appear and monster_pos[0] <= mouse_pos[0] <= monster_pos[0] + 100 and monster_pos[1] <= \
                        mouse_pos[1] <= monster_pos[1] + 159:
                    monster_life -= 1
                    if monster_life == 0:
                        score += 1
                        monster_appear = False
                        monster_spawn_time = set_monster_spawn_time() + timer
        # 怪物出現?
        if score >= 5 and not monster_appear:
            if timer >= monster_spawn_time:
                monster_spawn_time = set_monster_spawn_time() + timer
                monster_appear = True
                monster_life = random.randint(3, 5)
                monster_timer = timer
                monster_pos = random.randint(0, 750), random.randint(0, 550)
        match monster_life:
            case 1:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster1.png")),
                                                       (100, 159))
            case 2:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster2.png")),
                                                       (100, 159))
            case 3:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster3.png")),
                                                       (100, 159))
            case 4:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster4.png")),
                                                       (100, 159))
            case 5:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster5.png")),
                                                       (100, 159))
            case _:
                monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster.webp")),
                                                       (100, 159))
        if (monster_appear and
                (timer - monster_timer) > MONSTER_TIMEOUT):
            life -= 1
            monster_appear = False
            play_video(monster_timeout_video, monster_timeout_audio)
            monster_spawn_time = set_monster_spawn_time()
        if life <= 0:
            break
        # 更新地鼠位置
        timer = current_milli_time()
        if timer > scorePlusItem_update_time:
            scorePlusItem_position = (random.randint(0, WIDTH - 159), random.randint(0, HEIGHT - 159))
            scorePlusItem_update_time = timer + scorePlusItem_interval
            if random.randint(0, 1) == 0:
                show_plus_item = True
        if timer > scoreMinusItem_update_time:
            scoreMinusItem_position = (random.randint(0, WIDTH - 159), random.randint(0, HEIGHT - 159))
            scoreMinusItem_update_time = timer + scoreMinusItem_interval

        # 繪製背景和地鼠
        screen.blit(background, (0, 0))
        screen.blit(scoreMinusItem_image, scoreMinusItem_position)
        if show_plus_item:
            screen.blit(scorePlusItem_image, scorePlusItem_position)
        if monster_appear:
            screen.blit(monster_image, monster_pos)
        print(monster_spawn_time)
        # 更新時間
        remaining_time: int = int(game_time - timer + start_time)
        if remaining_time <= 0:
            break
        # 繪製分數
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        remaining_time_text = font.render(f"Time: {remaining_time // 1000}", True, (255, 255, 255))
        life_text = font.render(f"Life: {life}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(remaining_time_text, (10, 30))
        screen.blit(life_text, (10, 50))
        if score >= 100:
            break
        # 更新屏幕
        pygame.display.flip()

        # 控制遊戲速度
        pygame.time.delay(100)
    font = pygame.font.Font(None, 100)
    pygame.mixer.Channel(0).stop()
    if life <= 0:
        play_video(os.path.join("assets", "dead.mp4"), os.path.join("assets", "dead.mp3"))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            if keyboard.is_pressed("r"):
                main()
    elif remaining_time <= 0 and life > 0 and score < 100:
        score_text = font.render("TIME'S UP", True, (255, 30, 30))
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join("assets", "timeup.MP3")))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            if keyboard.is_pressed("r"):
                main()
    elif life > 0 and score >= 100:
        play_video(os.path.join("assets", "ending.mp4"), os.path.join("assets", "ending.MP3"))

# 遊戲變量
MONSTER_TIMEOUT = 3000  # ms
score = 0
scorePlusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
scoreMinusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
timer: int = current_milli_time()
scorePlusItem_interval = 1000  # 毫秒
scoreMinusItem_interval = 1000
scorePlusItem_update_time = timer + scorePlusItem_interval
scoreMinusItem_update_time = timer + scoreMinusItem_interval
game_time = 181000  # 180秒
remaining_time: int = int(timer + game_time)
start_time = timer
monster_appear = False
monster_life = 0
life = 3
monster_pos = (0, 0)
monster_spawn_time = set_monster_spawn_time()
show_plus_item = True
main()




pygame.quit()
sys.exit()