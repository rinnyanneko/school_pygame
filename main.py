import os
import pygame
import random
import sys
import time
#取得現在時間(ms)
def current_milli_time():
    return time.time() * 1000

WIDTH = 1280
HEIGHT = 720
# 初始化 Pygame
pygame.init()

# 設置遊戲窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打地鼠遊戲")

# 加載圖片
background = pygame.image.load(os.path.join("assets", "bliss.jpg")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

mole_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "gopher.png")), (100, 100))

# 設置字體
font = pygame.font.Font(None, 36)

# 遊戲變量
score = 0
mole_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50))
timer = current_milli_time()
mole_interval = 1000  # 毫秒
mole_update_time = timer + mole_interval
game_time = 61000  # 60秒
remaining_time:int = int(timer + game_time)
start_time = timer

# 遊戲主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mole_position[0] <= mouse_pos[0] <= mole_position[0] + 100 and mole_position[1] <= mouse_pos[1] <= mole_position[1] + 100:
                score += 1
                mole_position = (random.randint(0, 750), random.randint(0, 550))
                mole_update_time = timer + mole_interval

    # 更新地鼠位置
    timer = current_milli_time()
    if timer > mole_update_time:
        mole_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50))
        mole_update_time = timer + mole_interval

    # 繪製背景和地鼠
    screen.blit(background, (0, 0))
    screen.blit(mole_image, mole_position)

    # 更新時間
    remaining_time:int = int(game_time - timer + start_time)
    if remaining_time <= 0:
        break
    # 繪製分數
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    remaining_time_text = font.render(f"Time: {remaining_time // 1000}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(remaining_time_text, (10, 30))

    # 更新屏幕
    pygame.display.flip()

    # 控制遊戲速度
    pygame.time.delay(100)


font = pygame.font.Font(None, 100)
score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
pygame.display.flip()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
pygame.time.delay(5000)
pygame.quit()
sys.exit()