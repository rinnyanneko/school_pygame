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

scorePlusItem_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "plus.webp")), (100, 318))
scoreMinusItem_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "gopher.png")), (100, 318))
monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster.webp")), (100, 159))

# 設置字體
font = pygame.font.Font(None, 36)

# 遊戲變量
score = 0
scorePlusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
scoreMinusItem_position = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 159))
timer = current_milli_time()
scorePlusItem_interval = 1000  # 毫秒
scoreMinusItem_interval = 1000
scorePlusItem_update_time = timer + scorePlusItem_interval
scoreMinusItem_update_time = timer + scoreMinusItem_interval
game_time = 181000  # 180秒
remaining_time:int = int(timer + game_time)
start_time = timer
monster_appear = False
monster_life = 0
life = 3
monster_pos = (0, 0)
monster_timer = timer
monster_spawn_time = timer + random.randint(5000, 25000)

# 遊戲主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if scorePlusItem_position[0] <= mouse_pos[0] <= scorePlusItem_position[0] + 100 and scorePlusItem_position[1] <= mouse_pos[1] <= scorePlusItem_position[1] + 318:
                score += 1
                scorePlusItem_position = (random.randint(0, 750), random.randint(0, 550))
                scorePlusItem_update_time = timer + scorePlusItem_interval
            elif scoreMinusItem_position[0] <= mouse_pos[0] <= scoreMinusItem_position[0] + 100 and scoreMinusItem_position[1] <= mouse_pos[1] <= scoreMinusItem_position[1] + 318:
                score -= 1
                scoreMinusItem_position = (random.randint(0, 750), random.randint(0, 550))
                scoreMinusItem_update_time = timer + scoreMinusItem_interval
                if score < 0:score = 0
    #怪物出現?
    if score >= 5 and not monster_appear:
        if timer < monster_spawn_time< timer+100:
            monster_spawn_time = timer + random.randint(5000, 25000)
            monster_appear = True
            monster_life = random.randint(3, 5)
            monster_timer = timer
            monster_pos = random.randint(0, 750), random.randint(0, 550)
    match monster_life:
        case 0:
            monster_appear = False
        case 1:
            monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster1.webp")), (100, 159))
        case 2:
            monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster2.webp")), (100, 159))
        case 3:
            monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster3.webp")), (100, 159))
        case 4:
            monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster4.webp")), (100, 159))
        case 5:
            monster_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "monster5.webp")), (100, 159))
    if monster_appear:
        screen.blit(monster_image, monster_pos)
        if timer - monster_timer > 3000:
            life -= 1
            monster_appear = False
            monster_spawn_time = timer + random.randint(5000, 25000)

    # 更新地鼠位置
    timer = current_milli_time()
    if timer > scorePlusItem_update_time:
        scorePlusItem_position = (random.randint(0, WIDTH - 159), random.randint(0, HEIGHT - 159))
        scorePlusItem_update_time = timer + scorePlusItem_interval
    if timer > scoreMinusItem_update_time:
        scoreMinusItem_position = (random.randint(0, WIDTH - 159), random.randint(0, HEIGHT - 159))
        scoreMinusItem_update_time = timer + scoreMinusItem_interval

    # 繪製背景和地鼠
    screen.blit(background, (0, 0))
    screen.blit(scorePlusItem_image, scorePlusItem_position)
    screen.blit(scoreMinusItem_image, scoreMinusItem_position)

    # 更新時間
    remaining_time:int = int(game_time - timer + start_time)
    if remaining_time <= 0:
        break
    # 繪製分數
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    remaining_time_text = font.render(f"Time: {remaining_time // 1000}", True, (0, 0, 0))
    life_text = font.render(f"Life: {life}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(remaining_time_text, (10, 30))
    screen.blit(life_text, (10, 50))

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