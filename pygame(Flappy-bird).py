import pygame
import random

# 初始化 Pygame
pygame.init()

# 遊戲參數
WIDTH, HEIGHT = 400, 600
BIRD_SIZE = 30
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.55
FLAP_STRENGTH = -10
FPS = 60

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 建立屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flabby Bird")

# 字體設置，確保初始化字體
font = pygame.font.SysFont("Arial", 36)

# 匯入並調整圖片
background_img = pygame.image.load("img/background-day.png")  
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # 調整背景圖大小
bird_img_up = pygame.image.load("img/redbird-downflap.png")  
bird_img_mid = pygame.image.load("img/redbird-midflap.png")  
bird_img_down = pygame.image.load("img/redbird-upflap.png")  
pipe_img = pygame.image.load("img/pipe-green.png")  
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, HEIGHT))  # 調整管道圖片大小

# 音樂和音效
pygame.mixer.music.load("audio/swoosh.ogg")  
pygame.mixer.music.play(-1, 0.0)  

jump_sound = pygame.mixer.Sound("audio/wing.ogg") 
collision_sound = pygame.mixer.Sound("audio/hit.ogg")  

# 創建鳥
bird = pygame.Rect(WIDTH // 4, HEIGHT // 2, BIRD_SIZE, BIRD_SIZE)
bird_velocity = 0

# 管道列表
pipes = []
pipe_timer = 0

# 遊戲狀態
game_started = False
score = 0

# 用來追蹤管道是否已經計分
pipe_scores = []

def add_pipe():
    height = random.randint(100, HEIGHT - 100 - PIPE_GAP)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP)
    pipes.append((top_pipe, bottom_pipe))
    pipe_scores.append(False)  # 對應管道未計分

def move_pipes():
    global pipes, score
    for i, pipe in enumerate(pipes[:]):
        # 移動管道
        pipe[0].x -= 5
        pipe[1].x -= 5

        # 計算分數：當管道完全越過鳥的位置時增加分數
        if pipe[0].x + PIPE_WIDTH < bird.x and not pipe_scores[i]:
            score += 1
            pipe_scores[i] = True  # 防止重複計分

        # 如果管道已經離開螢幕，移除它
        if pipe[0].x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            pipe_scores.pop(i)  # 同時移除對應的計分紀錄

def draw_pipes():
    for pipe in pipes:
        # 上方管道
        top_pipe_img = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe_img, (pipe[0].x, pipe[0].y - HEIGHT + pipe[0].height))
        # 下方管道
        screen.blit(pipe_img, pipe[1])

def check_collision():
    for pipe in pipes:
        if bird.colliderect(pipe[0]) or bird.colliderect(pipe[1]):
            return True
    if bird.y < 0 or bird.y > HEIGHT:
        return True
    return False

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))

def draw_bird():
    # 根據速度判斷使用不同的鳥圖片
    if bird_velocity < 0:
        screen.blit(bird_img_up, bird)  # 上升時顯示上升的圖片
    elif bird_velocity > 0:
        screen.blit(bird_img_down, bird)  # 下降時顯示下降的圖片
    else:
        screen.blit(bird_img_mid, bird)  # 停止或在空中時顯示中間的圖片

# 主遊戲迴圈
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_img, (0, 0))  # 顯示背景圖片

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True  # 開始遊戲
                bird_velocity = FLAP_STRENGTH  # 讓鳥一開始就往上跳
                jump_sound.play()  # 播放跳躍音效
            else:
                bird_velocity = FLAP_STRENGTH  # 按空白鍵時讓鳥往上跳
                jump_sound.play()  # 播放跳躍音效

    if game_started:
        # 更新鳥的狀態
        bird_velocity += GRAVITY  # 加入重力影響
        bird.y += bird_velocity  # 更新鳥的位置

        # 更新管道
        pipe_timer += 1
        if pipe_timer > 90:  # 每隔一段時間生成新管道
            add_pipe()
            pipe_timer = 0
        move_pipes()

        # 檢查碰撞
        if check_collision():
            collision_sound.play()  # 播放碰撞音效
            draw_game_over()  # 顯示Game Over
            pygame.display.flip()
            pygame.time.wait(2000)  # 暫停 2 秒後結束遊戲
            running = False

        # 畫出管道
        draw_pipes()

        # 畫出鳥
        draw_bird()

        # 畫出分數
        draw_score()

    else:
        draw_game_over()  # 顯示遊戲結束畫面

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
