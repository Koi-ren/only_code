import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 테트로미노 모양 (L, J, I, O, S, T, Z)
SHAPES = [
    [[1, 1, 1], [0, 0, 1]],  # L
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1, 1, 1]],          # I
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# 게임 보드 초기화
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, self.color,
                                   [(self.x + j) * BLOCK_SIZE + (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2,
                                    (self.y + i) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

def check_collision(tetromino, dx=0, dy=0):
    for i in range(len(tetromino.shape)):
        for j in range(len(tetromino.shape[i])):
            if tetromino.shape[i][j]:
                new_x = tetromino.x + j + dx
                new_y = tetromino.y + i + dy
                if (new_x < 0 or new_x >= GRID_WIDTH or
                    new_y >= GRID_HEIGHT or
                    (new_y >= 0 and grid[new_y][new_x])):
                    return True
    return False

def merge(tetromino):
    for i in range(len(tetromino.shape)):
        for j in range(len(tetromino.shape[i])):
            if tetromino.shape[i][j]:
                grid[tetromino.y + i][tetromino.x + j] = tetromino.color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = GRID_HEIGHT - len(new_grid)
    grid = [[0 for _ in range(GRID_WIDTH)] * cleared] + new_grid
    return cleared

# 게임 루프
clock = pygame.time.Clock()
current_piece = Tetromino()
game_over = False
fall_time = 0
fall_speed = 50  # 떨어지는 속도 조정

while not game_over:
    fall_time += 1
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current_piece, dx=-1):
                current_piece.move(-1, 0)
            if event.key == pygame.K_RIGHT and not check_collision(current_piece, dx=1):
                current_piece.move(1, 0)
            if event.key == pygame.K_DOWN:
                if not check_collision(current_piece, dy=1):
                    current_piece.move(0, 1)

    if fall_time >= fall_speed:
        fall_time = 0
        if not check_collision(current_piece, dy=1):
            current_piece.move(0, 1)
        else:
            merge(current_piece)
            clear_lines()
            current_piece = Tetromino()
            if check_collision(current_piece):
                game_over = True

    # 그리기
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                               [x * BLOCK_SIZE + (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2,
                                y * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1])

    current_piece.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()