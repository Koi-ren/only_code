import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 설정
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# 공 설정
ball_width = 20
ball = pygame.Rect(screen_width // 2 - ball_width // 2, screen_height // 2 - ball_width // 2, ball_width, ball_width)
ball_speed_x = 5
ball_speed_y = 5

# 패들 설정
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 20, paddle_width, paddle_height)
paddle_speed = 10

# 벽돌 설정
brick_rows = 6
brick_cols = 10
brick_width = screen_width // brick_cols
brick_height = 30
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
        bricks.append(brick)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.right += paddle_speed

    # 공 이동
    ball.left += ball_speed_x
    ball.top += ball_speed_y

    # 공과 벽 충돌
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0 or ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y

    # 공과 벽돌 충돌
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            break

    # 화면 업데이트
    screen.fill(black)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, white, ball)
    for brick in bricks:
        pygame.draw.rect(screen, red, brick)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
